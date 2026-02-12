import hashlib
import base64

def generate_short_id(url: str, length: int = 6) -> str:
    """
    Generates a deterministic hash based on the URL.
    Uses MD5 to obtain a fingerprint and then encodes it to make it readable.
    """
    hash_object = hashlib.md5(url.encode())
    b64_string = base64.urlsafe_b64encode(hash_object.digest()).decode()
    
    return b64_string[:length]