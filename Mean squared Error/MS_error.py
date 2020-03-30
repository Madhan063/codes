# import statements

import sys
import numpy as np
from pylab import * 
import scipy.special as sp
from scipy.linalg import lstsq
import matplotlib.pyplot as plt 

def true_values(t,A,B):
	y = np.zeros(len(t))
	for i in range(len(t)):
		y[i]=A*sp.jn(2,t[i])+B*t[i]
	return y

dat = np.loadtxt('fitting.dat')

# defining time array and data array
t = np.zeros(len(dat))
data = dat[...,1:].T
for i in range(len(dat)):
	t[i] = dat[i][0]



# Standard deviation
stdev = logspace(-1,-3,9)

# plotting noise
noise = np.zeros(data.shape)
for i in range(len(t)):
	y=1.05*sp.jn(2,t[i])-0.105*t[i] # f(t) vector
	for j in  range(data.shape[0]):
		noise.T[i][j] = data.T[i][j] - y
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
for i in range(noise.shape[0]):
	ax.plot(t,noise[i],label = 'sigma'+str(i+1)+'='+str(stdev[i]))
ax.legend(frameon = True,fancybox = True)
plt.show()

#plotting data with noise and true value
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.plot(t,true_values(t,1.05,-0.105), label = 'True value')
for i in range(data.shape[0]):
	ax.plot(t,data[i],label = 'sigma'+str(i+1)+'='+str(stdev[i]))
ax.legend(fancybox = True, framealpha = 1, frameon = True)
plt.title('Data to be fitted')
plt.show()


# plot for first column of data with error bars
errorbar(t,data[0],stdev[0],fmt='ro', label = 'error bars for column 1')
plt.legend(framealpha = 1, frameon = True)
plt.show()

# plot of first column of data with every 5th item and compariosin plot
errorbar(t[::5],data[0][::5],stdev[0],fmt='ro', label = 'Error bar')
plt.plot(t,true_values(t,1.05,-0.105), label = 'True value')
plt.legend()
plt.title('Data points for sigma = '+str(stdev[0])+' along with exact function')
plt.show()

#constructing matrix M
x = np.zeros(len(t))
y = np.zeros(len(t))
for i in range(len(t)):
	x[i] = sp.jn(2,t[i])
	y[i] = t[i]
M = c_[x,y]

A0 = 1.05; B0 = -0.105
p0 = np.array([A0,B0])
d1 = np.matmul(M,p0)
d2 = true_values(t,1.05,-0.105)
for i in range(len(d1)):
		if d1[i] == d2[i]:
			pass
		else:
			print('ERROR!! Both vetcors are not equal')
			sys.exit()
A = np.arange(0,2,0.1)
B = np.arange(-0.2,0,0.01)

# calculating mean squared error
error = np.zeros(len(data))
e_1 = np.zeros((len(A),len(B)))
for l in range(len(data)):
	f = data[l]
	e = np.zeros((len(A),len(B)))
	for i in range(len(A)):
		for j in range(len(B)):
			sum = 0
			p = np.array([A[i],B[j]])
			g = np.matmul(M,p)
			for k in range(len(t)):
				sum = sum + (f[k] - g[k])**2
			sum = sum/101
			e[i][j] = sum
			if l == 0:
				e_1 = e
			error[l] = np.amin(e)

# plotting contour plot
X,Y = np.meshgrid(A,B)
cp = plt.contour(X,Y,e_1,15)
plt.clabel(cp, inline=True, fontsize=10)
plt.plot(1.05,-0.105,'ro')
plt.text(1.05,-0.105,'exact location')
plt.title('Contour plot of e for first data column')
plt.xlabel('A')
plt.ylabel('B')
plt.show()

# using lstsq function to get the estimte of A and B
try:
	Aerr = np.zeros(len(data))	
	Berr = np.zeros(len(data))
	for i in range(len(data)):
		x, residuals, rank, s = lstsq(M,data[i])
		Aerr[i] = abs(x[0] - A0)
		Berr[i] = abs(x[1] - B0)

	# normal plot
	plt.plot(stdev, Aerr,'rs',ls = '--', label = 'Aerr')
	plt.plot(stdev, Berr,'bo', ls = ':', label = 'Berr')
	plt.title('Variation of error with noise')	
	plt.xlabel('Noise Standard Deviation')
	plt.ylabel('MS error')
	plt.legend()	
	plt.show()

	# loglog plot
	plt.loglog(stdev,Aerr,'o')	
	plt.loglog(stdev,Berr,'o')
	errorbar(stdev,Aerr,stdev,fmt='ro', label = 'Aerr')
	errorbar(stdev,Berr,stdev,fmt='go', label = 'Berr')
	plt.title('variation of error with noise')
	plt.xlabel('Noise Standard Deviation')
	plt.ylabel('MS error')
	plt.legend()
	plt.show()
except np.linalg.LinAlgError:
	print('The matrix M is singular and the least squares cannot be calculated')

