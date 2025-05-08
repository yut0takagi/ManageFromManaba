from flask import Flask
from dotenv import load_dotenv
from application.v0.api import api
from application.extensions import firestore_db
from datetime import timedelta
import os

# Load environment variables from .env file
load_dotenv()

db = firestore_db

version = os.getenv("VERSION")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "kfsja:lkjfewe:jierjijroijvv"
    app.config['DEBUG'] = True
    app.permanent_session_lifetime = timedelta(minutes=30)
    app.register_blueprint(api, url_prefix='/api/v0')
    return app