import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    # Email Configuration
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USER = os.environ.get('EMAIL_USER', 'backendev.py@gmail.com')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
    
    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/portafolio')
    
    # Admin API Key
    ADMIN_API_KEY = os.environ.get('ADMIN_API_KEY', 'admin-secret-key-2024')
    
    # BitoService Configuration
    BITO_URL = os.environ.get('BITO_URL', 'https://api.bito.ai')
    BITO_API_KEY = os.environ.get('BITO_API_KEY', '')
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-2024')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true' 