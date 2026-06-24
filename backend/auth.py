from flask import Blueprint, request, jsonify
from supabase import create_client
import os
import jwt
import datetime
import re

auth_bp = Blueprint("auth", __name__)

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

JWT_SECRET = os.getenv("JWT_SECRET")


def extract_domain(email):
    match = re.search(r"@(.+)$", email)
    return match.group(1).lower() if match else None


def generate_token(user_id, email, workspace_id):
    payload = {
        "user_id": user_id,
        "email": email,
        "workspace_id": workspace_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def verify_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email", "").lower().strip()
    password = data.get("password", "")
    company_name = data.get("company_name", "").strip()

    if not email or not password or not company_name:
        return jsonify({"error": "Email, password and company name are required"}), 400

    domain = extract_domain(email)
    if not domain:
        return jsonify({"error": "Invalid email"}), 400

    # Check if workspace with this domain already exists
    existing = supabase.table("workspaces").select("*").eq("domain", domain).execute()

    if existing.data:
        workspace_id = existing.data[0]["id"]
    else:
        # Create new workspace
        workspace = supabase.table("workspaces").insert({
            "company_name": company_name,
            "domain": domain
        }).execute()
        workspace_id = workspace.data[0]["id"]

    # Create user
    try:
        user = supabase.table("users").insert({
            "email": email,
            "password_hash": password,  # In production use bcrypt
            "workspace_id": workspace_id
        }).execute()
        user_id = user.data[0]["id"]
    except Exception as e:
        return jsonify({"error": "Email already exists"}), 400

    token = generate_token(user_id, email, workspace_id)
    return jsonify({
        "token": token,
        "email": email,
        "workspace_id": workspace_id,
        "company_name": company_name
    })


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email", "").lower().strip()
    password = data.get("password", "")

    user = supabase.table("users").select("*, workspaces(*)").eq("email", email).eq("password_hash", password).execute()

    if not user.data:
        return jsonify({"error": "Invalid email or password"}), 401

    user_data = user.data[0]
    token = generate_token(user_data["id"], email, user_data["workspace_id"])

    return jsonify({
        "token": token,
        "email": email,
        "workspace_id": user_data["workspace_id"],
        "company_name": user_data["workspaces"]["company_name"]
    })


@auth_bp.route("/me", methods=["GET"])
def me():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "Invalid or expired token"}), 401
    return jsonify(payload)
