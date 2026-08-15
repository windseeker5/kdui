from flask import Blueprint

gallery_bp = Blueprint("gallery", __name__, url_prefix="/ui")

from app.blueprints.gallery import routes  # noqa: E402, F401
