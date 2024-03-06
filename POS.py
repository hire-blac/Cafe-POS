import csv
import pandas as pd
import time, datetime

from controllers import invoice_controller
#import pdf

def Calc(item_priceS,item_quantityS,Discount_onall=0,TAX=0.15):
	
	Actual_cost=[]
	counter=0
	Sum_exTAX=0

	Sum_inTAX=0

	for prices in item_priceS:
			prices=float(prices)
			Qty=int(item_quantityS[counter])
			ACost=prices*Qty
			Actual_cost.append(ACost)
			counter=counter+1
	#print(Actual_cost)
	for individual_cost in Actual_cost:
		Sum_exTAX=Sum_exTAX+individual_cost
	
	if Discount_onall>0:
		Discount=Sum_exTAX*Discount_onall
		if Discount < Sum_exTAX:
			Sum_exTAX=Sum_exTAX-Discount
		else: pass

	
	TAXs=Sum_exTAX*TAX
	Sum_inTAX=Sum_exTAX+TAXs
	#print(Sum_exTAX)
	#print(Sum_inTAX)
	return(Actual_cost,Sum_exTAX,TAXs,Sum_inTAX)

def Cart_ini():
	items_idcodes_inCart=[]
	items_priceS_inCart=[]
	items_QtyS_inCart=[]
	with open('cart.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				#print(f'Column names are {", ".join(row)}')
				line_count += 1
			else:
				idcode=row[0]
				items_idcodes_inCart.append(idcode)
				Price=row[1]
				items_priceS_inCart.append(Price)
				Quantity=row[2]
				items_QtyS_inCart.append(Quantity)
				#print(idcode,Price,Quantity)
				line_count += 1
	Calculate=Calc(items_priceS_inCart,items_QtyS_inCart)
	individual_costs=Calculate[0]
	Total_cost_ExTAX=Calculate[1]
	TAXs=Calculate[2]
	Total_cost_InTAX=Calculate[3]

	return(items_idcodes_inCart,individual_costs,Total_cost_ExTAX,TAXs,Total_cost_InTAX,items_QtyS_inCart)
	
def invoice_maker(InvID):
	InvoiceData=invoice_controller.get_invoice(InvID)
	#Vars=["Invid","Inv_datetime","Items","Prices","Qty","Total_NoTAXs","TAXs","Payment_ID","Payment_Method","Costumer_PNO","Cashier"]
	Invoice='''<!DOCTYPE html><html dir="rtl" lang="ar">
	        <body style="width:360px ; height:660px;" >

		{0} / invid</br>
		{1} / Time</br>
		{2}/ items</br>
		i names / </br>
		i names / </br>

		{3} / prcs</br>
		{4}/ qty</br>
		{5} / tot-txs</br>
		{6}/taxs</br>
		tot+txs / </br>

		{7} /pyid </br>

		{8}/ mthd</br>
		{9} costidpno</br>
		{10} cshr</br>
		</br>

	<body></html>'''.format(InvoiceData[0],InvoiceData[2],InvoiceData[3],InvoiceData[4],InvoiceData[5],InvoiceData[6],InvoiceData[7],InvoiceData[8],InvoiceData[9],InvoiceData[10])
	#name=str(InvID)
	#pdf.pdf(a,name)

	#get_item_price_from_db
#print(Cart[0])  
#Calc(Cart[1],Cart[2])
#AddtoCart("667","0.9",0.5)
#with open('cart.csv') as Cart:
#		print(Cart.read())
#updateQty(667,1)
#Delete_inCart_item(667)
#with open('cart.csv') as Cart:
#		print(Cart.read())
