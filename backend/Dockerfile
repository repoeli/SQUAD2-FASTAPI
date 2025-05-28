# ── Alpine-based image for minimal vulnerabilities ──────────────────────────────
FROM python:alpine

# Install build dependencies, then remove them to keep image small
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install --no-cache-dir --upgrade pip

WORKDIR /app

# Install your dependencies (including pytest)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pytest && \
    apk del .build-deps

# Copy application code
COPY app/ ./app/

# Copy run.py
COPY run.py .

# Expose the port you're running on
EXPOSE 8181

# Run Uvicorn via python -m so path is always correct
CMD ["python", "-m", "uvicorn", "app.main:app", \
    "--host", "0.0.0.0", "--port", "8181", "--reload"]
