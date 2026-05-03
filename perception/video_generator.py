import cv2
import numpy as np

def generate_tactical_video(output_path='input_match.mp4'):
    """
    Generates a high-quality tactical match animation (dots moving) 
    to serve as a real MP4 input for the Omni-Path pipeline.
    """
    width, height = 1280, 720
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 25, (width, height))

    # Defensive Line (4-4-2)
    defenders = [
        [300, 200], [300, 300], [300, 400], [300, 500], # Back 4
        [500, 250], [500, 350], [500, 450], [500, 550], # Mid 4
        [700, 300], [700, 400]                          # Front 2
    ]
    
    # Haaland (The Attacker)
    haaland = [100, 350]

    print("🎬 Generating Synthetic Tactical Match Video...")

    for frame in range(150): # 6 seconds of match
        # Background: Green Pitch
        img = np.zeros((height, width, 3), np.uint8)
        img[:] = (34, 139, 34) # Forest Green
        
        # Move Defenders slightly (Compact shift)
        for d in defenders:
            d[0] += np.random.randint(-1, 2)
            d[1] += np.random.randint(-1, 2)
            # Draw Defender (Blue) with Orientation Marker
            cv2.circle(img, (int(d[0]), int(d[1])), 10, (148, 70, 3), -1)
            cv2.line(img, (int(d[0]), int(d[1])), (int(d[0]+15), int(d[1])), (255, 255, 255), 2)

        # Move Haaland (Explosive Run through the middle)
        haaland[0] += 6 # High velocity
        haaland[1] += np.random.randint(-2, 3)
        # Draw Haaland (Light Blue)
        cv2.circle(img, (int(haaland[0]), int(haaland[1])), 12, (221, 172, 108), -1)
        # Orientation Arrow
        cv2.line(img, (int(haaland[0]), int(haaland[1])), (int(haaland[0]+20), int(haaland[1])), (255, 255, 255), 3)

        # Write frame
        out.write(img)

    out.release()
    print(f"✅ Synthetic Tactical Video Saved: {output_path}")

if __name__ == "__main__":
    generate_tactical_video()
