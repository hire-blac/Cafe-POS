from sqlalchemy.orm import sessionmaker
from controllers import transaction_controller
from models.models import Invoice, Transaction, engine
from sqlalchemy.exc import SQLAlchemyError

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)
        
def all_invoices():
    with Session() as session:
        try:
            invoices = session.query(Invoice).all()
            data = []
            for invoice in invoices:
                # get all transactions for each invoice
                purchase_items = [{
                    'id': transaction.id,
                    'item': transaction.item.name,
                    'item_price': str(transaction.item_price),
                    'quantity_sold': transaction.quantity_sold,
                    'subtotal': str(transaction.subtotal),
                } for transaction in invoice.purchase_items]

                # add invoice to data
                data.append({
                    'id': invoice.id,
                    'transactions': purchase_items,
                    'total_price': str(invoice.total_price),
                    'tax': str(invoice.tax),
                    'amount_paid': str(invoice.amount_paid),
                    'payment_method': str(invoice.payment_method),
                    # 'cashier_id': invoice.cashier_id,
                    'cashier_name': invoice.cashier_name,
                    # 'customer_PNO': invoice.customer_PNO,
                    'created_at': invoice.created_at.strftime("%Y-%m-%d %H:%M:%S") ,
                })

            return {'invoices': data, 'invoices_count': len(invoices)}
            
        except SQLAlchemyError as e:
            return {'message': str(e), 'invoices_count': 0}

def create_invoice(data):
    try:
        invoice = Invoice(
            total_price=data['total_price'],
            tax=data['tax'],
            amount_paid=data['amount_paid'],
            payment_method=data['payment_method'],
            # costumer_id=data['costumer_id'],
            costumer_PNO=data['costumer_PNO'],
            # cashier_id=data['cashier_id'],
            cashier_name=data['cashier_name']
        )

        with Session() as session:
            session.add(invoice)
            session.commit()
            
            inv_transactions = []
            # create transactions for this invoive
            for item in data['cart_items']:
                transaction = Transaction(
                    invoice_id=invoice.id,
                    item_id=item['item_id'],
                    item_price=item['item_price'],
                    quantity_sold=item['quantity_sold'],
                    subtotal=item['subtotal']
                )
                # save transaction
                session.add(transaction)
                session.commit()

                # add transaction to invoice
                inv_transactions.append({
                    'id': transaction.id,
                    'item': transaction.item.name,
                    'item_price': str(transaction.item_price),
                    'quantity': transaction.quantity_sold,
                    'subtotal': str(transaction.subtotal)
                })

            return {
                'id': invoice.id,
                'cart_items': inv_transactions,
                'total_price': str(invoice.total_price),
                'tax': str(invoice.tax),
                'amount_paid': str(invoice.amount_paid),
                'payment_method': str(invoice.payment_method),
                # 'costumer_PNO': invoice.costumer_PNO,
                # 'cashier_id': invoice.cashier_id,
                'cashier_name': invoice.cashier_name,
                'created_at': invoice.created_at.strftime("%Y-%m-%d %H:%M:%S") ,
            }
        
    except SQLAlchemyError as e:
        return {'message': e}


def get_invoice(invoice_id):
    with Session() as session:
        try:
            invoice = session.query(Invoice).get(invoice_id)
            # get all transactions for each invoice
            purchase_items = [{
                'id': transaction.id,
                'item': transaction.item.name,
                'item_price': str(transaction.item_price),
                'quantity_sold': transaction.quantity_sold,
                'subtotal': str(transaction.subtotal),
            } for transaction in invoice.purchase_items]

            return {
                'id': invoice.id,
                'transactions': purchase_items,
                'total_price': str(invoice.total_price),
                'tax': str(invoice.tax),
                'amount_paid': str(invoice.amount_paid),
                'payment_method': str(invoice.payment_method),
                # 'cashier_id': invoice.cashier_id,
                'cashier_name': invoice.cashier_name,
                'created_at': invoice.created_at.strftime("%Y-%m-%d %H:%M:%S") ,
            }

        except SQLAlchemyError as e:
            return {'message': str(e)}
        

def update_invoice(data, invoice_id):
    with Session() as session:
        try:
            invoice = session.query(Invoice).get(invoice_id)
            # edit invoice
        except SQLAlchemyError as e:
            return {'message': str(e)}
        

def delete_invoice(invoice_id):
    with Session() as session:
        try:
            invoice = session.query(Invoice).get(invoice_id)
            session.delete(invoice)
            session.commit()
            return f'Invoice with ID {invoice_id} deleted successfully'
        
        except SQLAlchemyError as e:
            return {'message': str(e)}
        
