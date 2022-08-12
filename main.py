from flask import Flask, request, make_response, redirect, render_template, session,url_for,flash
import unittest
from app import create_app

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')
    
app = create_app()

todos = ['Comprar cafe', 'Enviar solicitud de compra', 'Entregar video a productor ']


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello')
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')
    context = {
        'user_ip': user_ip,
        'todos': todos,
        'username' : username

    }

    return render_template('hello.html', **context)

@app.route('/sign_ig',methods=['GET','POST'])
def sign_in():
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')
    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username' : username
    }
    if login_form.validate_on_submit():
        username=login_form.username.data
        session['username']=username

        flash('Ingreso correcto')

        return redirect(url_for('index'))
        
    return render_template('sign_in.html', **context)
