"""test_factory tests the application factory"""

from flaskr import create_app

def test_config():
    """Test creating with different configurations"""
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello world'

