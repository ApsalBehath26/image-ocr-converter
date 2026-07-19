"""API routes for OCR converter"""

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from app.ocr_processor import OCRProcessor
import logging

logger = logging.getLogger(__name__)
ocr_bp = Blueprint('ocr', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ocr_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'image-ocr-converter',
        'version': '1.0.0'
    }), 200

@ocr_bp.route('/convert', methods=['POST'])
def convert_image():
    """Convert image to text using OCR"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Allowed: png, jpg, jpeg, gif, bmp'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        
        # Process OCR
        ocr_processor = OCRProcessor()
        result = ocr_processor.process_image(upload_path)
        
        # Clean up
        os.remove(upload_path)
        
        return jsonify({
            'success': True,
            'data': result,
            'filename': filename
        }), 200
    
    except Exception as e:
        logger.error(f'Error processing image: {str(e)}')
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@ocr_bp.route('/convert/batch', methods=['POST'])
def convert_batch():
    """Batch convert multiple images"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        results = []
        
        ocr_processor = OCRProcessor()
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)
                
                result = ocr_processor.process_image(upload_path)
                results.append({
                    'filename': filename,
                    'data': result
                })
                
                os.remove(upload_path)
        
        return jsonify({
            'success': True,
            'count': len(results),
            'results': results
        }), 200
    
    except Exception as e:
        logger.error(f'Error processing batch: {str(e)}')
        return jsonify({'error': f'Batch processing error: {str(e)}'}), 500

@ocr_bp.route('/info', methods=['GET'])
def info():
    """Get service information"""
    return jsonify({
        'name': 'Image OCR Converter',
        'version': '1.0.0',
        'description': 'Convert images to text using OCR',
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'max_file_size': '10MB'
    }), 200
