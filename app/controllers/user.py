from flask import Blueprint, render_template, request
from flask_login import login_required

user = Blueprint('user', __name__, template_folder="../views/templates")


@user.route('/home')
@login_required
def user_me():
    name = request.args.get('name')
    email = request.args.get('email')
    return render_template('home.html', name=name, email=email)

