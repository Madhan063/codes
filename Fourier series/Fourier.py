
# import statements
import sys
import numpy as np
from math import *
from pylab import *
import scipy.special as sp
from scipy.integrate import quad

# defining exponential funtions
def func_1(x):
	try:
		l = len(x)
	except TypeError:
		try:
			y = exp(x)
			return y
		except TypeError:
			print('Expected real number input')
			sys.exit()
	y = np.zeros(l)
	try:
		for i in range(l):
			y[i] = exp(x[i])
		return y
	except TypeError:
			print('Expected real number input')
			sys.exit()

def func_2(x):
	try:
		l = len(x)
	except TypeError:
		try:
			y = cos(cos(x))	# x is in radians
			return y
		except TypeError:
			print('Expected real number input for exponential')
			sys.exit()
	y = np.zeros(l)
	try:
		for i in range(l):
			y[i] = cos(cos(x[i]))
		return y
	except TypeError:
			print('Expected real number input for cos(cos(x))')
			sys.exit()

N = 700		# number of samples

#defining x-axis samples
t = linspace(-2*pi,4*pi,N)
x = linspace(0*pi,2*pi,N)

y1 = func_1(t)
y2 = func_2(t)
y3 = func_1(x)

# plotting the graphs
figure(1)
plt.semilogy(t,y1,'r',label = 'exponential')
plt.xlabel('t')
plt.ylabel('exp(t)')
plt.title('exponential plot')
plt.legend(frameon = True)
plt.grid()

figure(2)
plt.plot(t,y2,'g',label = 'cos(cos(x))')
plt.xlabel('t')
plt.ylabel('cos(cos(t))')
plt.title('plot of cos(cos(x))')
plt.legend(frameon = True)
plt.grid()

#fourier estimation curve assuming e^x is periodic i.e periodic extension of e^x
figure(3)
plt.plot(x-2*pi,y3,'r',label = 'exponential')
plt.plot(x,y3,'r')
plt.plot(x+2*pi,y3,'r')
plt.plot([0,0],[1,np.exp(2*np.pi)],'r--') 
plt.plot([2*np.pi,2*np.pi],[1,np.exp(2*np.pi)],'r--') 
plt.plot([4*np.pi,4*np.pi],[1,np.exp(2*np.pi)],'r--') 
plt.xlabel('x')
plt.ylabel('exp(x)')
plt.title('exponential plot estimated by fourier series')
plt.legend(frameon = True)
plt.grid()


#defining functions to use in integration
def func_3(x,k):
	f = exp(x)
	return f*cos(k*x)
def func_4(x,k):
	f = exp(x)
	return f*sin(k*x)
def func_5(x,k):
	f = cos(cos(x))
	return f*cos(k*x)
def func_6(x,k):
	f = cos(cos(x))
	return f*sin(k*x)

coeff_1 = np.zeros(51)	#coeff matrix of e^x
for i in range(26):
	val_1= quad(func_3,0,2*pi,args=i)[0]
	val_2= quad(func_4,0,2*pi,args=i)[0]
	if i == 0:
		coeff_1[i] = val_1/(2*pi)
	else:
		coeff_1[(2*i)-1] = val_1/(pi)
		coeff_1[2*i] = val_2/(pi)

coeff_2 = np.zeros(51) #coeff matrix of cos(cosx)
for i in range(26):
	val_1= quad(func_5,0,2*pi,args=i)[0]
	val_2= quad(func_6,0,2*pi,args=i)[0]
	if i == 0:
		coeff_2[i] = val_1/(2*pi)
	else:
		coeff_2[(2*i)-1] = val_1/(pi)
		coeff_2[2*i] = val_2/(pi)

n = np.array(range(51))

# least square approach
x = linspace(0,2*pi,401) 
x = x[:-1]

b1 = func_1(x)
b2 = func_2(x)

# Ac = b
A = np.zeros((400,51))  
A[:,0]=1  
for k in range(1,26):
	A[:,2*k-1] = cos(k*x)
	A[:,2*k] = sin(k*x)

c1 = lstsq(A,b1,rcond = -1)[0]
c2 = lstsq(A,b2,rcond = -1)[0]

#plotting
figure(4)
plt.semilogy(n,abs(coeff_1),'ro',label = 'coeff by integration method')
plt.semilogy(n,abs(c1),'go',label = 'coeff by lstsq method')
plt.xlabel('n')
plt.ylabel('coefficients in log scale')
plt.title ('Coefficients of exponential semilogy plot')
plt.legend()

figure(5)
plt.semilogy(n,abs(coeff_2),'ro',label = 'coeff by integration method')
plt.semilogy(n,abs(c2),'go',label = 'coeff by lstsq method')
plt.xlabel('n')
plt.ylabel('coefficients in log scale')
plt.title ('Coefficients of cos(cos(x)) semilogy plot')
plt.legend()

figure(6)
plt.loglog(n,abs(coeff_1),'ro',label = 'coeff by integration method')
plt.loglog(n,abs(c1),'go',label = 'coeff by lstsq method')
plt.xlabel('n')
plt.ylabel('coefficients in log scale')
plt.title ('Coefficients of exponential log-log')
plt.legend()


figure(7)
plt.loglog(n,abs(coeff_2),'ro',label = 'coeff by integration method')
plt.loglog(n,abs(c2),'go',label = 'coeff by lstsq method')
plt.xlabel('n')
plt.ylabel('coefficients in log scale')
plt.title ('Coefficients of cos(cos(x)) log-log plot')
plt.legend()

#difference or error calculation
diff_1 = abs(coeff_1 - c1)		
p1 = max(diff_1)
n1 = np.where(diff_1 == p1)

figure(8)
plt.plot(n,diff_1,'ro',label = 'diff')
plt.plot(n1,p1,'go',label = 'max_diff')
plt.title('coefficient difference for exponential')
plt.legend()

diff_2 = abs(coeff_2 - c2)
p2 = max(diff_2)
n2 = np.where(diff_2 == p2)

figure(9)
plt.plot(n,diff_2,'ro',label = 'diff')
plt.plot(n2,p2,'go',label = 'max_diff')
plt.title('coefficient difference for cos(cos(x))')
plt.legend()

A = np.zeros(51)
A[0] = 1
est_1 = np.zeros(len(x))
est_2 = np.zeros(len(x))
for i in range(len(x)):
	for k in range(1,26):
		A[2*k-1] = cos(k*x[i])
		A[2*k] = sin(k*x[i])
		est_1[i] = np.matmul(A.T,c1)
		est_2[i] = np.matmul(A.T,c2)

y3 = func_1(x)
y4 = func_2(x)

figure(10)
plt.semilogy(x,y3,'ro',label = 'exact exponential ')
plt.semilogy(x,est_1,'go',label = 'exponential from coeff by lstsq')
plt.legend(frameon = True)

figure(11)
plt.plot(x,y4,'ro',label = 'true cos(cos(x))')
plt.plot(x,est_2,'go',label = 'cos(cos(x)) from coeff by lstsq')
plt.legend(frameon = True)
plt.show()
