"""
Script to create an admin user.
Run this script to create the initial admin user.
"""
import sys
import os

# Add the root directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.database import SessionLocal, engine, Base
from app.models.models import Admin

def create_admin(username, email, password, role="staff"):
    """Create an admin user"""
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing_admin = db.query(Admin).filter(Admin.username == username).first()
        if existing_admin:
            print(f"Admin with username '{username}' already exists.")
            return
        
        # Create new admin
        admin = Admin.create_user(db, username, email, password, role)
        print(f"Admin user '{username}' created successfully with ID {admin.id} and role '{admin.role}'")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python create_admin.py <username> <email> <password> [role]")
        print("Role can be: superadmin, admin, staff (default: staff)")
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    role = sys.argv[4] if len(sys.argv) > 4 else "staff"
    
    create_admin(username, email, password, role) 