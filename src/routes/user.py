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
def perfil(prosseguir = 'false'):
    if current_user.is_authenticated:
        user = User.query.filter_by(cpf=current_user.cpf).first()
        if user.is_adm:
            return render_template('perfil-adm.html', user=user, prosseguir = prosseguir)
        else:
            return render_template('perfil-jr.html', user=user, prosseguir = prosseguir)
    else:
        return redirect(url_for('auth.login'))
    
@user_bp.route('/analisar_senha', methods=['GET', 'POST'])
@login_required
def analisar_senha():
    if request.method == 'POST':
        user = User.query.filter_by(cpf=current_user.cpf).first()
        senha_form = request.form.get('senha_atual')
        if check_password_hash(user.senha, senha_form):
            return redirect(url_for('user.perfil', prosseguir = 'true'))
        else:
            flash('Senha incorreta. Por favor, tente novamente.', 'red')
            return redirect(url_for('user.perfil'))

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
    
    
@user_bp.route('/cadastro-user', methods=['GET', 'POST'])
def cadastrar_user():
    
    if current_user.is_authenticated:
        
        if request.method == 'POST':
            cpf_str = request.form['cpf']
            cpf = cpf_str.replace('-', '').replace('.', '').strip()
            nome = request.form['nome'].strip()
            email = request.form['email'].strip()
            senha_pura = request.form['senha']
            senha_hash = generate_password_hash(senha_pura)
            is_adm_str = request.form.get('is_adm')
            if is_adm_str == 'true':
                is_adm_bool = True
            else:
                is_adm_bool = False
            
            
            new_user = User(
                cpf = cpf,
                nome = nome,
                email = email,
                senha = senha_hash,
                is_adm = is_adm_bool
            )
            
            try: 
                database.session.add(new_user)
                database.session.commit()
                flash('Usuário cadastrado com sucesso', 'green')
                return render_template('cadastro-user.html')
            except Exception as e:
                database.session.rollback()
                flash(f'Erro ao cadastrar usuário: {e}', 'red')
        
        return render_template('cadastro-user.html')
    
    else:
        return redirect(url_for('auth.login'))