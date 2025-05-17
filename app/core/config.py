import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()  # Load environment variables from .env file

class Settings:
    # App settings
    APP_NAME = "E-KYC Application"
    API_PREFIX = "/api"
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-for-development-only")
    
    # Admin credentials - should be moved to environment variables in production
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    ALLOW_HARDCODED_ADMIN = os.getenv("ALLOW_HARDCODED_ADMIN", "True").lower() in ("true", "1", "t")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ekyc.db")
    
    # Face recognition settings
    FACE_MATCH_THRESHOLD = 0.6  # Threshold for face match (lower is stricter)
    
    # File paths
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    UPLOAD_DIR = BASE_DIR / "app" / "static" / "uploads"
    AADHAAR_DIR = UPLOAD_DIR / "aadhaar"
    PAN_DIR = UPLOAD_DIR / "pan"
    SELFIE_DIR = UPLOAD_DIR / "selfies"

settings = Settings() 