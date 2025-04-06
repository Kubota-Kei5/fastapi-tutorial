import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from os.path import dirname, join
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'env/.env.local')
load_dotenv(dotenv_path)

# Use a service account.
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
    "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40fastapi-tutorial-59129.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
  })

app = firebase_admin.initialize_app(cred)

db = firestore.client()