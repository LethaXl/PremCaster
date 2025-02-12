from flask import Blueprint

# Import blueprints from route files
from .standings import standings_bp
from .fixtures import fixtures_bp
from .teams import teams_bp
from dotenv import load_dotenv
load_dotenv()

# List of blueprints to be used in app.py
blueprints = [standings_bp, fixtures_bp, teams_bp]
