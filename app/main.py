from fastapi import FastAPI, Request, Depends, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
import os

from app.database.database import engine, Base, get_db
from app.models.models import KYCVerification, Admin
from app.api import kyc_api, admin_api
from app.core.config import settings

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title="E-KYC Application")

# Mount static files
app.mount("/static", StaticFiles(directory=str(settings.BASE_DIR / "app" / "static")), name="static")

# Set up templates
templates = Jinja2Templates(directory=str(settings.BASE_DIR / "app" / "templates"))

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="ekyc_session"
)

# Include API routers
app.include_router(kyc_api.router, prefix=f"{settings.API_PREFIX}", tags=["KYC"])
app.include_router(admin_api.router, prefix=f"{settings.API_PREFIX}/admin", tags=["Admin"])

# Routes
@app.get("/")
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/user")
async def user_document_selection(request: Request):
    """User document selection page"""
    return templates.TemplateResponse("user/select_document.html", {"request": request})

@app.get("/user/aadhaar")
async def user_aadhaar_upload(request: Request):
    """Aadhaar upload page"""
    return templates.TemplateResponse("user/aadhaar_upload.html", {"request": request})

@app.get("/user/pan")
async def user_pan_upload(request: Request):
    """PAN upload page"""
    return templates.TemplateResponse("user/pan_upload.html", {"request": request})

@app.get("/admin")
async def admin_login(request: Request):
    """Admin login page"""
    # If already logged in, redirect to dashboard
    if request.session.get("admin_logged_in"):
        return RedirectResponse("/admin/dashboard")
    
    return templates.TemplateResponse("admin/login.html", {"request": request})

@app.get("/admin/dashboard")
async def admin_dashboard(request: Request):
    """Admin dashboard page"""
    # Check if logged in
    if not request.session.get("admin_logged_in"):
        return RedirectResponse("/admin")
    
    # Pass role to template
    admin_role = request.session.get("admin_role", "")
    admin_username = request.session.get("admin_username", "")
    
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "admin_role": admin_role,
        "admin_username": admin_username
    })

@app.get("/admin/users")
async def admin_users(request: Request):
    """Admin user management page"""
    # Check if logged in
    if not request.session.get("admin_logged_in"):
        return RedirectResponse("/admin")
    
    # Check if has appropriate role
    admin_role = request.session.get("admin_role", "")
    if admin_role not in ["superadmin", "admin"]:
        return RedirectResponse("/admin/dashboard")
    
    return templates.TemplateResponse("admin/users.html", {
        "request": request,
        "admin_role": admin_role
    })

@app.get("/admin/register")
async def admin_register(request: Request):
    """Admin registration page"""
    # Check if logged in
    if not request.session.get("admin_logged_in"):
        return RedirectResponse("/admin")
    
    # Check if has appropriate role
    admin_role = request.session.get("admin_role", "")
    if admin_role not in ["superadmin", "admin"]:
        return RedirectResponse("/admin/dashboard")
    
    return templates.TemplateResponse("admin/register.html", {
        "request": request,
        "admin_role": admin_role
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 