# Makefile — Master Control Panel for Project Chimera
# Use: make setup | make test | make lint | make build | make run

# Image name for Docker builds
IMAGE_NAME ?= project-chimera:local

.PHONY: setup test lint build run help

help:
	@echo "Targets: setup, test, lint, build, run"

setup:
	@echo "[Setup] Installing dev tools into current environment..."
	python -m pip install --upgrade pip setuptools wheel
	python -m pip install pytest coverage ruff pip-audit
	@echo "[Setup] Done."

# Run pytest with coverage. Tests are expected to fail initially (TDD goalposts).
test:
	@echo "[Test] Running pytest with coverage..."
	pytest -q --maxfail=1 --disable-warnings --cov=. --cov-report=term-missing

# Lint using ruff (configured in pyproject.toml)
lint:
	@echo "[Lint] Checking code quality with ruff..."
	ruff check .

# Build Docker image using the secure multi-stage Dockerfile
build:
	@echo "[Build] Building Docker image $(IMAGE_NAME)..."
	docker build -t $(IMAGE_NAME) .

# Execute the agent swarm locally (placeholder until runtime is implemented)
# Override as needed to start OpenClaw Gateway / agents.
run:
	@echo "[Run] Starting gateway demo..."
	python chimera/run_demo.py

# Serve the minimal frontend for examiners (defaults to :8080)
.PHONY: ui
ui:
	@echo "[UI] Serving ./frontend at http://localhost:8080 ... (Ctrl+C to stop)"
	python -m http.server 8080 -d frontend

.PHONY: ui-secure
ui-secure:
	@echo "[UI] Serving secure frontend with headers at http://localhost:8080 ..."
	python scripts/serve_ui_secure.py

.PHONY: api
api:
	@echo "[API] Starting FastAPI Orchestrator at http://localhost:8000 ..."
	uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload