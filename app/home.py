from flask import (Blueprint, flash, g, redirect,
                   render_template, request, url_for, session, jsonify)
from app.auth import login_required
from app.db import get_db
from datetime import datetime
import traceback


bp = Blueprint('home', __name__, url_prefix='/')


def get_label_filter(filter):
    filtro_etiquetas = {
        'all': 'Todos los productos',
        "1": 'Materiales',
        "2": 'Herramientas',
        "3": 'Equipo de protección'
    }
    return filtro_etiquetas.get(filter, 'Todos los productos')

@bp.route('/')
@login_required
def index():

    filter = request.args.get('filter', 'all')
    search = request.args.get('search', '')
    db, c = get_db()
    if search != '':
        c.execute("""SELECT p.id_producto,
                    p.nombre,
                    p.marca,
                    p.imagen,
                    p.cantidad_disponible,
                    tp.nombre,
                    p.tipo_producto
             FROM producto p
             JOIN tipo_producto tp
             ON p.tipo_producto = tp.id_tipo_producto
             WHERE LOWER(p.nombre) LIKE %s OR LOWER(p.marca) LIKE %s AND p.disponible = true AND cantidad_disponible > 0
             ORDER BY p.id_producto DESC""", ('%' + search.lower() + '%', '%' + search.lower() + '%'))

    
    elif filter == 'all':
        c.execute("""SELECT p.id_producto,
                    p.nombre,
                    p.marca,
                    p.imagen,
                    p.cantidad_disponible,
                    tp.nombre,
                    p.tipo_producto
                 FROM producto p
                 JOIN tipo_producto tp
                  ON p.tipo_producto = tp.id_tipo_producto
                 WHERE p.disponible = true AND cantidad_disponible > 0
              ORDER BY p.id_producto DESC""")
    else:
        c.execute("""SELECT p.id_producto,
                    p.nombre,
                    p.marca,
                    p.imagen,
                    p.cantidad_disponible,
                    tp.nombre,
                    p.tipo_producto
                 FROM producto p
                 JOIN tipo_producto tp
                  ON p.tipo_producto = tp.id_tipo_producto
                 WHERE p.tipo_producto = %s AND p.disponible = true AND cantidad_disponible > 0
              ORDER BY p.id_producto DESC""", (filter,))

    label_filter = get_label_filter(filter)

    productos = c.fetchall()


    return render_template('home/index.html', productos=productos, filter=label_filter)



@bp.route('/check', methods=['GET', 'POST'])
@login_required
def check_inventory():
    return render_template('home/check_inventory.html')



def get_product_details(product_names):
    db, c = get_db()
    placeholders = ', '.join(['%s' for _ in product_names])
    query = f"SELECT id_producto, nombre, marca, imagen, cantidad_disponible FROM producto WHERE nombre IN ({placeholders});"
    c.execute(query, product_names)
    products = c.fetchall()
    c.close()
    db.close()
    product_details = {}
    for product in products:
        id, nombre, marca, imagen, cantidad_disponible = product
        product_details[nombre] = {'id': id, 'marca': marca, 'imagen': imagen, 'cantidadDisponible': cantidad_disponible}
    return product_details

@bp.route('/get-inventory-products', methods=['POST'])
def get_inventory_products():
    try:
        product_names = request.get_json()
        products = get_product_details(product_names)

        return jsonify(products), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400



@bp.route('/confirm-inventory', methods=['POST'])
def confirm_inventory():
    try:
        products = request.get_json()
        for product in products:
            save_inventory(product)

        return jsonify({'success': True}), 200 

    except ValueError as ve:

        return jsonify({'success': False, 'message': str(ve)}), 400

    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': 'Error inesperado al guardar inventario'}), 500



def save_inventory(product):
    try: 
        db,c = get_db()
        id_producto = product['id']
        producto = product['producto']
        cantidad = product['cantidad']
        print(cantidad)
        fecha_devolucion = product.get('fechaDevolucion')  
        devolucion_dt = datetime.strptime(fecha_devolucion, "%Y-%m-%d")

        c.execute("SELECT cantidad_disponible FROM producto WHERE id_producto = %s", (id_producto,))
        cantidad_disponible = c.fetchone()[0]

        if cantidad_disponible < cantidad:
            print("Error aquí")
            raise ValueError(f"No hay suficiente cantidad disponible del producto {producto} para guardar el inventario")

        sql = """
        INSERT INTO asignacion (id_usuario, id_producto, cantidad, fecha_devolucion)
        VALUES (%s, %s, %s, %s)
        """
        c.execute(sql, (g.user_id, id_producto, cantidad, devolucion_dt))

        c.execute("UPDATE producto SET cantidad_disponible = (cantidad_disponible - %s) WHERE id_producto = %s", (cantidad, id_producto))


        db.commit()

    except Exception as e:
        if db:
            db.rollback()
            db.close()
            raise e


@bp.route('/request-product', methods=['GET', 'POST'])
def request_product():
    return render_template('home/request_product.html')
