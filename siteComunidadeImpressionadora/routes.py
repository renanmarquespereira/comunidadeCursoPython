import bcrypt
from flask import render_template, redirect, request, url_for, flash, Flask, abort
from siteComunidadeImpressionadora import app, database, cripitografarSenha
from siteComunidadeImpressionadora.forms import FormLogin, FormCriarConta, Form_editar_perfil, Form_criar_post
from siteComunidadeImpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template("home.html", posts=posts)

@app.route('/contato')
def contato():
    return render_template("contato.html")

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template("usuarios.html", lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    formLogin = FormLogin()
    formCriar = FormCriarConta()

    if formLogin.validate_on_submit() and "btnSubmitLogin" in request.form:
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first()

        if usuario and bcrypt.checkpw(formLogin.senhaLogin.data.encode("utf-8"), usuario.senha):
            #login_user grava em cache o usuario
            login_user(usuario, remember=formLogin.lembrarLogin.data)
            flash(f"Bem-Vindo {usuario.username} você esta logado agora.", "alert-success")

            param_next_url = request.args.get("next")

            if param_next_url:
                return redirect(param_next_url)
            else:
                return redirect(url_for("home"))
        else:
            flash(f"Falha no login, email ou senha incorretos.", "alert-danger")

    if formCriar.validate_on_submit() and "btnSubmitCriarConta" in request.form:
        senhaCripto = cripitografarSenha.generate_password_hash(formCriar.senhaCriarConta.data)
        novoUsuario = Usuario(username=formCriar.username.data, email=formCriar.email.data, senha=senhaCripto)
        database.session.add(novoUsuario)
        database.session.commit()

        flash(f"Usuario {formCriar.username.data} cadastrado com sucesso!", "alert-success")
        return redirect(url_for("home"))

    return render_template("login.html", formLogin=formLogin, formCriar=formCriar)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f"Desconectado!", "alert-success")
    return redirect(url_for("home"))

@app.route('/perfil')
@login_required
def perfil():
    imagem_perfil = url_for('static', filename=f'images/{current_user.foto_perfil}')
    return render_template("perfil.html", imagem_perfil=imagem_perfil)


def salvar_imagem(imagem):
    # Vai servir pra colocar um ID unico na imagem
    codigo = secrets.token_hex(8)

    # Aqui criando o nome da imagem
    nome, extensao = os.path.splitext(imagem.filename)
    nome_completo_arquivo = os.path.join(nome + codigo + extensao)

    # Reduzindo tamanho da imagem
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    # Criando onde imagem sera salva
    caminho_salva_imagem = os.path.join(app.root_path, "static/images", nome_completo_arquivo)

    # salvando a imagem reduzida
    imagem_reduzida.save(caminho_salva_imagem)
    return nome_completo_arquivo

def atualizar_cursos(form):
    cursos = []
    for campo in form:
        if campo.type == "BooleanField" and campo.data:
            cursos.append(campo.label.text)

    return ";".join(cursos)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = Form_editar_perfil()

    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.cursos = atualizar_cursos(form)

        if form.fotoPerfil.data:
            arquivo = salvar_imagem(form.fotoPerfil.data)
            current_user.foto_perfil = arquivo

        database.session.commit()
        flash(f"Dados Atualizados!", "alert-success")
        return redirect(url_for("perfil"))

    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username

    imagem_perfil = url_for('static', filename=f'images/{current_user.foto_perfil}')
    return render_template("editar_perfil.html", imagem_perfil=imagem_perfil, form=form)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criar_post = Form_criar_post()

    if form_criar_post.validate_on_submit():
        post = Post(titulo=form_criar_post.titulo.data, corpo=form_criar_post.corpo.data, autor=current_user )
        database.session.add(post)
        database.session.commit()
        flash("Post criado com sucesso!", "alert-success")
        return redirect(url_for("home"))

    return render_template("novo_post.html", form_criar_post=form_criar_post)




@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = Form_criar_post()
        # Se o ususario estiver carregando a pagina
        if request.method == "GET":
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash(f"Post Atualizar com sucesso!", "alert-success")
            return redirect(url_for("home"))
    else:
        form = None

    return render_template("post.html", post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash("Post deletado com sucesso!", "alert-danger")
        return redirect(url_for("home"))
    else:
        abort(403)