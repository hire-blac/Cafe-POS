from bottle import Bottle, request
from bottle import Bottle, template, route, run, static_file, request, get, post, put, delete, redirect, TEMPLATES
from bottle import jinja2_template as template
import POS
import os
from controllers import category_controller, invoice_controller, item_controller, transaction_controller
import posauth
# Import Bottle Extensions

import sqlite3 
import pandas as pd

app = Bottle()


@route("/")
def home():
    #return "Home"
    items_count = item_controller.all_items()['items_count']
    transaction_count = transaction_controller.all_transactions()['transaction_count']
    invoices_count = invoice_controller.all_invoices()['invoices_count']
    return template('index', items_count=items_count, transaction_count=transaction_count, invoices_count=invoices_count)


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
    item = item_controller.create_item(data)
    return item

# render new item page
@get("/new_item")
def new_item():
    return template('new_item')


@route("/item/<id_code>")
def get_item(id_code):
    item = item_controller.get_item(id_code)
    return template('get_item', item=item)

@get("/api/items/<id_code>")
def get_item(id_code):
    item = item_controller.get_item(id_code)
    return item

# add new item from page form
@post("/new_item")
def new_item():
    form_data = {
        'name': request.forms.get('name'),
        'category_id': request.forms.get('category'),
        'price': request.forms.get('price'),
        'quantity': request.forms.get('quantity'),
        'newcategory': request.forms.get('newcategory'),
    }
    print(form_data)
    if(form_data['category_id'] == "New Category"):
        new_category = category_controller.create_category(form_data)
        form_data['category_id'] = new_category['id']

    item = item_controller.create_item(form_data)
    return template('new_item', res="success")

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
            item_code =item['Id']
            name = item['Name']
            category = item['Category']
            price = item['Price']
            quantity = item['Quantity']
            if name != None or category != None or price != None or quantity != None:
                POS.add_item(item_idcode=item_code, item_name=name, item_category=category, item_price=price, quantity=quantity)
        return template('new_item', res="success")

    if ext == ".xlsx":
        df = pd.read_excel(upload.file)
        for index,item in df.iterrows():
            item_code = item['Id']
            name = item['Name']
            category = item['Category']
            price = item['Price']
            quantity = item['Quantity']
            if name != None or category != None or price != None or quantity != None:
                POS.add_item(item_idcode=item_code, item_name=name, item_category=category, item_price=price, quantity=quantity)
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
            if name != None or category != None or price != None or quantity != None:
                POS.add_item(item_idcode=item_code, item_name=name, item_category=category, item_price=price, quantity=quantity)
        return template('new_item', res="success")

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

@route("/new_cart")
def new_cart():
    return template('new_cart')

@post('/api/invoices')
def new_invoice():
    data = request.json
    data['cashier_name'] = "Jimmy"
    invoice = invoice_controller.create_invoice(data)
    return invoice, 201

@route('/invoice/<invoice_id>')
def invoice(invoice_id):
    invoice = invoice_controller.get_invoice(invoice_id)
    return template("invoice", invoice=invoice)

@get('/api/invoices/<invoice_id>')
def get_invoice(invoice_id):
    invoice = invoice_controller.get_invoice(invoice_id)
    return invoice, 200

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

@get("/register")
def register():
    return template("register")

@post("/pregister")
def pregister():
    username = request.forms.get("username")
    password = request.forms.get("password")
    name = request.forms.get("name")
    cashierId = request.forms.get("cashierId")
    usertype = request.forms.get("userType")
    redirect("/manage_user")

@route("/add_user")
def cart():
    return template('add_user')

@route("/manage_user")
def manage_usesr():
    
    return template("manage_user", rows=items)


@route("/user/<username>")
def get_user(username):
    # get user info
    user= ''
    return template('get_user', items=user)

@route("/user_profile")
def user_profile():
    return template('user_profile')


# CUSTOMER ROUTES



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