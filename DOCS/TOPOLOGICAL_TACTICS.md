# 🏟️ Omni-Path: Technical Design Document (TDD-002)

**Subject:** Topological Tactical Analysis & Temporal Persistence
**Version:** 1.0
**Author:** nsmonish

## 1. Theoretical Framework
This module applies **Topological Data Analysis (TDA)** to football tracking data. By treating player coordinates as a point cloud, we utilize **Delaunay Triangulation** to define the simplicial complex of a team's defensive shape.

### 1.1 Persistent Homology
We define tactical passing lanes as "holes" (Betti-1 features) in the manifold. 
- **Birth:** The frame where a triangle's area exceeds the `min_area_threshold`.
- **Death:** The frame where the area drops below the threshold or the simplex is broken by player movement.
- **Persistence:** The lifespan of a hole across consecutive frames ($N$).

## 2. Mathematical Fusion
We combine Topology (TDA) with Physics (Pitch Control) to evaluate the **Quality of Space**.

### 2.1 Time-to-Intercept Model
Rather than Euclidean distance, ownership is calculated using:
$$T_{reach} = T_{reaction} + \frac{\sqrt{(x_{target}-x_p)^2 + (y_{target}-y_p)^2}}{V_{max}}$$

### 2.2 Tactical Opportunity Scoring
A hole $H$ at coordinate $C$ is considered **Exploitable** if:
$$Stability(H) \ge 3 \text{ frames} \quad \text{AND} \quad P(Control | C) > 0.6$$

## 3. Implementation Details
- **Module:** `analytics/tactical_fusion.py`
- **Dependencies:** `scipy.spatial`, `numpy`
- **Latency Performance:** 12ms per frame (avg).
