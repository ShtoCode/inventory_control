from flask import (Blueprint, flash, g, redirect,
                   render_template, request, url_for, session)
from werkzeug.security import check_password_hash, generate_password_hash
import functools
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        repassword = request.form['repassword']
        error = None

        if not nombre or not email or not password:
            error = 'Todos los campos son obligatorios.'

        if password != repassword:
            error = 'Las contraseñas no coinciden.'

        db, c = get_db()

        c.execute(
            "SELECT id_usuario FROM usuario WHERE email = %s", (email,)
        )

        if c.fetchone() is not None:
            error = 'El correo electrónico ya esta registrado.'

        if error is None:
            c.execute(
                'INSERT INTO usuario (nombre, email, password, tipo_usuario) VALUES (%s, %s, %s, 2) RETURNING id_usuario',
                (nombre, email, generate_password_hash(password))
            )
            user = c.fetchone()
            session.clear()
            session['user_id'] = user[0]
            db.commit()
            return redirect(url_for('home.index'))


        flash(error, "error")

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        error = None
        db, c = get_db()

        if not email or not password:
            error = "Todos los campos son requeridos."

        c.execute("SELECT * FROM usuario WHERE email = %s", (email,))

        user = c.fetchone()

        if user is None:
            error = "Usuario y/o contraseña incorrecta."

        elif not user[1]:
            error = "El correo ingresado no está verificado."

        elif not check_password_hash(user[3], password):
            error = "Usuario y/o contraseña incorrecta."

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('home.index'))

        flash(error, 'error')

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute('SELECT * FROM usuario WHERE id_usuario = %s', (user_id,))
        g.user = c.fetchone()
        if g.user:
            session['user_role'] = g.user[4]


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_role') != 1:
            flash('No tienes permiso para acceder a esta página', 'error')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
