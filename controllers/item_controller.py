from sqlalchemy.orm import sessionmaker
from models.models import Category, Item, engine

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)


def create_item(data):
    print(data)
    try:
        item = Item(
            name=data['name'],
            price=data['price'],
            image_url=data['image'],
            quantity=data['quantity'],
            category_id=data['category_id'],
        )

        with Session() as session:
            session.add(item)            
            session.commit()    
            return {
                'id': item.id, 
                'name': item.name,
                'price': str(item.price),
                'image': item.image_url,
                'quantity': item.quantity,
                'category': item.category.name,
            }
    except:
        return {'message': "an error occured"}


def all_items():
    with Session() as session:
        items = session.query(Item).all()
        if items:
            data = []
            for item in items:
                data.append({
                    'id': item.id, 
                    'name': item.name,
                    'price': str(item.price),
                    'image': item.image_url,
                    'quantity': item.quantity,
                    'category': item.category.name,
                })

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
        item = session.query(Item).get(item_id)
        if item:
            transactions = [{
                'id': trans.id,
                'item_id': trans.item_id,
                'item_price': str(trans.item_price),
                'quantity_sold': trans.quantity_sold,
                'created_at': trans.created_at.strftime("%Y-%m-%d %H:%M:%S")
            } for trans in item.transactions]

            return {
                'id': item.id, 
                'name': item.name,
                'price': str(item.price),
                'image': item.image_url,
                'quantity': item.quantity,
                'category': item.category.name,
                'transactions': transactions,
            }
        else:
            return {'message': 'Item not found'}


def update_item(item_id, data):
    with Session() as session:
        item = session.query(Item).get(item_id)
        if item:
            category = session.query(Category).filter_by(name=data['category']).first()
            item.name = data['name']
            item.price = data['price']
            item.quantity = data['quantity']
            item.category_id = category.id
            session.add(item)
            session.commit()

            return {
                'id': item.id, 
                'name': item.name,
                'price': str(item.price),
                'image': item.image_url,
                'quantity': item.quantity,
                'category': item.category.name,
                }
        else:
            return {'message': 'Item not found'}

def reduce_quantity(item_id, quantity):
    with Session() as session:
        item = session.query(Item).get(item_id)
        if item:
            item.quantity -= quantity
            session.add(item)
            session.commit()
            return  {"message": f"item quantity with id {item_id} reduced by {quantity}"}
        else:
            return {'error': 'Item not found'}

def delete_item(item_id):
    with Session() as session:
        item = session.query(Item).get(item_id)
        if item:
            session.delete(item)            
            session.commit()
            return {
                'message':  f'Item with id {item_id} deleted'
            }
        else:
            return {'message': 'Item not found'}

