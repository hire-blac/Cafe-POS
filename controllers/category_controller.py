from sqlalchemy.orm import sessionmaker
from models.models import Category, engine

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)


def all_categories():
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
            return {'message': 'no categories'}

def create_category(data):
    category = Category(
            name=data['name'],
            store_id = data['store_id']
        )

    with Session() as session:
        session.add(category)
        session.commit()    
        return {
            'id': category.id, 
            'name': category.name
        }


def get_category(category_id):
    with Session() as session:
        category = session.get(Category, category_id)
        if category:
            # return category
            items = [{'id': item.id, 'name': item.name} for item in category.items]
            return {'id': category.id, 'name': category.name, 'items': items}
        else:
            return {'message': 'Category not found'}


def update_category(category_id, data):
    with Session() as session:
        category = session.get(Category, category_id)
        if category:
            category.name = data['name']
            session.add(category)
            session.commit()
        else:
            return {'message': 'Category not found'}
        

def delete_category(category_id):
    with Session() as session:
        category = session.get(Category, category_id)
        if category:
            session.delete(category)
            session.commit()
            return f'Category with ID {category_id} deleted successfully'
        else:
            return {'message': 'Category not found'}
        
