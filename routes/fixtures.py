from flask import Blueprint, render_template, request, session, redirect, url_for
import requests
import os

fixtures_bp = Blueprint('fixtures', __name__)

API_KEY = os.getenv("API_KEY", "default_api_key")
BASE_URL = "http://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}
MAX_MATCHDAY = 38  # Define maximum matchweek

# Global variable to store simulated standings across matchdays
simulated_standings = None

@fixtures_bp.route("/next-fixtures")
def next_fixtures():
    if "current_matchday" not in session:
        # Set to matchday 1 if get_current_matchday() returns None
        session["current_matchday"] = get_current_matchday() or 1
    matchday = session["current_matchday"]

    # Render final standings if matchday exceeds MAX_MATCHDAY
    if matchday > MAX_MATCHDAY:
        return render_template("updated_standings.html", table=simulated_standings)

    fixtures_url = f"{BASE_URL}/competitions/PL/matches?matchday={matchday}"
    response = requests.get(fixtures_url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        fixtures = [m for m in data.get("matches", []) if m["status"] in ["SCHEDULED", "TIMED"]]
        
        # If no fixtures available, assume matchday is over; increment and redirect
        if not fixtures:
            session["current_matchday"] += 1
            if session["current_matchday"] > MAX_MATCHDAY:
                return render_template("updated_standings.html", table=simulated_standings)
            return redirect(url_for("fixtures.next_fixtures"))
        
        return render_template("fixtures.html", fixtures=fixtures, matchday=matchday)
    else:
        if response.status_code == 429:
            error_message = "Too many requests. Please wait before retrying."
        else:
            error_message = f"Error fetching fixtures: {response.status_code}"
        return render_template("error.html", error_message=error_message)


def get_current_matchday():
    """Fetch the current matchweek dynamically."""
    competition_url = f"{BASE_URL}/competitions/PL"
    response = requests.get(competition_url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        matchday = data.get("currentSeason", {}).get("currentMatchday")
        return matchday
    return None



def get_teams():
    standings_url = f"{BASE_URL}/competitions/PL/standings"
    response = requests.get(standings_url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        if "standings" in data and len(data["standings"]) > 0:
            teams_data = data["standings"][0]["table"]
            # set initial_position for each team based on the starting order
            for idx, team in enumerate(teams_data):
                team["initial_position"] = idx + 1
                team["logo"] = team["team"]["crest"]  # Ensure logo is assigned
            return teams_data
        else:
            return []
    else:
        return []

# ✅ **Fixed update_standings: Now handles both standings & goal difference**
def update_standings(home_team_result, away_team_result, teams):
    for team in teams:
        if team["team"]["name"] == home_team_result["name"]:
            team["playedGames"] += 1
            team["goalDifference"] += home_team_result["goal_difference"]  # ✅ Fixed
            if home_team_result["result"] == "win":
                team["won"] += 1
                team["points"] += 3
            elif home_team_result["result"] == "draw":
                team["draw"] += 1
                team["points"] += 1
            elif home_team_result["result"] == "loss":
                team["lost"] += 1

        elif team["team"]["name"] == away_team_result["name"]:
            team["playedGames"] += 1
            team["goalDifference"] += away_team_result["goal_difference"]  # ✅ Fixed
            if away_team_result["result"] == "win":
                team["won"] += 1
                team["points"] += 3
            elif away_team_result["result"] == "draw":
                team["draw"] += 1
                team["points"] += 1
            elif away_team_result["result"] == "loss":
                team["lost"] += 1

    teams.sort(key=lambda x: (x["points"], x["goalDifference"], x["won"]), reverse=True)


def process_match_prediction(prediction, home_team, away_team, home_goals=None, away_goals=None):
    if prediction == "win_home":
        return {"name": home_team, "result": "win", "goal_difference": 3}, {"name": away_team, "result": "loss", "goal_difference": -3}
    elif prediction == "win_away":
        return {"name": away_team, "result": "win", "goal_difference": 3}, {"name": home_team, "result": "loss", "goal_difference": -3}
    elif prediction == "draw":
        return {"name": home_team, "result": "draw", "goal_difference": 0}, {"name": away_team, "result": "draw", "goal_difference": 0}
    elif prediction == "custom":
        if home_goals is not None and away_goals is not None:
            home_diff = home_goals - away_goals
            away_diff = away_goals - home_goals
            if home_goals > away_goals:
                return {"name": home_team, "result": "win", "goal_difference": home_diff}, {"name": away_team, "result": "loss", "goal_difference": away_diff}
            elif away_goals > home_goals:
                return {"name": away_team, "result": "win", "goal_difference": away_diff}, {"name": home_team, "result": "loss", "goal_difference": home_diff}
            else:
                return {"name": home_team, "result": "draw", "goal_difference": 0}, {"name": away_team, "result": "draw", "goal_difference": 0}
        else:
            return None, None
    else:
        return None, None

@fixtures_bp.route("/process_predictions", methods=["POST"])
def process_predictions():
    global simulated_standings  # Use global simulated standings
    if simulated_standings is None:
        simulated_standings = get_teams()
    predictions = {}
    # ...existing prediction processing...
    for key in request.form:
        if key.startswith("prediction_"):
            match_id = key.replace("prediction_", "")
            prediction = request.form.get(key)
            if not prediction:
                return "Error: Missing predictions for one or more matches", 400
            if prediction == "custom":
                home_goals = request.form.get(f"home_goals_{match_id}")
                away_goals = request.form.get(f"away_goals_{match_id}")
                if not home_goals or not away_goals:
                    return f"Error: Missing custom scores for match {match_id}", 400
                predictions[match_id] = {
                    "prediction": prediction,
                    "home_goals": int(home_goals),
                    "away_goals": int(away_goals)
                }
            else:
                predictions[match_id] = {"prediction": prediction}
    for match_id, data in predictions.items():
        home_team = request.form.get(f"home_team_{match_id}")
        away_team = request.form.get(f"away_team_{match_id}")
        prediction = data['prediction']
        home_goals = data.get('home_goals', None)
        away_goals = data.get('home_goals', None)
        home_team_result, away_team_result = process_match_prediction(
            prediction, home_team, away_team, home_goals, away_goals
        )
        if home_team_result is None or away_team_result is None:
            return f"Error: Invalid prediction or missing data for match {match_id}", 400
        update_standings(home_team_result, away_team_result, simulated_standings)
    # Save updated standings in session
    session["simulated_standings"] = simulated_standings
    if session["current_matchday"] == MAX_MATCHDAY:
        session["current_matchday"] = MAX_MATCHDAY + 1
        standings_matchday = "Final"
        return render_template("updated_standings.html", table=simulated_standings, standings_matchday=standings_matchday)
    else:
        session["current_matchday"] += 1
        return redirect(url_for("fixtures.next_fixtures"))

@fixtures_bp.route("/view-standings")
def view_standings():
    global simulated_standings
    if simulated_standings is None:
        # Retrieve standings from session if available; otherwise, initialize
        simulated_standings = session.get("simulated_standings") or get_teams()
    current = session.get("current_matchday", get_current_matchday() or 1)
    if current >= MAX_MATCHDAY + 1:
        standings_matchday = "Final"
    elif current > 1:
        standings_matchday = current - 1
    else:
        standings_matchday = current  # if current is 1
    return render_template("updated_standings.html", table=simulated_standings, standings_matchday=standings_matchday)