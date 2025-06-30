from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import User, Produtos, SolicitarAlteracao
from ..app import database
from datetime import datetime, timezone

alteracao_bp = Blueprint(
    'alteracao',
    __name__,
    template_folder='../templates'
)

@alteracao_bp.route('/solicitar_alteracao/<int:produto_id>', methods=['POST'])
@login_required
def solicitar_alteracao(produto_id):
    if current_user.is_adm:
        flash('Administradores não devem usar esta rota de solicitação. Use a página de detalhes para editar diretamente.', 'yellow')
        return redirect(url_for('produtos.detalhes_produto', produto_id=produto_id))

    produto = Produtos.query.get_or_404(produto_id)
    alteracoes_solicitadas = []

    # Campo: preco_venda
    novo_preco_venda_str = request.form.get('preco_venda')
    if novo_preco_venda_str is not None:
        try:
            novo_preco_venda = float(novo_preco_venda_str)
            if novo_preco_venda != produto.preco_venda:
                alteracoes_solicitadas.append({
                    'campo': 'preco_venda',
                    'anterior': str(produto.preco_venda), 
                    'novo': str(novo_preco_venda)
                })
        except ValueError:
            flash('Preço de venda inválido. Por favor, insira um número válido.', 'red')
            return redirect(url_for('produtos.detalhes_produto', produto_id=produto.id))

    # Campo: quantidade
    nova_quantidade_str = request.form.get('quantidade')
    if nova_quantidade_str is not None:
        try:
            nova_quantidade = int(nova_quantidade_str)
            if nova_quantidade != produto.quantidade:
                alteracoes_solicitadas.append({
                    'campo': 'quantidade',
                    'anterior': str(produto.quantidade),
                    'novo': str(nova_quantidade)
                })
        except ValueError:
            flash('Quantidade inválida. Por favor, insira um número inteiro.', 'red')
            return redirect(url_for('produtos.detalhes_produto', produto_id=produto.id))

    # Campo: data-validade
    nova_data_validade_str = request.form.get('data-validade') # Captura como AAAA-MM
    if nova_data_validade_str:
        data_validade_produto_str_formatada = produto.data_validade.strftime('%Y-%m') if produto.data_validade else ''
        
        if nova_data_validade_str != data_validade_produto_str_formatada:
            try:
                datetime.strptime(nova_data_validade_str, '%Y-%m') 
                alteracoes_solicitadas.append({
                    'campo': 'data_validade', 
                    'anterior': data_validade_produto_str_formatada,
                    'novo': nova_data_validade_str
                })
            except ValueError:
                flash('Formato de data de validade inválido. Use AAAA-MM.', 'red')
                return redirect(url_for('produtos.detalhes_produto', produto_id=produto.id))

    if not alteracoes_solicitadas:
        flash('Nenhuma alteração nos campos permitidos foi detectada para solicitação.', 'yellow')
        return redirect(url_for('produtos.detalhes_produto', produto_id=produto.id))

    try:
        for alteracao in alteracoes_solicitadas:
            nova_solicitacao = SolicitarAlteracao(
                id_prod=produto.id, # O id_prod está correto, sem 'tipo_entidade'
                campo_alterado=alteracao['campo'],
                valor_anterior=alteracao['anterior'], 
                valor_novo=alteracao['novo'],
                solicitante_cpf=current_user.cpf,
                status='Pendente'
            )
            database.session.add(nova_solicitacao)
        
        database.session.commit()
        flash('Sua solicitação de alteração foi enviada para aprovação!', 'green')
        
    except Exception as e:
        database.session.rollback()
        flash(f'Erro ao criar solicitação de alteração: {e}', 'red')
    
    return redirect(url_for('produtos.detalhes_produto', produto_id=produto.id))

@alteracao_bp.route('/solicitar_alteracao/aprovar/<int:solicitacao_id>', methods=['POST'])
@login_required
def aprovar_solicitacao(solicitacao_id):
    # 1. Verifica se o usuário logado é um administrador
    if not current_user.is_adm:
        flash('Acesso negado. Apenas administradores podem aprovar solicitações.', 'red')
        return redirect(url_for('user.perfil'))

    solicitacao = SolicitarAlteracao.query.get_or_404(solicitacao_id)

    try:
        produto = Produtos.query.get(solicitacao.id_prod) 

        if not produto:
            raise Exception(f"Produto (ID: {solicitacao.id_prod}) não encontrado para a solicitação {solicitacao.id}.")

        if solicitacao.campo_alterado == 'preco_venda':
            setattr(produto, solicitacao.campo_alterado, float(solicitacao.valor_novo))
        elif solicitacao.campo_alterado == 'quantidade':
            setattr(produto, solicitacao.campo_alterado, int(solicitacao.valor_novo))
        elif solicitacao.campo_alterado == 'data_validade':
            ano_mes = solicitacao.valor_novo.split('-')
            data_objeto = datetime(int(ano_mes[0]), int(ano_mes[1]), 1).date() 
            setattr(produto, solicitacao.campo_alterado, data_objeto)
        else:
            raise Exception(f"Campo '{solicitacao.campo_alterado}' não é um campo válido para alteração por solicitação.")

        solicitacao.status = 'Aprovada'
        solicitacao.aprovador_cpf = current_user.cpf
        solicitacao.data_aprovacao = datetime.now(timezone.utc)
        
        database.session.commit()
        flash(f'Solicitação {solicitacao.id} aprovada e produto atualizado com sucesso!', 'green')

    except Exception as e:
        database.session.rollback() # Desfaz as operações se algo der errado
        flash(f'Erro ao aprovar solicitação {solicitacao.id}: {e}', 'red')
    
    return redirect(url_for('user.listar_solicitacoes'))

@alteracao_bp.route('/solicitacoes/rejeitar/<int:solicitacao_id>', methods=['POST'])
@login_required
def rejeitar_solicitacao(solicitacao_id):
    if not current_user.is_adm:
        flash('Acesso negado. Apenas administradores podem rejeitar solicitações.', 'red')
        return redirect(url_for('user.perfil'))
    solicitacao = SolicitarAlteracao.query.get_or_404(solicitacao_id)

    try:
        motivo = request.form.get('motivo_rejeicao', 'Rejeitado pelo administrador.') 

        solicitacao.status = 'Rejeitada'
        solicitacao.aprovador_cpf = current_user.cpf
        solicitacao.data_aprovacao = datetime.now(timezone.utc)
        solicitacao.motivo_rejeicao = motivo
        
        database.session.commit()  
        flash(f'Solicitação {solicitacao.id} rejeitada com sucesso!', 'yellow')

    except Exception as e:
        database.session.rollback()
        flash(f'Erro ao rejeitar solicitação {solicitacao.id}: {e}', 'red')
    
    return redirect(url_for('user.listar_solicitacoes'))

@alteracao_bp.route('/minhas_solicitacoes', methods=['GET'])
@login_required
def minhas_solicitacoes():
    if current_user.is_adm:
        flash('Administradores não precisam ver suas próprias solicitações aqui. Use o painel de administração.', 'yellow')
        return redirect(url_for('user.perfil'))
    
    solicitacoes_pendentes = SolicitarAlteracao.query.filter_by(
        solicitante_cpf=current_user.cpf,
        status='Pendente'
    ).order_by(SolicitarAlteracao.data_solicitacao.desc()).all()

    solicitacoes_aprovadas = SolicitarAlteracao.query.filter_by(
        solicitante_cpf=current_user.cpf,
        status='Aprovada'
    ).order_by(SolicitarAlteracao.data_aprovacao.desc()).all() 

    solicitacoes_rejeitadas = SolicitarAlteracao.query.filter_by(
        solicitante_cpf=current_user.cpf,
        status='Rejeitada'
    ).order_by(SolicitarAlteracao.data_aprovacao.desc()).all()

    return render_template(
        'listar_solicitacao_junior.html',
        pendentes=solicitacoes_pendentes,
        aprovadas=solicitacoes_aprovadas,
        rejeitadas=solicitacoes_rejeitadas
    )