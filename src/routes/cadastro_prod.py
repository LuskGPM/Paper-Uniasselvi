from flask import Blueprint, redirect, render_template, request, flash, get_flashed_messages, url_for
from flask_login import current_user, login_required
from ..app import database
from ..models import Produtos
from datetime import datetime, timezone

cadastro_bp = Blueprint(
    'cadastro',
    __name__,
    template_folder='../templates'
)

@cadastro_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastrar_produto():
    
    if current_user.is_authenticated:
    
        data_validade_prod = None
        
        if request.method == 'POST':
            nome_prod = request.form['nome']
            descricao_prod = request.form.get('desc', '')
            preco_prod_compra = float(request.form['preco_compra'])
            quantidade_prod = int(request.form['quantidade'])     
            fornecedor_prod = request.form['fornecedor']
            data_validade_str = request.form.get('data-validade') + '-01'
            
            if data_validade_str:
                try:
                    data_validade_prod = datetime.strptime(data_validade_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
                except ValueError as e:
                    flash('Erro, data inválida', 'red')
                    return render_template('cadastro.html')
                
                novo_produto = Produtos(
                    nome_produto = nome_prod,
                    descricao = descricao_prod,
                    preco_compra = preco_prod_compra,
                    quantidade = quantidade_prod,
                    fornecedor = fornecedor_prod,
                    data_validade = data_validade_prod
                )
            
            try: 
                database.session.add(novo_produto)
                database.session.commit()
                flash('Cadastrado com sucesso', 'green')
                return render_template('cadastro.html')
            except Exception as e:
                database.session.rollback()
                flash(f'Erro ao cadastrar produto: {e}', 'red')
                return f'Erro no banco: {e}'
        
        return render_template('cadastro.html')
    
    else:
        return redirect(url_for('auth.login'))


        