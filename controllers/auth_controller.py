from sqlalchemy.orm import sessionmaker
from models.models import User, engine
from passlib.hash import pbkdf2_sha256

from posauth import GetAuthToken

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)


def all_users(store_id):
    if not store_id:
        return {'message': 'no users'}
    
    with Session() as session:
        users = session.query(User).filter_by(store_id=store_id).all()
        if users:
            data = []
            for user in users:
                data.append({
                    'id': user.id,
                    'name': user.name,
                    'username': user.username,
                    'usertype': user.usertype,
                })
            return {'users': data}
        else:
            return {'message': 'no users', 'status': 404}


def register_user(data):
    with Session() as session:
        user = session.query(User).filter_by(username=data['username']).first()
        if user:
                return {'error': "Username already in use"}
        else:
            try:
                password_hash = pbkdf2_sha256.hash(data['password'])
                user = User(
                        id=data['id'],
                        name=data['name'],
                        username=data['username'],
                        password=password_hash,
                        usertype = data['usertype'],
                        store_id = data['store_id']
                    )

                session.add(user)
                session.commit()
                return {
                    'id': user.id,
                    'name': user.name,
                    'username': user.username,
                    'usertype': user.usertype,
                }
            
            except:
                return {'error': "An error occured"}


def login_user(data):
    with Session() as session:
        user = session.query(User).filter_by(username=data['username']).first()
        if user:
            if pbkdf2_sha256.verify(data['password'], user.password):
                auth_token = GetAuthToken(user.username)
                if user.store:
                    return {
                        'res': 'success',
                        'id': user.id,
                        'name': user.name,
                        'username': user.username,
                        'usertype': user.usertype,
                        'store_id': user.store_id,
                        'shop_name': user.store.shop_name,
                        'tax_number': user.store.tax_number,
                        'shop_city': user.store.city,
                        'shop_street': user.store.street,
                        'shop_email': user.store.email,
                        'shop_zip_code': user.store.zip_code,
                        'shop_phone_number': user.store.phone_number,
                        'auth_token': auth_token
                    }
                return {
                    'res': 'success',
                    'id': user.id,
                    'name': user.name,
                    'username': user.username,
                    'usertype': user.usertype,
                    'store_id': user.store_id,
                }
            
            return {"error": "Login credentials are invalid."}
        
        else:
            return {"error": "Login credentials are invalid."}
        

def get_user(username):
    with Session() as session:
        user = session.query(User).filter_by(username=username).first()
        if user:
            shop_name = 'N/A'
            if user.store:
                shop_name  = user.store.shop_name
            return {
                'id': user.id, 
                'name': user.name,
                'username': user.username,
                'usertype': user.usertype,
                'store_id': user.store_id,
                'shop_name': shop_name,
            }
        else:
            return {'message': 'user not found'}


def update_user(data, user_id):
    with Session() as session:
        user = session.get(User, user_id)
        if user:
            user.name = data['name']
            user.username = data['username']
            user.usertype = data['usertype']
            user.store_id = data['store_id']

            session.add(user)
            session.commit()

            return {
                'id': user.id, 
                'name': user.name,
                'username': user.username,
                'usertype': user.usertype,
                'store_id': user.store_id,
                'store': user.store.shop_name,
            }
        else:
            return {'message': 'user not found'}
        
        
def change_password(username, data):
    with Session() as session:
        user = session.query(User).filter_by(username=username).first()
        if user:
            if pbkdf2_sha256.verify(data['old_password'], user.password):
                password_hash = pbkdf2_sha256.hash(data['new_password'])
                user.password = password_hash
                session.add(user)
                session.commit()
                return  {"message": "Password changed successfully"}
        else:
            return  {"message":"Username does not exist."}  


def delete_user(user_id):
    with Session() as session:
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            session.commit()
            return {'success': f'User with ID {user_id} deleted successfully'}
        else:
            return {'error': 'user not found'}
        
        
def all_admins():
    with Session() as session:
        users = session.query(User).filter_by(usertype="Administrator")
        if users:
            data = []
            for user in users:
                store_name = 'No store assigned'
                if user.store:
                    store_name = user.store.shop_name

                data.append({
                    'id': user.id,
                    'name': user.name,
                    'store': store_name,
                    'username': user.username,
                    'usertype': user.usertype,
                })
            return {'users': data, "admin_count": len(data)}
        
        else:
            return  {"message":"No users found.", "admin_count": 0}  

