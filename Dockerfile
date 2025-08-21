# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (so Docker can cache this step if unchanged)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Default command to run app (override in docker-compose or run command)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
