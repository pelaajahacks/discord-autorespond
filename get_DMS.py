from os import name, system
import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from colorama import *

def generate_key(password):
    password = password.encode()  # Convert to type bytes
    # CHANGE THIS - recommend using a key from os.urandom(16), must be of type
    # bytes
    salt = b'FuckOffSkids_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    # Can only use kdf oncemessage = "my deep dark secret".encode()
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def decrypt(encrypted, password):
    key = generate_key(password)
    f = Fernet(key)
    # Decrypt the bytes. The returning object is of type bytes
    return f.decrypt(encrypted.encode())

with open("code.py", "r") as file:
	exec(decrypt(file.read(), "pornhub"))