from bottle import HTTPResponse
from sqlalchemy.orm import sessionmaker
from models.models import User, engine
from passlib.hash import pbkdf2_sha256

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)


def create_super_user():
    with Session() as session:
        name = input("Enter your name: ")
        username = input("Enter your username: ")

        while session.query(User).filter_by(username=username).first():
            username = input("Username already in use. Enter another username: ")
        
        password = input("Enter your password: ")
        try:
            password_hash = pbkdf2_sha256.hash(password)
            user = User(
                    name=name,
                    username=username,
                    password=password_hash,
                    usertype = 'SuperUser'
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
            
if __name__ == '__main__':
     admin = create_super_user()
     print(admin)
     print('Super user created sucessfully')