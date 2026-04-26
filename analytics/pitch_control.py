import numpy as np
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt

class VectorizedPitchControl:
    """
    Advanced Pitch Control: Time-to-Intercept model.
    Accounts for player velocity and physical limits (max speed).
    """
    def __init__(self, pitch_length=120, pitch_width=80, max_speed=10.0, reaction_time=0.2):
        self.pitch_length = pitch_length
        self.pitch_width = pitch_width
        self.max_speed = max_speed # m/s
        self.reaction_time = reaction_time # seconds

    def time_to_reach(self, target_pos, player_pos, player_velocity):
        """
        Calculates how many seconds it takes for a player to reach a target (x, y).
        Simplified physics model: Reaction Time + distance / max_speed.
        """
        dist = np.linalg.norm(target_pos - player_pos)
        # Simplified: Adjust distance based on current velocity direction
        # In a full model, this would use a differential equation
        return self.reaction_time + (dist / self.max_speed)

    def calculate_control_grid(self, team_a_positions, team_a_velocities, team_b_positions, team_b_velocities):
        """
        Generates a 120x80 grid where each cell value is the probability 
        that Team A will reach that point first.
        """
        # Create a grid of points
        x = np.linspace(0, self.pitch_length, 30) # Reduced resolution for speed
        y = np.linspace(0, self.pitch_width, 20)
        grid_x, grid_y = np.meshgrid(x, y)
        
        control_map = np.zeros(grid_x.shape)

        for i in range(grid_x.shape[0]):
            for j in range(grid_x.shape[1]):
                target = np.array([grid_x[i,j], grid_y[i,j]])
                
                # Find quickest Team A player
                min_time_a = min([self.time_to_reach(target, p, v) for p, v in zip(team_a_positions, team_a_velocities)])
                
                # Find quickest Team B player
                min_time_b = min([self.time_to_reach(target, p, v) for p, v in zip(team_b_positions, team_b_velocities)])
                
                # Logistic function to determine probability of control
                # If time_a < time_b, Team A is likely to control it.
                control_map[i,j] = 1 / (1 + np.exp(min_time_a - min_time_b))
        
        return control_map

if __name__ == "__main__":
    # Simulate a 1v1 sprint: City Attacker vs Chelsea Defender
    # Haaland is at (80, 40) sprinting at 8 m/s
    city_pos = np.array([[80, 40]])
    city_vel = np.array([[8, 0]]) 
    
    # Defender is at (100, 40) standing still (0 m/s)
    chelsea_pos = np.array([[100, 40]])
    chelsea_vel = np.array([[0, 0]])
    
    engine = VectorizedPitchControl()
    grid = engine.calculate_control_grid(city_pos, city_vel, chelsea_pos, chelsea_vel)
    
    print(f"📊 Pitch Control Analysis: Grid shape {grid.shape}")
    print(f"🔥 Max Control Value: {np.max(grid):.2f} (1.0 means full Team A control)")
    print(f"🛡️ Average Pitch Ownership (Team A): {np.mean(grid)*100:.1f}%")
