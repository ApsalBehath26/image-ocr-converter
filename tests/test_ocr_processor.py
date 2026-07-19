"""Tests for OCR processor"""

import pytest
from app.ocr_processor import OCRProcessor
from PIL import Image, ImageDraw
import os
import tempfile

class TestOCRProcessor:
    """Test cases for OCRProcessor"""
    
    @pytest.fixture
    def ocr_processor(self):
        """Initialize OCR processor"""
        return OCRProcessor()
    
    @pytest.fixture
    def sample_image(self):
        """Create a sample test image with text"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img = Image.new('RGB', (200, 100), color='white')
            draw = ImageDraw.Draw(img)
            draw.text((10, 10), "Test Text", fill='black')
            img.save(tmp.name)
            yield tmp.name
            os.unlink(tmp.name)
    
    def test_processor_initialization(self, ocr_processor):
        """Test OCR processor initializes correctly"""
        assert ocr_processor is not None
        assert ocr_processor.languages == 'eng'
    
    def test_preprocess_image(self, ocr_processor, sample_image):
        """Test image preprocessing"""
        processed = ocr_processor.preprocess_image(sample_image)
        assert processed is not None
        assert len(processed.shape) == 2  # Grayscale image
    
    def test_process_image(self, ocr_processor, sample_image):
        """Test image processing and text extraction"""
        result = ocr_processor.process_image(sample_image)
        
        assert 'text' in result
        assert 'confidence' in result
        assert 'word_count' in result
        assert 'processing_time_seconds' in result
        assert result['confidence'] >= 0
