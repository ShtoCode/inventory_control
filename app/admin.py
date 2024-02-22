from flask import (Blueprint, flash, g, redirect,
                   render_template, request, current_app, url_for, jsonify)
import os
from app.auth import admin_required
from app.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@admin_required
def index():
    return render_template('admin/index.html')


@bp.route('/add-product', methods=['POST'])
@admin_required
def add_product():
    try:
        name = request.form.get('name')
        marca = request.form.get('marca')
        cantidad = request.form.get('cantidad')
        category = request.form.get('category')

        imagen = request.files['imagen']
        if imagen:
            carpeta = os.path.join(current_app.root_path,
                                   current_app.config['UPLOAD_FOLDER'])
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)  # Crear la carpeta si no existe
            ruta_img = os.path.join(carpeta, imagen.filename)
            imagen.save(ruta_img)

        tipo = None
        if category == "MT":
            tipo = 1
        elif category == "HH":
            tipo = 2
        elif category == "EPP":
            tipo = 3

        if tipo:
            db, c = get_db()
            try:
                c.execute(
                    f"INSERT INTO producto (nombre, marca, imagen, cantidad, tipo_producto) VALUES (%s, %s, %s, %s, %s)",
                    (name, marca, ruta_img if imagen else None, cantidad, tipo)
                )
                db.commit()

                return jsonify({'success': True})
            except Exception as e:
                print(e)
                return jsonify({'success': False, 'message': str(e)}), 400
        else:
            return jsonify({'success': False, 'message': 'Categoría no válida'}), 400
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': str(e)}), 400
