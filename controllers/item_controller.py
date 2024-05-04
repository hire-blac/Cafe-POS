from sqlalchemy.orm import sessionmaker
from models.models import Category, Item, engine
from . transaction_controller import transaction_details

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)

def item_details(item):
    cat = '-'
    if item.category:
        cat = item.category.name
    return {
        'message': "success",
        'id': item.id, 
        'name': item.name,
        'price': str(item.price),
        'image': item.image_url,
        'quantity': item.quantity,
        'category': cat
    }


def create_item(data):
    # try:
    item = Item(
        id=data['id'],
        name=data['name'],
        price=data['price'],
        image_url=data['image'],
        quantity=data['quantity'],
        category_id=data['category_id'],
        store_id=data['store_id'],
    )

    with Session() as session:
        session.add(item)            
        session.commit()
        return item_details(item)
    # except:
    #     return {'message': "error"}


def all_items(store_id):
    if not store_id:
        return {
            'message': "No items found",
            'items_count': 0
        }
        
    with Session() as session:
        items = session.query(Item).filter_by(store_id=store_id).all()
        if items:
            data = []
            for item in items:
                data.append(item_details(item))
                
            return {
                'items': data,
                'items_count': len(items)
            }
        else:
            return {
                'message': "No items found",
                'items_count': len(items)
            }


def get_item(item_id):
    with Session() as session:
        item = session.get(Item, item_id)
        if item:
            transactions = [transaction_details(trans) for trans in item.transactions]
            
            item = item_details(item)
            item['transactions'] = transactions

            return item
        else:
            return {'message': 'Item not found'}


def update_item(item_id, data):
    with Session() as session:
        item = session.get(Item, item_id)
        if item:
            category = session.query(Category).filter_by(name=data['category']).first()
            item.name = data['name']
            item.price = data['price']
            item.quantity = data['quantity']
            item.category_id = category.id
            session.add(item)
            session.commit()

            return item_details(item)
        else:
            return {'message': 'Item not found'}

def reduce_quantity(item_id, quantity):
    with Session() as session:
        item = session.get(Item, item_id)
        if item:
            item.quantity -= quantity
            session.add(item)
            session.commit()
            return  {"message": f"item quantity with id {item_id} reduced by {quantity}"}
        else:
            return {'error': 'Item not found'}

def delete_item(item_id):
    with Session() as session:
        item = session.get(Item, item_id)
        if item:
            session.delete(item)            
            session.commit()
            return {
                'message':  f'Item with id {item_id} deleted'
            }
        else:
            return {'message': 'Item not found'}

