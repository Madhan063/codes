import sys
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
			print("")
			print("element id = ",a[i][0])
			print("element = Resistor")
			print("from node = ",a[i][1])
			print("to node = ",a[i][2])
			print("value = ",a[i][3])
		elif "L" in a[i][0]:
			a[i] = a[i][0:4]
			print("")
			print("element id = ",a[i][0])
			print("element = Inductor")
			print("from node = ",a[i][1])
			print("to node = ",a[i][2])
			print("value = ",a[i][3])	
		elif "C" in a[i][0]:
			a[i] = a[i][0:4]
			print("")
			print("element id = ",a[i][0])
			print("element = Capacitor")
			print("from node = ",a[i][1])
			print("to node = ",a[i][2])
			print("value = ",a[i][3])
		elif "I" in a[i][0]:
			a[i] = a[i][0:4]
			print("")
			print("element id = ",a[i][0])
			print("element = Independent Current Source")
			print("from node = ",a[i][1])
			print("to node = ",a[i][2])
			print("value = ",a[i][3])
		elif "V" in a[i][0]:
			a[i] = a[i][0:4]
			print("")
			print("element id = ",a[i][0])
			print("element = IndependentVoltage Source")
			print("from node = ",a[i][1])
			print("to node = ",a[i][2])
			print("value = ",a[i][3])
		elif "E" in a[i][0]:
			a[i] = a[i][0:6]
			print("")
			print("element id = ",a[i][0])
			print("element = Voltage Controlled Voltage Source")
			print("from node = ",a[i][1])
			print("to node = ",a[i][2])
			print("source from node = ",a[i][3])
			print("source to node = ",a[i][4])
			print("value = ",a[i][5])
		elif "G" in a[i][0]:
			a[i] = a[i][0:6]
			print("")
			print("element id = ",a[i][0])
			print("element = Voltage Controlled Current Source")
			print("from node = ",a[i][1])
			print("to node = ",a[i][2])
			print("source from node = ",a[i][3])
			print("source to node = ",a[i][4])
			print("value = ",a[i][5])
		elif "H" in a[i][0]:
			a[i] = a[i][0:5]
			print("")
			print("element id = ",a[i][0])
			print("element = Current Controlled Voltage Source")
			print("from node = ",a[i][1])
			print("to node = ",a[i][2])
			print("Voltage Source id = ",a[i][3])
			print("value = ",a[i][4])
		elif "F" in a[i][0]:
			a[i] = a[i][0:5]
			print("")
			print("element id = ",a[i][0])
			print("element = Current Controlled Current Source")
			print("from node = ",a[i][1])
			print("to node = ",a[i][2])
			print("Voltage Source id = ",a[i][3])
			print("value = ",a[i][4])
		else:
			print("")
			print("element id = ",a[i][0])
			print("The element does not exit.")

st = 0
en = 0
check = 5
exit = 0        

argv = sys.argv

if len(argv) != 2:			#checking for number of arguments
	print("Error!")
	print('expected 2 arguments but got %d'%len(argv))
	sys.exit(0)

while True:					# check for the presence of file 
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

F.close()				#closing the file once the lines in it are read
print("")

val_1 = []
for i in range(0, len(lines)):
	val_1.append(lines[i].split(" "))		#splitting each part of lines into parts based on spaces
	removing_new_line(val_1[i])				#removing \n if present at the end of the line

try:
	for i in range(0,len(val_1)):
		if (val_1[i][0] == ".circuit") :	#finding the starting index of the circuit
			st = i
			check = 0
	if check != 0:							#error to be raised if .circuit is not at the starting of a line
		raise MalformedFileError("The input file is not in correct format.")

	for i in range(0,len(val_1)):			#finding the end index of the circuit
		if (val_1[i][0] == ".end"):
			en = i
			check = 1
	if check != 1:							#error to be raised if .end is not the part of the circuit
		raise MalformedFileError("The input file is not in correct format.")

except MalformedFileError as m:
	print(m.data)
	sys.exit(0)

try:
	if st >= en:							#checking for .circuit to come before .end and error to be raised if this doesnot happens
		raise MalformedFileError("Invalid circuit defnition")
except MalformedFileError as m:
	print(m.data)
	sys.exit(0)	


if exit != 1:
	print("Startting of the circut at index ", st)				#printing the index of .circuit
	print("Ending of the circuit description at index ", en)	#printing the index of .end
	print("")

	val = val_1[st + 1:en - 1]
	element_analysis(val)										#printing about all the elements that are part of the circuit

	print("")
	print("Printing in reverse format:")
	print("")

	for i in range(0, len(val)):								#printing in reverse format
		for a in range(0, len(val[-1 - i])):
			print(val[-1 - i][-1 - a], end=" ")
		print("\n")