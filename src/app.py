from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)

with app.app_context():
    import models
    database.create_all()
    
    from .routes.cadastro_produto import cadastro_bp
    app.register_blueprint(cadastro_bp)
@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    