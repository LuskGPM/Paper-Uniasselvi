from app import app, database
from datetime import datetime, timezone

class User(database.Model):
    cpf = database.Column(database.String(11), primary_key=True)
    nome = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(100), nullable=False)
    senha = database.Column(database.String(100), nullable=False)
    is_adm = database.Column(database.Boolean, default=False)
    created_at = database.Column(database.DateTime, default=lambda: datetime.now(timezone.utc))
    update_at = database.Column(database.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return '<User %r>' % self.nome
    
class produtos(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    nome_produto = database.Column(database.String(100), nullable=False)
    descricao = database.Column(database.String(100), nullable=False, default='Sem Descrição')
    preco = database.Column(database.Float, nullable=False)
    quantidade = database.Column(database.Integer, nullable=False)
    fornecedor = database.Column(database.String(100), nullable=False)
    data_compra = database.Column(database.DateTime, default=lambda: datetime.now(timezone.utc))
    data_validade = database.Column(database.DateTime, nullable=True)

    def __repr__(self):
        return '<produtos %r>' % self.nome_produto
    
with app.app_context():
    database.create_all()
