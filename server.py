from bottle import Bottle, request, HTTPResponse
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from decimal import Decimal

Base = declarative_base()

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
    quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='items')

# Create SQLite database and tables
engine = create_engine('sqlite:///new_test.db')
Base.metadata.create_all(engine)

# Create Bottle app and SQLAlchemy session
app = Bottle()
Session = sessionmaker(bind=engine)


@app.route("/categories", method=['GET', 'POST'])
def categories():
    if request.method == "POST":
        data = request.json
        category = Category(name=data['name'])

        with Session() as session:
            session.add(category)
            session.commit()
            return {
                'id': category.id, 
                'name': category.name
            }
    
    elif request.method == "GET":
        with Session() as session:
            categories = session.query(Category).all()
            if categories:
                data = []
                for cat in categories:
                    items = [{'id': item.id, 'name': item.name} for item in cat.items]
                    data.append({
                        'id': cat.id, 
                        'name': cat.name,
                        'items': items
                    })
                return {'categories': data}
            else:
                return HTTPResponse(status=404, body='no categories')
            

@app.route("/items", method=['GET', 'POST'])
def items():
    if request.method == "POST":
        data = request.json

        item = Item(
            name=data['name'],
            price=data['price'],
            quantity=data['quantity'],
            category_id=data['category_id'],
        )

        with Session() as session:
            session.add(item)            
            session.commit()
            return {
                'id': item.id, 
                'name': item.name,
                'price': str(item.price),
                'quantity': item.quantity,
                'category': item.category.name,
            }
    
    elif request.method == "GET":
        with Session() as session:
            items = session.query(Item).all()
            if items:
                data = []
                for item in items:
                    data.append({
                        'id': item.id, 
                        'name': item.name,
                        'price': str(item.price),
                        'quantity': item.quantity,
                        'category': item.category.name,
                    })
                return {'items': data}
            else:
                return {'message': 'no items'}
            
            

# Run the Bottle app
if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True, reloader=True)