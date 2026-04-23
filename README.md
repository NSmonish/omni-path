# 🏟️ Omni-Path: Production-Grade Tactical Intelligence Engine

**Targeting:** City Football Group (NYCFC / Manchester City)
**Developer:** nsmonish (Columbia University MSCS, Fall 2026)
**Heritage:** Bridging Feature-Guided Stellar Classification (FGSC) with Spatial Football Analytics.

---

## 🚀 Overview
Omni-Path is a high-dimensional spatial analytics engine designed to transform raw football match tracking data into actionable tactical intelligence. Built with an industrial, event-driven architecture, the system leverages **PostGIS** for spatial indexing, **Redis Streams** for real-time coordinate buffering, and **Topological Data Analysis (TDA)** to identify "holes" in defensive structures.

## 🏗️ Technical Stack & Architecture
*   **Perception:** YOLOv11-OBB (Oriented Bounding Boxes) + ByteTrack + Kalman Filter Path Prediction.
*   **Backbone:** Docker-Compose orchestration of **PostGIS** (PostgreSQL 15) and **Redis**.
*   **Validation:** Strict **Pydantic** schema enforcement for all incoming 100+ FPS tracking data.
*   **Intelligence:** 
    *   **Persistent Homology:** Tracking the "birth and death" of tactical passing lanes.
    *   **Pitch Control:** Vectorized Voronoi partitions for space ownership analysis.
    *   **Expected Threat (xT):** Quantifying spatial value on a 12x8 pitch grid.

## 📈 Real Data Core
The engine is fed by industry-standard datasets:
*   **StatsBomb Open Data:** 2022 World Cup Final (Messi vs. Mbappé) and Man City 2015/16 (Agüero).
*   **Haaland Career Suite:** Full historical performance data (Dortmund to Man City 2024/25).

## 📊 Documentation & Governance
*   [Technical Design Document (TDD-001)](./DOCS/TECHNICAL_DESIGN.md) - Architectural blueprint and performance targets.
*   [Interactive Sprint Plan](./AI%20Sprint_%20Football%20Analytics%20Plan.xlsx) - Real-time progress tracker with professional color-coding.

## 🛠️ Quick Start
1.  **Start Infra:** `docker-compose up -d`
2.  **Initialize DB:** `docker exec -it omni_app python main.py`
3.  **Ingest Elite Data:** `docker exec -it omni_app python statsbomb_ingestion.py`
4.  **Run Analytics:** `docker exec -it omni_app bash -c "export PYTHONPATH=$PYTHONPATH:/app && python analytics/persistent_homology.py"`

---
*Created for the April 2026 AI Sprint. Bridging the gap between R&D at Ericsson and Elite Sports Analytics at CFG.*
