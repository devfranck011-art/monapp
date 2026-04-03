from flask import Blueprint, jsonify

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return """
    <h1>UrbanHub Park</h1>
    <p>Module de gestion des places de stationnement</p>
    <ul>
        <li><a href='/health'>Health Check good</a></li>
        <li><a href='/spots'>Parking Spots API</a></li>
    </ul>
    """


@main.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "urbanhub-park"
    })


@main.route("/spots")
def spots():
    data = [
        {"id": 1, "zone": "A", "available": True},
        {"id": 2, "zone": "A", "available": False},
        {"id": 3, "zone": "B", "available": True},
        {"id": 4, "zone": "C", "available": True}
    ]
    return jsonify(data)
