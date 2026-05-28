from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect('/login')

# REGISTER
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    name = request.form['name']
    password = request.form['password']

    db = get_db()
    db.execute("INSERT INTO users (name, password, role) VALUES (?, ?, ?)", (name, password, "user"))
    db.commit()
    return redirect('/login')

# LOGIN
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_user', methods=['POST'])
def login_user():
    name = request.form['name']
    password = request.form['password']

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE name=? AND password=?", (name, password)).fetchone()

    if user:
        session['user'] = user['name']
        session['role'] = user['role']

        if user['role'] == "admin":
            return redirect('/admin')
        else:
            return redirect('/products')

    return "Invalid Login"

# PRODUCTS
@app.route('/products')
def products():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return render_template('products.html', products=products)

# CART
@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(id)
    session.modified = True
    return redirect('/products')

@app.route('/cart')
def cart():
    if 'cart' not in session:
        return render_template('cart.html', items=[], total=0)

    db = get_db()
    items = []

    for pid in session['cart']:
        product = db.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
        if product:
            items.append(product)

    total = sum(item['price'] for item in items)
    return render_template('cart.html', items=items, total=total)

# ADMIN
@app.route('/admin')
def admin():
    if session.get('role') != "admin":
        return redirect('/login')

    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return render_template('admin.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    if session.get('role') != "admin":
        return redirect('/login')

    name = request.form['name']
    price = request.form['price']
    image = request.form['image']

    db = get_db()
    db.execute("INSERT INTO products (name, price, image) VALUES (?, ?, ?)", (name, price, image))
    db.commit()
    return redirect('/admin')

@app.route('/delete/<int:id>')
def delete(id):
    if session.get('role') != "admin":
        return redirect('/login')

    db = get_db()
    db.execute("DELETE FROM products WHERE id=?", (id,))
    db.commit()
    return redirect('/admin')

# EDIT
@app.route('/edit/<int:id>')
def edit(id):
    if session.get('role') != "admin":
        return redirect('/login')

    db = get_db()
    product = db.execute("SELECT * FROM products WHERE id=?", (id,)).fetchone()
    return render_template('edit_product.html', product=product)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if session.get('role') != "admin":
        return redirect('/login')

    name = request.form['name']
    price = request.form['price']
    image = request.form['image']

    db = get_db()
    db.execute("UPDATE products SET name=?, price=?, image=? WHERE id=?",
               (name, price, image, id))
    db.commit()
    return redirect('/admin')

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)