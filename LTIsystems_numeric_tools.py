# import statements
import numpy as np 
import scipy.signal as sp 
import matplotlib.pyplot as plt


# question 1
'''
		num = s+0.5
		den = s^4+s^3+4.75s^2+2.25s+5.625
'''
system = ([1.0,0.5],[1.0,1.0,4.75,2.25,5.625])
t,x = sp.impulse(system,None,np.linspace(0,50,501))
plt.plot(t,x,label = 'damping = 0.5')
plt.ylabel('x')
plt.xlabel('t')

# question 2
'''
	num = s+0.05
	dem = s^4+0.1s^3+4.5025s^2+0.225s+5.068125	
'''
system = ([1.0,0.05],[1.0,0.1,4.5025,0.225,5.068125])
t,x = sp.impulse(system,None,np.linspace(0,50,501))
plt.plot(t,x,label = 'damping = 0.05')
plt.legend()
plt.show()

# question 3
#defining f(t) function
def func(t,w):
	return (np.cos(w*t))*(np.exp(-0.05*t)*(np.heaviside(t,1)))
# defining the system response of the system
H = sp.lti([1.0],[1.0,0.0,2.25])
time = np.linspace(0,50,501)
# performing convolution for various w values
for w in [1.4,1.45,1.5,1.55,1.6]:
	u = func(time,w)
	tout,y,x = sp.lsim(H,u,time)
	plt.plot(tout,y,label = 'w = %0.2f'%w)
plt.legend()
plt.show()

# question 4
# X(s)
H1 = sp.lti([1,0,2],[1,0,3,0])
# Y(s)
H2 = sp.lti([2],[1,0,3,0])
time = np.linspace(0,20,1000)
# obtaining x(t) and y(t)
t,x = sp.impulse(H1,None,time)	
t,y = sp.impulse(H2,None,time)
plt.plot(t,x,label = 'x(t)')
plt.plot(t,y,label = 'y(t)')
plt.title('coupled spring problem')
plt.legend()
plt.show()

# question 5
l = 10**(-6)
c = 10**(-6)
r = 100  
# steadt state transfer function
H = sp.lti([1.0],[l*c,r*c,1.0])
# bode plots
w,s,phi = H.bode()
plt.subplot(2,1,1)
plt.semilogx(w,s,'r',label = 'magnitude response')
plt.legend()
plt.subplot(2,1,2)
plt.semilogx(w,phi,'b', label = 'phase response')
plt.legend()
plt.show()

# question 6
# transfer function of the system
H = sp.lti([1.0],[l*c,r*c,1.0])
global w1,w2
w1 = 10**3
w2 = 10**6
t1 = 30*(10**(-6))
t2 = 10*(10**(-3))
# defining input 
def func1(t):
	a = np.cos(w1*t)*np.heaviside(t,1)
	b = np.cos(w2*t)*np.heaviside(t,1)
	return a-b
# analyzing the system for time intevals shorter than 1us
time1 = np.linspace(0,t1,1000)
u1 = func1(time1)
tout,y,x = sp.lsim(H,u1,time1)
plt.plot(tout,y)
plt.xlabel('t')
plt.ylabel('Vout')
plt.title('Vout in 0<t<30us')
plt.show()
# analyzing the system over a long time interval
time2 = np.linspace(0,t2,1000)
u2 = func1(time2)
tout,y,x = sp.lsim(H,u2,time2)
plt.plot(tout,y)
plt.xlabel('t')
plt.ylabel('Vout')
plt.title('Vout in t=10ms')
plt.show()