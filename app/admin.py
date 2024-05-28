from flask import (Blueprint, flash, g, redirect,
                   render_template, request, current_app, url_for, jsonify)
import os
from app.auth import admin_required
from app.db import get_db
from werkzeug.utils import secure_filename

bp = Blueprint('admin', __name__, url_prefix='/admin')


def get_label_filter(filter):
    filtro_etiquetas = {
        'all': 'Todos los productos',
        "1": 'Material',
        "2": 'Herramienta',
        "3": 'EPP'
    }
    return filtro_etiquetas.get(filter, 'Todos los productos')

@bp.route('/', methods=['GET'])
@admin_required
def index():
    filter = request.args.get('filter', 'all')
    search = request.args.get('search', '')
    db, c = get_db()
    if search != '':
        c.execute("""SELECT p.id_producto,
                    p.nombre,
                    p.marca,
                    p.cantidad,
                    p.imagen,
                    tp.nombre,
                    p.tipo_producto,
                    p.disponible
             FROM producto p
             JOIN tipo_producto tp
             ON p.tipo_producto = tp.id_tipo_producto
             WHERE LOWER(p.nombre) LIKE %s OR LOWER(p.marca) LIKE %s
             ORDER BY p.disponible DESC, p.id_producto DESC""", ('%' + search.lower() + '%', '%' + search.lower() + '%'))

    elif filter == 'all':
        c.execute("""SELECT p.id_producto,
                        p.nombre,
                        p.marca,
                        p.cantidad_disponible,
                        p.imagen,
                        tp.nombre,
                        p.tipo_producto,
                        p.disponible
                 FROM producto p
                 JOIN tipo_producto tp
                  ON p.tipo_producto = tp.id_tipo_producto
              ORDER BY p.disponible DESC, p.id_producto DESC""")
    else:
        c.execute("""SELECT p.id_producto,
                        p.nombre,
                        p.marca,
                        p.cantidad_disponible,
                        p.imagen,
                        tp.nombre,
                        p.tipo_producto,
                        p.disponible
                 FROM producto p
                 JOIN tipo_producto tp
                  ON p.tipo_producto = tp.id_tipo_producto
                 WHERE p.tipo_producto = %s
              ORDER BY p.disponible DESC, p.id_producto DESC""", (filter,))

    label_filter = get_label_filter(filter)

    productos = c.fetchall()
    return render_template('admin/index.html', productos=productos, filter=label_filter)





@ bp.route('/add-product', methods=['POST'])
@ admin_required
def add_product():
    try:
        name = request.form.get('name')
        marca = request.form.get('marca')
        cantidad = request.form.get('cantidad')
        category = request.form.get('category')

        imagen = request.files['imagen']
        nombre_imagen = None

        if name:
            db, c = get_db()
            c.execute("SELECT * FROM producto WHERE nombre = %s", (name,))
            producto = c.fetchall()
            if producto: 
                return jsonify({'success': False, 'message': f"Ya existe un producto con el nombre \"{name}\"."}), 400


        if imagen:
            carpeta = os.path.join(current_app.root_path,
                                   current_app.config['UPLOAD_FOLDER'])
            nombre_imagen = secure_filename(imagen.filename)
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
            ruta_img = os.path.join(carpeta, imagen.filename)
            imagen.save(ruta_img)

        tipo = None
        if category == "Material":
            tipo = 1
        elif category == "Herramienta":
            tipo = 2
        elif category == "EPP":
            tipo = 3

        if tipo:
            try:
                c.execute(
                    f"INSERT INTO producto (nombre, marca, imagen, cantidad, cantidad_disponible, tipo_producto) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, marca, nombre_imagen, cantidad, cantidad, tipo)
                )
                db.commit()

                return jsonify({'success': True}), 200
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)}), 400
        else:
            print("Categoría no válida")
            return jsonify({'success': False, 'message': 'Categoría no válida'}), 400
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route('/edit-product/<id>', methods=['POST'])
@admin_required
def edit_product(id):
    try:
        name = request.form.get('nombre-producto')
        marca = request.form.get('marca')
        cantidad = request.form.get('cantidad-total')
        category = request.form.get('category')

        imagen = request.files['imagen']

        print("id: ", id)

        tipo = None
        print(category)
        try:
            db,c = get_db()
            c.execute("SELECT * FROM producto WHERE id_producto=%s", (id,))
            original = c.fetchone()
            print("original: ", original)

        except Exception as e:
            print(str(e))
            return jsonify({'success': False, 'message': str(e)}), 400



        if category == "Material":
            tipo = 1
        elif category == "Herramienta":
            tipo = 2
        elif category == "EPP":
            tipo = 3
        nombre_imagen = None


        if imagen:
            carpeta = os.path.join(current_app.root_path,
                                   current_app.config['UPLOAD_FOLDER'])
            nombre_imagen = secure_filename(imagen.filename)
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
            ruta_img = os.path.join(carpeta, imagen.filename)
            imagen.save(ruta_img)

            if tipo:
                db, c = get_db()
                try:
                    c.execute(
                        f"UPDATE producto SET nombre = %s, marca = %s, imagen = %s, cantidad = %s, tipo_producto = %s WHERE id_producto = %s",
                        (name, marca, nombre_imagen, cantidad, tipo, id)
                    )
                    print("PRODUCTO ACTUALIZADO")
                    db.commit()

                    if c.rowcount > 0:
                        return jsonify({'success': True}), 200
                    else:
                        return jsonify({'success': False, 'message': 'El producto no se encontró o no se actualizó correctamente.'}), 400


                except Exception as e:
                    print(e)
                    return jsonify({'success': False, 'message': str(e)}), 400

        print("Tipo: ", tipo)
        if tipo:
            db, c = get_db()
            try:
                c.execute(
                    f"UPDATE producto SET nombre = %s, marca = %s, cantidad = %s, tipo_producto = %s WHERE id_producto = %s",
                    (name, marca, cantidad, tipo, id)
                )
                print("PRODUCTO ACTUALIZADO")
                db.commit()

                return jsonify({'success': True}), 200
            except Exception as e:
                print(e)
                return jsonify({'success': False, 'message': str(e)}), 400
        else:
            return jsonify({'success': False, 'message': 'Categoría no válida'}), 400
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route('/disable/<id>', methods=['POST'])
def disable_product(id):
    try:
        print(id)
        db, c = get_db()
        c.execute("UPDATE producto SET disponible = false WHERE id_producto = %s", (id,))
        db.commit()

        return jsonify({'success': True}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route('/enable/<id>', methods=['POST'])
def enable_product(id):
    try:
        print(id)
        db, c = get_db()
        c.execute("UPDATE producto SET disponible = true WHERE id_producto = %s", (id,))
        db.commit()

        return jsonify({'success': True}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route('/inventarios', methods=['GET'])
def inventories():
    return render_template('admin/inventario.html')