import numpy as np
from analytics.pitch_control import VectorizedPitchControl
from intelligence.valuation import ExpectedThreatEngine

class TacticalValuationEngine:
    """
    The 'Executive Brain' of Omni-Path.
    Fuses Pitch Control (Ownership) with xT (Value) to calculate Controlled Threat.
    """
    def __init__(self):
        self.pitch_engine = VectorizedPitchControl()
        self.xt_engine = ExpectedThreatEngine()

    def calculate_controlled_threat(self, team_a_pos, team_a_vel, team_b_pos, team_b_vel):
        """
        Calculates the total xT value currently controlled by Team A.
        Total xT = Sum( Probability_of_Control(cell) * xT_Value(cell) )
        """
        # 1. Generate Pitch Control Grid (20x30 resolution from Day 2)
        control_grid = self.pitch_engine.calculate_control_grid(
            team_a_pos, team_a_vel, team_b_pos, team_b_vel
        )
        
        # 2. Resample or map xT grid to match control grid
        # Control grid is (20, 30), xT grid is (8, 12). 
        # For this professional demo, we'll map each control cell to its xT value.
        total_xt_controlled = 0
        
        # Grid dimensions
        rows, cols = control_grid.shape
        x_steps = np.linspace(0, 120, cols)
        y_steps = np.linspace(0, 80, rows)

        for i in range(rows):
            for j in range(cols):
                # Get xT value for this specific cell coordinate
                cell_xt = self.xt_engine.get_value_at(x_steps[j], y_steps[i])
                # Weighted threat: control probability * area value
                total_xt_controlled += control_grid[i, j] * cell_xt

        # Normalize by number of cells to get a 'Threat Score'
        return round(float(total_xt_controlled / (rows * cols)), 4)

if __name__ == "__main__":
    engine = TacticalValuationEngine()
    
    # Simulation: City in a dangerous attacking position
    city_pos = np.array([[100, 40], [95, 35]]) # Near goal
    city_vel = np.array([[5, 0], [5, 0]])
    
    chelsea_pos = np.array([[110, 40], [105, 45]]) # Defenders
    chelsea_vel = np.array([[0, 0], [0, 0]])
    
    threat_score = engine.calculate_controlled_threat(city_pos, city_vel, chelsea_pos, chelsea_vel)
    
    print(f"🏟️  TACTICAL VALUATION REPORT:")
    print(f"   - Match State: City Attacking Final Third")
    print(f"   - 🔥 CONTROLLED THREAT SCORE: {threat_score}")
    print(f"   - Insight: City currently 'owns' {threat_score*100:.2f}% of total scoring potential.")
