#Heard on the Street Q1.46: 52cards, 26red(+1) and 26black(-1), what is your strategy to maximize expected pay-off
import numpy as np
k = input('How many red cards and black cards do we have seperately\n')
k=int(k)
v = np.zeros(shape=(k+1,2*k+1))
for j in range(2*k+1):
	if j <= k:
		for i in range(j+1):
			v[i,j]=j-2*i
	else:
		for i in range(2*k+1-j):
			v[i,j]=2*k-j-2*i
for j in range(2*k-1,-1,-1):
	if j < k:
		for i in range(j+1):
			v[i,j]=max(v[i,j],(k-j+i)/(2*k-j)*v[i,j+1]+(k-i)/(2*k-j)*v[i+1,j+1])
	else:
		v[0,j]=max(v[0,j+1],v[0,j])
		v[2*k-j,j]=max(v[2*k-1-j,j+1],v[2*k-j,j])
		if j<2*k-1:
			for i in list(range(1,2*k+1-j)):
				v[i,j]=max(v[i,j],i/(2*k-j)*v[i-1,j+1]+(2*k-i-j)/(2*k-j)*v[i,j+1])
print (v)
