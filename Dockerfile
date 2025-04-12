# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy project files into container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "We_app:app", "--host", "0.0.0.0", "--port", "8000"]
