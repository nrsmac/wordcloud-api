from fastapi.testclient import TestClient
from wordcloud_api.app import app

client = TestClient(app)


def test_create_wordcloud():
    text = "This is a sample text for creating a wordcloud. It should work well."
    response = client.post("/create_wordcloud", json={"text": text})

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


def test_create_wordcloud_empty():
    response = client.post("/create_wordcloud", json={"text": ""})

    assert response.status_code == 400


def test_create_wordcloud_invalid_input():
    response = client.post("/create_wordcloud", json={"invalid_key": "value"})

    assert response.status_code == 422
