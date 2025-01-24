FROM python:3.12.6-slim

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . /app

# Expose the Cloud Run port
EXPOSE 8080

# Start Gunicorn, binding to 0.0.0.0:8080, using the app object in app.py
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "600", "app:app"]