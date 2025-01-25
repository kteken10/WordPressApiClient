import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

def get_auth():
    user = os.getenv("WORDPRESS_USER")
    password = os.getenv("WORDPRESS_API_PASSWORD")
  
    if not user or not password:
        raise ValueError("Les identifiants WordPress ne sont pas correctement configurés.")
    return HTTPBasicAuth(user, password)
