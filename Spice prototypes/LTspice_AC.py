import sys
import numpy as np
from cmath import *
class UnAcceptedValueError(Exception):
	def __init__(self, data):
		self.data = data
	def __str__(self):
		return repr(self.data)

class MalformedFileError(Exception):
	def __init__(self, data):
		self.data = data
	def __str__(self):
		return repr(self.data)

def removing_new_line(b):
	for i in range(0,len(b)):
		if "\n" in b[i]:
			ind = b[i].index("\n")
			b[i] = b[i][0:ind]
	
def element_analysis(a):
	for i in range(0,len(a)):
		if "R" in a[i][0]:
			a[i] = a[i][0:4]
		elif "L" in a[i][0]:
			a[i] = a[i][0:4]
		elif "C" in a[i][0]:
			a[i] = a[i][0:4]
		elif "I" in a[i][0]:
			if a[i][3] == 'ac':
				a[i] = a[i][0:6]
			elif a[i][3] == 'dc':
				a[i] = a[i][0:5]
			else:
				a[i] = a[i][0:4]
		elif "V" in a[i][0]:
			if a[i][3] == 'ac':
				a[i] = a[i][0:6]
			elif a[i][3] == 'dc':
				a[i] = a[i][0:5]
			else:
				a[i] = a[i][0:4]
		elif "E" in a[i][0]:
			a[i] = a[i][0:6]
		elif "G" in a[i][0]:
			a[i] = a[i][0:6]
		elif "H" in a[i][0]:
			a[i] = a[i][0:5]
		elif "F" in a[i][0]:
			a[i] = a[i][0:5]

st = 0
en = 0
ind_ac = 0
check = 5
exit = 0        

argv = sys.argv

if len(argv) != 2:
	print("Error!")
	print('required 2 arguments but got %d'%len(argv))
	sys.exit(0)

while True:
	try:
		if bool(argv[1]) == True:			
			F = open(argv[1])
			lines = F.readlines()
			break
		else: 
			file_name = input('enter file name: ')
			if(len(file_name) == 0):
				raise UnAcceptedValueError("File name not entered. Try again...")
			F = open(file_name)
			lines = F.readlines()
			break
	except UnAcceptedValueError as e:
		print(e.data)
		
	except FileNotFoundError:
		argv[1] = 0
		print("Oops!  There is no file on that name.  Try again...")

F.close()
print("")

val_1 = []
for i in range(0, len(lines)):
	val_1.append(lines[i].split(" "))
	removing_new_line(val_1[i])

try:
	for i in range(0,len(val_1)):
		if (val_1[i][0] == ".circuit") :
			st = i
			check = 0
	if check != 0:
		raise MalformedFileError("The input circuit is not in correct format.")

	for i in range(0,len(val_1)):
		if (val_1[i][0] == ".end"):
			en = i
			check = 1
	if check != 1:
		raise MalformedFileError("The input ckt is not in correct format.")
	for i in range(0,len(val_1)):
		if val_1[i][0] == '.ac':
			ind_ac = i
except MalformedFileError as m:
	print(m.data)
	sys.exit(0)
if ind_ac!= 0:		
	ac_freq = val_1[ind_ac][0:3]
	freq = float(ac_freq[2])
	w = 2*pi*freq
else:
	ind_ac = en+1
try:
	if st >= en:
		raise MalformedFileError("Invalid circuit defnition a")
	if ind_ac<= st or ind_ac <= en:
		raise MalformedFileError("Invalid circuit defnition b")
except MalformedFileError as m:
	print(m.data)
	sys.exit(0)	


if exit != 1:
	val = val_1[st + 1:en]	
	element_analysis(val)

# week_2



class component:

	d_st_node = "NULL"							#definig component class
	d_en_node = "NULL"

	def __init__(self,name,st_node,en_node,d_st_node,d_en_node,in_src_id,value,s_type,phase):
		self.name = name
		self.st_node = st_node
		self.en_node = en_node
		self.d_st_node = d_st_node
		self.d_en_node = d_en_node
		self.in_src_id = in_src_id
		self.value = value
		self.s_type = s_type
		self.phase = phase
		
def value_update(a):

	value = a.value
	value = value.split('e')						# changing value of components to float and if source is ac 
	if len(value) == 2:								# it to phasor and updating the value back to the object
		value = float(value[0])*10**int(value[1])
		a.value = value
	elif len(value) == 1:
		value = float(value[0])
	if (a.name[0] == 'V' or a.name[0] == 'I') and a.s_type == 'ac':
		value = float(value)
		phase = float(a.phase)
		value = complex(value*cos((phase*pi)/180),value*sin((phase*pi)/180))
		a.value = value
		
	return value	

	

obj = []
volt = []
r,l,c,v,i_1,e,g,h,f = 0,0,0,0,0,0,0,0,0
nodes = []

for i in range(0,len(val)):
	nodes.append(val[i][1])
	nodes.append(val[i][2])
nodes = list(dict.fromkeys(nodes))							#extracting distinct nodes in the circuit
dict_1 = {}
c_gnd = 1
for n in nodes:
	if n == 'GND':
		for i in range(0,len(nodes)):
			if nodes[i] == 'GND':
				dict_1[nodes[i]] = 0
				nodes.remove('GND')
				break										#if ground in circuit it is taken as refernce node and
		for i in range(0,len(nodes)):						# remaing nodes numbered further if no ground node in 
			dict_1[nodes[i]] = i+1							# circuit fixing a node as zero node and assigning nodes to
			c_gnd = 1										# corresponding matrix
if c_gnd != 1:
	for i in range(0,len(nodes)):
			dict_1[nodes[i]] = i

for i in range(0,len(val)):
	if val[i][0][0] == 'R':
		obj.append(component(val[i][0],dict_1[val[i][1]],dict_1[val[i][2]],'','','',val[i][3],'',''))
		r = r+1
	if val[i][0][0] == 'L':
		obj.append(component(val[i][0],dict_1[val[i][1]],dict_1[val[i][2]],'','','',val[i][3],'',''))		#updating elements by creating component object to each
		l =l+1																								# component and storing them in a list for further refrence
	if val[i][0][0] == 'C':
		obj.append(component(val[i][0],dict_1[val[i][1]],dict_1[val[i][2]],'','','',val[i][3],'',''))
		c = c+1
	if val[i][0][0] == 'V':
		if val[i][3] == 'ac':
			obj.append(component(val[i][0],dict_1[val[i][1]],dict_1[val[i][2]],'','','',val[i][4],val[i][3],val[i][5]))
			v = v+1
			volt.append(val[i][0])
		elif val[i][3] == 'dc':
			obj.append(component(val[i][0],dict_1[val[i][1]],dict_1[val[i][2]],'','','',val[i][4],val[i][3],''))
			v = v+1
			volt.append(val[i][0])
		else:
			obj.append(component(val[i][0],dict_1[val[i][1]],dict_1[val[i][2]],'','','',val[i][3],'',''))
			v = v+1
			volt.append(val[i][0])
	if val[i][0][0] == 'I':
		if val[i][3] == 'ac':
			obj.append(component(val[i][0],dict_1[val[i][1]],dict_1[val[i][2]],'','','',val[i][4],val[i][3],val[i][5]))
			i_1 = i_1+1
		elif val[i][3] == 'dc':
			obj.append(component(val[i][0],dict_1[val[i][1]],dict_1[val[i][2]],'','','',val[i][4],val[i][3],''))
			i_1 = i_1+1
		else:
			obj.append(component(val[i][0],dict_1[val[i][1]],dict_1[val[i][2]],'','','',val[i][3],'',''))
			i_1 = i_1+1
	if val[i][0][0] == 'E':
		obj.append(component(val[i][0],dict_1[val[i][1]],dict_1[val[i][2]],dict_1[val[i][3]],dict_1[val[i][4]],'',val[i][5],'',''))
		e = e+1
	if val[i][0][0] == 'G':
		obj.append(component(val[i][0],dict_1[val[i][1]],dict_1[val[i][2]],dict_1[val[i][3]],dict_1[val[i][4]],'',val[i][5],'',''))
		g = g+1
	if val[i][0][0] == 'H':
		obj.append(component(val[i][0],dict_1[val[i][1]],dict_1[val[i][2]],'','',val[i][3],val[i][4],'',''))
		h = h+1
	if val[i][0][0] == 'F':
		obj.append(component(val[i][0],dict_1[val[i][1]],dict_1[val[i][2]],'','',val[i][3],val[i][4]),'','')
		f = f+1

for i in range(len(obj)):
	obj[i].value = value_update(obj[i])

val_dict = list(dict_1.values())
dist_val = list(dict.fromkeys(val_dict))



length = len(dist_val)+v
M = np.zeros((length,length), dtype = complex)				#creating both M and b np arrays
b= np.zeros(length, dtype = complex)
dist = len(dist_val)
k=0
#filling of the impediances in their respective positions
for i in range(1,len(dist_val)):
	for n in range(0,len(obj)):
		if obj[n].st_node == i  or obj[n].en_node == i:
			if obj[n].st_node == i:
				
				if obj[n].name[0] == 'R':
					M[i][i] = M[i][i] + (float(obj[n].value))**-1
					clm = obj[n].en_node
					M[i][clm] = M[i][clm] - (float(obj[n].value))**-1

				elif obj[n].name[0] == 'V':
					clm = obj[n].en_node
					k = volt.index(obj[n].name)
					M[i][dist+k] = M[i][dist+k] + 1
					M[dist+k][i] = M[dist+k][i] + 1
					M[dist+k][clm] = M[dist+k][clm] - 1
					b[dist+k] = b[dist+k] + obj[n].value

				elif obj[n].name[0] == 'I':
					b[i] = b[i]-obj[n].value
				elif obj[n].name[0] == 'C':
					z = complex(0,-(w*obj[n].value)**-1)
					M[i][i] = M[i][i] + (z)**-1 
					clm = obj[n].en_node
					M[i][clm] = M[i][clm] - (z)**-1
				elif obj[n].name[0] == 'L':
					z = complex(0,w*obj[n].value)
					M[i][i] = M[i][i] + (z)**-1 
					clm = obj[n].en_node
					M[i][clm] = M[i][clm] - (z)**-1

			if obj[n].en_node == i:
				
				if obj[n].name[0] == 'R':
					clm = obj[n].st_node
					M[i][i] = M[i][i] + (float(obj[n].value))**-1 
					M[i][clm] = M[i][clm] - (float(obj[n].value))**-1

				elif obj[n].name[0] == 'V':
					clm = obj[n].st_node
					k = volt.index(obj[n].name)
					M[i][len(dist_val)+k] = M[i][len(dist_val)+k] - 1
					M[len(dist_val)+k][i] = M[len(dist_val)+k][i] - 1 
					M[len(dist_val)+k][clm] = M[len(dist_val) + k][clm]+1
					b[len(dist_val)+k] = b[len(dist_val)+k] + obj[n].value
				
				elif obj[n].name[0] == 'I':
					b[i] = b[i]+obj[n].value
				elif obj[n].name[0] == 'C':
					z = complex(0,-(w*obj[n].value)**-1)
					M[i][i] = M[i][i] + (z)**-1 
					clm = obj[n].st_node
					M[i][clm] = M[i][clm] - (z)**-1
				elif obj[n].name[0] == 'L':
					z = complex(0,w*obj[n].value)
					M[i][i] = M[i][i] + (z)**-1 
					clm = obj[n].st_node
					M[i][clm] = M[i][clm] - (z)**-1
M[0][0] = 1
b[0] = 0 

try:
	x = np.linalg.solve(M,b)
except np.linalg.LinAlgError:
	print('Singular Matrix cannot be inverted')
a = list(dict_1)
for i in range(len(dist_val)):
	print('V-%d node-%s = %f+%fj'%(i,a[i],x[i].real,x[i].imag))
for i in range(0,len(volt)):
	print('I-%d in %s = %f+%fj'%(i,volt[i],x[len(dist_val)+i].real,x[len(dist_val)+i].imag))