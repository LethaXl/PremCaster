from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

# Replace with your Football-Data.org API key
API_KEY = os.getenv("API_KEY", "default_api_key")
BASE_URL = "http://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}
TEAM_IDS = {"Manchester United": 66}

@app.route("/")
def home():
    # Fetch Premier League standings
    standings_url = f"{BASE_URL}/competitions/PL/standings"
    response = requests.get(standings_url, headers=HEADERS)

    if response.status_code == 200:
        standings_data = response.json()
        # Extract the table data
        table = standings_data["standings"][0]["table"]
        return render_template("index.html", table=table)
    else:
        return f"Error fetching data: {response.status_code}"

if __name__ == "__main__":
    app.run(debug=True)
