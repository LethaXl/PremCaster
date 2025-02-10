from flask import Blueprint, render_template
import requests

standings_bp = Blueprint('standings', __name__)

API_KEY = "ad80cb98885d40d382ec91db7e4351de"
BASE_URL = "http://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

# Route to display the Premier League table
@standings_bp.route("/")
def home():
    standings_url = f"{BASE_URL}/competitions/PL/standings"
    response = requests.get(standings_url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        table = data["standings"][0]["table"]  # First "standings" array contains the actual league table
        return render_template("index.html", table=table)
    else:
        return f"Error fetching standings: {response.status_code}"

