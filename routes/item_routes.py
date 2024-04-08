import os
from bottle import Bottle
from bottle import Bottle, template, route, request, get, post, put, delete
from sqlalchemy.orm import sessionmaker
from bottle import jinja2_template as template
import sqlite3 
import pandas as pd
from controllers import category_controller, item_controller
from models.models import Category, engine


# Create SQLAlchemy session
Session = sessionmaker(bind=engine)

item_app = Bottle()

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
        'store_id': request.forms.getunicode('store_id'),
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
    store_id = request.get_cookie('store_id')
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
                    'store_id': store_id,
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
                    'store_id': store_id,
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
                    'store_id': store_id,
                    'image': '',
                }
                item = item_controller.create_item(item_dict)
        return template('new_item', res="success")
    