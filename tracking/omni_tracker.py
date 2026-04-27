import logging
from tracking.kalman_filter import KalmanFilter2D

logger = logging.getLogger("OmniTracker")

class OmniTracker:
    """
    Manages multiple player tracks using Kalman Filters.
    Ensures identity stability for the Omni-Path system.
    """
    def __init__(self, max_ghost_frames=10):
        self.tracks = {} # {player_id: KalmanFilter2D}
        self.missed_frames = {} # {player_id: int}
        self.max_ghost_frames = max_ghost_frames

    def update_player(self, player_id, x, y):
        """Update a specific player's position."""
        if player_id not in self.tracks:
            self.tracks[player_id] = KalmanFilter2D()
            logger.info(f"🆕 NEW TRACK: {player_id}")
        
        self.missed_frames[player_id] = 0
        return self.tracks[player_id].update(x, y)

    def predict_all(self):
        """Predict positions for all players (Ghosting)."""
        predictions = {}
        to_delete = []
        
        for p_id, kf in self.tracks.items():
            self.missed_frames[p_id] += 1
            
            if self.missed_frames[p_id] > self.max_ghost_frames:
                to_delete.append(p_id)
                continue
            
            predictions[p_id] = kf.predict()
            
        for p_id in to_delete:
            del self.tracks[p_id]
            del self.missed_frames[p_id]
            logger.info(f"❌ TRACK LOST: {p_id}")
            
        return predictions

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tracker = OmniTracker(max_ghost_frames=5)
    
    print("🏟️  Tracking Manchester City attacking trio...")
    tracker.update_player("Haaland_9", 50, 40)
    tracker.update_player("KDB_17", 45, 30)
    tracker.update_player("Foden_47", 40, 20)
    
    # Simulate Haaland disappearing for 2 frames
    print("\n⚠️ Haaland obscured by defender!")
    for f in range(2):
        # We only update KDB and Foden
        tracker.update_player("KDB_17", 46, 31)
        tracker.update_player("Foden_47", 41, 21)
        
        # Ghost Haaland
        all_pos = tracker.predict_all()
        print(f"Frame {f+1}: Haaland Ghost position: {all_pos['Haaland_9']}")
    
    # Haaland reappears
    print("\n✨ Haaland reappeared!")
    pos = tracker.update_player("Haaland_9", 55, 40)
    print(f"Re-Tracked Haaland at: {pos}")
