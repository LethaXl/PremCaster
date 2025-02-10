import requests

API_KEY = "ad80cb98885d40d382ec91db7e4351de"
BASE_URL = "http://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

def get_upcoming_fixtures():
    """Fetch next 10 scheduled fixtures from Football-Data.org"""
    fixtures_url = f"{BASE_URL}/competitions/PL/matches?status=SCHEDULED"
    response = requests.get(fixtures_url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        return data["matches"][:10]  # Return the next 10 fixtures
    else:
        return []
