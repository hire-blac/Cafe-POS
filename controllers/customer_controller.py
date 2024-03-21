from sqlalchemy.orm import sessionmaker
from models.models import Customer, Order, engine

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)

def all_customers():
    with Session() as session:
        customers = session.query(Customer).all()
        if customers:
            data = []
            for cat in customers:
                data.append({
                    'id': cat.id, 
                    'name': cat.name,
                    'phone': cat.phone
                })
            return {'customers': data}
        else:
            return {'message': 'no customers'}

def create_customer(data):
    customer = Customer(
        name=data['customer_name'],
        phone=data['customer_phone']
    )

    with Session() as session:
        session.add(customer)
        session.commit()    
        return {
            'id': customer.id, 
            'name': customer.name,
            'phone': customer.phone
        }


def get_customer(customer_id):
    with Session() as session:
        customer = session.query(Customer).get(customer_id)
        if customer:
            customer_orders = []
            orders = session.query(Order).filter_by(customer_name=customer.name).order_by(-Order.created_at).all()
            if orders:
                customer_orders = [{
                'id': order.id,
                'total_price': str(order.total_price),
                'tax': str(order.tax),
                'payment_status': order.payment_status,
                'status': order.status,
                'cashier_id': order.cashier_id,
                'order_type': order.order_type,
                'created_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S") ,
            } for order in orders]

            return {
                'id': customer.id, 
                'name': customer.name, 
                'phone': customer.phone,
                'orders': customer_orders
            }
        else:
            return {'message': 'customer not found'}


def update_customer(customer_id, data):
    with Session() as session:
        customer = session.query(Customer).get(customer_id)
        if customer:
            customer.name = data['name']
            customer.phone = data['phone']
            session.add(customer)
            session.commit()
        else:
            return {'message': 'customer not found'}
        

def delete_customer(customer_id):
    with Session() as session:
        customer = session.query(Customer).get(customer_id)
        if customer:
            session.delete(customer)
            session.commit()
            return f'customer with ID {customer_id} deleted successfully'
        else:
            return {'message': 'customer not found'}
        
