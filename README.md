# TinyURL Clone

This project implements a **microservices** architecture using Docker containers to orchestrate the Frontend, Backend, and Database.

## System Architecture

The project is divided into three main interconnected services:

1. **Frontend (React + Vite):** Clean user interface to enter URLs and view results.
2. **Backend (FastAPI + Python):** Handles shortening, validation, and redirection logic.
3. **Database (MongoDB):** Persistent NoSQL storage. Optimized with indexes for searches and duplicate validation.

## Quick Start

### Prerequisites
- Docker and Docker Compose installed on your system.

### Running the Project
To bring up the entire environment, you only need one command at the root of the project:

```bash
docker compose up --build```