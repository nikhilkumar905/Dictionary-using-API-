import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from dictionary_service import DictionaryService, clear_history, get_history


def get_allowed_origins():
    origins = os.getenv("FRONTEND_ORIGIN", "*").strip()
    if origins == "*":
        return "*"
    return [origin.strip() for origin in origins.split(",") if origin.strip()]


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": get_allowed_origins()}})


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/search")
def search_word():
    word = request.args.get("word", "").strip()
    if not word:
        return jsonify({"error": "Please provide a word."}), 400

    service = DictionaryService(word)
    result = service.get_meaning()
    return jsonify({"word": word.lower(), "result": result})


@app.get("/api/history")
def history():
    return jsonify({"history": get_history()})


@app.delete("/api/history")
def delete_history():
    clear_history()
    return jsonify({"message": "Search history cleared successfully!"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
