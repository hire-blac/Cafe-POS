from bottle import HTTPResponse
from sqlalchemy.orm import sessionmaker
from models.models import User, engine
from passlib.hash import pbkdf2_sha256

from posauth import GetAuthToken

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)


def all_users():
    with Session() as session:
        users = session.query(User).all()
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
                        usertype = data['usertype']
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

                return {
                    'res': 'success',
                    'id': user.id,
                    'name': user.name,
                    'username': user.username,
                    'usertype': user.usertype,
                    'auth_token': auth_token
                }
            return {"error": "Login credentials are invalid."}
        
        else:
            return {"error": "Login credentials are invalid."}
        

def get_user(username):
    with Session() as session:
        user = session.query(User).filter_by(username=username).first()
        if user:
            return {
                'id': user.id, 
                'name': user.name,
                'username': user.username,
                'usertype': user.usertype,
            }
        else:
            return {'message': 'user not found'}


def update_user(data, user_id):
    with Session() as session:
        user = session.query(User).get(user_id)
        if user:
            user.name = data['name']
            user.username = data['username']
            user.usertype = data['usertype']

            session.add(user)
            session.commit()

            return {
                'id': user.id, 
                'name': user.name,
                'username': user.username,
                'usertype': user.usertype,
            }
        else:
            return {'message': 'user not found'}
        
def change_password(username, data):
    with Session() as session:
        user = session.query(User).filter_by(username=username).first()
        if user:
            password_hash = pbkdf2_sha256.hash(data['password'])
            user.password = password_hash
            session.add(user)
            session.commit()
            return  {"message": "Password changed successfully"}
        else:
            return  {"message":"Username does not exist."}  


def delete_user(user_id):
    with Session() as session:
        user = session.query(User).get(user_id)
        if user:
            session.delete(user)
            session.commit()
            return {'success': f'User with ID {user_id} deleted successfully'}
        else:
            return {'error': 'user not found'}
        
