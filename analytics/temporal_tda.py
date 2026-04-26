import numpy as np
from scipy.spatial import Delaunay
import uuid
import time

class TacticalPersistenceTracker:
    """
    Advanced Temporal TDA: Tracks the lifespan of tactical 'holes' in a defense.
    A 'Persistent' hole is one that survives across multiple frames.
    """
    def __init__(self, min_area_threshold=100, stability_frames=3):
        self.min_area_threshold = min_area_threshold
        self.stability_frames = stability_frames
        self.active_holes = {} # {hole_id: {'centroid': (x,y), 'lifespan': int}}

    def _get_centroids(self, points):
        tri = Delaunay(points)
        centroids = []
        for simplex in tri.simplices:
            p_tri = points[simplex]
            # Calculate Area
            area = 0.5 * np.abs(p_tri[0][0]*(p_tri[1][1]-p_tri[2][1]) + 
                               p_tri[1][0]*(p_tri[2][1]-p_tri[0][1]) + 
                               p_tri[2][0]*(p_tri[0][1]-p_tri[1][1]))
            
            if area > self.min_area_threshold:
                centroid = np.mean(p_tri, axis=0)
                centroids.append(centroid)
        return centroids

    def update(self, player_positions):
        """Processes a new frame and updates the lifespan of detected holes."""
        new_centroids = self._get_centroids(np.array(player_positions))
        updated_holes = {}
        
        # Match new centroids to existing holes (simple nearest neighbor)
        for nc in new_centroids:
            matched_id = None
            for h_id, data in self.active_holes.items():
                dist = np.linalg.norm(nc - data['centroid'])
                if dist < 5.0: # 5m threshold for 'same hole'
                    matched_id = h_id
                    break
            
            if matched_id:
                updated_holes[matched_id] = {
                    'centroid': nc,
                    'lifespan': self.active_holes[matched_id]['lifespan'] + 1
                }
            else:
                # New hole born
                updated_holes[str(uuid.uuid4())[:8]] = {'centroid': nc, 'lifespan': 1}
        
        self.active_holes = updated_holes
        
        # Return only 'Stable' holes (those that have persisted)
        stable_holes = [h_id for h_id, d in self.active_holes.items() if d['lifespan'] >= self.stability_frames]
        return stable_holes

if __name__ == "__main__":
    tracker = TacticalPersistenceTracker(min_area_threshold=80, stability_frames=3)
    
    # Simulate a defensive line shifting slightly over 5 frames
    defenders_base = np.array([
        [20, 20], [20, 40], [20, 60], # Back line
        [40, 30], [40, 50]            # Mid line
    ])

    print(f"🌌 Starting Temporal TDA Persistence Tracking...")
    for frame in range(1, 11): # Increased to 10 frames
        # Add slight jitter to simulate movement
        jitter = np.random.normal(0, 0.5, defenders_base.shape)
        current_defenders = defenders_base + jitter
        
        stable_holes = tracker.update(current_defenders)
        
        print(f"[FRAME {frame:02d}] Holes: {len(tracker.active_holes)} | STABLE: {len(stable_holes)}")
        if stable_holes:
            print(f"   🔥 TACTICAL ALERT: Found {len(stable_holes)} persistent passing lanes!")
        time.sleep(0.05)
    print("✅ Simulation Complete.")
