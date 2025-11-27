import os
from flask import Flask, jsonify, request
from pymongo import MongoClient

MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", "27017"))
MONGO_DB = os.environ.get("MONGO_DB", "flaskdb")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")

if MONGO_USER and MONGO_PASSWORD:
    mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
else:
    mongo_uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

client = MongoClient(mongo_uri)
db = client[MONGO_DB]
items_col = db["items"]

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health():
    return jsonify(
        status="ok",
        message="Flask-MongoDB app is running",
        mongo_host=MONGO_HOST,
        mongo_db=MONGO_DB,
    )


@app.route("/items", methods=["GET"])
def get_items():
    items = []
    for doc in items_col.find():
        doc["_id"] = str(doc["_id"])
        items.append(doc)
    return jsonify(items)


@app.route("/items", methods=["POST"])
def create_item():
    data = request.json or {}
    result = items_col.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201


if __name__ == "__main__":
    # For Docker/K8s we bind to 0.0.0.0
    app.run(host="0.0.0.0", port=5000, debug=True)
