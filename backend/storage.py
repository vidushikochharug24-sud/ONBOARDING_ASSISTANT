from flask import Blueprint, request, jsonify
from supabase import create_client
from auth import verify_token
import os
import uuid

storage_bp = Blueprint("storage", __name__)

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

BUCKET = "codebase-files"


@storage_bp.route("/upload", methods=["POST"])
def upload_file():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401

    workspace_id = payload["workspace_id"]

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filename = file.read()
    ext = file.filename.rsplit(".", 1)[-1].lower()

    if ext not in ["zip", "pdf"]:
        return jsonify({"error": "Only ZIP and PDF files are supported"}), 400

    unique_name = f"{workspace_id}/{uuid.uuid4()}.{ext}"

    try:
        supabase.storage.from_(BUCKET).upload(
            unique_name,
            filename,
            {"content-type": "application/octet-stream"}
        )
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

    # Save file record to DB
    record = supabase.table("uploaded_files").insert({
        "workspace_id": workspace_id,
        "file_path": unique_name,
        "original_name": file.filename,
        "file_type": ext
    }).execute()

    return jsonify({
        "file_path": unique_name,
        "file_id": record.data[0]["id"],
        "original_name": file.filename
    })


@storage_bp.route("/files", methods=["GET"])
def list_files():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401

    files = supabase.table("uploaded_files").select("*").eq(
        "workspace_id", payload["workspace_id"]
    ).execute()

    return jsonify(files.data)
