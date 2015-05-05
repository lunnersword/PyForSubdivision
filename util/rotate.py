from numpy import *
def rotateX(CP,theta):
	rotateCP = CP.copy()
	for i in range(6):
		
		#rotate the control polygon of the curve around x-axis
		rotateCP[:,i,1] = CP[:,i,1]*cos(theta) - CP[:,i,2]*sin(theta)
		rotateCP[:,i,2] = CP[:,i,1]*sin(theta) + CP[:,i,2]*cos(theta)
	return rotateCP

def rotateY(CP, theta):
	rotateCP = CP.copy()
	for i in range(6):
		#around y-axis
		
		rotateCP[:,i,0] = CP[:,i,0]*cos(theta) + CP[:,i,2]*sin(theta)
		rotateCP[:,i,2] = CP[:,i,0]*(-sin(theta)) + CP[:,i,2]*cos(theta)
	return rotateCP

def rotateZ(CP, theta):
	rotateCP = CP.copy()
	for i in range(6):
		#around z-axis
		
		rotateCP[:,i,0] = CP[:,i,0] * cos(theta) - CP[:,i,1] * sin(theta)
		rotateCP[:,i,1] = CP[:,i,0] * sin(theta) + CP[:,i,1] * cos(theta)
	return rotateCP

def rotateOrigin(CP, theta):
	rotateCP = CP.copy()
	for i in range(len(CP[:,0,0])):
		for j in range(6):
			r = srqt(CP[i,j,0]**2 + CP[i,j,1]**2)
			#rotate the control polygon of the curve around z-axis
			rotateCP[i,j,0] = r * cos(theta + atan(CP[i,j,1]/CP[i,j,0]))
			rotateCP[i,j,1] = r * sin(theta + atan(CP[i,j,1]/CP[i,j,0]))
	return rotateCP
def rotateOtherwise(CP,theta):
	print 'the axis_logo is undefined!'
	return Non
def rotate(CP, axis_logo='otherwise', theta=0):
	'''
	constructing a base surface by rotate shifts of above standard conics
	'''
	
	return {
	'x': rotateX,
	'y': rotateY,
	'z': rotateZ,
	'origin': rotateOrigin,
	'otherwise': rotateOtherwise
	}[axis_logo](CP,theta)
	
