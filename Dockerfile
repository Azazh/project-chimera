# Dockerfile — Secure Multi-Stage Build for Project Chimera (Python Agent Runtime)

########################################
# Stage 1: Builder
########################################
FROM python:3.12-slim AS builder

# Install system dependencies needed for common Python libraries (e.g., psycopg2)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       curl \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment for reproducible builds
ENV VENV_PATH=/opt/venv
RUN python -m venv "$VENV_PATH"
ENV PATH="$VENV_PATH/bin:$PATH"

# Upgrade pip tooling
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install baseline orchestrator dependencies
# Notes:
# - jsonschema: Contract-first validation for Planner/Worker/Judge IO
# - requests: HTTP interactions for MCP adapters and external tools
# - weaviate-client: Vector memory client
# - psycopg2-binary: PostgreSQL connectivity for OCC and audit logs
# - pytest: Test framework for CI
# - Optional: coinbase SDK for AgentKit (generic coinbase Python client)
# - Optional: openai (as a stand-in for OpenClaw-related LLM calls if needed)
RUN pip install --no-cache-dir \
    jsonschema \
    requests \
    weaviate-client \
    psycopg2-binary \
    pytest \
    coinbase \
    openai \
    fastapi \
    uvicorn

# Copy project metadata and source (if any) for installing local package later
WORKDIR /app
COPY pyproject.toml README.md ./
# Copy the rest of the repository (including specs, skills, tests)
COPY . .

# (Optional) If you later publish as a package, you could do:
# RUN pip install --no-cache-dir .

########################################
# Stage 2: Runtime (Non-root, Safety-First)
########################################
FROM python:3.12-slim AS runtime

# Create non-root user and group
ARG APP_UID=10001
ARG APP_GID=10001
RUN groupadd -g ${APP_GID} appgroup \
    && useradd -m -u ${APP_UID} -g ${APP_GID} appuser

# Copy virtual environment from builder
ENV VENV_PATH=/opt/venv
COPY --from=builder ${VENV_PATH} ${VENV_PATH}
ENV PATH="$VENV_PATH/bin:$PATH"

# Create app directory and set permissions
WORKDIR /app
COPY --chown=appuser:appgroup . /app

# Environment variable placeholders (to be provided via CI/CD or docker run)
# Coinbase AgentKit / Wallet Manager
ENV COINBASE_API_KEY="changeme"
ENV COINBASE_API_SECRET="changeme"
ENV COINBASE_API_PASSPHRASE="changeme"
# OpenClaw / LLM Provider
ENV OPENAI_API_KEY="changeme"
# MCP Gateway / External Adapters
ENV MCP_SERVER_URL="https://example-mcp-gateway"
ENV MOLTBOOK_API_KEY="changeme"
# Database / Storage
ENV DATABASE_URL="postgresql://user:pass@db:5432/chimera"
ENV WEAVIATE_ENDPOINT="http://weaviate:8080"

# Run as non-root for security
USER appuser

# Default command (placeholder): Print readiness & run tests if desired
# You can override CMD in docker-compose or CI to start your gateway/runtime.
CMD ["python", "-c", "print('Chimera agent runtime container ready')"]
