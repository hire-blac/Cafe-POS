from sqlalchemy.orm import sessionmaker
from models.models import User, engine

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)


def all_users():
    with Session() as session:
        users = session.query(User).all()
        if users:
            data = []
            for cat in users:
                items = [{'id': item.id, 'name': item.name} for item in cat.items]
                data.append({
                    'id': cat.id, 
                    'name': cat.name,
                    'items': items
                })
            return {'users': data}
        else:
            return None
            # return {'message': 'no users', 'status': 404}

def create_user(data):
    # data = request.json
    user = User(name=data['name'])

    with Session() as session:
        session.add(user)
        session.commit()
        return user
    
        # return {
        #     'id': user.id, 
        #     'name': user.name
        # }


def get_user(user_id):
    with Session() as session:
        user = session.query(User).get(user_id)
        if user:
            return user
        
            # items = [{'id': item.id, 'name': item.name} for item in user.items]
            # return {'id': user.id, 'name': user.name, 'items': items}
        else:
            return None
            # return {'message': 'user not found'}


def update_user(data, user_id):
    with Session() as session:
        user = session.query(User).get(user_id)
        if user:
            pass
        else:
            return None
            # return {'message': 'user not found'}
        

def delete_user(user_id):
    with Session() as session:
        user = session.query(User).get(user_id)
        if user:
            session.delete(user)
            session.commit()
            return f'User with ID {user_id} deleted successfully'
            # return {'status': 'success', 'message': f'user with ID {user_id} deleted successfully'}
        else:
            return None
        
