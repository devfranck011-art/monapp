from app import create_app


def test_home():
    app = create_app()
    client = app.test_client()

    response = client.get("/")
    assert response.status_code == 200
    assert b"UrbanHub Park" in response.data


def test_health():
    app = create_app()
    client = app.test_client()

    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_spots():
    app = create_app()
    client = app.test_client()

    response = client.get("/spots")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert len(response.get_json()) > 0
