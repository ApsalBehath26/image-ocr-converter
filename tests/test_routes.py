"""Tests for API routes"""

import pytest
from app import create_app
from io import BytesIO
from PIL import Image
import tempfile

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def create_test_image():
    """Create a test image"""
    img = Image.new('RGB', (100, 100), color='white')
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

class TestRoutes:
    """Test cases for API routes"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'
    
    def test_info_endpoint(self, client):
        """Test info endpoint"""
        response = client.get('/api/info')
        assert response.status_code == 200
        assert 'name' in response.json
        assert response.json['name'] == 'Image OCR Converter'
    
    def test_convert_no_file(self, client):
        """Test convert endpoint without file"""
        response = client.post('/api/convert')
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_convert_invalid_file(self, client):
        """Test convert endpoint with invalid file type"""
        data = {
            'file': (BytesIO(b'test content'), 'test.txt')
        }
        response = client.post('/api/convert', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        assert 'not allowed' in response.json['error'].lower()
