import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


password = b'samplepassword1'
salt = b'PythonIsCool'
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000
)

fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(password)))

text = input('Podaj wiadomosc:')
safe_text = fernet.encrypt(text.encode('utf8'))
print(safe_text)
print('*' * 100)

print(fernet.decrypt(safe_text).decode('utf'))