import os
from flask import Flask
from routes import blueprints  # Import all blueprints
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY") 
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")

# Register all blueprints dynamically
for bp in blueprints:
    app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
