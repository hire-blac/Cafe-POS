import tlv8
import base64
import qrcode

#charset

structTLV = {
    1: tlv8.DataType.STRING,
    2: tlv8.DataType.STRING,
    3: tlv8.DataType.STRING,
    4: tlv8.DataType.STRING,
    5: tlv8.DataType.STRING 
}
def InvoiceToQR(InvoiceID, SellerName='string', TAX_ID='string', Time='yr-m-d h:m:s', InvoiceTotal='InclusiveTAX', TAX="TAX_amount"):
	parms=[SellerName, TAX_ID, Time, InvoiceTotal, TAX]

	for i in range(0,4):
		parms[i].encode('utf-8')
	Invoice = [
		tlv8.Entry(1, SellerName),
		tlv8.Entry(2, TAX_ID),
		tlv8.Entry(3,Time),
        tlv8.Entry(4,InvoiceTotal),
        tlv8.Entry(5,TAX)
	]
	
	TLV = tlv8.encode(Invoice,structTLV)
	# print(TLV)
	
	b64Inv = str(base64.b64encode(TLV))
	output = b64Inv[2:len(b64Inv)-1]
	img = qrcode.make(output)
	QR_ImgName = "static/{0}.png".format(InvoiceID)
	img.save(QR_ImgName)
	b64QRtext = output
	
	return (QR_ImgName, b64QRtext)


def QRdecode():
	pass;

# print(InvoiceToQR(1040770,'sayer','300498609900003','2023-02-14T12:48:13Z','40000','4000'))
