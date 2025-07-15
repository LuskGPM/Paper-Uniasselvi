from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user 
from ..models import User, database

auth_bp = Blueprint(
    'auth',
    __name__,
    template_folder='../templates'
)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        # O campo de entrada pode ser CPF ou e-mail
        user_identifier = request.form.get('login') # Novo nome para o campo
        senha = request.form.get('senha')

        user = None
        # Tenta encontrar o usuário pelo CPF (se for numérico e tiver 11 dígitos)
        if user_identifier and user_identifier.isdigit() and len(user_identifier) == 11:
            user = database.session.get(User, user_identifier)
        
        # Se não encontrou por CPF, tenta encontrar por e-mail
        if not user and user_identifier and '@' in user_identifier:
            user = User.query.filter_by(email=user_identifier).first()

        # Verifica se o usuário existe e se a senha está correta
        if user and check_password_hash(user.senha, senha):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('CPF/E-mail ou senha inválidos.', 'red')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'yellow')
    return redirect(url_for('auth.login'))

@auth_bp.route('/createadm') 
def criarAdm():
    cpf = '12345678900'
    nome = 'adm'
    email = 'adm.unico@sistema.com'
    senha = generate_password_hash('12345678')
    is_adm = True
    new_user = User(cpf=cpf, nome=nome, email=email, senha=senha, is_adm=is_adm)
    database.session.add(new_user)
    database.session.commit()
    return redirect(url_for('auth.login'))
