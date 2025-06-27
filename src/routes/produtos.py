from flask import Blueprint, redirect, render_template, request, flash, get_flashed_messages, url_for
from flask_login import login_required
from ..app import database
from ..models import Produtos
from datetime import datetime, timezone

produtos_bp = Blueprint(
    'produtos',
    __name__,
    template_folder='../templates'
)

@produtos_bp.route('/produtos')
@login_required
def listar_produtos():
    search_query = request.args.get('q','').strip()
    
    if search_query:
        todos_produtos = Produtos.query.filter(Produtos.nome_produto.ilike(f'%{search_query}%'))
    else:
        todos_produtos = Produtos.query
    
    todos_produtos = todos_produtos.order_by(Produtos.nome_produto).all()
    return render_template('listar_produtos.html', produtos=todos_produtos)

@produtos_bp.route('/produtos/list/<int:produto_id>')
def detalhes_produto(produto_id):
    produto = Produtos.query.get_or_404(produto_id)
    return render_template('detalhes_produtos.html', produto = produto)

@produtos_bp.route('/produtos/update/<int:produto_id>', methods=['POST'])
def update_produto(produto_id):
    produto = Produtos.query.get_or_404(produto_id)
    
    try:
        produto.nome_produto = request.form['nome']
        produto.descricao = request.form['desc']
        produto.preco_compra = float(request.form['preco_compra'])
        preco_venda_str = request.form['preco_venda']
        if preco_venda_str:
            produto.preco_venda=float(preco_venda_str)
        produto.quantidade = int(request.form['quantidade'])
        produto.fornecedor = request.form['fornecedor']
        data_compra_str = str(request.form['data-compra'])
        
        if data_compra_str:
            produto.data_compra = datetime.strptime(data_compra_str, '%Y-%m').replace(day=1, tzinfo=timezone.utc)
        data_validade_str = str(request.form['data-validade'])
        
        if data_validade_str:
            produto.data_validade = datetime.strptime(data_validade_str,'%Y-%m').replace(day=1, tzinfo=timezone.utc) 
        
        database.session.commit()
        flash(f'Fármaco atualizado com sucesso', 'green')
        return redirect(url_for('produtos.detalhes_produto', produto_id=produto.id))
    
    except ValueError as e:
        flash(f'Erro de validação de dados: {e}', 'red')
        return redirect(url_for('produtos.detalhes_produto', produto_id=produto.id))
    
    except Exception as e:
        flash(f'Erro ao cadastrar produto: {e}', 'red')
        return redirect(url_for('produtos.detalhes_produto', produto_id=produto.id))
 
@produtos_bp.route('/produtos/deletar/<int:produto_id>', methods=['POST'])
def deletar_produto(produto_id):
    produto = database.session.get(Produtos, produto_id) 

    if not produto:
        flash('Produto não encontrado.', 'error')
        return redirect(url_for('produtos.listar_produtos'))

    try:
        database.session.delete(produto)
        database.session.commit() 

        flash(f'Produto "{produto.nome_produto}" deletado com sucesso!', 'green')
        return redirect(url_for('produtos.listar_produtos'))

    except Exception as e:
        database.session.rollback()
        flash(f'Erro interno ao deletar produto: {e}', 'red') 
        return redirect(url_for('produtos.listar_produtos'))  