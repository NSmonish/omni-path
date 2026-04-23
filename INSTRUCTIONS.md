# Omni-Path Developer Log 🚀

## 🛠️ Environment & Setup
- **Start Container:** `docker-compose up -d`
- **Stop Container:** `docker-compose down`
- **Rebuild Python App:** `docker-compose build app`

## 🐘 PostGIS / Database
- **Enable Spatial Extension:** `docker exec -it omni_db psql -U monish_admin -d football_analytics -c "CREATE EXTENSION postgis;"`
- **Check PostGIS Version:** `docker exec -it omni_db psql -U monish_admin -d football_analytics -c "SELECT PostGIS_full_version();"`
- **Spatial Indexing:** Added GIST indices to `location` and `path` columns for high-speed spatial queries.

## 🐍 Python Commands
- Run Main App: `docker exec -it omni_app python main.py`
- Ingest StatsBomb Data: `docker exec -it omni_app python statsbomb_ingestion.py`
- Ingest Career Stats: `docker exec -it omni_app python ingest_career_stats.py`
- Run Spatial Analytics (TDA/Voronoi): `docker exec -it omni_app bash -c "export PYTHONPATH=$PYTHONPATH:/app && python analytics/spatial_geometry.py"`

- **Run Redis Stream Processor:** `docker exec -it omni_app bash -c "export PYTHONPATH=$PYTHONPATH:/app && python analytics/stream_processor.py"`
- **Interactive Bash:** `docker exec -it omni_app bash`

## 🐙 Git & GitHub (SSH Mode)
- **Identity Fix:** Switched from HTTPS to SSH to bypass macOS Keychain case-sensitivity issues.
- **Verification:** Run `ssh -T git@github.com` to confirm "Hi nsmonish!"
- **Update Remote:** `git remote set-url origin git@github.com:nsmonish/omni-path.git`
- **Standard Push:** `git push origin main`

---

## 🏗️ Architecture Notes (Updated April 23)

* **Spatial Backbone:** Utilized **PostGIS** with GIST indexing for high-performance geometric calculations like distance, area, and intercept trajectories.
* **Real-time Caching:** Integrated **Redis Streams** with **Pydantic Validation** to buffer 100+ FPS tracking data. Enforces pitch-boundary integrity before persistence.
* **High-Dimensional Analytics (TDA):** Applied **Delaunay Triangulation** and **Persistent Homology** concepts to identify "holes" (passing lanes) in the defensive block.
* **Production Observability:** Implemented structured logging and latency monitoring for all ETL processes.
* **Documentation:** Maintained a **Technical Design Document (TDD)** in `DOCS/` for architectural governance.
* **Data Sources:** Switched to **StatsBomb Open Data** for industry-standard event and trajectory data.
