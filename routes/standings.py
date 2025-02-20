from flask import Blueprint, session, redirect, url_for, render_template
from routes.fixtures import get_teams  
import routes.fixtures as fixtures_module  # to reset simulated_standings
import requests
import os
from dotenv import load_dotenv
load_dotenv()

standings_bp = Blueprint('standings', __name__)

API_KEY = os.getenv("API_KEY", "default_api_key")
BASE_URL = "http://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

# Route to display the Premier League table
@standings_bp.route("/")
def home():
    # Reset simulation state
    session.pop("current_matchday", None)
    fixtures_module.simulated_standings = None
    teams = get_teams()  # load latest teams for home page
    return render_template("index.html", table=teams)

