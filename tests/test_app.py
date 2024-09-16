import pytest

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client  # client instance for testing

def test_root_path(client):
    """Test the root GET route"""
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["data"] == "root path"

# def test_echo_success(client):
#     """Test the /echo POST route with valid data"""
#     response = client.post('/echo', json={"message": "Hello, Test!"})
#     assert response.status_code == 200
#     json_data = response.get_json()
#     assert json_data["message"] == "Hello, Test!"

# def test_echo_no_message(client):
#     """Test the /echo POST route with missing data"""
#     response = client.post('/echo', json={})
#     assert response.status_code == 400
#     json_data = response.get_json()
#     assert json_data["error"] == "No message provided"