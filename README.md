# Image to OCR Text Converter

A scalable web application that converts images to text using OCR technology, containerized with Docker, automated with Jenkins CI/CD, and deployed to AWS ECR.

## Features

- **Image Upload**: Support for JPG, PNG, GIF, BMP formats
- **OCR Processing**: High-accuracy text extraction using Tesseract OCR
- **Text Output**: Clean, formatted text extraction with confidence scores
- **Batch Processing**: Handle multiple image conversions
- **Docker Containerization**: Lightweight, portable deployment
- **Jenkins Automation**: Automated build, test, and deploy pipeline
- **AWS ECR Integration**: Push images to Amazon Elastic Container Registry

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Jenkins (for CI/CD pipeline)
- AWS Account with ECR repository
- Python 3.9+

### Local Development

```bash
# Clone the repository
git clone https://github.com/ApsalBehath26/image-ocr-converter.git
cd image-ocr-converter

# Build Docker image
docker build -t image-ocr-converter:latest .

# Run with Docker Compose
docker-compose up -d

# Access the application
http://localhost:5000
```

### Jenkins Deployment

1. Configure Jenkins pipeline with `Jenkinsfile`
2. Set AWS credentials in Jenkins
3. Pipeline automatically builds, tests, and pushes to ECR

## Project Structure

```
.
├── app/                      # Flask application
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── routes.py            # API routes
│   ├── ocr_processor.py     # OCR logic
│   └── config.py            # Configuration
├── tests/                    # Test suite
├── Dockerfile               # Container image definition
├── docker-compose.yml       # Multi-container setup
├── Jenkinsfile             # CI/CD pipeline
├── requirements.txt         # Python dependencies
└── README.md
```

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed AWS ECR and Jenkins setup instructions.

## License

MIT
