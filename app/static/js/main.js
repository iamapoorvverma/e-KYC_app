// Main JavaScript for E-KYC Application

// Show loading spinner
function showLoader(element) {
    // Create loader div
    const loader = document.createElement('div');
    loader.className = 'loader';
    
    // Clear element content and append loader
    if (element) {
        element.innerHTML = '';
        element.appendChild(loader);
    }
}

// Format date
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Format verification status
function formatVerificationStatus(isVerified) {
    if (isVerified) {
        return '<span class="badge bg-success">Verified</span>';
    } else {
        return '<span class="badge bg-danger">Failed</span>';
    }
}

// Format document type
function formatDocumentType(docType) {
    if (docType === 'aadhaar') {
        return 'Aadhaar Card';
    } else if (docType === 'pan') {
        return 'PAN Card';
    } else {
        return docType;
    }
}

// Format confidence score
function formatConfidenceScore(score) {
    if (score === null || score === undefined) return 'N/A';
    return `${Math.round(score * 100)}%`;
}

// Show error message
function showError(message, elementId = 'error-message') {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorElement.style.display = 'none';
        }, 5000);
    } else {
        console.error(message);
    }
}

// Handle HTTP errors
function handleHttpError(response) {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response;
}

// Validate file type
function validateImageFile(file) {
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
        return false;
    }
    return true;
}

// Preview image
function previewImage(file, previewElement) {
    if (!file || !previewElement) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        previewElement.innerHTML = `<img src="${e.target.result}" alt="Preview" style="max-width: 100%; max-height: 100%;">`;
    };
    reader.readAsDataURL(file);
}

// Ready event
document.addEventListener('DOMContentLoaded', function() {
    // Add global event listeners or initialize components
}); 