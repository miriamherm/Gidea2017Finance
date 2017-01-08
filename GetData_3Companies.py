#!/usr/bin/env python
import urllib.request
import pytz
import pandas as pd
import numpy as np
import time
import math

from pandas.io.data import DataReader
from datetime import datetime

#declare global variables 
T=15 #time chunk unit
START = datetime(2007, 3, 1, 0, 0, 0, 0, pytz.utc)
END =datetime(2008, 12, 31, 0, 0, 0, 0, pytz.utc)

#Update with code reading stock ticker from internet list.
tickers=['IBM','GOOG','YHOO']


#use YAHOO api and pandas to get data.
data = DataReader(tickers, 'yahoo', START, END)
companies=data['Adj Close']
CompanyNames=list()
for companyName in companies:
	CompanyNames.append(companyName)
# print(CompanyNames)
#Declare  Needed Vectors
X={}

# Create function: def getShiftData():
# Manipulate data to correct format,  only necessary pieces of info

for company in CompanyNames:
	#Save Adj Close data
	x= data['Adj Close'][company]
#	print(company, x)
	#Shift the column down by one, so column 0: is yesterday's price
	ShiftData= pd.DataFrame({0:x.shift(), 1:x})
#	print(ShiftData)
	#Calculate the Return, (T-Y)/Y
	ShiftData['Return']= (ShiftData[1]-ShiftData[0])/ShiftData[0]
#	print(ShiftData)
	#declare column for the Xbars- called 'AvgT'
	ShiftData['AvgT']=ShiftData['Return']
	ShiftData['SumT^2']=ShiftData['Return']
	numrows=len(ShiftData.index)

	#Average the values of return in row i, with the 15 rows ahead of it.
	for i in range(numrows):
		ShiftData['AvgT'][i]=np.mean(ShiftData['Return'][i:i+T])
#	print(ShiftData)
	#calculate X-Xbar, save as 'brackets'
	ShiftData['Brackets']=ShiftData['Return']-ShiftData['AvgT']
	ShiftData['Brackets^2']=ShiftData['Brackets']**2
	
	for i in range(numrows):
		ShiftData['SumT^2'][i]=np.sum(ShiftData['Brackets^2'][i:i+T])
#	print(ShiftData)
	#save all 5 pieces of information in X, under the comapny name.
	X[company]=ShiftData


itera=1
#df = pd.DataFrame(columns=('date', 'I', "J", 'Num', 'Den','Cij' ))
numrows=len(X[CompanyNames[0]].index)
for date in X[CompanyNames[0]].index:
	for I in CompanyNames:
		for J in CompanyNames:
			X[I][J]= X[I]['Brackets']* X[J]['Brackets']
			X[I][J+"^2"]= (X[I]['SumT^2']* X[J]['SumT^2'])**.5
	if itera<=2*T:
		print(X[I].head())
		itera=itera+1
	else: break

#print(numrows)

for I in CompanyNames:
	for J in CompanyNames:
		X[I]['C'+J]=X[I][J]
		for i in range(numrows):
			X[I]['C'+J][i]=np.sum(X[I][J][i:i+T])
			# X[I]['sumT'+ J]=np.sum(x[i:i+T])
			# print(X[I])11
			# print([i:i+T])
			# print(np.sum(X[I][J][i:i+T]))
 
# #C.set_index([CompanyNames])
#for date in X[CompanyNames[0]].index:
for date in X[CompanyNames[0]].index:
	C=pd.DataFrame(columns=CompanyNames, index=CompanyNames)
	D=pd.DataFrame(columns=CompanyNames, index=CompanyNames)
	for I in C.index:
		for J in CompanyNames:
			C[J][I]=X[I]['C'+J][date]/X[I][J+"^2"][date]
			D[J][I]=(2*(1-C[J][I]))**.5
	
	filename=str(date)[0:10]+'_D.xlsx'
	writer = pd.ExcelWriter(filename)
	D.to_excel(writer, 'Data')
	writer.save()

# for I in CompanyNames:
# 	filename=I+'.xlsx'
# 	writer = pd.ExcelWriter(filename)
# 	X[I].to_excel(writer, 'Data')
# 	writer.save()



# filename=fildate[0:10]+'.xlsx'
# writer = pd.ExcelWriter(filename)
# df.to_excel(writer, 'Data')
# writer.save()
