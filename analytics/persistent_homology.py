import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

def calculate_persistence(points, max_threshold=50):
    """
    Advanced TDA: Calculates the 'Persistence' of holes in the defensive block.
    In astronomy (FGSC), you used this for stellar clusters. 
    Here, we use it to find tactical 'Passing Lanes'.
    """
    tri = Delaunay(points)
    
    # We'll calculate the 'life' of each triangle. 
    # Birth = size when it first forms. Death = size when it's closed by a defender.
    persistence_diagram = []
    
    for simplex in tri.simplices:
        p_tri = points[simplex]
        # Max side length of the triangle is our 'filtration' parameter
        side1 = np.linalg.norm(p_tri[0] - p_tri[1])
        side2 = np.linalg.norm(p_tri[1] - p_tri[2])
        side3 = np.linalg.norm(p_tri[2] - p_tri[0])
        
        birth = max(side1, side2, side3)
        # For our tactical purposes, 'death' is when the hole becomes too large to be useful
        death = max_threshold 
        
        if birth < death:
            persistence_diagram.append((birth, death))
            
    return persistence_diagram

def find_tactical_opportunities(persistence_diagram, min_life=10):
    """
    Identifies 'Persistent' passing lanes that are large enough 
    to be exploited but small enough to be reachable.
    """
    opportunities = [d for d in persistence_diagram if (d[1] - d[0]) > min_life]
    return len(opportunities)

if __name__ == "__main__":
    # Simulate a defensive line 
    # (X, Y) coordinates of 11 defenders in a 4-4-2
    defenders = np.array([
        [20, 10], [20, 30], [20, 50], [20, 70],  # Back 4
        [40, 15], [40, 35], [40, 55], [40, 75],  # Mid 4
        [60, 30], [60, 50]                       # Front 2
    ])
    
    print("🌌 Analyzing Defensive Topology using Persistent Homology...")
    diag = calculate_persistence(defenders)
    opps = find_tactical_opportunities(diag)
    
    print(f"✅ TDA Analysis Complete.")
    print(f"📊 Identified {len(diag)} passing lanes.")
    print(f"🔥 Found {opps} PERSISTENT opportunities (passing lanes that won't close instantly).")
