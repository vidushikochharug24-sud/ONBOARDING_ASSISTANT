from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

# Validate required environment variables before importing modules that
# instantiate clients (these imports use env vars at import time).
REQUIRED_ENVS = [
    "SUPABASE_URL",
    "SUPABASE_SERVICE_KEY",
    "JWT_SECRET",
    "GROQ_API_KEY",
]
missing = [v for v in REQUIRED_ENVS if not os.getenv(v) or not os.getenv(v).strip()]
if missing:
    print("Missing required environment variables: " + ", ".join(missing))
    print("Set them in your host (Render) or your environment. Do NOT commit secrets to the repo.")
    import sys

    sys.exit(1)

from auth import auth_bp
from analyze import analyze_bp
from chat import chat_bp
from storage import storage_bp

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET"] = os.getenv("JWT_SECRET")

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(analyze_bp, url_prefix="/api/analyze")
app.register_blueprint(chat_bp, url_prefix="/api/chat")
app.register_blueprint(storage_bp, url_prefix="/api/storage")

@app.route("/")
def home():
    return jsonify({"status": "Onboarding Assistant API running"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
