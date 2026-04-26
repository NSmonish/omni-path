import cv2
import numpy as np
import logging

logger = logging.getLogger("HomographyTransformer")

class HomographyTransformer:
    """
    Projects broadcast TV pixels (x, y) to a 2D Pitch Map (X, Y) in meters.
    Standard Pitch: 120m x 80m (StatsBomb scale).
    """
    def __init__(self):
        # 1. Destination Points: Standard 120x80 pitch coordinates in meters
        # Anchors: Top-Left, Top-Right, Bottom-Right, Bottom-Left of the 18-yard box
        self.dst_pts = np.array([
            [0, 18], [18, 18], [18, 62], [0, 62]
        ], dtype=np.float32)

        # 2. Source Points: Realistic pixel coordinates from a high-angle camera
        self.src_pts = np.array([
            [500, 300], [700, 300], [1000, 800], [200, 800]
        ], dtype=np.float32)

        # 3. Calculate 3x3 Transformation Matrix
        self.H, _ = cv2.findHomography(self.src_pts, self.dst_pts)

    def project_point(self, x_pixel, y_pixel):
        """
        Warps a single (x, y) pixel to (X, Y) meters.
        """
        point = np.array([[[x_pixel, y_pixel]]], dtype=np.float32)
        transformed = cv2.perspectiveTransform(point, self.H)
        
        # Output is (X_meters, Y_meters)
        X, Y = transformed[0][0]
        return round(float(X), 2), round(float(Y), 2)

if __name__ == "__main__":
    transformer = HomographyTransformer()
    
    # Simulate a player detected at center of frame
    px, py = 960, 540
    mx, my = transformer.project_point(px, py)
    
    print(f"👁️  Computer Vision Calibration:")
    print(f"   - Input Pixel: ({px}, {py})")
    print(f"   - Projected Pitch Coord: {mx}m, {my}m")
    
    # Verify bounds
    if 0 <= mx <= 120 and 0 <= my <= 80:
        print("   ✅ Point is within Pitch Boundaries.")
    else:
        print("   ⚠️  Point is OUT OF BOUNDS. Calibration required.")
