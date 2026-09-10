from flask import render_template

from app.blueprints.public import public_bp


@public_bp.route("/")
def index():
    return render_template("landing.html")
