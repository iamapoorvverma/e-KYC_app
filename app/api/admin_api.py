from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional
import os

from app.database.database import get_db
from app.models.models import KYCVerification, Admin
from app.core.config import settings

router = APIRouter()

@router.post("/login")
async def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Admin login endpoint
    """
    # Check if using hardcoded credentials is allowed (for backward compatibility)
    if settings.ALLOW_HARDCODED_ADMIN and username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
        request.session["admin_logged_in"] = True
        request.session["admin_username"] = username
        request.session["admin_role"] = "superadmin"  # Default role for hardcoded admin
        return {"success": True}
    
    # Check database for user
    admin = db.query(Admin).filter(Admin.username == username, Admin.is_active == True).first()
    if not admin or not Admin.verify_password(password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Set session data
    request.session["admin_logged_in"] = True
    request.session["admin_username"] = admin.username
    request.session["admin_id"] = admin.id
    request.session["admin_role"] = admin.role
    
    return {"success": True}

@router.post("/logout")
async def admin_logout(request: Request):
    """
    Admin logout endpoint
    """
    request.session.pop("admin_logged_in", None)
    request.session.pop("admin_username", None)
    request.session.pop("admin_id", None)
    request.session.pop("admin_role", None)
    return {"success": True}

@router.get("/auth-status")
async def auth_status(request: Request):
    """
    Check if admin is logged in
    """
    is_logged_in = request.session.get("admin_logged_in", False)
    role = request.session.get("admin_role", "") if is_logged_in else ""
    username = request.session.get("admin_username", "") if is_logged_in else ""
    return {"logged_in": is_logged_in, "role": role, "username": username}

@router.get("/dashboard")
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    """
    Get statistics for admin dashboard
    """
    if not request.session.get("admin_logged_in"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Get total verifications
    total_verifications = db.query(KYCVerification).count()
    
    # Get verified verifications
    verified_count = db.query(KYCVerification).filter(KYCVerification.is_verified == True).count()
    
    # Get failed verifications
    failed_count = db.query(KYCVerification).filter(KYCVerification.is_verified == False).count()
    
    # Get document type counts
    aadhaar_count = db.query(KYCVerification).filter(KYCVerification.document_type == "aadhaar").count()
    pan_count = db.query(KYCVerification).filter(KYCVerification.document_type == "pan").count()
    
    return {
        "total_verifications": total_verifications,
        "verified_count": verified_count,
        "failed_count": failed_count,
        "aadhaar_count": aadhaar_count,
        "pan_count": pan_count
    }

@router.get("/users")
async def get_users(request: Request, db: Session = Depends(get_db)):
    """
    Get all admin users (for admin/superadmin)
    """
    # Check if logged in and has appropriate role
    if not request.session.get("admin_logged_in"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    role = request.session.get("admin_role", "")
    if role not in ["superadmin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view users"
        )
    
    # Get all users
    users = db.query(Admin).all()
    
    # Convert to dict and exclude sensitive information
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        for user in users
    ]

@router.get("/users/{user_id}")
async def get_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Get a specific admin user (for admin/superadmin)
    """
    # Check if logged in and has appropriate role
    if not request.session.get("admin_logged_in"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    role = request.session.get("admin_role", "")
    if role not in ["superadmin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view users"
        )
    
    # Get user
    user = db.query(Admin).filter(Admin.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Check if admin is trying to view superadmin
    if role == "admin" and user.role == "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view superadmin users"
        )
    
    # Return user details without sensitive information
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }

@router.post("/register")
async def register_admin(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Register a new admin user (for admin/superadmin)
    """
    # Check if logged in and has appropriate role
    if not request.session.get("admin_logged_in"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    current_role = request.session.get("admin_role", "")
    if current_role not in ["superadmin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to register users"
        )
    
    # Check if admin is trying to create superadmin
    if current_role == "admin" and role == "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create superadmin users"
        )
    
    # Validate role
    if role not in ["superadmin", "admin", "staff"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )
    
    # Check if username or email already exists
    existing_user = db.query(Admin).filter(
        (Admin.username == username) | (Admin.email == email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    
    # Create new admin user
    try:
        new_admin = Admin.create_user(db, username, email, password, role)
        return {"success": True, "id": new_admin.id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    request: Request,
    email: str = Form(...),
    role: str = Form(...),
    is_active: bool = Form(...),
    password: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Update an admin user (for admin/superadmin)
    """
    # Check if logged in and has appropriate role
    if not request.session.get("admin_logged_in"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    current_role = request.session.get("admin_role", "")
    if current_role not in ["superadmin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update users"
        )
    
    # Get user to update
    user = db.query(Admin).filter(Admin.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Check if admin is trying to update superadmin
    if current_role == "admin" and user.role == "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update superadmin users"
        )
    
    # Check if admin is trying to set role to superadmin
    if current_role == "admin" and role == "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to set superadmin role"
        )
    
    # Validate role
    if role not in ["superadmin", "admin", "staff"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )
    
    # Update user
    try:
        user.email = email
        user.role = role
        user.is_active = is_active
        
        # Update password if provided
        if password:
            user.hashed_password = pwd_context.hash(password)
        
        db.commit()
        return {"success": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        ) 