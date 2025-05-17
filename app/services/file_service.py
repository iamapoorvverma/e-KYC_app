import os
import shutil
from fastapi import UploadFile
from pathlib import Path
import uuid
from app.core.config import settings

async def save_upload_file(upload_file: UploadFile, destination_dir: Path, filename_prefix: str = "") -> str:
    """
    Save an uploaded file to the destination directory and return the file path
    """
    # Create destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)
    
    # Generate a unique filename
    file_extension = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{filename_prefix}_{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(destination_dir, unique_filename)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    # Reset file pointer
    upload_file.file.seek(0)
    
    return file_path

async def save_aadhaar_front(upload_file: UploadFile) -> str:
    """Save Aadhaar front image and return file path"""
    return await save_upload_file(upload_file, settings.AADHAAR_DIR, "aadhaar_front")

async def save_aadhaar_back(upload_file: UploadFile) -> str:
    """Save Aadhaar back image and return file path"""
    return await save_upload_file(upload_file, settings.AADHAAR_DIR, "aadhaar_back")

async def save_pan_front(upload_file: UploadFile) -> str:
    """Save PAN card image and return file path"""
    return await save_upload_file(upload_file, settings.PAN_DIR, "pan_front")

async def save_selfie(upload_file: UploadFile) -> str:
    """Save selfie image and return file path"""
    return await save_upload_file(upload_file, settings.SELFIE_DIR, "selfie") 