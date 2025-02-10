import requests
from flask import Blueprint, render_template
from config import BASE_URL, HEADERS, TEAM_IDS
from routes.utils import get_upcoming_fixtures  # Import from utils.py

teams_bp = Blueprint("teams", __name__)

@teams_bp.route("/manutd-fixtures")
def manutd_fixtures():
    """Fetch and display next 5 Manchester United fixtures"""
    future_fixtures = get_upcoming_fixtures()
    if not future_fixtures:
        return []

    mu_fixtures = [
        match for match in future_fixtures 
        if match["homeTeam"]["id"] == TEAM_IDS["Manchester United"] or match["awayTeam"]["id"] == TEAM_IDS["Manchester United"]
    ]

    return render_template("manutd_fixtures.html", fixtures=mu_fixtures[:5])
