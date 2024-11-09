# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install Python dependencies all at once for better layer caching
RUN pip install --no-cache-dir \
    Flask==2.3.2 \
    joblib==1.3.1 \
    scikit-learn==1.2.2 \
    requests>=2.31.0 \
    pyngrok==6.0.3

# Copy the rest of your application code into the container
COPY . .

# Expose the port that Flask will run on
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]