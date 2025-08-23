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

The service will be available at `http://localhost:8001`

## API Documentation

Once the service is running, you can access:

- API Documentation: `http://localhost:8001/docs`
- Alternative Documentation: `http://localhost:8001/redoc`