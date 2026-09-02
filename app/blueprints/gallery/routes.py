from flask import render_template
from app.blueprints.gallery import gallery_bp


@gallery_bp.route("/")
def index():
    return render_template("gallery/index.html")


@gallery_bp.route("/how-it-works")
def how_it_works():
    return render_template("gallery/how_it_works.html")


@gallery_bp.route("/maintainer")
def maintainer():
    return render_template("gallery/maintainer.html")


@gallery_bp.route("/components")
def components():
    return render_template("gallery/components.html")


@gallery_bp.route("/blocks")
def blocks():
    return render_template("gallery/blocks.html")
