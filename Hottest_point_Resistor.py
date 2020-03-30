# importing libraries
import numpy as np
from pylab import * 
import mpl_toolkits.mplot3d.axes3d as p3

# parameters defnition
if len(sys.argv) == 5:
	Nx = int(sys.argv[1])
	Ny = int(sys.argv[2])
	radius = int(sys.argv[3])
	Niter = int(sys.argv[4])
	print('from given values')
else:
	Nx=25 		# size along x 
	Ny=25		# size along y 
	radius=8	# radius of central lead 
	Niter=1500 	# number of iterations to perform
	print('by defalut values')
lx = 0.5		# x half length of the plate
ly = 0.5		# y half length of the plate


phi = np.zeros((Ny,Nx), dtype = 'float')		# defining phi matrix
x = np.linspace(-lx,lx,Nx)						# defining x line space
y = np.linspace(-ly,ly,Ny)						# defining y line space
Y,X=meshgrid(y,x)
ind_x,ind_y = np.where(X**2+Y**2<=0.35*0.35)		# array with indices that satisfy the given cindition
phi[ind_x,ind_y] = 1							# updating the matrix phi with the values of points with 1V potential
ab = phi.copy()

# contour plot
plt.contour(Y,X[::-1],phi)
plt.xlabel('X-->')
plt.ylabel('Y-->')
plt.title('contour plot of potential')
plt.scatter(X,Y,ab*20,'r')
plt.show()

error = np.zeros(Niter)							# creating an array to store error in each iteration

for k in range(Niter):
	oldphi = phi.copy()							# saving a copy of phi for future refrence
	phi[1:-1,1:-1] = 0.25*(phi[1:-1,0:-2]+phi[1:-1,2:]+phi[2:,1:-1]+phi[0:-2,1:-1])		# updating phi array
	# Boundary conditions
	phi[1:-1,0] = phi[1:-1,1]
	phi[1:-1,-1] = phi[1:-1,-2]
	phi[0,1:-1] = phi[1,1:-1]
	phi[-1,1:-1] = 0
	phi[ind_x,ind_y] = 1
	error[k] = (abs(phi-oldphi)).max()

# Graph results
#Error semilog and loglog plot
plt.semilogy(range(0,Niter),error,'r', label = 'whole data')
plt.semilogy(range(0,Niter,50),error[::50],'ro', label = 'every 50th point')
plt.xlabel('k')
plt.ylabel('Error[k]')
plt.title('Error[k] semilogy plot')
plt.legend()
plt.show()

plt.loglog(range(Niter),error, label = 'whole data')
plt.loglog(range(0,Niter,50),error[::50],'ro', label = 'every 50th point')
plt.xlabel('k')
plt.ylabel('Error[k]')
plt.title('Error[k] loglog plot')
plt.legend()
plt.show()

# curve fitting

#actual error plot
plt.plot(range(0,Niter),np.log(error),'b',label = 'error curve')
#fit1
x_data = range(0,Niter)
y_data = error							
z = np.polyfit(x_data,np.log(y_data),1)
p = np.poly1d(z)
plt.plot(x_data[::50],p(x_data[::50]),'ro',label = 'fit1')				# plotting every 50th point to check coincience
#fit2
x_data = range(501,Niter)
y_data = error[501:]
z = np.polyfit(x_data,np.log(y_data),1)
p = np.poly1d(z)
plt.plot(x_data[501::100],p(x_data[501::100]),'gs',label = 'fit2')				# plotting every 100th point for visual clarity and also to check coincidence
plt.title('Error plot and best fit error plots in semilogy scale using np.polyfit() function')
plt.legend()
plt.show()

# curve fitting using numpy.linalg.lstsq
#actual error plot
plt.plot(range(0,Niter),np.log(error),'b',label = 'error curve')
#fit1
x_data = range(0,Niter)
A = np.vstack([x_data, np.ones(len(x_data))]).T
y_data = np.log(error)
m1,c1 = np.linalg.lstsq(A, y_data, rcond=None)[0]
plt.plot(x_data[::50],m1*x_data[::50]+c1,'ro',label = 'fit1')
#fit2
x_data = range(501,Niter)
A = np.vstack([x_data, np.ones(len(x_data))]).T
y_data = np.log(error[501:])
m2,c2 = np.linalg.lstsq(A, y_data, rcond=None)[0]
plt.plot(x_data[501::100],m2*x_data[501::100]+c2,'gs',label = 'fit2')
plt.title('Error plot and best fit error plots in semilogy scale using lstsq function')
plt.legend()
plt.show()

# surface plot
fig1=figure(6) # open a new figure 
ax=p3.Axes3D(fig1) # Axes3D is the means to do a surface plot 
plt.title('The 3-D surface plot of the potential') 
surf = ax.plot_surface(Y, X, phi.T, rstride=1, cstride=1, cmap=cm.jet,linewidth=0, antialiased=False)
plt.show()

# contour plot of potential
plt.contourf(Y,X[::-1],phi)
plt.xlabel('X-->')
plt.ylabel('Y-->')
plt.title('contour plot of potential')
plt.scatter(X,Y,ab*20,'r')
plt.colorbar()
plt.show()


# current plots
jx = 0.5*phi[1:-1,0:-2]-0.5*phi[1:-1,2:]
jy = 0.5*phi[0:-2,1:-1]-0.5*phi[2:,1:-1]
plt.quiver(Y[1:-1,1:-1],-X[1:-1,1:-1],-jx[:,::-1],-jy)
plt.scatter(X,Y,ab*20,'r')
plt.title('current flow vector plot')
plt.show()