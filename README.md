# E-KYC Application

Hey there! 👋 Welcome to my E-KYC (Electronic Know Your Customer) application. I built this to simplify identity verification processes that are typically tedious and time-consuming. This app lets users verify their identity online by uploading their documents and taking a selfie - no more waiting in long queues or dealing with paperwork!

## What's this all about?

This application provides a complete digital solution for identity verification using government-issued ID cards (Aadhaar and PAN). It uses optical character recognition (OCR) to extract information from documents and facial recognition to verify that the person submitting the documents is actually who they claim to be.

## ✨ Key Features

- **Multi-Document Support**: Verify using either Aadhaar card (front and back) or PAN card
- **Smart OCR Processing**: Automatically extracts key information like name, date of birth, ID numbers, and address
- **Face Verification**: Uses facial recognition to match selfie with the photo on ID documents
- **Admin Dashboard**: Complete management interface with verification statistics and user search
- **Role-Based Access**: Different admin roles (superadmin, admin, staff) with appropriate permissions
- **Responsive Design**: Works smoothly on mobile, tablet, and desktop devices
- **Secure Storage**: All data is stored securely with proper encryption
- **Real-time Feedback**: Instant verification results with confidence scores

## 🛠️ Tech Stack

I've used modern technologies to build this application:

- **FastAPI**: High-performance Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **EasyOCR**: For extracting text from document images
- **face_recognition**: For facial recognition and matching
- **Bootstrap 5**: For responsive and clean UI design
- **Jinja2**: For HTML templating
- **SQLite**: For database storage (easily upgradable to PostgreSQL/MySQL)

## 🚀 Getting Started

### Prerequisites

Before you begin, make sure you have:

- Python 3.7 or newer
- pip (Python package installer)
- Git (optional, for cloning the repository)
- Basic understanding of terminal/command prompt

### Installation

1. **Clone the repository** (or download and extract the ZIP):
   ```bash
   git clone https://github.com/yourusername/ekyc-app.git
   cd ekyc-app
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   > 💡 **Pro tip**: The face_recognition library can be tricky to install. On Linux, you might need these packages first:
   > ```bash
   > sudo apt-get update
   > sudo apt-get install -y build-essential cmake
   > sudo apt-get install -y libopenblas-dev liblapack-dev
   > sudo apt-get install -y libx11-dev libgtk-3-dev
   > sudo apt-get install -y python3-dev
   > ```
   > On Windows, you might need Visual C++ Build Tools.

4. **Create upload directories**:
   ```bash
   mkdir -p app/static/uploads/aadhaar
   mkdir -p app/static/uploads/pan
   mkdir -p app/static/uploads/selfies
   ```

5. **Set up environment variables**:
   Create a `.env` file in the root directory with:
   ```
   SECRET_KEY=your-secret-key-here
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=secure-password
   DATABASE_URL=sqlite:///./ekyc.db
   FACE_MATCH_THRESHOLD=0.6
   ```

### Running the Application

1. **Start the server**:
   ```bash
   python run.py
   ```

2. **Access the application**:
   Open your browser and go to `http://localhost:8000`

3. **Default Admin Credentials**:
   Since the database is not included in the repository, you'll need to use these default credentials for admin access:
   - Username: `admin`
   - Password: `admin123`
   
   > ⚠️ **Important**: Please change these credentials immediately after first login for security purposes!

## 📱 How to Use

### For Users

1. **Start verification**:
   - Go to the homepage and click "Get Verified"
   - Choose your document type (Aadhaar or PAN)

2. **Upload documents**:
   - For Aadhaar: Upload both front and back sides
   - For PAN: Upload the front side only
   - Make sure images are clear and all text is visible!

3. **Take a selfie**:
   - Allow camera access when prompted
   - Ensure good lighting and face the camera directly
   - Click the capture button when ready

4. **View results**:
   - Get instant verification results
   - See extracted information and face match confidence score

### For Admins

1. **Access admin panel**:
   - Click "Login" under the Admin section on the homepage
   - Enter your admin credentials

2. **Dashboard features**:
   - View verification statistics and recent activities
   - Search users by name, Aadhaar number, or PAN number
   - View detailed verification records
   - Manage admin users (superadmin only)

## 📂 Project Structure

Here's how I've organized the code:

```
ekyc_app/
├── app/                           # Main application package
│   ├── api/                       # API endpoints
│   │   ├── admin_api.py           # Admin-related APIs
│   │   └── kyc_api.py             # KYC verification APIs
│   ├── core/                      # Core configuration
│   │   └── config.py              # Application settings
│   ├── database/                  # Database setup
│   │   └── database.py            # Database connection and session
│   ├── models/                    # Database models
│   │   └── models.py              # SQLAlchemy ORM models
│   ├── services/                  # Business logic services
│   │   ├── face_service.py        # Face recognition functionality
│   │   ├── file_service.py        # File handling utilities
│   │   └── ocr_service.py         # OCR processing logic
│   ├── static/                    # Static assets
│   │   ├── css/                   # CSS files
│   │   ├── js/                    # JavaScript files
│   │   ├── images/                # Image assets
│   │   └── uploads/               # User uploaded files
│   │       ├── aadhaar/           # Aadhaar card images
│   │       ├── pan/               # PAN card images
│   │       └── selfies/           # User selfie images
│   ├── templates/                 # HTML templates
│   │   ├── admin/                 # Admin panel templates
│   │   └── user/                  # User flow templates
│   └── main.py                    # FastAPI application instance
├── requirements.txt               # Project dependencies
├── run.py                         # Application entry point
├── .env                           # Environment variables (create this)
└── README.md                      # Project documentation
```

## 🔮 Future Plans

I'm constantly working to improve this application. Here's what's coming next:

- Support for more document types (Voter ID, Driver's License, Passport)
- Enhanced security features with encryption for sensitive data
- Mobile app integration with API endpoints
- Multi-language support for wider accessibility
- Batch processing for enterprise use cases
- Cloud storage integration options

## 🐛 Troubleshooting

**Common issues:**

- **Face recognition not working**: Make sure you have good lighting and your face is clearly visible
- **OCR extraction issues**: Ensure document images are clear, not blurry, and all text is visible
- **Installation problems**: Check that all system dependencies are installed, especially for face_recognition

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Built with ❤️ by Apoorv

If you have any questions or feedback, feel free to reach out! 