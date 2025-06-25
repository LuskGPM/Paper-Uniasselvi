from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from ..app import database

user_bp = Blueprint(
    'user',
    __name__,
    template_folder='../templates'
)

@user_bp.route('/perfil')
def perfil():
    if current_user.is_authenticated:
        user = User.query.filter_by(cpf=current_user.cpf).first()
        if user.is_adm:
            return render_template('perfil-adm.html', user=user)
        else:
            return render_template('perfil-jr.html', user=user)
    else:
        return redirect(url_for('auth.login'))
    
@user_bp.route('/analisar_senha', methods=['GET', 'POST'])
@login_required
def analisar_senha(prosseguir = False):
    if request.method == 'POST':
        user = user.query.filter_by(cpf=current_user.cpf).first()
        senha_form = request.form.get('senha_atual')
        if check_password_hash(user.senha, senha_form):
            prosseguir = True
            return prosseguir
        else:
            flash('Senha incorreta. Por favor, tente novamente.', 'red')
            prosseguir = False
            return prosseguir

@user_bp.route('/atualizar_usuario', methods=['GET', 'POST'])
@login_required
def atualizar_senha():
    if request.method == 'POST':
        senha_nova = request.form.get('senha_nova')
        senha_hash = generate_password_hash(senha_nova)
        user = user.query.filter_by(cpf=current_user.cpf).first()
        user.senha = senha_hash
        database.session.commit()
        flash('Senha atualizada com sucesso!', 'green')
        return redirect(url_for('user.perfil'))
    