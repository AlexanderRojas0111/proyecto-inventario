import os
import jwt
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import hashlib
import logging

# Configuración inicial
load_dotenv()
logging.basicConfig(filename='security.log', level=logging.INFO)

class SecurityManager:
    def __init__(self):
        self.secret_key = os.getenv('SECRET_KEY', Fernet.generate_key().decode())
        self.fernet = Fernet(self.secret_key.encode())
        
    # Autenticación JWT
    def create_token(self, user_id, roles):
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'roles': roles
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logging.warning("Token expirado")
            return None
        except jwt.InvalidTokenError:
            logging.warning("Token inválido")
            return None

    # Encriptación de datos
    def encrypt_data(self, data):
        if isinstance(data, str):
            data = data.encode()
        return self.fernet.encrypt(data).decode()

    def decrypt_data(self, encrypted_data):
        return self.fernet.decrypt(encrypted_data.encode()).decode()

    # Hash seguro para contraseñas
    def hash_password(self, password):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return salt + key

    def verify_password(self, password, stored_hash):
        salt = stored_hash[:32]
        stored_key = stored_hash[32:]
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return new_key == stored_key

# Middleware de seguridad
def security_headers_middleware(app):
    @app.middleware
    async def add_security_headers(request, response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response
