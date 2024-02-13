from flask import Flask
from dotenv import load_dotenv
import os


def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        FLASK_DATABASE_USER=os.environ.get("FLASK_DATABASE_USER"),
        FLASK_DATABASE_PASSWORD=os.environ.get("FLASK_DATABASE_PASSWORD"),
        FLASK_DATABASE_HOST=os.environ.get("FLASK_DATABASE_HOST"),
        FLASK_DATABASE_PORT=os.environ.get("FLASK_DATABASE_PORT"),
        FLASK_DATABASE=os.environ.get("FLASK_DATABASE"),
        UPLOAD_FOLDER='static/img/'
    )

    from . import db

    db.init_app(app)

    from . import auth
    from . import home
    from . import admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(admin.bp)

    return app
