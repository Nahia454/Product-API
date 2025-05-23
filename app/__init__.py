from flask import Flask
from app.extensions import db, migrate, jwt
from app.controllers.product_controller import product  # this is your Blueprint


# application factory function
def create_app():
    
    # app instance
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)  # initialize the jwt

    # import the models (optional if only needed for migration discovery)
    from app.models.product import Product  # Correct class name

    # registering blueprint
    app.register_blueprint(product)

    @app.route("/")
    def home():
        return "Python Exam"

    return app
