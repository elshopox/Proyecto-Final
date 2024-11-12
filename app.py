from flask import Flask, render_template, flash, request, redirect, url_for, session
from datetime import datetime
import sqlite3

app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Clave para las sesiones

# Función para conectar con la base de datos
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear la base de datos y la tabla de productos
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL,
        image_url TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

# Ruta principal (inicio)
@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Ruta de checkout que procesa el formulario y genera la factura
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        buyer_name = request.form['buyer_name']
        ci = request.form['ci']
        date = request.form['date']
        
        cart_items = session['cart']
        total = sum(item['price'] for item in cart_items)
        
        # Cambia 'items' a 'product_list' aquí
        receipt = {
            'buyer_name': buyer_name,
            'ci': ci,
            'date': date,
            'product_list': cart_items,  # Cambio aquí
            'total': total
        }
        
        return render_template('receipt.html', receipt=receipt)
    return render_template('checkout.html')

# Ruta para agregar productos
@app.route('/add_product', methods=('GET', 'POST'))
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image_url = request.form['image_url']

        conn = get_db_connection()
        conn.execute('INSERT INTO products (name, description, price, image_url) VALUES (?, ?, ?, ?)',
                     (name, description, price, image_url))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_product.html')

# Ruta para el carrito de compras
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    cart_total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, cart_total=cart_total)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Aquí debes obtener el producto por su ID de tu base de datos o lista de productos
    product = {
        'id': product_id,
        'name': 'Producto ' + str(product_id),
        'price': 10.0  # Ejemplo: todos los productos tienen precio 10 Bs.
    }
    # Agregar el producto al carrito en la sesión
    session['cart'].append(product)
    flash('Producto añadido al carrito', 'success')
    return redirect(url_for('index'))

# Ruta para buscar productos
@app.route('/search')
def search():
    query = request.args.get('query')
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + query + '%',)).fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Inicializa el carrito en la sesión
@app.before_request
def initialize_cart():
    session.setdefault('cart', [])

if __name__ == '__main__':
    app.run(debug=True)
