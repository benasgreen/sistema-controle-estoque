import os
from flask import Flask
from flask_login import LoginManager
from .extensions import db

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para acessar esta página."

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-chave-trocar-em-producao"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///estoque.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config:
        app.config.update(test_config)
    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)
    login_manager.init_app(app)

    from . import models
    from .routes import main_bp, auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()
        # Conta demonstrativa criada apenas quando o banco ainda não possui usuários.
        # Troque a senha e configure SECRET_KEY antes de qualquer uso real.
        from .models import User
        if User.query.count() == 0:
            demo_user = User(username="admin")
            demo_user.set_password("admin123")
            db.session.add(demo_user)
            db.session.commit()

    return app
