import json
import re
import time
import base64
from curl_cffi import requests
from sqlalchemy.orm import sessionmaker
from main import UnderstatShot, engine

# Constants
PITCH_LENGTH, PITCH_WIDTH = 105.0, 68.0

def get_match_ids():
    """Hits the team's data endpoint directly using TLS Impersonation."""
    url = "https://understat.com/team/Manchester_City/2024"
    print(f"📡 Requesting Direct Data Feed: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        # impersonate="chrome120" is the secret sauce to bypass Cloudflare without a browser
        response = requests.get(url, headers=headers, impersonate="chrome120", timeout=20)
        content = response.text
        
        # Understat embeds the data in a script tag as a Base64 string inside JSON.parse
        match = re.search(r"JSON\.parse\(['\"](.*?)['\"]\)", content)
        if not match:
            print("❌ Regex failed. Understat might be blocking this IP.")
            return []

        # Step 1: Decode the string
        # Understat uses a mix of hex-escaping and base64
        raw_val = match.group(1).encode('utf-8').decode('unicode_escape')
        
        # Step 2: Handle the Base64/JSON layer
        try:
            # Understat data is often base64 encoded as a string within a string
            decoded_val = base64.b64decode(raw_val).decode('utf-8')
            data = json.loads(decoded_val)
        except Exception:
            # If not base64, try direct JSON load
            data = json.loads(raw_val)

        # Step 3: Handle potential double-encoding or nested strings
        if isinstance(data, str):
            data = json.loads(data)

        # Step 4: Filter for played matches (isResult)
        if isinstance(data, dict):
            schedule = data.get('dates', data)
        else:
            schedule = data
        
        match_ids = []
        if isinstance(schedule, list):
            match_ids = [m['id'] for m in schedule if (m.get('isResult') or str(m.get('isResult')) == '1')]
        
        print(f"✅ Success! Found {len(match_ids)} match IDs.")
        return match_ids

    except Exception as e:
        print(f"❌ API Error: {e}")
        return []

def fetch_and_load_match(match_id, db_session):
    """Fetches shots for a specific match and loads into PostGIS."""
    url = f"https://understat.com/match/{match_id}"
    try:
        response = requests.get(url, impersonate="chrome120", timeout=15)
        match = re.search(r"shotsData\s*=\s*JSON\.parse\(['\"](.*?)['\"]\)", response.text)
        if not match: return 0
            
        raw_val = match.group(1).encode('utf-8').decode('unicode_escape')
        try:
            decoded_val = base64.b64decode(raw_val).decode('utf-8')
            shots_data = json.loads(decoded_val)
        except:
            shots_data = json.loads(raw_val)

        if isinstance(shots_data, str):
            shots_data = json.loads(shots_data)
        
        # Unpack Home and Away shots
        new_count = 0
        for side in ['h', 'a']:
            for shot in shots_data.get(side, []):
                # Duplicate check
                if not db_session.query(UnderstatShot).filter_by(id=shot['id']).first():
                    db_session.add(UnderstatShot(
                        id=shot['id'],
                        minute=int(shot['minute']),
                        player=shot['player'],
                        team=shot['h_team'] if shot['h_a'] == 'h' else shot['a_team'],
                        result=shot['result'],
                        xg=float(shot['xG']),
                        location=f"POINT({float(shot['X'])*PITCH_LENGTH} {float(shot['Y'])*PITCH_WIDTH})"
                    ))
                    new_count += 1
        db_session.commit()
        return new_count
    except: return 0

if __name__ == "__main__":
    ids = get_match_ids()
    if ids:
        Session = sessionmaker(bind=engine)
        s = Session()
        for i, mid in enumerate(ids, 1):
            n = fetch_and_load_match(mid, s)
            print(f"📈 [{i}/{len(ids)}] Match {mid}: +{n} shots.")
            time.sleep(1) # Be a "good" crawler