# 🏟️ Omni-Path: Technical Design Document (TDD-003)

**Subject:** Kalman Filtering & State Estimation in Player Tracking
**Version:** 1.0
**Author:** nsmonish

## 1. Mathematical Model
To handle noisy YOLO detections and temporary occlusions, Omni-Path utilizes a **2D Constant Velocity Kalman Filter**.

### 1.1 State Vector ($x$)
The state of each player is defined by a 4-dimensional vector:
$$x = [x, y, v_x, v_y]^T$$
where $(x, y)$ is the position in pitch meters and $(v_x, v_y)$ is the instantaneous velocity.

### 1.2 State Transition Matrix ($F$)
Assuming constant velocity between frames ($\Delta t = 0.04s$):
$$F = \begin{bmatrix} 1 & 0 & \Delta t & 0 \\ 0 & 1 & 0 & \Delta t \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

## 2. Occlusion Handling (Ghosting)
When the perception layer fails to detect a player (Measurement $z_k$ is null), the system enters **Prediction Mode**.
The state is updated solely via the transition matrix:
$$x_{k|k-1} = F x_{k-1}$$
This allows the **Tactical Fusion Engine** to continue analyzing a player's threat even when they are physically obscured by other players.

## 3. Implementation Details
- **Module:** `tracking/kalman_filter.py` and `tracking/omni_tracker.py`
- **Latency:** < 1ms per player update.
- **Integration:** Wrapped within the `StreamProcessor` for automatic smoothing of the PostGIS event stream.
