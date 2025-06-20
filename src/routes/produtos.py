from flask import Blueprint, render_template, request, flash, get_flashed_messages, url_for
from ..app import database
from ..models import produtos
from datetime import datetime, timezone

produtos_bp = Blueprint(
    'produtos',
    __name__,
    template_folder='../templates'
)

@produtos_bp.route('/produtos')
def listar_produtos():
    todos_produtos = produtos.query.all()
    return render_template('listar_produtos.html', produtos=todos_produtos)

@produtos_bp.route('/produtos/<int:produto_id>')
def detalhes_produto(produto_id):
    produto = produtos.query.get_or_404(produto_id)
    return render_template('detalhes_produtos.html', produto = produto)

@produtos_bp.route('/produtos/test')
def update_produto():
    return 'Olá, Mundo!'