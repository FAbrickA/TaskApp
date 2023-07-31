import hashlib


def generate_password_hash(password):
    password_bytes = password.encode('utf-8')
    salt = hashlib.sha256()
    salt.update(password_bytes)
    password_hash = hashlib.pbkdf2_hmac('sha256', password_bytes, salt.digest(), 100000)
    return password_hash.hex()


def check_password_hash(password, password_hash):
    return generate_password_hash(password) == password_hash

