from flask import Flask
from routes import blueprints  # Import all blueprints

app = Flask(__name__)
app.secret_key = "my_secret_key"  # Ensure sessions persist

# Register all blueprints dynamically
for bp in blueprints:
    app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
