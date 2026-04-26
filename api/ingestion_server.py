from fastapi import FastAPI, HTTPException
from analytics.schemas import TrackingCoordinate
from analytics.stream_processor import StreamProcessor
import uvicorn
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IngestionAPI")

app = FastAPI(title="Omni-Path Distributed Ingestion")
processor = StreamProcessor()

@app.post("/ingest/coordinate")
async def ingest_coordinate(coord: TrackingCoordinate):
    """
    Receives validated coordinates from the Cloud Vision (Colab) engine.
    Pushes to Redis Stream for persistence.
    """
    success = processor.push_coordinate(
        player_id=coord.player_id,
        x=coord.x,
        y=coord.y,
        timestamp=coord.timestamp,
        heading=coord.heading # Added for Day 4
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Data validation failed")
    
    return {"status": "success", "player": coord.player_id}

@app.get("/health")
async def health_check():
    return {"status": "online", "engine": "Omni-Path"}

if __name__ == "__main__":
    # In production, this would run on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
