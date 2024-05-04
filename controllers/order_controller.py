from sqlalchemy.orm import sessionmaker
from controllers import customer_controller, delivery_controller, item_controller
from controllers import invoice_controller
from models.models import Order, OrderedItem, engine
from sqlalchemy.exc import SQLAlchemyError
import random
from . ordered_items_controller import ordered_item_details

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)
        
def all_orders(store_id):
    if not store_id:
        return {'message': 'no orders', 'orders_count': 0}
    
    with Session() as session:
        orders = session.query(Order).order_by(Order.created_at.desc()).filter_by(store_id=store_id).all()
        if orders:
            data = []
            for order in orders:
                # get all ordered_items for each order
                ordered_items = [ordered_item_details(ordered_item) for ordered_item in order.ordered_items]

                # add order to data
                data.append({
                    'id': order.id,
                    'ordered_items': ordered_items,
                    'customer_name': order.customer_name,
                    'customer_phone': order.customer_phone,
                    'order_type': order.order_type,
                    'total_price': str(order.total_price),
                    'tax': str(order.tax),
                    'payment_status': order.payment_status,
                    'cashier_id': order.cashier_id,
                    'status': order.status,
                    'created_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S") ,
                })

            return {'orders': data, 'orders_count': len(orders)}
            
        else:
            return {'message': "no orders found", 'orders_count': 0}


def create_order(data):
    order = Order(
        id=data['id'],
        total_price=data['total_price'],
        tax=data['tax'],
        customer_name=data['customer_name'],
        customer_phone=data['customer_phone'],
        order_type=data['order_type'],
        payment_status=data['payment_status'],
        status=data['status'],
        cashier_id=data['cashier_id'],
        store_id=data['store_id'],
    )

    with Session() as session:
        session.add(order)
        session.commit()
        
        ordered_items = []
        # create ordered_items for this invoive
        for item in data['cart_items']:
            item['quantity_sold'] = item['quantity_ordered']
            min = 1111
            max = 999999999
            ordered_item_id = random.randrange(min, max)
            ordered_item = OrderedItem(
                id=ordered_item_id,
                order_id=order.id,
                item_id=item['item_id'],
                item_name=item['item_name'],
                item_price=item['item_price'],
                quantity_ordered=item['quantity_ordered'],
                subtotal=item['subtotal']
            )
            # save ordered_item
            session.add(ordered_item)
            session.commit()

            # add ordered_item to order
            ordered_items.append(ordered_item_details(ordered_item))
        
        # create customer
        customer = customer_controller.create_customer(data)
        
        # create an invoice if the order is paid
        if order.payment_status == 'Paid':
            data['order_id'] = order.id
            invoice = invoice_controller.create_invoice(data)
        
        # create delivery if order type is delivery
        if order.order_type == 'Delivery':
            data['order_id'] = order.id
            delivery = delivery_controller.create_delivery(data)

        return {
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
        


def get_order(order_id):
    with Session() as session:
        order = session.get(Order, order_id)
        if order:
            # get all ordered_items for each order
            ordered_items = [ordered_item_details(ordered_item) for ordered_item in order.ordered_items]

            return {
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

        else:
            return {'message': "order not found"}
        

def update_order(data, order_id):
    with Session() as session:
        order = session.get(Order, order_id)
        if order:
            # edit order
            pass
        else:
            return {'message': "order not found"}
        

def delete_order(order_id):
    with Session() as session:
        order = session.get(Order, order_id)
        if order:
            session.delete(order)
            session.commit()
            return f'order with ID {order_id} deleted successfully'
        
        else:
            return {'message': "order not found"}
        
