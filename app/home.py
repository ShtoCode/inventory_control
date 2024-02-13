from flask import (Blueprint, flash, g, redirect,
                   render_template, request, url_for, session, jsonify)
from app.auth import login_required
from app.db import get_db


bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
@login_required
def index():
    db, c = get_db()
    c.execute(
        "SELECT * FROM producto"
    )
    productos = c.fetchall()
   

    return render_template('home/index.html', productos=productos)


@bp.route('/add-inventory', methods=['POST'])
@login_required
def add_inventory():
    data = request.get_json()
    producto = data.get('producto')
    cantidad = data.get('quantity')
    print(producto, cantidad)
    return jsonify({'success': True})
