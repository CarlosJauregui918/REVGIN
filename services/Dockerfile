FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY setup.py .
COPY api api/

# Install Python packages
RUN pip install -e .

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# List contents of /app directory
RUN ls -la /app

# Run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 