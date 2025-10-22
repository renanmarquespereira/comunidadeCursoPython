from siteComunidadeImpressionadora import database, loginManager
from datetime import datetime
from flask_login import UserMixin

# Diz para o flask que essa e a funcao que procura o usuario
@loginManager.user_loader
def load_usuario(id_usuario):
    # Procura por id
    return Usuario.query.get(int(id_usuario))

# UserMixin diz qual a classe que faz login
class Usuario(database.Model, UserMixin):
    id = database.Column('id', database.Integer, primary_key=True)
    username = database.Column('username', database.String, unique=True, nullable=False)
    senha = database.Column('senha', database.String, nullable=False)
    email = database.Column('email', database.String, unique=True, nullable=False)
    foto_perfil = database.Column('foto_perfil', database.String, default='default.jpg', nullable=False)
    posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column('cursos', database.String, nullable=False, default='Não informado')

    def contar_posts(self):
        return len(self.posts)

class Post(database.Model):
    id = database.Column('id', database.Integer, primary_key=True)
    titulo = database.Column('titulo', database.String, nullable=False)
    corpo = database.Column('corpo', database.Text, nullable=False)
    dataCriacao = database.Column('dataCriacao', database.DateTime, nullable=False, default=datetime.now)
    id_usuario = database.Column('id_usuario', database.Integer, database.ForeignKey('usuario.id'), nullable=False)