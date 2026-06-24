from flask import Blueprint, request, jsonify

from auth import verify_token
from rag import chat_with_codebase

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/", methods=["POST"])
def chat():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    guide_id = data.get("guide_id")
    question = data.get("question")
    conversation_history = data.get("conversation_history", [])

    if not guide_id or not question:
        return jsonify({"error": "guide_id and question required"}), 400

    answer = chat_with_codebase(
        payload["workspace_id"],
        guide_id,
        question,
        conversation_history,
    )

    return jsonify({"answer": answer})