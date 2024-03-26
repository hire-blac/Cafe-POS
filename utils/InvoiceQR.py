import os
import tlv8
import base64
import qrcode
from io import BytesIO

#charset
structTLV = {
    1: tlv8.DataType.STRING,
    2: tlv8.DataType.STRING,
    3: tlv8.DataType.STRING,
    4: tlv8.DataType.STRING,
    5: tlv8.DataType.STRING 
}

def InvoiceToQR(InvoiceID, SellerName='string', TAX_ID='string', Time='yr-m-d h:m:s', InvoiceTotal='InclusiveTAX', TAX="TAX_amount"):
	parms = [SellerName, TAX_ID, Time, InvoiceTotal, TAX]

	for i in range(0,4):
		parms[i].encode('utf-8')
		
	Invoice = [
		tlv8.Entry(1, InvoiceID),
		tlv8.Entry(2, SellerName),
		tlv8.Entry(3, TAX_ID),
		tlv8.Entry(4, Time),
		tlv8.Entry(5, InvoiceTotal),
		tlv8.Entry(6, TAX)
	]
	
	TLV = tlv8.encode(Invoice, structTLV)
	
	# b64Inv = str(base64.b64encode(TLV))
	# output = b64Inv[2:len(b64Inv)-1]
	
	qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
	# qr.add_data(output)
	qr.add_data(TLV)
	qr.make(fit=True)
	img_buffer = BytesIO()
	qr.make_image(fill_color="black", back_color="white").save(img_buffer, format="PNG")
	img_buffer.seek(0)
	code = 'data:image/png;base64, ' + base64.b64encode(img_buffer.read()).decode('utf-8')
	return code


def QRdecode():
	pass;


if __name__ == "__main__":
	invoiceId = input("input the invoice id: ")
	res = InvoiceToQR(InvoiceID=invoiceId)
	print(res)