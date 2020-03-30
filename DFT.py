from pylab import * 

# for sin^3t
t=linspace(-4*pi,4*pi,513)
t=t[:-1] 
y = sin(t)*sin(t)*sin(t)
Y=fftshift(fft(y))/512.0 
w=linspace(-64,64,513)
w=w[:-1]
figure() 
subplot(2,1,1) 
plot(w,abs(Y),lw=2) 
xlim([-15,15]) 
ylabel(r"$|Y|$",size=16) 
title(r"Spectrum of $\sin^3t$") 
grid(True) 
subplot(2,1,2) 
plot(w,angle(Y),'ro',lw=2) 
ii=where(abs(Y)>1e-3) 
plot(w[ii],angle(Y[ii]),'go',lw=2) 
xlim([-15,15]) 
ylabel(r"Phase of $Y$",size=16) 
xlabel(r"$\omega$",size=16) 
grid(True) 

# for cos^3t
t=linspace(-4*pi,4*pi,513)
t=t[:-1] 
y = cos(t)*cos(t)*cos(t)
Y=fftshift(fft(y))/512.0 
w=linspace(-64,64,513)
w=w[:-1]
figure() 
subplot(2,1,1) 
plot(w,abs(Y),lw=2) 
xlim([-15,15]) 
ylabel(r"$|Y|$",size=16) 
title(r"Spectrum of $\cos^3t$") 
grid(True) 
subplot(2,1,2) 
plot(w,angle(Y),'ro',lw=2)
ii=where(abs(Y)>1e-3) 
plot(w[ii],angle(Y[ii]),'go',lw=2)  
xlim([-15,15]) 
ylabel(r"Phase of $Y$",size=16) 
xlabel(r"$\omega$",size=16) 
grid(True) 

# task 3
t=linspace(-4*pi,4*pi,513)
t=t[:-1] 
y = cos(20*t+5*cos(t))
Y=fftshift(fft(y))/512.0 
w=linspace(-64,64,513)
w=w[:-1]
figure() 
subplot(2,1,1) 
plot(w,abs(Y),lw=2) 
xlim([-40,40]) 
ylabel(r"$|Y|$",size=16) 
title(r"Spectrum of $\cos\left(20t+5\cos\left(t\right)\right)$") 
grid(True) 
subplot(2,1,2)
ii=where(abs(Y)>1e-3) 
plot(w[ii],angle(Y[ii]),'go',lw=2)  
xlim([-40,40]) 
ylabel(r"Phase of $Y$",size=16) 
xlabel(r"$\omega$",size=16) 
grid(True) 
show()