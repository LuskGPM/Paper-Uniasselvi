import os
from flask import Flask as fl, render_template
from flask_sqlalchemy import SQLAlchemy as sqldb

app = fl(__name__, template_folder='../pages')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../database/farma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = sqldb(app)

@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)