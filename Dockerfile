# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create static directory if it doesn't exist
RUN mkdir -p static

# Expose port
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Run the application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app

