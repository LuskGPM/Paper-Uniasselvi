from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../src/db/farma.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '5ea7fa863c57c2f9103c5af6072916cfbf7e2e64b2ff3406'
    database.init_app(app)

    with app.app_context():
        
        from . import models
        database.create_all()
        
        from .routes.cadastro_prod import cadastro_bp
        app.register_blueprint(cadastro_bp)
        
        from .routes.produtos import produtos_bp
        app.register_blueprint(produtos_bp)
        
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app
