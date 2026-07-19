"""OCR Processing Logic"""

import pytesseract
from PIL import Image
import cv2
import numpy as np
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class OCRProcessor:
    """Handles OCR processing of images"""
    
    def __init__(self):
        """Initialize OCR processor"""
        self.languages = 'eng'  # Default to English
        self.config = r'--oem 3 --psm 6'  # Tesseract config
    
    def preprocess_image(self, image_path):
        """Preprocess image for better OCR accuracy"""
        try:
            # Read image
            img = cv2.imread(image_path)
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(thresh, h=10)
            
            # Upscale for better OCR
            upscaled = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            
            return upscaled
        except Exception as e:
            logger.error(f'Error preprocessing image: {str(e)}')
            return cv2.imread(image_path)
    
    def process_image(self, image_path, languages='eng'):
        """Process image and extract text using OCR"""
        try:
            # Start timer
            start_time = datetime.now()
            
            # Preprocess image
            processed_img = self.preprocess_image(image_path)
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(processed_img, lang=languages, config=self.config)
            
            # Get detailed data
            data = pytesseract.image_to_data(
                processed_img,
                lang=languages,
                config=self.config,
                output_type=pytesseract.Output.DICT
            )
            
            # Calculate confidence scores
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # End timer
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            return {
                'text': text.strip(),
                'confidence': avg_confidence,
                'word_count': len(text.split()),
                'processing_time_seconds': processing_time,
                'language': languages,
                'timestamp': start_time.isoformat(),
                'details': {
                    'total_words_detected': len(data['text']),
                    'word_confidences': confidences[:10]  # Top 10 word confidences
                }
            }
        
        except Exception as e:
            logger.error(f'Error processing image with OCR: {str(e)}')
            raise
    
    def extract_text_with_coordinates(self, image_path, languages='eng'):
        """Extract text with bounding box coordinates"""
        try:
            img = cv2.imread(image_path)
            
            data = pytesseract.image_to_data(
                img,
                lang=languages,
                config=self.config,
                output_type=pytesseract.Output.DICT
            )
            
            results = []
            for i, text in enumerate(data['text']):
                if text.strip():
                    results.append({
                        'text': text,
                        'confidence': int(data['conf'][i]),
                        'x': int(data['left'][i]),
                        'y': int(data['top'][i]),
                        'width': int(data['width'][i]),
                        'height': int(data['height'][i])
                    })
            
            return results
        
        except Exception as e:
            logger.error(f'Error extracting text with coordinates: {str(e)}')
            raise
