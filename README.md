# Problem of the Day (POTD) Generator Service

A FastAPI-based service that generates and manages coding problems for developers.

## Features

- Daily curated coding problems
- Topic-based problem threads
- Custom problem generation
- Team collaboration support

## Prerequisites

- Python 3.11+
- Docker and Docker Compose

## Setup

1. Clone the repository
2. Create a `.env` file in the root directory (if needed)
3. Build and start the service using Docker Compose:

```bash
docker-compose up --build
```

The service will be available at `http://localhost:8000`

## API Documentation

Once the service is running, you can access:

- API Documentation: `http://localhost:8000/docs`
- Alternative Documentation: `http://localhost:8000/redoc`

## Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure

```
generator/
├── app/
│   ├── __init__.py
│   └── main.py         # Main FastAPI application
├── .env                # Environment variables
├── .gitignore
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## License

[Specify License]