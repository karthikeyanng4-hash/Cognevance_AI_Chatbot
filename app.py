from flask import Flask, render_template, request, jsonify

from chatbot import get_response


app = Flask(__name__)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# CHAT API
# ============================================================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json() or {}

    message = data.get("message", "")
    password = data.get("password", None)
    context = data.get("context", {})

    response = get_response(message, password, context)

    return jsonify({
        "response": response,
        "context": context
    })


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )