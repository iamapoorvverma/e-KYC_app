from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum
from sqlalchemy.sql import func
import enum
from passlib.context import CryptContext

from app.database.database import Base

# Password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DocumentType(enum.Enum):
    AADHAAR = "aadhaar"
    PAN = "pan"

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="staff")  # Options: superadmin, admin, staff
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    @classmethod
    def create_user(cls, db, username, email, password, role="staff"):
        hashed_password = pwd_context.hash(password)
        user = cls(username=username, email=email, hashed_password=hashed_password, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

class KYCVerification(Base):
    __tablename__ = "kyc_verifications"
    
    id = Column(Integer, primary_key=True, index=True)
    document_type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    dob = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    address = Column(String, nullable=True)
    aadhaar_number = Column(String, nullable=True)
    pan_number = Column(String, nullable=True)
    face_match_score = Column(Float, nullable=True)
    is_verified = Column(Boolean, default=False)
    doc_front_path = Column(String, nullable=False)
    doc_back_path = Column(String, nullable=True)
    selfie_path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "document_type": self.document_type,
            "name": self.name,
            "dob": self.dob,
            "gender": self.gender,
            "address": self.address,
            "aadhaar_number": self.aadhaar_number,
            "pan_number": self.pan_number,
            "face_match_score": self.face_match_score,
            "is_verified": self.is_verified,
            "doc_front_path": self.doc_front_path,
            "doc_back_path": self.doc_back_path,
            "selfie_path": self.selfie_path,
            "created_at": self.created_at.isoformat() if self.created_at else None
        } 