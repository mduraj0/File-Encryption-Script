import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from threading import Thread


class EncryptDecrypt:
    """Common data and function for encryption and decryption of file
    """

    verbosity = 0

    def __init__(self, path, password):
        self.path = path
        self.password = password

    @staticmethod
    def create_key(password):
        salt = b"\\xda\\x01\\xsa\\asd-asd\\dsd\\x2131\xadbsa"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        return key


class Append(EncryptDecrypt):
    def __init__(self, path, password, text):
        self.text = text.encode('utf-8')
        super().__init__(path, password)

    def run(self):

        with open(self.path, 'r') as file:
            data = file.read()

        fernet = Fernet(self.create_key(self.password))
        encrypted_content = fernet.decrypt(data.encode('utf-8'))
        # encrypted_content += '\n'
        encrypted_content += self.text
        encrypted_content = fernet.encrypt(encrypted_content)

        with open(self.path, 'w') as file:
            file.write(encrypted_content.decode('utf-8'))


class Decryption(EncryptDecrypt):

    def run(self):
        with open(self.path, 'r') as file:
            data_to_encrypt = file.read()

        fernet = Fernet(self.create_key(self.password))
        encrypted_content = fernet.decrypt(data_to_encrypt.encode('utf-8'))

        with open(self.path.rename(self.path.with_suffix('.txt')), 'w') as file:
            file.write(encrypted_content.decode('utf-8'))


class Encryption(EncryptDecrypt):

    def run(self):
        with open(self.path, 'r') as file:
            data_to_encrypt = file.read()

        fernet = Fernet(self.create_key(self.password))
        encrypted_content = fernet.encrypt(data_to_encrypt.encode('utf-8'))

        with open(self.path.rename(self.path.with_suffix('.dokodu')), 'w') as file:
            file.write(encrypted_content.decode('utf-8'))
