from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

CLIENT_ID = os.getenv("PISTE_CLIENT_ID")
CLIENT_SECRET = os.getenv("PISTE_CLIENT_SECRET")

@app.route("/search", methods=["POST"])
def search_legifrance():
    try:
        token_url = "https://oauth.piste.gouv.fr/api/oauth/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        token_response = requests.post(token_url, data=data)
        token_json = token_response.json()
        access_token = token_json.get("access_token")

        if not access_token:
            return jsonify({"error": "Impossible d'obtenir un token", "details": token_json}), 401

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        api_url = "https://api.piste.gouv.fr/dila/legifrance/lf-engine-app/search"
        response = requests.post(api_url, headers=headers, json=request.json)

        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
