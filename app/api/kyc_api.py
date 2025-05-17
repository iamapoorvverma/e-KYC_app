from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import Dict, Optional
import os

from app.database.database import get_db
from app.models.models import KYCVerification, DocumentType
from app.services.ocr_service import perform_ocr, extract_aadhaar_front, extract_aadhaar_back, extract_pan_front, validate_document_type
from app.services.face_service import compare_faces
from app.services.file_service import save_aadhaar_front, save_aadhaar_back, save_pan_front, save_selfie

router = APIRouter()

@router.post("/upload-aadhaar-front")
async def upload_aadhaar_front(file: UploadFile = File(...)):
    """Upload and process Aadhaar card front side"""
    try:
        # Save the uploaded file
        file_path = await save_aadhaar_front(file)
        
        # Perform OCR
        texts = perform_ocr(file_path)
        
        # Validate document type
        doc_type = validate_document_type(texts)
        if doc_type != "aadhaar":
            return {
                "success": False,
                "message": "The uploaded document does not appear to be an Aadhaar card front side",
                "file_path": file_path
            }
        
        # Extract information
        extracted_data = extract_aadhaar_front(texts)
        
        return {
            "success": True,
            "file_path": file_path,
            "extracted_data": extracted_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing Aadhaar front: {str(e)}"
        )

@router.post("/upload-aadhaar-back")
async def upload_aadhaar_back(file: UploadFile = File(...)):
    """Upload and process Aadhaar card back side"""
    try:
        # Save the uploaded file
        file_path = await save_aadhaar_back(file)
        
        # Perform OCR
        texts = perform_ocr(file_path)
        
        # Extract information (address)
        extracted_data = extract_aadhaar_back(texts)
        
        return {
            "success": True,
            "file_path": file_path,
            "extracted_data": extracted_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing Aadhaar back: {str(e)}"
        )

@router.post("/upload-pan")
async def upload_pan(file: UploadFile = File(...)):
    """Upload and process PAN card"""
    try:
        # Save the uploaded file
        file_path = await save_pan_front(file)
        
        # Perform OCR
        texts = perform_ocr(file_path)
        
        # Validate document type
        doc_type = validate_document_type(texts)
        if doc_type != "pan":
            return {
                "success": False,
                "message": "The uploaded document does not appear to be a PAN card",
                "file_path": file_path
            }
        
        # Extract information
        extracted_data = extract_pan_front(texts)
        
        return {
            "success": True,
            "file_path": file_path,
            "extracted_data": extracted_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing PAN card: {str(e)}"
        )

@router.post("/upload-selfie")
async def upload_selfie(
    file: UploadFile = File(...),
    doc_path: str = Form(...),
    doc_type: str = Form(...),
    doc_front_path: str = Form(...),
    doc_back_path: Optional[str] = Form(None),
    name: str = Form(...),
    dob: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    aadhaar_number: Optional[str] = Form(None),
    pan_number: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Upload selfie and complete KYC verification"""
    try:
        # Save the selfie file
        selfie_path = await save_selfie(file)
        
        # Compare faces
        confidence_score, is_match = compare_faces(selfie_path, doc_front_path)
        
        # Ensure values are Python native types, not NumPy types
        confidence_score = float(confidence_score)
        is_match = bool(is_match)
        
        # Create KYC verification record
        kyc_verification = KYCVerification(
            document_type=doc_type,
            name=name,
            dob=dob,
            gender=gender,
            address=address,
            aadhaar_number=aadhaar_number,
            pan_number=pan_number,
            face_match_score=confidence_score,
            is_verified=is_match,
            doc_front_path=doc_front_path,
            doc_back_path=doc_back_path,
            selfie_path=selfie_path
        )
        
        # Save to database
        db.add(kyc_verification)
        db.commit()
        db.refresh(kyc_verification)
        
        return {
            "success": True,
            "kyc_id": kyc_verification.id,
            "is_verified": bool(is_match),  # Convert to Python bool again to be safe
            "confidence_score": float(confidence_score),  # Convert to Python float again to be safe
        }
    except Exception as e:
        print(f"Error in upload_selfie: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing selfie and completing KYC: {str(e)}"
        )

@router.get("/verifications")
async def get_verifications(db: Session = Depends(get_db)):
    """Get all KYC verifications (for admin)"""
    verifications = db.query(KYCVerification).all()
    return [verification.to_dict() for verification in verifications]

@router.get("/verifications/{kyc_id}")
async def get_verification(kyc_id: int, db: Session = Depends(get_db)):
    """Get a specific KYC verification (for admin)"""
    verification = db.query(KYCVerification).filter(KYCVerification.id == kyc_id).first()
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"KYC verification with ID {kyc_id} not found"
        )
    return verification.to_dict()

@router.get("/search")
async def search_verifications(
    name: Optional[str] = None,
    aadhaar: Optional[str] = None,
    pan: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Search KYC verifications by name, Aadhaar number, or PAN number"""
    query = db.query(KYCVerification)
    
    if name:
        query = query.filter(KYCVerification.name.ilike(f"%{name}%"))
    if aadhaar:
        query = query.filter(KYCVerification.aadhaar_number == aadhaar)
    if pan:
        query = query.filter(KYCVerification.pan_number == pan)
    
    verifications = query.all()
    return [verification.to_dict() for verification in verifications] 