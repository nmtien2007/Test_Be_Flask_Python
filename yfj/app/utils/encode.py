import hashlib


def encrypt_string(text):
    if not text:
        return ''

    data = str(text).encode()
    return hashlib.sha1(data).hexdigest()
