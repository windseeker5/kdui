from flask import render_template
from app.blueprints.public import public_bp


@public_bp.route("/")
def index():
    return render_template("blocks/landing_page.html")


@public_bp.route("/login")
def login():
    return render_template("blocks/login_page.html")
