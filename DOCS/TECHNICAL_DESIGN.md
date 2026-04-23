# 🏟️ Omni-Path: Technical Design Document (TDD-001)

**Version:** 2.0 (Production Expansion)
**Project Lead:** nsmonish (Columbia MSCS, Fall 2026)
**Target:** City Football Group (NYCFC / Man City)

## 1. Executive Summary
Omni-Path is an event-driven, high-dimensional spatial analytics engine. It transforms raw match video (Perception) into tactical intelligence (Intelligence) by leveraging PostGIS spatial indexing, Redis stream buffering, and Topological Data Analysis (TDA). The system is designed to handle 25+ FPS tracking data with < 50ms latency for real-time stadium inference.

## 2. System Architecture (The "Production" Stack)

### A. Perception Layer (The "Eyes")
- **Model:** YOLOv11-OBB (Oriented Bounding Boxes) to capture player 'heading' (orientation).
- **Tracker:** ByteTrack for consistent ID assignment under occlusion (e.g., corners, scuffles).
- **Motion:** Kalman Filter (2D Constant Velocity) to predict 'next-state' player locations and smooth raw detections.

### B. Ingestion & Storage Layer (The "Backbone")
- **Broker:** Redis Streams for low-latency coordinate ingestion.
- **Relational DB:** PostgreSQL 15 + PostGIS 3.3 with GIST spatial indexing.
- **Caching:** Redis-Key-Value for 'Hot' player positions (Current Frame).

### C. Analytics Layer (The "Brain")
- **Spatial Geometry:** Voronoi partitions for dynamic Pitch Control (Space Ownership).
- **Topology (TDA):** Persistent Homology (using Delaunay filtration) to detect passing lanes (Betti-1 holes) in the defensive block.
- **Valuation:** Expected Threat (xT) maps to quantify the goal-probability of any $(x, y)$ coordinate on the pitch.

## 3. Data Integrity & Validation
- **Schema Enforcement:** Pydantic models for all incoming events to ensure coordinates are within pitch bounds (120x80m).
- **Coordinate Homography:** 3x3 Transformation Matrix to project broadcast TV coordinates to the normalized 2D Pitch Map.

## 4. Performance Metrics (Production Targets)
- **Ingestion Latency:** < 5ms (Redis to DB).
- **Inference Latency:** < 50ms (Frame Processing).
- **TDA Latency:** < 20ms (Persistent Homology calculations).

## 5. Deployment & Scalability
- **Containerization:** Docker-Compose (app, db, redis) for development parity.
- **Edge Inference:** Models converted to ONNX for deployment on stadium servers.
- **Interface:** FastAPI REST endpoints + Streamlit Real-Time Dashboard.
