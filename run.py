from sqlalchemy.orm import sessionmaker
from bottle import Bottle, request
from bottle import Bottle, template, route, run, static_file, request, get, post, put, delete, redirect, TEMPLATES, TEMPLATE_PATH
from bottle import jinja2_template as template
import os
import sqlite3 
import pandas as pd
from controllers import auth_controller, category_controller, customer_controller, delivery_controller, invoice_controller, item_controller, order_controller, store_controller, transaction_controller
import posauth
from models.models import Category, engine

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)

TEMPLATE_PATH.append('./views')

app = Bottle()


@route("/")
def home():
    #return "Home"
    items_count = item_controller.all_items()['items_count']
    transaction_count = transaction_controller.all_transactions()['transaction_count']
    invoices_count = invoice_controller.all_invoices()['invoices_count']
    orders_count = order_controller.all_orders()['orders_count']
    deliveries_count = delivery_controller.all_deliveries()['deliveries_count']
    return template(
        'index', 
        items_count=items_count, 
        transaction_count=transaction_count, 
        invoices_count=invoices_count, 
        orders_count=orders_count,
        deliveries_count=deliveries_count,
    )


@route("/super")
def home():
    store_count = store_controller.all_stores()['store_count']
    admin_count = auth_controller.all_admins()['admin_count']
    return template(
        'super_user_index', 
        store_count=store_count, 
        admin_count=admin_count
    )


# CATEGORY ROUTES
# get all categories
@get("/category_api")
def category_api():
    categories = category_controller.all_categories()
    return categories

@route('/categories')
def categories():
    return template("categories")

@get("/api/categories")
def categories():
    categories = category_controller.all_categories()
    return categories

@get("/api/delete_category/<id>")
def categories(id):
    categories = category_controller.delete(id)
    return categories

# add new category from api
@post("/api/categories")
def new_categories():
    data =  request.json
    category = category_controller.create_category(data)
    return category

# ITEM ROUTES
# get all items
@get("/items")
def items():
    items = item_controller.all_items()
    return template("items", rows=items.items)

@get("/api/items")
def items():
    items = item_controller.all_items()
    return items

# add new item from api
@post("/api/items")
def new_items():
    data =  request.json
    # Handle file upload
    image_upload = request.files.get('image')
    if image_upload:
        image_filename = f"static/images/{data['name']}_{image_upload.filename}"
        image_upload.save(image_filename)
        data['image'] = image_filename
    else:
        data['image'] = ''
    item = item_controller.create_item(data)
    return item

# render new item page
@get("/new_item")
def new_item():
    return template('new_item')

# add new item from page form
@post("/new_item")
def new_item():
    form_data = {
        'id': request.forms.getunicode('id'),
        'name': request.forms.getunicode('name'),
        'category_id': request.forms.getunicode('category'),
        'price': request.forms.getunicode('price'),
        'quantity': request.forms.getunicode('quantity'),
        'newcategory': request.forms.getunicode('newcategory'),
        'image': ''
    }

    # Handle file upload
    image_upload = request.files.get('image')
    if image_upload:
        image_filename = f"static/images/{form_data['name']}_{image_upload.filename}"
        image_upload.save(image_filename)
        form_data['image'] = image_filename

    if(form_data['category_id'] == "New Category"):
        new_cat = {'name': form_data['newcategory']}
        new_category = category_controller.create_category(new_cat)
        form_data['category_id'] = new_category['id']
    item = item_controller.create_item(form_data)
    return template('new_item', res=item['message'])


@route("/item/<id_code>")
def get_item(id_code):
    item = item_controller.get_item(id_code)
    return template('get_item', item=item)

@get("/api/items/<id_code>")
def get_item(id_code):
    item = item_controller.get_item(id_code)
    return item

@put("/api/items/<id_code>/update")
def update_item(id_code):
    data = request.json
    item = item_controller.update_item(id_code, data)
    return item

@delete("/api/items/<id_code>/delete")
def delete_item(id_code):
    item = item_controller.delete_item(id_code)
    return item

# upload items from file
@route('/upload_item', method='POST')
def do_upload():
    upload = request.files.get('itemsfile') #request.POST['itemfile']
    name, ext = os.path.splitext(upload.filename)
    #print("Name: {}, Ext: {}".format(name, ext))
    #print("{}".format(upload.file))
    if ext not in ('.xlsx', '.csv', '.db'):
        #return "File extension not allowed."
        return template('new_item', res="error")

    if ext == ".csv":
        fname = name + '.csv'
        df = pd.read_csv(upload.file)
        print("DataFrame: {}".format(df))
        for index,item in df.iterrows():
            item_code =item['Item ID']
            name = item['Item Name']
            category = item['Category']
            price = item['Price']
            quantity = item['Quantity']

            if name != None or price != None or quantity != None:
                category_id = ''
                if category and isinstance(category, str):
                    with Session() as session:
                        cat = session.query(Category).filter_by(name=category).first()
                        if cat:
                            category_id = cat.id
                        else:
                            cat = category_controller.create_category({'name': category})
                            category_id = cat.id

                item_dict = {
                    'id': item_code,
                    'name': name,
                    'price': price,
                    'quantity': quantity,
                    'category_id': category_id,
                    'image': '',
                }
                item = item_controller.create_item(item_dict)
                # POS.add_item(item_idcode=item_code, item_name=name, item_category=category, item_price=price, quantity=quantity)
        return template('new_item', res="success")

    if ext == ".xlsx":
        df = pd.read_excel(upload.file)
        for index,item in df.iterrows():
            item_code = item['Item ID']
            name = item['Item Name']
            category = item['Category']
            price = item['Price']
            quantity = item['Qty']

            if name != None or price != None or quantity != None:
                category_id = ''
                if category and isinstance(category, str):
                    with Session() as session:
                        cat = session.query(Category).filter_by(name=category).first()
                        if cat:
                            category_id = cat.id
                        else:
                            cat = category_controller.create_category({'name': category})
                            category_id = cat['id']
                    
                item_dict = {
                    'id': item_code,
                    'name': name,
                    'price': price,
                    'quantity': quantity,
                    'category_id': category_id,
                    'image': '',
                }
                item = item_controller.create_item(item_dict)
                # POS.add_item(item_idcode=item_code, item_name=name, item_category=category, item_price=price, quantity=quantity)
        return template('new_item', res="success")

    if ext == ".db":
        try:
            conn = sqlite3.connect(upload.file)    
        except Exception as e:
            print(e)
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Items")
        all_items = cursor.fetchall()
        for ait in all_items:
            item_code = ait['idcode']
            name = ait['Name']
            category = ait['Category']
            price = ait['Price']
            quantity = ait['Qty']
            
            if name != None  or price != None or quantity != None:
                category_id = ''
                if category and isinstance(category, str):
                    with Session() as session:
                        cat = session.query(Category).filter_by(name=category).first()
                        if cat:
                            category_id = cat.id
                        else:
                            cat = category_controller.create_category({'name': category})
                            category_id = cat.id
                    
                item_dict = {
                    'id': item_code,
                    'name': name,
                    'price': price,
                    'quantity': quantity,
                    'category_id': category_id,
                    'image': '',
                }
                item = item_controller.create_item(item_dict)
        return template('new_item', res="success")
    

# ORDER ROUTES
@get("/new-order")
def new_order():
    return template( "new_order" )

@get("/orders")
def get_all_order():
    return template( "orders" )

@get("/orders/<order_id>")
def get_order(order_id):
    return template( "order" )

@get("/api/orders")
def all_order():
    orders = order_controller.all_orders()
    return orders

@post("/api/orders")
def create_order():
    data = request.json
    order = order_controller.create_order(data)
    return order

@get("/api/orders/<order_id>")
def single_order(order_id):
    order = order_controller.get_order(order_id)
    return order


# DELIVERY ROUTES
@get("/deliveries")
def get_all_deliveries():
    return template( "deliveries" )

@get("/deliveries/<delivery_id>")
def get_order(delivery_id):
    return template( "delivery" )

@get("/api/deliveries")
def all_order():
    deliveries = delivery_controller.all_deliveries()
    return deliveries

@get("/api/deliveries/<delivery_id>")
def single_delivery(delivery_id):
    delivery = delivery_controller.get_Delivery(delivery_id)
    return delivery


# TRANSACTION ROUTES
@get("/transactions")
def get_transactions():
    transactions = transaction_controller.all_transactions()
    return template("transactions", transactions=transactions)

@get('/api/transactions')
def transactions():
    transactions = transaction_controller.all_transactions()
    return transactions

@get('/api/transactions/<transaction_id>')
def transactions(transaction_id):
    transaction = transaction_controller.get_transaction(transaction_id)
    return transaction


# INVOICE ROUTES
@route("/invoices")
def invoices():
    return template('invoices')

@get('/api/invoices')
def all_invoices():
    invoices = invoice_controller.all_invoices()
    return invoices

@route("/cart")
def new_cart():
    return template('cart')

@post('/api/invoices')
def new_invoice():
    data = request.json
    invoice = invoice_controller.create_invoice(data)
    return invoice

@route('/invoice/<invoice_id>')
def invoice(invoice_id):
    invoice = invoice_controller.get_invoice(invoice_id)
    return template("invoice", invoice=invoice)

@get('/api/invoices/<invoice_id>')
def get_invoice(invoice_id):
    invoice = invoice_controller.get_invoice(invoice_id)
    return invoice

@put("/api/invoices/<invoice_id>")
def update_invoice(invoice_id):
    data = request.json
    invoice  = invoice_controller.update_invoice(invoice_id, data)
    return invoice,  200

@delete("/api/invoices/<invoice_id>")
def delete_invoice(invoice_id):
    res = invoice_controller.delete_invoice(invoice_id)
    return res
    

# USER ROUTES
@get("/login")
def login():
    return template("login")

@post("/login")
def login_post():
    data = request.json
    auth_user = auth_controller.login_user(data)
    print(auth_user)
    return auth_user

@get("/register")
def register():
    return template("register")


@post("/register")
def register_post():
    data = request.json
    print(data)
    user = auth_controller.register_user(data)
    return user


@route("/add_user")
def create_user():
    return template('add_user')

@route("/add_admin")
def create_admin():
    return template('add_admin')

@route("/admin-users")
def manage_admin_users():
    if posauth.isSuper(request):
        users = auth_controller.all_admins()
        return template("manage_admin_user", rows=users)
    return {'error': "Unauthorized"}


@route("/manage_user")
def manage_usesr():
    # print([{k: v} for k, v in request.headers.items()])
    if posauth.isAdmin(request):
        users = auth_controller.all_users()
        return template("manage_user", rows=users)
    return {'error': "Unauthorized"}


@get('/api/admin-users')
def getUsers():
    users = auth_controller.all_admins()
    return users

@get('/api/users')
def getUsers():
    users = auth_controller.all_users()
    return users

@get("/api/user/<username>")
def get_user(username):
    # get user info
    user= auth_controller.get_user(username)
    return user

@get("/user/<username>")
def get_user(username):
    # get user info
    return template('get_user')

@put('/api/user/<user_id>/update')
def updateUsers(user_id):
    data = request.json
    users = auth_controller.update_user(data, user_id)
    return users

@route("/user_profile")
def user_profile():
    if posauth.Auth(request):
        username = request.get_cookie('user_name')
        user= auth_controller.get_user(username)
        return template('user_profile', user=user)
    else:
        return {"error": "Please login"}

@route("/api/user_profile")
def user_profile_api():
    if posauth.Auth(request):
        username = request.get_cookie('user_name')
        user= auth_controller.get_user(username)
        return user
    else: 
        return {"error": "Please login"}

@post("/user-profile/change-password")
def change_password():
    data = request.json
    if posauth.Auth(request):
        username = request.get_cookie('user_name')
        user = auth_controller.change_password(username, data)
        return user
    else:
        return {"error": "Please login"}
    
@delete('/api/user/<user_id>/delete')
def deleteUser(user_id):
    users = auth_controller.delete_user(user_id)
    return users


# CUSTOMER ROUTES
@get("/manage_customers")
def manage_customers():
    return template( "customers" )

@get("/customers/<customer_id>")
def get_customer(customer_id):
    return template( "get_customer" )

@get("/api/customers")
def all_customers():
    customers = customer_controller.all_customers()
    return customers

@post("/api/customers")
def add_customer():
    data = request.json
    customer = customer_controller.create_customer(data)
    return customer

@get("/api/customers/<customer_id>")
def single_customer(customer_id):
    customer = customer_controller.get_customer(customer_id)
    return customer

@put("/api/customers/<customer_id>/update")
def single_customer(customer_id):
    data = request.json
    customer = customer_controller.update_customer(customer_id, data)
    return customer

@get("/api/customers/<customer_id>/delete")
def single_customer(customer_id):
    customer = customer_controller.delete_customer(customer_id)
    return customer


# COMPANY ROUTES
@get("/my-store")
def get_company():
    return template("get_store")

@get("/api/company/<company_id>")
def get_company(company_id):
    company = store_controller.get_company(company_id)
    return company

@get("/store/new-store")
def new_company():
    return template("new_store")

@post("/store/new-store")
def create_store():
    data = {
        'company_name': request.forms.getunicode('companyName'),
        'cr_number': request.forms.getunicode('crNumber'),
        'tax_number': request.forms.getunicode('taxNumber'),
        'shop_name': request.forms.getunicode('shopName'),
        'unit_number': request.forms.getunicode('unitNumber'),
        'district': request.forms.getunicode('district'),
        'city': request.forms.getunicode('city'),
        'street': request.forms.getunicode('street'),
        'zip_code': request.forms.getunicode('zipCode'),
        'phone_number': request.forms.getunicode('phoneNumber'),
        'email': request.forms.getunicode('email'),
        'website': request.forms.getunicode('website'),
        'logo': '',
    }
    store = store_controller.create_store(data)
    return template("company", res_company_id=store['id'])

@post("/api/store")
def create_store():
    data = request.json
    data['logo'] = ''
    store = store_controller.create_store(data)
    return store

@put("/api/company/<company_id>/update")
def update_company(company_id):
    data = request.json
    company = store_controller.update_company(company_id, data)
    return company

# STORE ROUTES
@get('/stores')
def stores():
    return template( "stores" )

@get('/api/stores')
def stores():
    return store_controller.all_stores()

@get('/stores/<store_id>')
def get_store(store_id):
    return template("get_store")

@get('/api/stores/<store_id>')
def get_store(store_id):
    store = store_controller.get_store(store_id)
    return store

@put('/api/stores/<store_id>/update')
def get_store(store_id):
    data = request.json
    store = store_controller.update_store(store_id, data)
    return store

@delete('/api/stores/<store_id>/delete')
def get_store(store_id):
    store = store_controller.delete_store(store_id)
    return store


@route('/test')
def test():
    return template("test")

@route('/<filename>.css')
def stylesheets(filename):
    return static_file('{}.css'.format(filename), root='static')

@route('/<filename>.png')
def stylesheets(filename):
    return static_file('{}.png'.format(filename), root='static')


TEMPLATES.clear()
#print("OS Env: {} Port: {}".format(os.environ.get('DYNO'), os.environ.get("PORT")))
#if os.environ.get('DYNO') != None:
#pass#run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
#elif os.environ.get('DYNO') == None:
run(host='127.0.0.1', port=8080, debug=True, reloader=True)