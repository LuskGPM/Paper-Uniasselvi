from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import SolicitarAlteracao, User
from ..app import database
from datetime import datetime, timezone

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
def analisar_senha():
    if request.method == 'POST':
        user = User.query.filter_by(cpf=current_user.cpf).first()
        senha_form = request.form.get('senha_atual')
        if check_password_hash(user.senha, senha_form):
            return redirect(url_for('user.alterar_senha'))
        else:
            flash('Senha incorreta. Por favor, tente novamente.', 'red')
            return redirect(url_for('user.perfil'))
        
@user_bp.route('/atualizar_senha/redirect', methods=['GET', 'POST'])
@login_required
def alterar_senha():
    return render_template('atualizar-senha.html')

@user_bp.route('/atualizar_senha/alterar', methods=['GET', 'POST'])
def atualizar_senha(): 
    try:
        if request.method == 'POST':
            senha_nova = request.form.get('senha_nova')
            repetir_senha = request.form.get('repetir_senha')
            
            if senha_nova != repetir_senha:
                flash('As senhas digitadas devem ser iguais.', 'red')
                return redirect(url_for('user.alterar_senha'))
            
            senha_hash = generate_password_hash(senha_nova)
            user = User.query.filter_by(cpf=current_user.cpf).first()
            user.senha = senha_hash
            database.session.commit()
            flash('Senha atualizada com sucesso!', 'green')
            return redirect(url_for('user.perfil'))
        
    except Exception as e:
        database.session.rollback()
        flash(f'Erro ao atualizar senha: {e}', 'red')
        return redirect(url_for('user.perfil'))
    
    return redirect(url_for('user.alterar_senha'))

@user_bp.route('/recuperar-senha')
def recuperar_senha():
    flash('Entre em contato com o Email ou o Número mencionados', 'yellow')
    return redirect(url_for('index'))
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
    
    
@user_bp.route('/listar-users', methods=['GET', 'POST'])
@login_required
def listar_user():
    if current_user.is_adm:
        
        search_query = request.args.get('q','').strip()
        
        if search_query:
            todos_usuarios = User.query.filter(User.nome.ilike(f'%{search_query}%'))
        else:
            todos_usuarios = User.query
        
        todos_usuarios = todos_usuarios.order_by(User.nome).all()
        return render_template('listar-users.html', usuarios=todos_usuarios)
    else:
        flash('Acesso negado', 'red')
        return redirect(url_for('user.perfil'))

@user_bp.route('/deletar-user/<string:user_cpf>', methods=['POST'])
def deletar_user(user_cpf):
    user_cpf = user_cpf.replace('-', '').replace('.', '').strip()
    try:
        user = User.query.filter_by(cpf=user_cpf).first()
        database.session.delete(user)
        database.session.commit()
        flash('Usuário deletado com sucesso!', 'green')
    except Exception as e:
        database.session.rollback()
        flash(f'Erro ao deletar usuário: {e}', 'red')
    return redirect(url_for('user.listar_user'))

@user_bp.route('/admin/solicitacoes', methods=['GET'])
@login_required
def listar_solicitacoes():
    if not current_user.is_adm:
        flash('Acesso negado. Esta área é exclusiva para administradores.', 'red')
        return redirect(url_for('main.dashboard'))

    # 2. Consulta as solicitações de alteração com status 'Pendente'
    # Ordenamos pela data de solicitação para ver as mais antigas primeiro.
    solicitacoes = SolicitarAlteracao.query.filter_by(status='Pendente').order_by(SolicitarAlteracao.data_solicitacao.asc()).all()

    # 3. Renderiza o template, passando a lista de solicitações para ele
    return render_template('listar_solicitacao_adm.html', solicitacoes=solicitacoes)
