import cv2
import time
import numpy as np
from ultralytics import YOLO
from perception.homography import HomographyTransformer
from analytics.stream_processor import StreamProcessor

def process_local_video(video_path='input_match.mp4'):
    """
    Day 8 Final Proof: Processes a local MP4 file.
    1. YOLOv11-OBB detects players + heading.
    2. Homography warps pixels to pitch meters.
    3. StreamProcessor smooths data and saves to PostGIS.
    """
    # Initialize Engines
    model = YOLO('yolo11n-obb.pt')
    transformer = HomographyTransformer()
    processor = StreamProcessor()
    
    cap = cv2.VideoCapture(video_path)
    print(f"🎬 Processing {video_path}...")

    frame_count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if not success: break
        
        frame_count += 1
        # Run Inference
        results = model(frame, verbose=False)
        
        for r in results:
            if r.obb:
                obb_data = r.obb.xywhr.cpu().numpy()
                for i, box in enumerate(obb_data):
                    px, py, w, h, rot = box
                    
                    # 1. Warp to Pitch
                    mx, my = transformer.project_point(px, py)
                    
                    # 2. Feed to System (Memory + DB)
                    processor.push_coordinate(
                        player_id=f"Player_{i}",
                        x=mx,
                        y=my,
                        heading=float(np.degrees(rot) % 360)
                    )
        
        # Periodically persist to DB every 25 frames (1 second of match)
        if frame_count % 25 == 0:
            processor.persist_to_db()
            print(f"✅ Processed 1 second of match (Frame {frame_count})")

    cap.release()
    print("🏁 Video Processing Complete.")

if __name__ == "__main__":
    process_local_video()
