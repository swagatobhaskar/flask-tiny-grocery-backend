from flask import Flask
from flask_migrate import Migrate
from os import getenv

from config import DevConfig, ProdConfig
from .routes.products import product_bp
from .routes.categories import category_bp
from .routes.inventory import inventory_bp
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
    app.register_blueprint(category_bp, url_prefix='/category')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    return app
