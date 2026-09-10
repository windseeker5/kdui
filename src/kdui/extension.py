"""Flask extension that exposes KD UI templates and compiled assets."""

from flask import Blueprint


class KDUI:
    """Register namespaced Jinja macros and static assets with Flask."""

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if "kdui" not in app.blueprints:
            blueprint = Blueprint(
                "kdui",
                __name__,
                template_folder="templates",
                static_folder="static",
                static_url_path="/kdui-assets",
            )
            app.register_blueprint(blueprint)
        app.extensions["kdui"] = self
