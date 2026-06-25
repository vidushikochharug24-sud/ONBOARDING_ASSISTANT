from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

from auth import auth_bp
from analyze import analyze_bp
from storage import storage_bp
from chat import chat_bp

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET"] = os.getenv("JWT_SECRET")

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(analyze_bp, url_prefix="/api/analyze")
app.register_blueprint(storage_bp, url_prefix="/api/storage")
app.register_blueprint(chat_bp, url_prefix="/api/chat")

@app.route("/")
def home():
    return jsonify({"status": "Onboarding Assistant API running"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
