from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
import json
import hashlib


class CryptoManager:
    
    @staticmethod
    def derive_key(password, username):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=username.encode(),
            iterations=100000,
            backend=default_backend()
        )
        
        return urlsafe_b64encode(kdf.derive(password.encode()))
    
    @staticmethod    
    def encrypt_file(file, data, key):
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(json.dumps(data).encode())
        with open(file, "wb") as file:
            file.write(encrypted_data)
    
    @staticmethod    
    def decrypt_file(file, key):
        fernet = Fernet(key)
        with open(file, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
    
    @staticmethod
    def generate_hash(user, password):
        hash = hashlib.sha256("f{user}{password}".encode()).hexdigest()
        return hash