class Config:
    """Base configuration for the starter app."""

    SECRET_KEY = "dev-secret-key-change-me"
    TEMPLATES_AUTO_RELOAD = True


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False
