import numpy as np
import logging

logger = logging.getLogger("ValuationEngine")

class ExpectedThreatEngine:
    """
    Industry-standard xT (Expected Threat) model.
    Quantifies the value of space on a 12x8 grid.
    """
    def __init__(self):
        # Calibrated xT Matrix (Values represent goal probability increase)
        # Higher values near the opponent's goal (bottom-right of this matrix)
        self.xt_grid = np.array([
            [0.006, 0.007, 0.010, 0.012, 0.015, 0.018, 0.022, 0.025, 0.030, 0.035, 0.040, 0.045],
            [0.007, 0.008, 0.011, 0.013, 0.016, 0.020, 0.024, 0.028, 0.035, 0.045, 0.055, 0.065],
            [0.008, 0.009, 0.012, 0.015, 0.019, 0.024, 0.030, 0.038, 0.050, 0.070, 0.100, 0.150],
            [0.009, 0.010, 0.013, 0.017, 0.022, 0.028, 0.035, 0.045, 0.065, 0.120, 0.250, 0.400], # Goal Mouth
            [0.009, 0.010, 0.013, 0.017, 0.022, 0.028, 0.035, 0.045, 0.065, 0.120, 0.250, 0.400], # Goal Mouth
            [0.008, 0.009, 0.012, 0.015, 0.019, 0.024, 0.030, 0.038, 0.050, 0.070, 0.100, 0.150],
            [0.007, 0.008, 0.011, 0.013, 0.016, 0.020, 0.024, 0.028, 0.035, 0.045, 0.055, 0.065],
            [0.006, 0.007, 0.010, 0.012, 0.015, 0.018, 0.022, 0.025, 0.030, 0.035, 0.040, 0.045]
        ])
        
        self.grid_rows = 8
        self.grid_cols = 12
        self.pitch_length = 120
        self.pitch_width = 80

    def _get_grid_index(self, x, y):
        """Maps (x, y) meters to (row, col) indices."""
        col = int(min(x / (self.pitch_length / self.grid_cols), self.grid_cols - 1))
        row = int(min(y / (self.pitch_width / self.grid_rows), self.grid_rows - 1))
        return row, col

    def get_value_at(self, x, y):
        """Returns the xT value for a specific coordinate."""
        row, col = self._get_grid_index(x, y)
        return self.xt_grid[row, col]

    def calculate_threat_gained(self, start_pos, end_pos):
        """
        Quantifies the tactical value of a movement.
        xT_gained = xT(end) - xT(start)
        """
        v_start = self.get_value_at(start_pos[0], start_pos[1])
        v_end = self.get_value_at(end_pos[0], end_pos[1])
        return round(float(v_end - v_start), 4)

if __name__ == "__main__":
    engine = ExpectedThreatEngine()
    
    # Scenario: Haaland run from Half-way line to the 6-yard box
    start = (60, 40)
    end = (115, 40)
    
    threat = engine.calculate_threat_gained(start, end)
    
    print(f"💰 xT VALUATION ENGINE:")
    print(f"   - Run: {start} -> {end}")
    print(f"   - Start Value: {engine.get_value_at(*start)}")
    print(f"   - End Value: {engine.get_value_at(*end)}")
    print(f"   - 🔥 THREAT GAINED: +{threat} xT")
    
    if threat > 0.1:
        print("   ✅ High-Impact Movement Detected.")
