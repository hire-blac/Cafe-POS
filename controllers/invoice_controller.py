from sqlalchemy.orm import sessionmaker
from utils.InvoiceQR import InvoiceToQR
from controllers import item_controller
from models.models import Invoice, Transaction, engine
import random
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml

from utils.invoice_json import generate_json
from utils.uuid_gen import uuid_gen
from . transaction_controller import transaction_details

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)
        
def all_invoices(store_id):
    print('store id: ', store_id)
    with Session() as session:
        invoices = session.query(Invoice).order_by(Invoice.created_at.desc()).filter_by(store_id=store_id).all()
        if invoices:
            data = []
            for invoice in invoices:
                # get all transactions for each invoice
                purchase_items = [transaction_details(transaction) for transaction in invoice.purchase_items]

                # add invoice to data
                data.append({
                    'id': invoice.id,
                    'uuid': invoice.uuid,
                    'transactions': purchase_items,
                    'total_price': str(invoice.total_price),
                    'tax': str(invoice.tax),
                    'amount_paid': str(invoice.amount_paid),
                    'payment_method': str(invoice.payment_method),
                    'customer_PNO': invoice.costumer_PNO,
                    'cashier_id': invoice.cashier_id,
                    'created_at': invoice.created_at.strftime("%Y-%m-%d %H:%M:%S") ,
                })

            return {'invoices': data, 'invoices_count': len(invoices)}
            
        else:
            return {'message': "no invoices found", 'invoices_count': 0}


def create_invoice(data):
    # try:
    uuid = str(uuid_gen())
    invoice = Invoice(
        id=data['id'],
        uuid=uuid,
        total_price=data['total_price'],
        tax=data['tax'],
        amount_paid=data['amount_paid'],
        payment_method=data['payment_method'],
        payment_id=data['payment_id'],
        costumer_PNO=data['customer_PNO'],
        cashier_id=data['cashier_id'],
        store_id=data['store_id']
    )

    with Session() as session:
        session.add(invoice)
        session.commit()

        # create invoice qrcode
        invoice_qrcode = InvoiceToQR(
            InvoiceID=invoice.id,
            SellerName="Sayer",
            TAX_ID="318765367897613",
            Time=invoice.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            InvoiceTotal=str(invoice.total_price),
            TAX=str(invoice.tax)
        )
        
        invoice.qrcode_url = invoice_qrcode[0]
        invoice.qrcode = invoice_qrcode[1]
        session.add(invoice)
        session.commit()

        inv_transactions = []
        # create transactions for this invoive
        for item in data['cart_items']:
            min = 1111
            max = 999999999
            transaction_id = random.randrange(min, max)
            transaction = Transaction(
                id=transaction_id,
                invoice_id=invoice.id,
                item_id=item['item_id'],
                item_name=item['item_name'],
                item_price=item['item_price'],
                quantity_sold=item['quantity_sold'],
                subtotal=item['subtotal'],
                store_id=data['store_id']
            )
            # save transaction
            session.add(transaction)
            session.commit()

            # add transaction to invoice
            inv_transactions.append(transaction_details(transaction))

            # update item quantity
            item_controller.reduce_quantity(item['item_id'], item['quantity_sold'])

        # generate invoice json
        invoice_json = generate_json(invoice)

        # create invoice xml
        invoice_xml = dicttoxml(invoice_json, attr_type = False)
        dom = parseString(invoice_xml)
        # print(dom.toprettyxml())

        return {
            'id': invoice.id,
            'uuid': invoice.uuid,
            'cart_items': inv_transactions,
            'total_price': str(invoice.total_price),
            'tax': str(invoice.tax),
            'amount_paid': str(invoice.amount_paid),
            'payment_method': str(invoice.payment_method),
            'customer_PNO': invoice.costumer_PNO,
            'cashier_id': invoice.cashier_id,
            'qrcode_url': invoice.qrcode_url,
            'qrcode': invoice.qrcode,
            'invoice_json': invoice_json,
            'invoice_xml': dom.toprettyxml(),
            # 'cashier_name': invoice.cashier.name,
            'created_at': invoice.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        
    # except:
    #     return {'error': "An error occured"}


def get_invoice(invoice_id):
    with Session() as session:
        invoice = session.get(Invoice, invoice_id)
        if invoice:
            # get all transactions for each invoice
            purchase_items = [transaction_details(transaction) for transaction in invoice.purchase_items]

            return {
                'id': invoice.id,
                'uuid': invoice.uuid,
                'transactions': purchase_items,
                'total_price': str(invoice.total_price),
                'tax': str(invoice.tax),
                'amount_paid': str(invoice.amount_paid),
                'payment_method': str(invoice.payment_method),
                'customer_PNO': invoice.costumer_PNO,
                'qrcode_url': invoice.qrcode_url,
                'qrcode': invoice.qrcode,
                'cashier_id': invoice.cashier_id,
                # 'cashier_name': invoice.cashier.name,
                'created_at': invoice.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }

        else:
            return {'message': "Invoice not found"}
        

def update_invoice(data, invoice_id):
    with Session() as session:
        invoice = session.get(Invoice, invoice_id)
        if invoice:
            # edit invoice
            pass
        else:
            return {'message': "invoice not found"}
        

def delete_invoice(invoice_id):
    with Session() as session:
        invoice = session.get(Invoice, invoice_id)
        if invoice:
            session.delete(invoice)
            session.commit()
            return f'Invoice with ID {invoice_id} deleted successfully'
        
        else:
            return {'message': "invoice not found"}
        
