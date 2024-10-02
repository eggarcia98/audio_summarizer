FROM python:3.12.6-slim
WORKDIR /app
COPY . /app
# Create and activate a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN apt-get update && apt-get install -y libpq-dev
# Install dependencies within the virtual environment
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "app:app"]
