import face_recognition
import numpy as np
from typing import Tuple
import os
from app.core.config import settings

def compare_faces(selfie_path: str, doc_path: str) -> Tuple[float, bool]:
    """
    Compare faces between a selfie and document image
    Returns:
        Tuple of (confidence score, is_match)
    """
    try:
        # Load the images
        selfie_image = face_recognition.load_image_file(selfie_path)
        doc_image = face_recognition.load_image_file(doc_path)
        
        # Get face encodings
        selfie_encodings = face_recognition.face_encodings(selfie_image)
        doc_encodings = face_recognition.face_encodings(doc_image)
        
        # Check if faces were detected in both images
        if not selfie_encodings or not doc_encodings:
            return 0.0, False
        
        # Use the first detected face in each image
        selfie_encoding = selfie_encodings[0]
        doc_encoding = doc_encodings[0]
        
        # Calculate face distance
        face_distance = face_recognition.face_distance([selfie_encoding], doc_encoding)[0]
        
        # Convert distance to confidence score (inverse relationship)
        # Lower distance means higher confidence
        confidence_score = float(1 - face_distance)  # Convert to Python float
        
        # Determine if it's a match based on threshold
        is_match = bool(face_distance < settings.FACE_MATCH_THRESHOLD)  # Convert numpy.bool to Python bool
        
        return confidence_score, is_match
        
    except Exception as e:
        print(f"Error comparing faces: {e}")
        return 0.0, False 