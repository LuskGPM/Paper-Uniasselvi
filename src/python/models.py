from app import app, database
from sqlalchemy.orm import relationship

class User(database.Model):
    cpf = database.Column(database.String(11), primary_key=True)
    nome = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(100), nullable=False)
    senha = database.Column(database.String(100), nullable=False)
    is_adm = database.Column(database.Boolean, default=False)
    
    def __init__(self, cpf, nome, email, senha, is_adm=False):
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.senha = senha
        self.is_adm = is_adm
        
    def salvar(self):        
        if self.is_adm:
            user_adm = UserADM(cpf_adm=self.cpf, nome_adm=self.nome, email_adm=self.email)
            database.session.add(user_adm)
            
        else:
            user_jr = UserJR(cpf_jr=self.cpf, nome_jr=self.nome, email_jr=self.email)
            database.session.add(user_jr)
    def __repr__(self):
        return '<User %r>' % self.nome

class UserADM(database.Model):
    cpf_adm = database.Column(database.String(11), database.ForeignKey('user.cpf'), primary_key=True)
    nome_adm = database.Column(database.String(100), nullable=False)
    email_adm = database.Column(database.String(50), nullable=False)
    senha_adm = database.Column(database.String(100), nullable=False)
    
    def __repr__(self):
        return '<UserADM %r>' % self.nome_adm
    
class UserJR(database.Model):
    cpf_jr = database.Column(database.String(11), database.ForeignKey('user.cpf'), primary_key=True)
    nome_jr = database.Column(database.String(100), nullable=False)
    email_jr = database.Column(database.String(50), nullable=False)
    senha_jr = database.Column(database.String(100), nullable=False)
    
    def __repr__(self):
        return '<UserJR %r>' % self.nome_jr
    
class produtos(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_produto = database.Column(database.String(100), nullable=False)
    descricao = database.Column(database.String(100), nullable=False)
    preco = database.Column(database.Float, nullable=False)
    estoque = database.Column(database.Integer, nullable=False)
    categoria = database.Column(database.String(100), nullable=False)
    fornecedor = database.Column(database.String(100), nullable=False)

    def __repr__(self):
        return '<produtos %r>' % self.nome_produto
    
with app.app_context():
    database.create_all(checkfirst=True)
    
if __name__ == '__main__':
    app.run()
