from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import User
from ..app import database

user_bp = Blueprint(
    'user',
    __name__,
    template_folder='../templates'
)

@user_bp.route('/perfil')
def perfil():
    if current_user.is_authenticated:
        user = User.query.filter_by(cpf=current_user.cpf).first()
        return render_template('perfil.html', user=user)
    else:
        return redirect(url_for('auth.login'))
    
