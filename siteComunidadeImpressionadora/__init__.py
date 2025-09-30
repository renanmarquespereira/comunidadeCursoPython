from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)

#Token de seguranca
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

# importar arquivos de links
from siteComunidadeImpressionadora import routes
