# Use a stable Python version compatible with sklearn/numpy
FROM python:3.10-slim

# Create work directory
WORKDIR /app

# Install system libraries needed for numpy/scipy
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    gfortran \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first (for Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files
COPY . .

# Expose port for the container
EXPOSE 8000

# Run app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
