from sqlalchemy.orm import sessionmaker
from controllers.ordered_items_controller import ordered_item_details
from models.models import Delivery, engine

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)


def create_delivery(data):
    # try:
    delivery = Delivery(
        id=data['id'],
        order_id=data['order_id'],
        customer_name=data['customer_name'],
        customer_phone=data['customer_phone'],
        delivery_address=data['delivery_address'],
    )

    with Session() as session:
        session.add(delivery)            
        session.commit()
        
        return {
            'id': delivery.id,
            'order_id': delivery.order_id,
            'customer_name': delivery.customer_name,
            'customer_phone': delivery.customer_phone,
            'delivery_address': delivery.delivery_address,
            'status': delivery.status,
            'created_at': delivery.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    # except:
    #     return {'message': "error"}


def all_deliveries():
    with Session() as session:
        deliveries = session.query(Delivery).all()
        if deliveries:
            data = []
            for delivery in deliveries:
                data.append({
                    'id': delivery.id,
                    'order_id': delivery.order_id,
                    'customer_name': delivery.customer_name,
                    'customer_phone': delivery.customer_phone,
                    'delivery_address': delivery.delivery_address,
                    'status': delivery.status,
                    'created_at': delivery.created_at.strftime("%Y-%m-%d %H:%M:%S")
                })
                
            return {
                'deliveries': data,
                'deliveries_count': len(deliveries)
            }
        else:
            return {
                'message': "No deliverys found",
                'deliveries_count': len(deliveries)
            }


def get_Delivery(delivery_id):
    with Session() as session:
        delivery = session.query(Delivery).get(delivery_id)
        if delivery:
            order = delivery.order
            # get all ordered_items for each order
            ordered_items = [ordered_item_details(ordered_item) for ordered_item in order.ordered_items]
            order_details = {
                'id': order.id,
                'ordered_items': ordered_items,
                'total_price': str(order.total_price),
                'tax': str(order.tax),
                'customer_name': order.customer_name,
                'customer_phone': order.customer_phone,
                'payment_status': order.payment_status,
                'status': order.status,
                'cashier_id': order.cashier_id,
                'order_type': order.order_type,
                'created_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S") ,
            }

            return {
                'id': delivery.id,
                'order': order_details,
                'customer_name': delivery.customer_name,
                'customer_phone': delivery.customer_phone,
                'delivery_address': delivery.delivery_address,
                'status': delivery.status,
                'created_at': delivery.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }

        else:
            return {'message': 'delivery not found'}


def update_Delivery(delivery_id, data):
    with Session() as session:
        delivery = session.query(Delivery).get(delivery_id)
        if delivery:
            delivery.customer_name=data['customer_name'],
            delivery.customer_phone=data['customer_phone'],
            delivery.delivery_address=data['delivery_address']
            delivery.status=data['delivery_statusaddress']

            session.add(delivery)
            session.commit()

            return {
                'id': delivery.id,
                'order_id': delivery.order_id,
                'customer_name': delivery.customer_name,
                'customer_phone': delivery.customer_phone,
                'delivery_address': delivery.delivery_address,
                'status': delivery.status,
                'created_at': delivery.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return {'message': 'delivery not found'}
        

def delete_Delivery(delivery_id):
    with Session() as session:
        delivery = session.query(Delivery).get(delivery_id)
        if delivery:
            session.delete(delivery)            
            session.commit()
            return {
                'message':  f'delivery with id {delivery_id} deleted'
            }
        else:
            return {'message': 'delivery not found'}

