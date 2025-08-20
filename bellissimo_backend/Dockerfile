# Stage 1: Base build stage
FROM python:3.13-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.13-slim

# Add system dependencies for postgres client tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

COPY --chown=appuser:appuser . .

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_ENV=production  

USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
