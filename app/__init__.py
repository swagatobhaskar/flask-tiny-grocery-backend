from flask import Flask
from flask_migrate import Migrate
from os import getenv


from config import DevConfig, ProdConfig
from .routes import product_bp
from .extensions import db

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    config_obj = DevConfig if getenv('ENV') == 'development' else ProdConfig
    app.config.from_object(config_obj)
    print(config_obj)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(product_bp, url_prefix='/')

    return app
