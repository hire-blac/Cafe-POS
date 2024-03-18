from sqlalchemy.orm import sessionmaker
from models.models import Transaction, engine

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)

def transaction_details(transaction):
    item = transaction.item_name
    if transaction.item:
        item = transaction.item.name

    return {
    'id': transaction.id,
    'invoice_id': transaction.invoice_id,
    'item_id': transaction.item_id,
    'item': item,
    'item_price': str(transaction.item_price),
    'quantity_sold': transaction.quantity_sold,
    'subtotal': str(transaction.subtotal),
    'created_at': transaction.created_at.strftime("%Y-%m-%d %H:%M:%S"),
}


def all_transactions():
    with Session() as session:
        transactions = session.query(Transaction).all()
        data = []
        if transactions:
            for transaction in transactions:
                data.append(transaction_details(transaction))
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
            return transaction_details(transaction)
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
        
