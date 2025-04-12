import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, firestore

# Get base64-encoded Firebase credentials from environment variable
b64_cred = os.getenv("FIREBASE_CREDENTIALS_B64")

if not b64_cred:
    raise ValueError("Environment variable 'FIREBASE_CREDENTIALS_B64' not found.")

# Decode the base64 string and convert to dictionary
cred_dict = json.loads(base64.b64decode(b64_cred).decode("utf-8"))

# Initialize Firebase with decoded credentials
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

# Create Firestore client
db = firestore.client()

def save_message(session_id: str, user: str, message: str):
    doc_ref = db.collection("sessions").document(session_id).collection("messages").document()
    doc_ref.set({
        "sender": user,
        "message": message,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
