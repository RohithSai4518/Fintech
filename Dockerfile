# Fintech Enterprise Core Banking & Trading Platform Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Environment configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    HOST=0.0.0.0

# Copy project source files
COPY . /app

# Expose HTTP service port
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/api/kpis')" || exit 1

# Launch application
CMD ["python", "main.py"]
