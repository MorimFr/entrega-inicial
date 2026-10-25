FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1 AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY pyproject.toml README.md ./
COPY campusflow ./campusflow
RUN pip install --no-cache-dir . \
    && groupadd --system campusflow \
    && useradd --system --gid campusflow --no-create-home campusflow \
    && mkdir -p /app/data \
    && chown campusflow:campusflow /app/data

FROM base AS tests
RUN pip install --no-cache-dir ".[dev]"
COPY tests ./tests
COPY scripts/run_harness.py scripts/demo_api.py ./scripts/
CMD ["python", "scripts/run_harness.py"]

FROM base AS runtime
USER campusflow
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=5 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn", "campusflow.api:app", "--host", "0.0.0.0", "--port", "8000"]
