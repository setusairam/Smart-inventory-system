from flask import Flask
from config import DEBUG, SECRET_KEY
from routes.inventory_routes import inventory_bp
import os
import sqlite3
from config import DATABASE_PATH


def init_db():
    # ensure database directory exists
    db_dir = os.path.dirname(DATABASE_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    # create connection to initialize tables
    conn = sqlite3.connect(DATABASE_PATH)
    conn.close()


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = DEBUG
    app.config['SECRET_KEY'] = SECRET_KEY
    app.register_blueprint(inventory_bp)
    return app


if __name__ == '__main__':
    init_db()
    app = create_app()
    app.run()