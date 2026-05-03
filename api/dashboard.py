import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch
from sqlalchemy import text
from main import engine
from analytics.pitch_control import VectorizedPitchControl
from analytics.temporal_tda import TacticalPersistenceTracker
from intelligence.valuation import ExpectedThreatEngine

# --- APP CONFIG ---
st.set_page_config(page_title="Omni-Path | Tactical Intelligence", layout="wide")
st.title("🏟️ Omni-Path: Real-Time Tactical Intelligence")
st.sidebar.header("Control Panel")

# --- INITIALIZE ENGINES ---
pitch_control = VectorizedPitchControl()
tda_tracker = TacticalPersistenceTracker()
xt_engine = ExpectedThreatEngine()

def get_latest_frame():
    """Fetches the latest player coordinates from PostGIS."""
    query = text("""
        SELECT player_id, ST_X(location) as x, ST_Y(location) as y, orientation 
        FROM events 
        ORDER BY timestamp DESC 
        LIMIT 22;
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

# --- DASHBOARD LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Pitch View")
    
    # Create the Pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(10, 7))

    # Fetch Data
    df = get_latest_frame()
    
    if not df.empty:
        # 1. Plot Players
        # (Assuming City are 'Home' and Chelsea are 'Away' for visualization)
        city_players = df[df['player_id'].str.contains('Haaland|KDB|Foden|City')]
        other_players = df[~df['player_id'].isin(city_players['player_id'])]
        
        pitch.scatter(city_players.x, city_players.y, s=300, color='#6cabdd', edgecolors='white', linewidth=2, label='Manchester City', ax=ax)
        pitch.scatter(other_players.x, other_players.y, s=300, color='#034694', edgecolors='white', linewidth=2, label='Opponent', ax=ax)
        
        # 2. Draw Orientation Arrows
        for _, p in df.iterrows():
            if p.orientation is not None:
                # Basic arrow logic based on orientation angle
                u = np.cos(np.radians(p.orientation))
                v = np.sin(np.radians(p.orientation))
                ax.quiver(p.x, p.y, u, v, color='white', width=0.005, alpha=0.6)

    st.pyplot(fig)

with col2:
    st.subheader("Intelligence Metrics")
    
    if not df.empty:
        # 1. Expected Threat (xT) Leaderboard
        st.write("**Top Threat Generators**")
        df['xT'] = df.apply(lambda r: xt_engine.get_value_at(r.x, r.y), axis=1)
        st.table(df[['player_id', 'xT']].sort_values('xT', ascending=False).head(5))
        
        # 2. TDA Stability Alert
        st.write("**Topological Pass Lanes**")
        stable_holes = tda_tracker.update(df[['x', 'y']].values)
        if stable_holes:
            st.success(f"🔥 {len(stable_holes)} STABLE passing lanes detected!")
        else:
            st.info("🛡️ Defense is currently compact.")

    # Auto-refresh
    if st.sidebar.button('Live Sync'):
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("**Architecture:** PostGIS + Redis + TDA")
st.sidebar.write("**MSCS Sprint:** Day 7")
