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

def test_process_audio__with_url(client):
    """Test the /summarize_audio POST route with valid data"""
    response = client.post('/summarize_audio',
        json={"url": "https://www.youtube.com/watch?v=221F55VPp2M&pp=ygUOc2hvcnRzIGZyaWVuZHM%3D"})
    assert response.status_code == 200
    # json_data = response.get_json()
    # assert json_data["message"] == "Hello, Test!"
