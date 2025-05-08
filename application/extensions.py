import os
import firebase_admin
import requests
from firebase_admin import credentials, firestore

# サービスアカウントキーのJSONを使う
cred = credentials.Certificate("application/managemanaba-firebase-adminsdk-fbsvc-57c713c4eb.json")
firebase_admin.initialize_app(cred)

firestore_db = firestore.client()