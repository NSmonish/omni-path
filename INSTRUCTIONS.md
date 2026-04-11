# Omni-Path Developer Log 🚀

## 🛠️ Environment & Setup
- **Start Container:** `docker-compose up -d`
- **Stop Container:** `docker-compose down`
- **Rebuild Python App:** `docker-compose build app`

## 🐘 PostGIS / Database
- **Enable Spatial Extension:** `docker exec -it omni_db psql -U monish_admin -d football_analytics -c "CREATE EXTENSION postgis;"`
- **Check PostGIS Version:** `docker exec -it omni_db psql -U monish_admin -d football_analytics -c "SELECT PostGIS_full_version();"`

## 🐍 Python Commands
- **Run Main App:** `docker exec -it omni_app python main.py`
- **Interactive Bash:** `docker exec -it omni_app bash`

## 🐙 Git & GitHub (SSH Mode)
- **Identity Fix:** Switched from HTTPS to SSH to bypass macOS Keychain case-sensitivity issues.
- **Verification:** Run `ssh -T git@github.com` to confirm "Hi nsmonish!"
- **Update Remote:** `git remote set-url origin git@github.com:nsmonish/omni-path.git`
- **Standard Push:** `git push origin main`

---

## 🏗️ Architecture Notes

* **Spatial Backbone:** Utilized **PostGIS** for player tracking to leverage advanced `ST` (Spatial-Temporal) functions. This allows for high-performance geometric calculations like distance, area, and intercept trajectories directly within the database layer.
* **Real-time Caching:** Integrated **Redis** for stream caching of high-frequency player coordinates. This serves as a buffer to handle rapid data ingestion before periodically persisting processed analytics to **PostgreSQL**.
* **Containerization:** Full multi-container orchestration via **Docker**, ensuring consistency between local development and future deployment to cloud environments.
