from sqlalchemy.orm import sessionmaker
from models.models import Store, User, engine

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)

def all_stores():
    with Session() as session:
        stores = session.query(Store).all()
        if stores:
            data = [{
                'id': store.id,
                'company_name': store.company_name,
                'cr_number': store.cr_number,
                'city': store.city,
                'street': store.street,
                'zip_code': store.zip_code,
                'tax_number': store.tax_number,
                'phone_number': store.phone_number,
                'logo': store.logo,
                'email': store.email,
                'website': store.website,
                'shop_name': store.shop_name,
                'district': store.district,
                'unit_number': store.unit_number
            } for store in stores]

            return {'stores': data, 'store_count': len(data)}
        return {'message': "no orders found", 'store_count': 0}
    

def create_store(data):
    data['shop_name'] = data['company_name']
    store = Store(
        company_name=data['company_name'], 
        cr_number=data['cr_number'],
        shop_name=data['shop_name'],
        district=data['district'],
        unit_number=data['unit_number'],
        city=data['city'],
        street=data['street'],
        zip_code=int(data['zip_code']),
        tax_number=data['tax_number'],
        phone_number=data["phone_number"],
        logo=data['logo'],
        email=data['email'],
        website=data['website']
    )

    with Session() as session:
        session.add(store)
        session.commit()

        # add user to store users
        user = session.get(User, data["user"])
        user.store_id = store.id
        session.add(user)
        session.commit()

        return {
                'res': 'success',
                'id': store.id,
                'company_name': store.company_name,
                'cr_number': store.cr_number,
                'city': store.city,
                'street': store.street,
                'zip_code': store.zip_code,
                'tax_number': store.tax_number,
                'phone_number': store.phone_number,
                'logo': store.logo,
                'email': store.email,
                'website': store.website,
                'shop_name': store.shop_name,
                'district': store.district,
                'unit_number': store.unit_number
            }


def get_store(store_id):
    with Session() as session:
        store = session.get(Store, store_id)
        if store:
            return {
                'id': store.id,
                'company_name': store.company_name,
                'cr_number': store.cr_number,
                'city': store.city,
                'street': store.street,
                'zip_code': store.zip_code,
                'tax_number': store.tax_number,
                'phone_number': store.phone_number,
                'logo': store.logo,
                'email': store.email,
                'website': store.website,
                'shop_name': store.shop_name,
                'district': store.district,
                'unit_number': store.unit_number
            }
        
        return {'error': "company not found"}
    
    
def update_store(store_id, data):
    with Session() as session:
        store = session.get(Store, store_id)
        if store:
            store.company_name = data['company_name']
            store.cr_number = data['cr_number']
            store.shop_name = data['shop_name']
            store.district = data['district']
            store.unit_number = data['unit_number']
            store.city = data['city']
            store.street = data['street']
            store.zip_code = data['zip_code']
            store.tax_number = data['tax_number']
            store.phone_number = data['phone_number']
            store.email = data['email']
            store.website = data['website']

            session.add(store)
            session.commit()

            return {
                    'id': store.id,
                    'company_name': store.company_name,
                    'cr_number': store.cr_number,
                    'city': store.city,
                    'street': store.street,
                    'zip_code': store.zip_code,
                    'tax_number': store.tax_number,
                    'phone_number': store.phone_number,
                    'logo': store.logo,
                    'email': store.email,
                    'website': store.website,
                    'shop_name': store.shop_name,
                    'district': store.district,
                    'unit_number': store.unit_number
                }
        
        return {'error': 'Store not found'}
    

def delete_store(store_id):
    with Session() as session:
        store = session.query(Store).get(store_id)
        if store:
            session.delete(store)
            session.commit()
            return f'store with ID {store_id} deleted successfully'
        
        else:
            return {'message': "store not found"}