# Lightweight image of Python 3.12
FROM python:3.12-slim

# Working directory within the container
WORKDIR /app

# Create new group, new user 
RUN addgroup --system appgroup && adduser --system --group appuser

# Requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# We five the 'appuser' permission on the /app folder
RUN chown -R appuser:appgroup /app

# Beyond here, nothing execute as root
USER appuser

# Start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]