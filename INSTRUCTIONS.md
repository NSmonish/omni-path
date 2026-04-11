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
