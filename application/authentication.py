import os
import requests
from dotenv import load_dotenv

load_dotenv()
FIREBASE_KEY = os.getenv("FIREBASE_API_KEY")

# Sign up by calling google api to firebase
# Input: User's email and password
# Output: Create access to the app
def sign_up(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_KEY}"

    payload = {"email": email, "password": password, "returnSecureToken": True}

    response = requests.post(url, json=payload)
    data = response.json()

    if response.status_code == 200:
        print(f"Sign up successful")
        return data
    
    else:
        error_msg = data.get("error", {}).get("message", "Unknown error")
        print(f"Sign up failed: {error_msg}")
        return data

# Sign in by calling google api to firebase
# Input: User's email and password
# Output: Access to the app
def sign_in(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_KEY}"

    payload = {"email": email, "password": password, "returnSecureToken": True}

    response = requests.post(url, json=payload)
    data = response.json()

    if response.status_code == 200:
        print(f"Sign in successful")
        return data
    
    else:
        error_msg = data.get("error", {}).get("message", "Unknown error")
        print(f"Sign in failed: {error_msg}")
        return data