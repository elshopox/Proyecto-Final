from flask import Flask, render_template, flash, request, redirect, url_for, session
from datetime import datetime
import sqlite3

app = Flask(__name__)

app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

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

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        buyer_name = request.form['buyer_name']
        ci = request.form['ci']
        date = request.form['date']
        
        cart_items = session['cart']
        total = sum(item['price'] for item in cart_items)
        
        receipt = {
            'buyer_name': buyer_name,
            'ci': ci,
            'date': date,
            'product_list': cart_items, 
            'total': total
        }
        
        return render_template('receipt.html', receipt=receipt)
    return render_template('checkout.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Obtener datos del formulario
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image_url = request.form['image_url']
        
        # Crear un diccionario para el producto
        product = {
            'name': name,
            'description': description,
            'price': price,
            'image_url': image_url
        }
        
        # Agregar el producto a la lista
        product.append(product)
        
        # Mostrar un mensaje de éxito
        flash('Producto agregado exitosamente', 'success')
        
        # Redirigir a la página de inicio o a la lista de productos
        return redirect(url_for('index'))
    
    return render_template('add_product.html')


@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    cart_total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, cart_total=cart_total)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = {
        'id': product_id,
        'name': 'Producto ' + str(product_id),
        'price': 10.0 
    }
    session['cart'].append(product)
    flash('Producto añadido al carrito', 'success')
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('query')
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + query + '%',)).fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.before_request
def initialize_cart():
    session.setdefault('cart', [])

if __name__ == '__main__':
    app.run(debug=True)
