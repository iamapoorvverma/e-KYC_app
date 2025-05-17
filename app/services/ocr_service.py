import easyocr
import io
import re
import os
from typing import Dict, List, Tuple, Optional
import numpy as np
import cv2
from pathlib import Path

# Initialize the OCR reader once
reader = easyocr.Reader(['en'])

def perform_ocr(image_path: str) -> List[str]:
    """
    Perform OCR on an image and return the extracted text
    """
    # Read the image
    image = cv2.imread(image_path)
    
    # Perform OCR
    result = reader.readtext(image)
    
    # Extract text from OCR results
    texts = [text[1] for text in result]
    
    return texts

def extract_aadhaar_front(texts: list) -> Dict:
    """
    Extract information from Aadhaar card front side
    """
    data = {}
    # Extract name (usually before DOB")
    name_pattern = re.compile(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+){1,2}\b')
    for i, text in enumerate(texts):
        if "DOB" in text:
            index = i
            for j in range(index - 1, -1, -1):  # reverse search
                match = name_pattern.search(texts[j])
                if match:
                    data["name"] = match.group()
                    break
            break
    # Extract DOB (DD/MM/YYYY format)
    dob_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')  
    for text in texts:
        match = dob_pattern.search(text)
        if match:
            data["dob"] = match.group()
            break
    
    # Extract gender
    gender_pattern = re.compile(r'(Male|Female|Other)', re.IGNORECASE)
    for text in texts:
        match = gender_pattern.search(text)
        if match:
            data["gender"] = match.group().capitalize()
            break
    
    # Extract Aadhaar number (12 digits)
    aadhaar_pattern = re.compile(r'\d{4}\s?\d{4}\s?\d{4}')
    for text in texts:
        match = aadhaar_pattern.search(text)
        if match:
            data["aadhaar_number"] = match.group().replace(" ", "")
            break
    
    return data

def extract_aadhaar_back(texts: list) -> Dict:
    """
    Extract address information from Aadhaar card back side
    """
    data = {}
    address_lines = []
    pin_code_pattern = re.compile(r"\b\d{6}\b")

    # Find the index of the line that contains 'address'
    start_index = -1
    for i, text in enumerate(texts):
        if "address" in text.lower() or text.lower().strip().startswith("ad"):
            start_index = i + 1  # Start collecting from the next line
            break

    # If address start is found
    if start_index != -1:
        for text in texts[start_index:]:
            clean_text = text.strip()
            address_lines.append(clean_text)
            if pin_code_pattern.search(clean_text):
                break  # Stop when a 6-digit PIN code is found

    data["address"] = " ".join(address_lines)
    return data

def extract_pan_front(texts: list) -> Dict:
    """
    Extract information from PAN card
    """
    data = {}
    # Extract PAN number (10 alphanumeric characters)
    pan_pattern = re.compile(r'[A-Z]{5}\d{4}[A-Z]{1}')
    for text in texts:
        match = pan_pattern.search(text)
        if match:
            data["pan_number"] = match.group()
            break
    
    # Extract name (usually after "Name")
    for i, text in enumerate(texts):
        if "Name" in text:
            if i+1 < len(texts):
                data["name"] = texts[i+1].strip()
            break
    
    # Extract DOB (DD/MM/YYYY format)
    dob_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
    for text in texts:
        match = dob_pattern.search(text)
        if match:
            data["dob"] = match.group()
            break
    
    return data

def validate_document_type(texts: list) -> Optional[str]:
    """
    Validate if the document is Aadhaar or PAN
    """
    # Check for Aadhaar card indicators
    for text in texts:
        if "aadhaar" in text.lower() or "आधार" in text or "unique identification" in text.lower():
            return "aadhaar"
        if re.search(r'\d{4}\s?\d{4}\s?\d{4}', text):  # Aadhaar number pattern
            return "aadhaar"
    
    # Check for PAN card indicators
    for text in texts:
        if "income tax" in text.lower() or "permanent account number" in text.lower():
            return "pan"
        if re.search(r'[A-Z]{5}\d{4}[A-Z]{1}', text):  # PAN number pattern
            return "pan"
    
    return None  # Unknown document type 