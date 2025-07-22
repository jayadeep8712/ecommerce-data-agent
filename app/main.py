# app/main.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response  # IMPORT Response

from app.api.endpoints import router as api_router

app = FastAPI(title="E-commerce AI Agent")

# CORRECTED/VERIFIED: This line tells FastAPI to serve files from the 'app/static'
# directory when a URL starts with '/static'. This must match your folder structure.
# ProjectRoot/app/static/styles.css -> http://127.0.0.1:8000/static/styles.css
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates for the frontend
templates = Jinja2Templates(directory="app/templates")

# Include the API router
app.include_router(api_router, prefix="/api")

# ADDED: This handles the browser's automatic request for a tab icon.
# It returns a "204 No Content" response, which stops the 404 error
# from appearing in your terminal logs.
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

# Serve the frontend
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})