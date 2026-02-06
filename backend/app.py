from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import os

app = FastAPI(title="Chimera Orchestrator API")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/acceptance")
def acceptance():
    # Try to load JSON acceptance criteria if present; fallback to markdown stub
    json_path = os.path.join(ROOT, "docs", "acceptance_criteria.json")
    md_path = os.path.join(ROOT, "docs", "acceptance_criteria.md")
    if os.path.exists(json_path):
        with open(json_path) as f:
            return JSONResponse(json.load(f))
    if os.path.exists(md_path):
        with open(md_path) as f:
            return {"markdown": f.read()}
    return {"message": "Acceptance criteria not found."}

@app.get("/servers")
def servers():
    mcp_path = os.path.join(ROOT, ".vscode", "mcp.json")
    if os.path.exists(mcp_path):
        with open(mcp_path) as f:
            try:
                return JSONResponse(json.load(f))
            except Exception:
                return {"error": "Invalid JSON in .vscode/mcp.json"}
    return {"servers": []}

# Serve the frontend statically under /
frontend_dir = os.path.join(ROOT, "frontend")
if os.path.isdir(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
