import datetime

from flask import Flask, render_template, request, session, redirect
from database import Database

app = Flask(__name__)
app.secret_key = '1234'
app.permanent_session_lifetime = datetime.timedelta(days=365)
db = Database()


@app.route('/', methods=['get', 'post'])
def main_page():
    products = db.select("SELECT * from products")
    brands = db.select("SELECT DISTINCT manufacturer from products")
    colours = db.select("SELECT DISTINCT colour from products")
    if request.method == 'POST':
        maillog = request.form.get('mailmini')
        passwordlog = request.form.get('passwordmini')
        name = request.form.get('name')
        surname = request.form.get('surname')
        phone = request.form.get('phone')
        mail = request.form.get('mail')
        dob = str(request.form.get('dob')).split('.')
        dob.reverse()
        dob = '-'.join(dob)
        password = request.form.get('password')
        if name:
            db.insert(
                f"INSERT INTO users VALUES('{name}', '{surname}', '{phone}', '{mail}', '{password}', '{dob}', 'n')")
            session['is_logged'] = True
            session['mail'] = mail
            if 'saved' not in list(session.keys()):
                session['saved'] = []
            if 'cart' not in list(session.keys()):
                session['cart'] = []
        elif maillog and passwordlog:
            if len(db.select(f"SELECT name FROM users WHERE mail='{maillog}'")):
                session['is_logged'] = True
                session['mail'] = maillog
                if 'saved' not in list(session.keys()):
                    session['saved'] = []
                if 'cart' not in list(session.keys()):
                    session['cart'] = []
            else:
                session['is_logged'] = False
                session['mail'] = False
                return render_template("error.html", title='Error :(', error='your login or password are incorrect')
    return render_template("main_page.html", title='Welcome!', session=session, products=products,
                           brands=brands, colours=colours)


@app.route('/profile')
def show_profile():
    print(session)
    if session['is_logged']:
        info = db.select(f"SELECT * FROM users WHERE mail='{session['mail']}'")
        return render_template("profile.html", title='Profile', info=info)
    return render_template("error.html", title='Error :(', error='firstly you need to log in or register')


@app.route('/aboba', methods=['post'])
def aboba():
    first = request.values.get('first')
    db.insert(f"UPDATE users SET name = '{first}' where mail = '{session['mail']}'")

    return {'aboba': first}


@app.route('/left')
def leave_account():
    session['is_logged'] = False
    session['mail'] = False

    return redirect('/')


@app.route('/filter_prod')
def filter_prod():
    brands = db.select("SELECT DISTINCT manufacturer from products")
    colours = db.select("SELECT DISTINCT colour from products")
    req = request.values.to_dict(flat=False)
    if req:
        temp = '('
        for key in list(req.keys()):
            for item in req[key]:
                if item != req[key][len(req[key]) - 1]:
                    if key.split('[]')[0] == 'price':
                        temp += f"{key.split('[]')[0]}>='{item}' AND "
                    else:
                        temp += f"{key.split('[]')[0]}='{item}' OR "
                else:
                    if key.split('[]')[0] == 'price':
                        if item != -1:
                            temp += f"{key.split('[]')[0]}<='{1000000}')"
                        else:
                            temp += f"{key.split('[]')[0]}<='{item}')"
                    else:
                        temp += f"{key.split('[]')[0]}='{item}')"
            if key != list(req.keys())[len(list(req.keys())) - 1]:
                temp += ' AND ('
        req_to_db = f"SELECT * FROM products WHERE {temp}"
    else:
        req_to_db = f"SELECT * FROM products"
    if not db.select(req_to_db):
        return '<h3>Sorry, but there is no products you have chosen :(</h3>'
    return db.select(req_to_db)


@app.route('/set_saved', methods=['post'])
def set_saved():
    saved_product = request.values.to_dict(flat=False)['toSave'][0]
    if saved_product in session['saved']:
        session['saved'].remove(saved_product)
    else:
        session['saved'].append(saved_product)
    if not session.modified:
        session.modified = True
    return session['saved']


@app.route('/set_cart', methods=['post'])
def set_cart():
    in_cart_product = request.values.to_dict(flat=False)['toCart'][0]
    if in_cart_product in session['cart']:
        session['cart'].remove(in_cart_product)
    else:
        session['cart'].append(in_cart_product)
    if not session.modified:
        session.modified = True
    return session['cart']


@app.route('/saved', methods=['get', 'post'])
def show_saved():
    saved = "','".join(session['saved'])
    products = db.select(f"SELECT * from products WHERE name in ('{saved}')")
    if products:
        return render_template("cart.html", title='Saved', products=products)
    return render_template("cart.html", title='Saved', message='Sorry, but you should firstly like products :(')


@app.route('/cart', methods=['get', 'post'])
def show_cart():
    summa = 0
    cart = "','".join(session['cart'])
    products = db.select(f"SELECT * from products WHERE name in ('{cart}')")
    if len(session['cart']) > 1:
        for product in products:
            summa += product['price']
    if products:
        return render_template("cart.html", title='Cart', products=products, summa=summa if len(session['cart']) > 1 else products['price'])
    return render_template("cart.html", title='Cart', message='Sorry, but you should firstly choose products :(')


@app.route('/product/<product_name>')
def get_product(product_name):
    product = db.select(f"SELECT * FROM products WHERE name='{product_name}'")
    if len(product):
        return render_template("product.html", product=product)
    return render_template("error.html", title='Error :(', error=f'there is no such product in our shop')


@app.route('/products/<product_category>/<product_property>')
def get_category_and_property(product_category, product_property):
    products = db.select(
        f"SELECT * FROM products WHERE category='{product_category}' AND (colour in ('{product_property}','{product_property}') OR manufacturer in ('{product_property}','{product_property}'))")
    if products:
        return render_template("category.html", title=f'{product_category} | {product_property}', session=session,
                               products=products)
    return render_template("error.html", error='there is no products from this category with this properties')


@app.route('/products/<product_category>')
def get_category(product_category):
    products = db.select(f"SELECT * FROM products WHERE category='{product_category}'")
    if products:
        return render_template("category.html", title=f'{product_category}', session=session, products=products)
    return render_template("error.html", error='there is no products from this category')


# @app.route('/find', methods=['get'])
# def finder():
#     result_products = []
#     find = request.form
#     print(find)
#     products = db.select("SELECT * FROM products")
#     brands = db.select("SELECT DISTINCT manufacturer from products")
#     colours = db.select("SELECT DISTINCT colour from products")
#     for product in products:
#         if find.lower() in product['name'].lower():
#             result_products.append(product)
#     if result_products:
#         return render_template("main_page.html", title=f'Find for {need_to_find}', session=session, colours=colours, brands=brands,
#                                products=result_products)
#     return render_template("error.html", error="we can't find it")
#     return True


@app.route('/make_order', methods=['get', 'post'])
def make_order():
    summa = request.values.to_dict(flat=False)['summa'][0]
    products_for_db = ','.join(session['cart'])
    db.insert(f"INSERT INTO orders VALUES('{products_for_db}', {summa}, '{session['mail']}')")
    session['cart'] = []
    if not session.modified:
        session.modified = True
    return session['cart']


@app.route('/show_orders')
def show_orders():
    orders = db.select(f"SELECT * FROM orders WHERE user_mail='{session['mail']}'")
    return render_template("orders.html", title='Orders', orders=orders)


@app.route('/get_admin', methods=['get', 'post'])
def get_admin():
    if request.method == 'POST':
        if request.form.get("admin") == 'admin':
            print(f"UPDATE users SET is_admin = 'y' where mail = '{session['mail']}'")
            db.insert(f"UPDATE users SET is_admin = 'y' where mail = '{session['mail']}'")
    return render_template("get_admin.html", title="ADMIN")


@app.route('/get_admin/create_product', methods=['get', 'post'])
def create_product():
    is_admin = db.select(f"SELECT is_admin FROM users WHERE mail='{session['mail']}'")
    if is_admin['is_admin'] != 'n':
        if request.method == 'POST':
            name = request.form.get("name")
            brand = request.form.get("brand")
            desc = request.form.get("desc")
            category = request.form.get("category")
            colour = request.form.get("colour")
            price = int(request.form.get("price"))
            status = request.form.get("status")
            photo = request.form.get("photo")
            db.insert(
                f"INSERT INTO products VALUES('{name}', '{brand}', '{desc}', '{category}', '{colour}', {price}, '{status}', '{photo}')")
        return render_template("create_product.html", title='Create product')
    else:
        return render_template("error.html", title="Error", error='you should be admin')


@app.route('/get_admin/delete_product', methods=['get', 'post'])
def delete_product():
    is_admin = db.select(f"SELECT is_admin FROM users WHERE mail='{session['mail']}'")
    if is_admin['is_admin'] != 'n':
        if request.method == 'POST':
            name_to_del = request.form.get("name_to_del")
            db.insert(f"DELETE FROM products WHERE name='{name_to_del}'")
            print(f"DELETE FROM products WHERE name='{name_to_del}'")
        return render_template("delete_product.html", title='Delete product')
    else:
        return render_template("error.html", title="Error", error='you should be admin')


if __name__ == '__main__':
    app.run(port=8000, debug=True)
