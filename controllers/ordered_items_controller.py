from sqlalchemy.orm import sessionmaker
from models.models import OrderedItem, engine

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)

def ordered_item_details(ordered_item):
    item = ordered_item.item_name
    if ordered_item.item:
        item = ordered_item.item.name

    return {
    'id': ordered_item.id,
    'order_id': ordered_item.order_id,
    'item_id': ordered_item.item_id,
    'item': item,
    'item_price': str(ordered_item.item_price),
    'quantity_ordered': ordered_item.quantity_ordered,
    'subtotal': str(ordered_item.subtotal),
    'created_at': ordered_item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
}


def all_ordered_items(store_id):
    with Session() as session:
        ordered_items = session.query(OrderedItem).filter_by(store_id=store_id).order_by(OrderedItem.created_at.desc()).all()
        data = []
        if ordered_items:
            for ordered_item in ordered_items:
                data.append(ordered_item_details(ordered_item))
            return {
                'ordered_items': data,
                'ordered_item_count': len(ordered_items)
            }
        else:
            return {
                'message': 'no ordered_items',
                'ordered_item_count': 0
            }
        

def get_ordered_item(ordered_item_id):
    with Session() as session:
        ordered_item = session.get(OrderedItem, ordered_item_id)
        if ordered_item:
            return ordered_item_details(ordered_item)
        else:
            return {'message': 'ordered_item not found'}


def update_ordered_item(data, ordered_item_id):
    with Session() as session:
        ordered_item = session.get(OrderedItem, ordered_item_id)
        if ordered_item:
            pass
        else:
            return {'message': 'ordered_item not found'}
        

def delete_ordered_item(ordered_item_id):
    with Session() as session:
        ordered_item = session.get(OrderedItem, ordered_item_id)
        if ordered_item:
            session.delete(ordered_item)
            session.commit()
            return {'message': f'ordered_item with ID {ordered_item_id} deleted successfully'}
        else:
            return {'message': 'ordered_item not found'}
        
