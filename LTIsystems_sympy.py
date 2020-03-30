# import statements
from sympy import * 
import numpy as np 
from math import *
import scipy.signal as sp
import pylab as p 
import matplotlib.pyplot as plt

# Function to get the impulse response of the system
def impulse_resp(expr):
	num, denom = expr.as_numer_denom()
	num = Poly(num, s).all_coeffs()
	denom = Poly(denom, s).all_coeffs()
	num = [float(i) for i in num]
	denom = [float(i) for i in denom]
	return sp.lti(num,denom)
# Task 1
R1,R2,C1,C2,G = 10000,10000,1e-11,1e-11,1.586
# defining impulse response of the system
H = sp.lti([G],[2*C1*C2*R1*R2, -C1*G*R1 + 2*C1*R1 + 2*C2*R1 + 2*C2*R2, 2])
t_1 = np.linspace(0,10,1001)			# time space 
V_in = np.heaviside(t_1,1)
t_1,V_o,svec = sp.lsim(H,V_in,t_1)		# convolution of the input and impulse response
plt.plot(t_1,V_o,label = 'Step response')
plt.title('Step response of the system')
plt.legend()
plt.show()

# Task 2
w1 = 2000*pi
w2 = 2*(10**6)*pi
def func_1(t):				# defining input function
	a = np.sin(w1*t)
	b = np.cos(w2*t)
	return (a+b)*(np.heaviside(t,1))

t_1 = np.linspace(0,10*10**-3,1001)		# time space to observe the output over large time interval
u1 = func_1(t_1)
t_1,V_o1,svec = sp.lsim(H,u1,t_1)
plt.plot(t_1,V_o1,label = 'output')
plt.title('response of the system for 0<t<10ms')
plt.legend()
plt.show()

t_2 = np.linspace(0,10**-6,1001)		# time space to observe the output over small time interval
u2 = func_1(t_2)
t_2,V_o2,svec = sp.lsim(H,u2,t_2)
plt.plot(t_2,V_o2,label = 'output')
plt.title('response of the system for 0<t<10us')
plt.legend()
plt.show()

s=symbols('s')

def highpass(R1,R3,C1,C2,G,Vi):
	A = Matrix([[0,1,0,-1/G],
				[((-s*R3*C2)/(1+s*R3*C2)),0,1,0],
				[0,G,-G,-1],
				[(1+(C2/C1)+1/(s*C1*R1)),0,-C2/C1,-1/(s*R1*C1)]])
	b = Matrix([0,0,0,Vi])
	V = A.inv()*b
	return (A,b,V)

# analysis for impulse response
A,b,V=highpass(10000,10000,1e-9,1e-9,1.586,1) 
Vo=V[3] 
H = impulse_resp(Vo)
ww=p.logspace(0,10,10001) 
ss=1j*ww 
hf=lambdify(s,Vo,'numpy') 
v=hf(ss) 
plt.loglog(ww,abs(v),lw=2) 
plt.grid(True) 
plt.show()

# for a damping sinusoid without convolution
omega = [pi,10*pi,100*pi,500*pi,1000*pi,2000*pi]
a = 3
for w in omega:
	u = w/(((s+a)**2)+w**2)
	A,b,V = highpass(10000,10000,1e-9,1e-9,1.586,u)
	Vo= V[3]
	ww=p.logspace(0,8,8001) 
	ss=1j*ww 
	hf=lambdify(s,Vo,'numpy') 
	v=hf(ss) 
	plt.loglog(ww,abs(v),lw=2,label = 'w=%d*pi'%(w/pi)) 
plt.grid(True)
plt.legend() 
plt.show() 

# for a damping sinusoid with convolution 
def func_2(t,a,b):
	c = np.exp(-a*t)
	d = np.sin(b*t)
	return c*d*np.heaviside(t,1)
t_1 = np.linspace(0,10**-2,1001)
u = func_2(t_1,3,2000*pi)
t_1,V_o1,svec = sp.lsim(H,u,t_1)
print(H)
plt.plot(t_1,V_o1)
plt.show()
# for unit step function
u = 1/s
A,b,V = highpass(10000,10000,1e-9,1e-9,1.586,u)
Vo= V[3]
ww=p.logspace(0,8,8001) 
ss=1j*ww 
hf=lambdify(s,Vo,'numpy') 
v=hf(ss) 
plt.loglog(ww,abs(v),lw=2) 
plt.grid(True) 
plt.show()
