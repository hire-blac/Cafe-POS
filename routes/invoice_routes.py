from bottle import Bottle
from bottle import Bottle, template, route, request, get, post, put, delete
from sqlalchemy.orm import sessionmaker
from bottle import jinja2_template as template
from controllers import invoice_controller
from models.models import engine


# Create SQLAlchemy session
Session = sessionmaker(bind=engine)

invoice_routes = Bottle()

# INVOICE ROUTES
@route("/invoices")
def invoices():
    return template('invoices')

@get('/api/invoices')
def all_invoices():
    invoices = invoice_controller.all_invoices()
    return invoices

@route("/cart")
def new_cart():
    return template('cart')

@post('/api/invoices')
def new_invoice():
    data = request.json
    invoice = invoice_controller.create_invoice(data)
    return invoice

@route('/invoice/<invoice_id>')
def invoice(invoice_id):
    invoice = invoice_controller.get_invoice(invoice_id)
    return template("invoice", invoice=invoice)

@get('/api/invoices/<invoice_id>')
def get_invoice(invoice_id):
    invoice = invoice_controller.get_invoice(invoice_id)
    return invoice

@put("/api/invoices/<invoice_id>")
def update_invoice(invoice_id):
    data = request.json
    invoice  = invoice_controller.update_invoice(invoice_id, data)
    return invoice,  200

@delete("/api/invoices/<invoice_id>")
def delete_invoice(invoice_id):
    res = invoice_controller.delete_invoice(invoice_id)
    return res