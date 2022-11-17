import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


class Encryption:
    def __init__(self, path):
        self.path = path

    def create_key(self, password):
        salt = b"\\xda\\x01\\xsa\\asd-asd\\dsd\\x2131\xadbsa"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        return key

    def execute(self, password):
        with open(self.path, 'r') as file:
            data_to_encrypt = file.read()

        fernet = Fernet(self.create_key(password))
        encrypted_content = fernet.encrypt(data_to_encrypt.encode('utf-8'))

        with open(self.path.rename(self.path.with_suffix('.dokodu')), 'w') as file:
            file.write(encrypted_content.decode('utf-8'))
