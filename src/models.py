from .app import database
from datetime import datetime, timezone
from flask_login import UserMixin

class User(database.Model, UserMixin):
    
    cpf = database.Column(database.String(11), primary_key=True)
    
    nome = database.Column(database.String(100), nullable=False)
    
    email = database.Column(database.String(100), nullable=False)
    
    senha = database.Column(database.String(100), nullable=False)
    
    is_adm = database.Column(database.Boolean, default=False)
    
    created_at = database.Column(database.DateTime, default=lambda: datetime.now(timezone.utc))
    
    update_at = database.Column(database.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return '<User %r>' % self.nome
    
    def get_id(self):
        return str(self.cpf)
    
class Produtos(database.Model):
    
    dataHoje = datetime.now(timezone.utc)
    
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    
    nome_produto = database.Column(database.String(100), nullable=False)
    
    descricao = database.Column(database.String(600), nullable=False, default='Sem Descrição')
    
    preco_compra = database.Column(database.Float, nullable=False)
    
    preco_venda = database.Column(database.Float, nullable=True)
    
    quantidade = database.Column(database.Integer, nullable=False)
    
    fornecedor = database.Column(database.String(100), nullable=False)
    
    data_compra = database.Column(database.DateTime, default=dataHoje)
    
    data_validade = database.Column(database.DateTime, nullable=True)

    def __repr__(self):
        return '<produtos %r>' % self.nome_produto
    
    
class SolicitarAlteracao(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    id_prod = database.Column(database.Integer, nullable=False)
    campo_alterado = database.Column(database.String(100), nullable=False)
    valor_anterior = database.Column(database.String(100), nullable=False)
    valor_novo = database.Column(database.String(100), nullable=False)
    solicitante_cpf = database.Column(
        database.String(11), 
        database.ForeignKey('user.cpf', ondelete='CASCADE'), # Adicionado ondelete='CASCADE' aqui
        nullable=False
    )
    solicitante = database.relationship('User', backref='solicitacoes_feitas', foreign_keys=[solicitante_cpf])

    # Se o aprovador_cpf também precisar ser nulo ou cascata, você pode adicionar a mesma lógica:
    aprovador_cpf = database.Column(
        database.String(11), 
        database.ForeignKey('user.cpf', ondelete='SET NULL'), # Ou 'CASCADE' se a solicitaç"ão deve sumir se o aprovador for deletado
        nullable=True
    )
    aprovador = database.relationship('User', backref='solicitacoes_aprovadas', foreign_keys=[aprovador_cpf])

    status = database.Column(database.String(100), nullable=False, default='Pendente')
    data_solicitacao = database.Column(database.DateTime, default=datetime.now(timezone.utc))
    aprovador_cpf = database.Column(database.String(11), database.ForeignKey('user.cpf'), nullable=True)
    aprovador = database.relationship('User', backref='solicitacoes_aprovadas', foreign_keys=[aprovador_cpf])
    data_aprovacao = database.Column(database.DateTime, nullable=True)
    motivo_rejeicao = database.Column(database.String(100), nullable=True)
    
    def __repr__(self):
        return '<SolicitarAlteracao %r>' % self.id