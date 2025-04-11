import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("credentials.json")  # your Firebase key
firebase_admin.initialize_app(cred)
db = firestore.client()

def save_message(session_id: str, user: str, message: str):
    doc_ref = db.collection("sessions").document(session_id).collection("messages").document()
    doc_ref.set({
        "sender": user,
        "message": message,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
