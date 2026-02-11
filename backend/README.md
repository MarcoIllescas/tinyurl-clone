# TinyURL Clone - Backend

Backend built with **FastAPI** and **MongoDB** for shortening URLs and redirecting traffic. This service is containerized with Docker for easy deployment.

## Technologies 
- **Language:** Python 3.12
- **Framework:** FastAPI (Asynchronous)
- **Database:** MongoDB (Driver engine)
- **Infraestructure:** Docker & Docker Compose

## Installation and Running

### Prerequisites
- Docker and Docker Compose installed.
- (Optional) Python 3.12+ for local development without Docker.

### Running with Docker (Recommended)

From the project root (where the `docker-compose.yml` is located):

1. **Build and start the services:**
```bash
docker compose up --build