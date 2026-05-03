import cv2
import time
import numpy as np
import os
from ultralytics import YOLO
from perception.homography import HomographyTransformer
from analytics.stream_processor import StreamProcessor

def run_xai_processor(video_path='input_match.mp4', frame_dir='frames'):
    """
    Explainable AI (XAI) Processor.
    1. Runs YOLOv11-OBB.
    2. Draws annotations (Boxes + Headings) for visual proof.
    3. Warps to Pitch and Persists to DB.
    4. Saves annotated frames for Dashboard display.
    """
    if not os.path.exists(frame_dir):
        os.makedirs(frame_dir)

    # Initialize Engines
    print("🧠 Initializing YOLOv11-OBB and Homography Engines...")
    model = YOLO('yolo11n-obb.pt')
    transformer = HomographyTransformer()
    processor = StreamProcessor()
    
    cap = cv2.VideoCapture(video_path)
    print(f"🎬 Starting XAI Analysis on {video_path}...")

    frame_count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            # Loop for demo purposes
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
        frame_count += 1
        
        # Run Inference
        results = model(frame, verbose=False)
        
        annotated_frame = frame.copy()
        
        for r in results:
            if r.obb:
                obb_data = r.obb.xywhr.cpu().numpy()
                for i, box in enumerate(obb_data):
                    px, py, w, h, rot = box
                    
                    # --- XAI ANNOTATION ---
                    # Draw Oriented Box
                    rect = ((px, py), (w, h), np.degrees(rot))
                    box_points = cv2.boxPoints(rect)
                    box_points = box_points.astype(int) # Fixed Numpy 2.0 compatibility
                    cv2.drawContours(annotated_frame, [box_points], 0, (0, 255, 0), 2)
                    
                    # Draw Heading Arrow
                    angle_deg = np.degrees(rot)
                    u = int(20 * np.cos(rot))
                    v = int(20 * np.sin(rot))
                    cv2.arrowedLine(annotated_frame, (int(px), int(py)), (int(px+u), int(py+v)), (0, 0, 255), 2)
                    cv2.putText(annotated_frame, f"ID:{i}", (int(px), int(py)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                    # --- PIPELINE PROCESSING ---
                    mx, my = transformer.project_point(px, py)
                    processor.push_coordinate(
                        player_id=f"Player_{i}",
                        x=mx,
                        y=my,
                        heading=float(angle_deg % 360)
                    )
        
        # Save frame for Streamlit to display (XAI Proof)
        cv2.imwrite(os.path.join(frame_dir, 'current_frame.jpg'), annotated_frame)
        
        # Periodically persist to DB
        if frame_count % 10 == 0:
            processor.persist_to_db()
            print(f"✅ XAI Proof: Processed frame {frame_count}. Visual data synced.")

    cap.release()

if __name__ == "__main__":
    run_xai_processor()
