from email_validator import ValidatedEmail
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from siteComunidadeImpressionadora.models import Usuario
from flask_login import current_user
from flask_wtf.file import FileAllowed, FileRequired, FileField

class FormCriarConta(FlaskForm):
    username = StringField('', render_kw={"placeholder": "Nome de usuário"}, validators=[DataRequired()])
    email = StringField('', render_kw={"placeholder": "E-mail"}, validators=[DataRequired(), Email()])
    senhaCriarConta = PasswordField('', render_kw={"placeholder": "Senha"}, validators=[DataRequired(), Length(6, 20)])
    senhaConfirma = PasswordField('', render_kw={"placeholder": "Confirmar Senha"}, validators=[DataRequired(), EqualTo('senhaCriarConta')])
    btnSubmitCriarConta = SubmitField('Criar Conta')

    # o metodo precisa ter o nome de validate para usar uma funcionalidade do flask
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail ja existe.")

class FormLogin(FlaskForm):
    email = StringField('', render_kw={"placeholder": "E-mail"}, validators=[DataRequired(), Email()])
    senhaLogin = PasswordField('', render_kw={"placeholder": "Senha"}, validators=[DataRequired(), Length(6, 20)])
    lembrarLogin = BooleanField('Lembrar dados de Acesso ')
    btnSubmitLogin = SubmitField('Login')

class Form_editar_perfil(FlaskForm):
    username = StringField('', render_kw={"placeholder": "Nome de usuário"}, validators=[DataRequired()])
    email = StringField('', render_kw={"placeholder": "E-mail"}, validators=[DataRequired(), Email()])
    fotoPerfil = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    cursoExcel = BooleanField('Excel')
    cursoVba = BooleanField('VBA')
    cursoPowerbi = BooleanField('PowerBI')
    cursoPython = BooleanField('Python')
    cursoCss = BooleanField('CSS')
    cursoSql = BooleanField('Sql')
    cursoHtml = BooleanField('Html')

    btnSubmitConfirmarEdicao = SubmitField('Atualizar')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError("E-mail ja existe.")


class Form_criar_post(FlaskForm):
    titulo = StringField('', render_kw={"placeholder": "Titulo"}, validators=[DataRequired()])
    corpo = TextAreaField('', render_kw={"placeholder": "Escreva seu post aqui..."}, validators=[DataRequired()])
