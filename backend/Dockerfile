FROM python:3.11-slim

WORKDIR /code

# Install dependencies first (leverages Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Production: no --reload flag (hot-reload is added via docker-compose for dev)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
