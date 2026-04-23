import numpy as np
from sqlalchemy import text
from main import engine
from scipy.spatial import Delaunay

def calculate_passing_lanes_tda(player_positions):
    """
    TDA Twist: Uses Delaunay Triangulation to identify passing lanes.
    In TDA, we look for 'holes'. Here, large triangles in the triangulation
    represent areas where defenders are too far apart (passing lanes).
    """
    points = np.array(player_positions)
    tri = Delaunay(points)
    
    # Calculate area of each triangle in the triangulation
    # Area = 0.5 * |x1(y2-y3) + x2(y3-y1) + x3(y1-y2)|
    lane_count = 0
    for simplex in tri.simplices:
        p1, p2, p3 = points[simplex]
        area = 0.5 * np.abs(p1[0]*(p2[1]-p3[1]) + p2[0]*(p3[1]-p1[1]) + p3[0]*(p1[1]-p2[1]))
        if area > 100: # Threshold for a "significant hole"
            lane_count += 1
            
    return lane_count
def calculate_pitch_control(player_positions):
    """
    Given a list of (x, y) coordinates for all players, 
    return the Voronoi partition (Space Ownership).
    """
    points_wkt = "MULTIPOINT(" + ",".join([f"{p[0]} {p[1]}" for p in player_positions]) + ")"
    
    # Use ST_Dump to explode the GeometryCollection into individual polygons
    query = text(f"""
        SELECT ST_AsText((ST_Dump(ST_VoronoiPolygons(ST_GeomFromText('{points_wkt}')))).geom) as poly_wkt;
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query)
        polygons = [row[0] for row in result]
    
    return polygons

def calculate_defensive_compactness(defender_positions):
    """
    Uses Convex Hull to measure the area occupied by the defensive block.
    This is the first step toward Topological Data Analysis (TDA).
    """
    points_wkt = "MULTIPOINT(" + ",".join([f"{p[0]} {p[1]}" for p in defender_positions]) + ")"
    
    query = text(f"""
        SELECT ST_Area(ST_ConvexHull(ST_GeomFromText('{points_wkt}'))) as area;
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query)
        area = result.scalar()
    
    return area

if __name__ == "__main__":
    # Test with mock player positions
    # Imagine 5 defenders in a block
    defenders = [(20, 30), (22, 50), (35, 40), (25, 20), (30, 60)]
    area = calculate_defensive_compactness(defenders)
    print(f"🛡️ Defensive Compactness (Hull Area): {round(area, 2)} square meters")
    
    # TDA Passing Lanes
    lanes = calculate_passing_lanes_tda(defenders)
    print(f"🌌 TDA Space Analysis: Identified {lanes} major 'holes' in the defensive block.")

    # Imagine all 22 players
    all_players = defenders + [(50, 40), (60, 20), (70, 50)] 
    voronoi = calculate_pitch_control(all_players)
    print(f"⚽ Generated {len(voronoi)} Voronoi cells for Pitch Control.")
