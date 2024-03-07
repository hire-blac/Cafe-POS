from sqlalchemy.orm import sessionmaker
from models.models import Item, engine

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)


def create_item(data):
    try:
        item = Item(
            name=data['name'],
            price=data['price'],
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
            return {
                'id': item.id, 
                'name': item.name,
                'price': str(item.price),
                'quantity': item.quantity,
                'category': item.category.name,
                }
        else:
            return {'message': 'Item not found'}
