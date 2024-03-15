# from enum import Enum
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric, Float, Enum, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

# Define SQLAlchemy models

class StoreProfile(Base):
    __tablename__ = 'store profiles'
    id = Column(Integer, primary_key=True)
    store_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    tax_id = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)  # Column to store image URL


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    usertype = Column(String, nullable=False)


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)


class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    items = relationship('Item', back_populates='category')


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(precision=8, scale=2), nullable=False)
    image_url = Column(String, nullable=True)  # Column to store image URL
    quantity = Column(Integer, nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    category = relationship('Category', back_populates='items')


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    item_price = Column(Numeric(precision=8, scale=2), nullable=False)
    quantity_sold = Column(String, nullable=False)
    subtotal = Column(Numeric(precision=8, scale=2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Define the relationship with Item
    item = relationship('Item', backref=backref('transactions'))


class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True)
    tax = Column(Numeric(precision=8, scale=2), nullable=False)
    total_price = Column(Numeric(precision=8, scale=2), nullable=False)
    # costumer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    costumer_PNO = Column(String)
    payment_method = Column(String, nullable=False)
    amount_paid = Column(Numeric(precision=8, scale=2), nullable=False)
    payment_id = Column(String, nullable=True)
    cashier_id = Column(Integer, ForeignKey('users.id'))
    cashier_name = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Define the relationships
    purchase_items = relationship('Transaction', backref=backref('transactions', uselist=False))
    cashier = relationship('User', backref=backref('cashier'))
    # customer = relationship('Customer', backref=backref('customer'))


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    tax = Column(Numeric(precision=2, scale=2), nullable=False)
    total_price = Column(Numeric(precision=8, scale=2), nullable=False)
    costumer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    order_type = Column(String, nullable=False) # Delivery or Pickup
    payment_status = Column(String, nullable=False, default="Unpaid") # unpaid or paid
    status = Column(String, nullable=False, default="pending") # pending or fulfilled
    # amount_paid = Column(Numeric(precision=8, scale=2), nullable=False)
    cashier_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, server_default=func.now())

    # Define the relationships
    # ordered_items = relationship('Transaction', backref=backref('orderes_items', uselist=False))
    # # cashier = relationship('User', backref=backref('cashier'))
    # customer = relationship('Customer', backref=backref('orders'))

# Create SQLite database and tables
engine = create_engine('sqlite:///POS_DB.db')
Base.metadata.create_all(engine)
