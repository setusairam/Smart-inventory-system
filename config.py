import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'inventory.db')

# Flask configuration
DEBUG = True
SECRET_KEY = 'your_secret_key_here'