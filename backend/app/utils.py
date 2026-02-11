import string
import secrets

def generate_short_id(length: int = 6) -> str:
	""" Generates a safe, 6-character alphanumeric random string """
	chars = string.ascii_letters + string.digits
	return "".join(secrets.choice(chars) for _ in range(length))