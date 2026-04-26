import redis
import json
import time
import logging
from sqlalchemy.orm import sessionmaker
from main import MatchEvent, engine
from analytics.schemas import TrackingCoordinate

# Configure production-grade logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("StreamProcessor")

class StreamProcessor:
    def __init__(self, redis_url="redis://redis:6379/0"):
        self.redis = redis.from_url(redis_url)
        self.Session = sessionmaker(bind=engine)
        self.stream_key = "match_tracking_stream"

    def push_coordinate(self, player_id, x, y, timestamp=None, heading=None):
        """
        Pushes a single player coordinate to the Redis stream.
        Uses Pydantic for strict schema validation.
        """
        try:
            coord = TrackingCoordinate(
                player_id=player_id,
                x=x,
                y=y,
                timestamp=timestamp or time.time(),
                heading=heading
            )
            self.redis.xadd(self.stream_key, {"payload": coord.model_dump_json()})
            return True
        except Exception as e:
            logger.error(f"❌ Validation Error for {player_id}: {e}")
            return False

    def persist_to_db(self, batch_size=100):
        """Drains the Redis stream and performs a bulk insert into PostGIS."""
        session = self.Session()
        messages = self.redis.xread({self.stream_key: "0-0"}, count=batch_size)
        
        if not messages:
            return 0

        events_to_add = []
        message_ids = []

        start_time = time.perf_counter()
        for stream, msgs in messages:
            for msg_id, payload in msgs:
                try:
                    coord = TrackingCoordinate.model_validate_json(payload[b"payload"])
                    event = MatchEvent(
                        player_id=coord.player_id, 
                        location=f"POINT({coord.x} {coord.y})",
                        orientation=coord.heading # Persisting Orientation
                    )
                    events_to_add.append(event)
                    message_ids.append(msg_id)
                except Exception as e:
                    logger.error(f"Failed to validate stream message {msg_id}: {e}")

        if events_to_add:
            session.add_all(events_to_add)
            session.commit()
            self.redis.xdel(self.stream_key, *message_ids)
            
        latency = (time.perf_counter() - start_time) * 1000
        if len(events_to_add) > 0:
            logger.info(f"💾 Persisted {len(events_to_add)} events. Latency: {latency:.2f}ms")
        
        session.close()
        return len(events_to_add)

if __name__ == "__main__":
    processor = StreamProcessor()
    
    print("🛰️  Testing Production Stream Processor...")
    # Test 1: Valid coordinate
    processor.push_coordinate("Haaland_9", 50, 40)
    
    # Test 2: INVALID coordinate (Off Pitch - X=150)
    print("\n🧐 Testing Off-Pitch Validation (X=150):")
    processor.push_coordinate("Haaland_9", 150, 40)
    
    print(f"\n📥 Persisting buffer...")
    processor.persist_to_db()
