from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)
app.secret_key = "superstrongsecretkey"  

# Fortnite API key
API_KEY = "8b38f1c5-f0de-41c2-8dd8-935cc78b7f1d"  # Replace with your actual API key

# Simple credentials for login (replace with a database for production)
USERNAME = "mpampis"
PASSWORD = "nigger"

def get_fortnite_account_id(username, api_key):
    if not api_key:
        return {"error": "API key is missing."}

    url = f"https://fortnite-api.com/v2/stats/br/v2?name={username}"
    headers = {
        'Authorization': api_key
    }

    # Configure retries for the session
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    # Make the request
    response = session.get(url, headers=headers)

    # Handle responses
    if response.status_code == 200:
        try:
            data = response.json()
            if 'data' in data and 'account' in data['data']:
                return {"account_id": data['data']['account']['id']}
            else:
                return {"error": "Unexpected data format.", "response": data}
        except (ValueError, KeyError) as e:
            return {"error": f"Error parsing JSON: {str(e)}"}
    elif response.status_code == 401:
        return {"error": "Invalid or missing API key."}
    else:
        return {"error": f"HTTP {response.status_code}: {response.reason}"}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/home")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")  # Create this template for the input form

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/get_account_id", methods=["POST"])
def get_account_id():
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized"}), 403

    username = request.form.get("username")
    if not username:
        return jsonify({"error": "Username is required."}), 400

    result = get_fortnite_account_id(username, API_KEY)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
