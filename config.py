import os
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-chave-trocar-em-producao")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///estoque.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
