# Notion-Integration

A scalable FastAPI application with vector database integration using pinecone for document processing and semantic search capabilities.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Docker Integration](#docker-integration)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Project Overview

This project combines FastAPI's high-performance web framework with pinecone's vector database capabilities to create a robust system for document processing, vectorization.

## ✨ Features

- Document processing and vectorization
- PDF text extraction and indexing
- Semantic search capabilities
- Custom metadata handling
- Azure OpenAI integration
- Containerized deployment with Docker

## 📁 Project Structure

```
my_project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point for the application
│   ├── schemas/             # Pydantic models for request/response validation
│   │   ├── __init__.py
│   │   └── document.py
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   └── document_service.py
│   ├── utils/               # Helper functions and utilities
│   │   ├── __init__.py
│   │   └── pdf_processor.py
│   └── config.py            # Application configuration
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── Dockerfile
├── .dockerignore
├── .env
├── .gitignore
└── requirements.txt

It will be updated accordingly
```

## 🔧 Installation

### Prerequisites
- Python 3.9+
- Docker and Docker Compose
- Azure OpenAI API access (for embeddings)

### Local Setup


1. Create a virtual environment:
```bash
cd Notion-Slack
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. scheduler set up 
```bash
cd app
python scheduler.py
# Edit .env with your configuration
```

## ⚙️ Configuration

Create a `.env` file with the following variables:

```
# FastAPI Configuration
FASTAPI_PORT=8000
DEBUG=True


## 🚀 Usage

### Running with Docker Compose (Recommended)

```bash
docker compose up -d
```

This will start both the FastAPI application and Wpinecone in containers with proper networking.

### Running Locally

1. Start Connecting with Cloud Wpinecone

2. Run the FastAPI application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once the application is running, access the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🐳 Docker Integration

The project includes Docker support for easy deployment:

```bash
# Build and start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License