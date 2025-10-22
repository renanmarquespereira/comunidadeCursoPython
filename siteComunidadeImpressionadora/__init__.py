from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy

app = Flask(__name__)

# Token de segurança
app.config["SECRET_KEY"] = "7fff09fe31cb95069ca7515bd5022585"

# Banco de dados
if os.getenv("DATABASE_URL"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

database = SQLAlchemy(app)
cripitografarSenha = Bcrypt(app)

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"
loginManager.login_message = "Faça o login para acessar a pagina !"
loginManager.login_message_category = "alert-info"

# ⚠️ Importar models só depois de configurar o banco
from siteComunidadeImpressionadora import models

engine = sqlalchemy.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
inspector = sqlalchemy.inspect(engine)

if not inspector.has_table("usuario"):
    with app.app_context():
        database.create_all()
        print("BASE DE DADOS CRIADA")
else:
    print("BASE DE DADOS JA EXISTENTE")

# Importar rotas por último
from siteComunidadeImpressionadora import routes