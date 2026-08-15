from flask import Flask

from app.config import DevConfig


def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    from app.blueprints.public import public_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.gallery import gallery_bp
    # SCAFFOLD:IMPORTS
    from app.blueprints.project import project_bp







    app.register_blueprint(public_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(gallery_bp)
    # SCAFFOLD:REGISTER
    app.register_blueprint(project_bp)







    from app.cli import scaffold_cli
    app.cli.add_command(scaffold_cli)

    return app

