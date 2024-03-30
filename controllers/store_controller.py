from sqlalchemy.orm import sessionmaker
from models.models import StoreProfile, CompanyProfile, User, engine

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)

def get_company(company_id):
    with Session() as session:
        company = session.query(CompanyProfile).get(company_id)
        if company:
            company_stores = [shop_details(store) for store in company.stores]
            return {
                'id': company.id,
                'company_name': company.company_name,
                'cr_number': company.cr_number,
                'city': company.city,
                'street': company.street,
                'zip_code': company.zip_code,
                'tax_number': company.tax_number,
                'phone_number': company.phone_number,
                'logo': company.logo,
                'email': company.email,
                'website': company.website,
                'stores': company_stores,
            }
        return {'error': "company not found"}
    
    
def create_company(data):
    company = CompanyProfile(
        company_name=data['company_name'], 
        cr_number=data['cr_number'],
        city=data['city'],
        street=data['street'],
        zip_code=int(data['zip_code']),
        tax_number=data['tax_number'],
        phone_number=data["phone_number"],
        logo=data['logo'],
        email=data['email'],
        website=data['website']
    )

    company_stores = []
    with Session() as session:
        session.add(company)
        session.commit()

        # create store
        data['company_id'] = company.id
        store = create_store(data)

        # add user to company
        user = session.query(User).filter_by(username=data['user']).first()
        user.company_id = company.id
        session.commit()

        return {
                'res': "success",
                'id': company.id,
                'company_name': company.company_name,
                'cr_number': company.cr_number,
                'city': company.city,
                'street': company.street,
                'zip_code': company.zip_code,
                'tax_number': company.tax_number,
                'phone_number': company.phone_number,
                'logo': company.logo,
                'email': company.email,
                'website': company.website
            }


def update_company(company_id, data):
    with Session() as session:
        company = session.query(CompanyProfile).get(company_id)
        if company:
            company.company_name = data['company_name']
            company.cr_number = data['cr_number']
            company.city = data['city']
            company.street = data['street']
            company.zip_code = data['zip_code']
            company.tax_number = data['tax_number']
            company.phone_number = data['phone_number']
            company.email = data['email']
            company.website = data['website']

            session.add(company)
            session.commit()
            return {'message': "The Company Profile has been updated."}
        else:
            return {'error': 'Company not found'}


def shop_details(store):
    return {
        'id': store.id,
        'shop_name': store.shop_name,
        'phone_number': store.phone_number,
        'zip_code': store.zip_code,
        'district': store.district,
        'unit_number': store.unit_number
    }


def all_stores():
    with Session() as session:
        stores = session.query(StoreProfile).all()
        if stores:
            data = [{
                'id': store.id,
                'shop_name': store.shop_name,
                'phone_number': store.phone_number,
                'zip_code': store.zip_code,
                'district': store.district,
                'district': store.district,
                'unit_number': store.unit_number
            } for store in stores]

            return {'stores': data}
        return {'message': "no orders found", 'orders_count': 0}
    

def create_store(data):
    data['shop_name'] = data['company_name']
    store = StoreProfile(
        shop_name=data['shop_name'],
        phone_number=data['phone_number'],
        zip_code=data['zip_code'],
        district=data['district'],
        unit_number=data['unit_number'],
        company_id=data['company_id'],
    )

    with Session() as session:
        session.add(store)
        session.commit()

        return {
                'id': store.id,
                'shop_name': store.shop_name,
                'phone_number': store.phone_number,
                'zip_code': store.zip_code,
                'district': store.district,
                'unit_number': store.unit_number
            }


def get_store(store_id):
    with Session() as session:
        store = session.get(StoreProfile, store_id)
        if store:
            return shop_details(store)
        
        return {'error': "company not found"}
    
    
def update_store(store_id, data):
    with Session() as session:
        store = session.get(StoreProfile, store_id)
        if store:
            store.shop_name = data['shop_name']
            store.phone_number = data['phone_number']
            store.zip_code = data['zip_code']
            store.district = data['district']
            store.unit_number = data['unit_number']

            session.add(store)
            session.commit()

            return {
                    'id': store.id,
                    'shop_name': store.shop_name,
                    'phone_number': store.phone_number,
                    'zip_code': store.zip_code,
                    'district': store.district,
                    'unit_number': store.unit_number
                }
        return {'error': 'Store not found'}
    

def delete_store(store_id):
    with Session() as session:
        store = session.query(StoreProfile).get(store_id)
        if store:
            store.delete(store)
            session.commit()
            return f'store with ID {store_id} deleted successfully'
        
        else:
            return {'message': "store not found"}