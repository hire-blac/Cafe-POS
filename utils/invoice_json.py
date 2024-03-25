import decimal
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_json(invoice):
    # invoice transactions
    transactions = [{
        "quantity": transaction.quantity_sold,
        "price": str(transaction.item_price),
        "netAmount": str(transaction.subtotal),
        "vatAmount": str(transaction.subtotal * decimal.Decimal(0.15)),
        "amountInclusiveVAT": str(transaction.subtotal+(transaction.subtotal * decimal.Decimal(0.15))),
        "itemName": transaction.item_name,
        "vat": {
            "categoryCode": "S",
            "percent": 15
        },
    } for transaction in invoice.purchase_items]

    """Generate a JSON object from an Invoice instance."""
    return {
        "document": {
            "invoiceType": "SIMPLIFIED_TAX_INVOICE",
            "generalInvoiceInfo": {
                "number": invoice.id,
                "uuid": invoice.uuid,
                "icv": 1,
                # "issueDateTime": invoice.created_at,
                "issueDateTime": invoice.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                "actualDeliveryDate": "2024-01-15",
                "previousInvoiceHash": "NWZlY2ViNjZmZmM4NmYzOGQ5NTI3ODZjNmQ2OTZjNzljMmRiYzIzOWRkNGU5MWI0NjcyOWQ3M2EyN2ZiNTdlOQ==",
                "currency": "SAR",
                "paymentMeans": ["30", "10"],
                "purchaseOrder": "BC126598745",
                "contractNumber": "161313031"
            },
            "seller": {
                "name": os.environ.get('SELLER_NAME'),
                "address": {
                    "street": os.environ.get('SELLER_STREET'),
                    "buildingNumber": "1111",
                    "additionalNumber": "1234",
                    "district": "dicsdv",
                    "city": os.environ.get('SELLER_CITY'),
                    "postalCode": os.environ.get('SELLER_POSTAL_CODE'),
                    "countryCode": "SA"
                },
                "vatNumber": os.environ.get('SELLER_TAX_NUMBER'),
                "id": {
                    "idType": "CRN",
                    "value": os.environ.get('SELLER_ID_REGISTRATION_NUMBER')
                }
            },
            "allowances": [
                {
                    "reason": "Discount 1",
                    "reasonCode": "95",
                    "percent": 10,
                    "baseAmount": 200,
                    "vat": {
                        "categoryCode": "S",
                        "percent": 15
                    },
                    "chargeIndicator": False
                },
                {
                    "reason": "Delivery",
                    "reasonCode": "DL",
                    "amount": 7,
                    "vat": {
                        "categoryCode": "S",
                        "percent": 15
                    },
                    "chargeIndicator": True
                }
            ],
            "invoiceLines": transactions
        },
        "privateKey": os.environ.get('PRIVATE_KEY'),
        "binarySecurityToken": os.environ.get('BINARY_SECURITY_TOKEN'),
        "secret": os.environ.get('SECRET')
    }