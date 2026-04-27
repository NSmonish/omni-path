import numpy as np

class KalmanFilter2D:
    """
    2D Constant Velocity Kalman Filter.
    State Vector (x): [x, y, vx, vy]^T
    """
    def __init__(self, dt=0.04, process_noise=0.1, measurement_noise=1.0):
        # dt = 1/25 fps = 0.04s
        self.dt = dt
        
        # State Transition Matrix (F)
        self.F = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        # Measurement Matrix (H) - we only measure position (x, y)
        self.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])
        
        # Process Noise Covariance (Q)
        self.Q = np.eye(4) * process_noise
        
        # Measurement Noise Covariance (R)
        self.R = np.eye(2) * measurement_noise
        
        # Initial Covariance (P)
        self.P = np.eye(4) * 100
        
        # Initial State (x)
        self.x = np.zeros((4, 1))
        
        self.initialized = False

    def initialize(self, pos_x, pos_y):
        self.x = np.array([[pos_x], [pos_y], [0], [0]], dtype=np.float32)
        self.initialized = True

    def predict(self):
        """State prediction step."""
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        return self.x[:2].flatten()

    def update(self, pos_x, pos_y):
        """Measurement update step."""
        if not self.initialized:
            self.initialize(pos_x, pos_y)
            return self.x[:2].flatten()
            
        z = np.array([[pos_x], [pos_y]], dtype=np.float32)
        
        # Innovation (y)
        y = z - self.H @ self.x
        
        # Innovation Covariance (S)
        S = self.H @ self.P @ self.H.T + self.R
        
        # Kalman Gain (K)
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Update State
        self.x = self.x + K @ y
        
        # Update Covariance
        self.P = (np.eye(4) - K @ self.H) @ self.P
        
        return self.x[:2].flatten()

if __name__ == "__main__":
    kf = KalmanFilter2D()
    
    print("🏃 Simulating noisy Haaland movement...")
    # Real path: constant velocity from (10, 10) to (14, 14) over 5 frames
    real_path = [(10+i, 10+i) for i in range(5)]
    
    for i, (rx, ry) in enumerate(real_path):
        # Add noise to simulate raw YOLO detection
        noise_x = rx + np.random.normal(0, 0.5)
        noise_y = ry + np.random.normal(0, 0.5)
        
        # Update Kalman
        smoothed = kf.update(noise_x, noise_y)
        
        print(f"Frame {i}: Raw=({noise_x:.2f}, {noise_y:.2f}) -> Smoothed=({smoothed[0]:.2f}, {smoothed[1]:.2f})")
    
    # Simulate Occlusion (No detection for 3 frames)
    print("\n⚠️  OCCLUSION DETECTED: Player hidden behind defender...")
    for i in range(5, 8):
        ghost_pos = kf.predict()
        print(f"Frame {i}: [GHOST PREDICTION]=({ghost_pos[0]:.2f}, {ghost_pos[1]:.2f})")
