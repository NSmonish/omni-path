# 🧠 Omni-Path: AI Agent Knowledge Base

This file serves as the "Single Source of Truth" for Gemini CLI sessions. It ensures continuity, architectural governance, and strategic alignment with the City Football Group (CFG) career target.

---

## 🎯 Project Mission
**Developer:** nsmonish (Columbia MSCS, Fall 2026)
**Target:** Securing an R&D role at City Football Group (NYCFC / Manchester City).
**Unique Edge:** Applying high-dimensional astronomical research (Feature-Guided Stellar Classification) to football spatial-temporal tracking.

---

## 🏁 Progress State (Last Update: April 23, 2026)

### ✅ Day 1: Industrial Infrastructure (COMPLETED)
- **Database:** PostGIS 3.3 configured with **GIST spatial indices** for trajectories (`LINESTRING`) and shots.
- **Streaming:** Implemented **Redis Streams** to buffer 100+ FPS tracking data, decoupling ingestion from persistence.
- **Validation:** Strict **Pydantic** enforcement in `analytics/schemas.py` (Rejecting off-pitch data).
- **Intelligence:** Developed `persistent_homology.py` using Delaunay triangulation to identify tactical passing lanes.
- **Data Ingested:** Real StatsBomb Open Data (WC Final 2022, Man City 2015/16) and Haaland Career statistics.
- **Documentation:** Authored **TDD-001** and a professional GitHub README.

### ✅ Day 4: Perception & Orientation (COMPLETED)
- **Heading Engine:** Developed `perception/orientation_engine.py` to normalize YOLOv11-OBB angles into standard 0-360° headings.
- **API Expansion:** Updated FastAPI ingestion endpoints to handle orientation data for real-time tactical insights.
- **Persistence:** Refactored PostGIS schema and StreamProcessor to store player body orientation in the `events` table.

---

## 🗺️ Execution Roadmap (April 27 – April 30)

| Date | Phase | Primary Task |
| :--- | :--- | :--- |
| **April 27** | **Tracking** | **Kalman + ByteTrack:** Occlusion-resistant path prediction. |
| **April 28** | **Valuation** | **Expected Threat (xT):** Mapping spatial value to Haaland's runs. |
| **April 29** | **Interface** | **FastAPI + Streamlit:** Building the live tactical dashboard. |
| **April 30** | **Delivery** | **ONNX + Portfolio:** Edge optimization and final repo polish. |

---

## ⚙️ Technical Governance
- **Pitch Dimensions:** Normalized to 120m x 80m.
- **Performance:** End-to-end latency target is < 50ms per frame.
- **Modular Imports:** Always use `export PYTHONPATH=$PYTHONPATH:/app` when running analytics.
- **Validation:** 0% invalid data is allowed to reach PostGIS (Pydantic-gated).

---
*GEMINI INSTRUCTION: Always read this file at the start of a session to resume the "Master-Level" sprint.*
