from flask import Flask
from kdui import KDUI

from app.config import DevConfig


def create_app(config_object=DevConfig):
    """Create the KD UI showroom application."""
    app = Flask(__name__)
    app.config.from_object(config_object)
    KDUI(app)

    from app.blueprints.public import public_bp
    from app.blueprints.gallery import gallery_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(gallery_bp)
    return app
