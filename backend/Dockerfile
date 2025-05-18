# Stage 1: build with all deps
FROM python:3.13-alpine AS builder

# install build-time deps for any C‐extensions
RUN apk add --no-cache gcc musl-dev postgresql-dev

WORKDIR /app
COPY requirements.txt .

# install everything (uvicorn included)
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: runtime
FROM python:3.13-alpine

WORKDIR /app

# copy libraries and console‐scripts
COPY --from=builder /usr/local/lib/python3.13/site-packages \
                   /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY app/ ./app/

EXPOSE 8181

# ← invoke via python -m to avoid missing uvicorn script
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8181", "--reload"]
