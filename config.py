import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Change this to something random and secret before deploying
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this')

    # Where uploaded student photos are stored
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max upload size
