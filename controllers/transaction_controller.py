from sqlalchemy.orm import sessionmaker
from models.models import Transaction, engine

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)
        
def all_transactions():
    with Session() as session:
        transactions = session.query(Transaction).all()
        data = []
        if transactions:
            for transaction in transactions:
                data.append({
                    'id': transaction.id,
                    'invoice_id': transaction.invoice_id,
                    'item_id': transaction.item_id,
                    'item': transaction.item.name,
                    'item_price': str(transaction.item_price),
                    'quantity_sold': transaction.quantity_sold,
                    'subtotal': str(transaction.subtotal),
                    'created_at': transaction.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                })
            return {
                'transactions': data,
                'transaction_count': len(transactions)
            }
        else:
            return {
                'message': 'no transactions',
                'transaction_count': 0
            }
        

def get_transaction(transaction_id):
    with Session() as session:
        transaction = session.query(Transaction).get(transaction_id)
        if transaction:
            return {
            'id': transaction.id,
            'invoice_id': transaction.invoice_id,
            'item_id': transaction.item_id,
            'item': transaction.item.name,
            'item_price': str(transaction.item_price),
            'quantity_sold': transaction.quantity_sold,
            'subtotal': str(transaction.subtotal),
            'created_at': transaction.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        else:
            return {'message': 'transaction not found'}


def update_transaction(data, transaction_id):
    with Session() as session:
        transaction = session.query(Transaction).get(transaction_id)
        if transaction:
            pass
        else:
            return {'message': 'transaction not found'}
        

def delete_transaction(transaction_id):
    with Session() as session:
        transaction = session.query(Transaction).get(transaction_id)
        if transaction:
            session.delete(transaction)
            session.commit()
            return {'message': f'transaction with ID {transaction_id} deleted successfully'}
        else:
            return {'message': 'transaction not found'}
        
