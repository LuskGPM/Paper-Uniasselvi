from flask import Flask as fl, render_template
from flask_sqlalchemy import SQLAlchemy as sqldb

app = fl(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = sqldb(app)

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
    