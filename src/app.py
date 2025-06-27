from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

database = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../src/db/farma.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '5ea7fa863c57c2f9103c5af6072916cfbf7e2e64b2ff3406'
    
    database.init_app(app)
    migrate.init_app(app, database)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Faça login para acessar esta página'

    with app.app_context():
        
        from .models import User, Produtos
        database.create_all()
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(str(user_id))
        
        from .routes.auth import auth_bp
        from .routes.cadastro_prod import cadastro_bp
        from .routes.produtos import produtos_bp
        from .routes.user import user_bp
        
        app.register_blueprint(cadastro_bp)
        app.register_blueprint(produtos_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(user_bp)
        
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app
