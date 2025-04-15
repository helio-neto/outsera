from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_movie():
    # Test for movie with id 1 (adjust as needed for your data)
    response = client.get("/movie/1")
    assert response.status_code == 200
    # Response may be None if no movie with id 1 exists
    assert response.json() is None or isinstance(response.json(), list) or isinstance(response.json(), tuple)

def test_get_movie_winners():
    response = client.get("/movie/analysis/winners")
    assert response.status_code == 200
    # Should return a list (possibly empty)
    assert isinstance(response.json(), dict)
