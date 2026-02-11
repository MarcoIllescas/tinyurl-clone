# Lightweight image of Python 3.12
FROM python:3.12-slim

# Working directory within the container
WORKDIR /app

# Requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]