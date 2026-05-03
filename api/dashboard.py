import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch
from sqlalchemy import text
from main import engine
from analytics.pitch_control import VectorizedPitchControl
from analytics.temporal_tda import TacticalPersistenceTracker
from intelligence.valuation import ExpectedThreatEngine
import time

# --- APP CONFIG ---
st.set_page_config(page_title="Omni-Path | Tactical Intelligence", layout="wide")
st.title("🏟️ Omni-Path: Real-Time Tactical Intelligence")

# 1. Simple Auto-Refresh
if 'count' not in st.session_state:
    st.session_state.count = 0
st.sidebar.write(f"🔄 Last Auto-Sync: {pd.Timestamp.now().strftime('%H:%M:%S')}")

# --- INITIALIZE ENGINES ---
@st.cache_resource
def load_engines():
    return VectorizedPitchControl(), TacticalPersistenceTracker(), ExpectedThreatEngine()

pitch_control, tda_tracker, xt_engine = load_engines()

def get_latest_frame():
    """Fetches the latest player coordinates from PostGIS."""
    query = text("""
        SELECT player_id, ST_X(location) as x, ST_Y(location) as y, orientation 
        FROM events 
        ORDER BY timestamp DESC 
        LIMIT 22;
    """)
    try:
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"DB Connection Error: {e}")
        return pd.DataFrame()

# --- DASHBOARD LAYOUT ---
col1, col2 = st.columns([2, 1])

df = get_latest_frame()

with col1:
    st.subheader("Live Pitch View")
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(10, 7))

    if not df.empty:
        # Highlight City/Main players
        city_mask = df['player_id'].str.contains('Haaland|KDB|Foden|City|Synthetic|Player_0|Player_1', case=False)
        city_players = df[city_mask]
        other_players = df[~city_mask]
        
        pitch.scatter(city_players.x, city_players.y, s=300, color='#6cabdd', edgecolors='white', linewidth=2, label='Manchester City', ax=ax)
        pitch.scatter(other_players.x, other_players.y, s=300, color='#034694', edgecolors='white', linewidth=2, label='Opponent', ax=ax)
        
        for _, p in df.iterrows():
            if p.orientation is not None:
                u = np.cos(np.radians(p.orientation))
                v = np.sin(np.radians(p.orientation))
                ax.quiver(p.x, p.y, u, v, color='white', width=0.005, alpha=0.6)
    
    st.pyplot(fig)

with col2:
    st.subheader("Intelligence Metrics")
    if not df.empty:
        st.write("**Top Threat Generators (xT)**")
        df['xT'] = df.apply(lambda r: xt_engine.get_value_at(r.x, r.y), axis=1)
        st.table(df[['player_id', 'xT']].sort_values('xT', ascending=False).head(5))
        
        st.write("**Tactical Stability**")
        stable_holes = tda_tracker.update(df[['x', 'y']].values)
        if stable_holes:
            st.success(f"🔥 {len(stable_holes)} Persistent Lanes Active")
        else:
            st.info("🛡️ Defensive Block is Solid")

# Refresh the app
time.sleep(2)
st.rerun()
