from flask import Flask, request, jsonify
from dotenv import load_dotenv
from moralis import evm_api
from flask_cors import CORS
import json
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get Moralis API key from environment variable
api_key = os.getenv("MORALIS_API_KEY")

@app.route("/get_token_balance", methods=["GET"])
def get_tokens():
    try:
        chain = request.args.get("chain")
        address = request.args.get("address")

        if not chain or not address:
            return jsonify({"error": "Missing required parameters 'chain' or 'address'"}), 400

        params = {
            "address": address,
            "chain": chain,
        }

        result = evm_api.balance.get_native_balance(
            api_key=api_key,
            params=params,
        )

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_user_nfts", methods=["GET"])
def get_nfts():
    try:
        address = request.args.get("address")
        chain = request.args.get("chain")

        if not chain or not address:
            return jsonify({"error": "Missing required parameters 'chain' or 'address'"}), 400

        params = {
            "address": address,
            "chain": chain,
            "format": "decimal",
            "limit": 100,
            "token_addresses": [],
            "cursor": "",
            "normalizeMetadata": True,
        }

        result = evm_api.nft.get_wallet_nfts(
            api_key=api_key,
            params=params,
        )

        # Converting it to json because of unicode characters
        response = json.dumps(result, indent=4)
        print(response)
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
