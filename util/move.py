from numpy import *
def moveOnX(moveCP, dist):
	moveCP[:,:,0] += dist
def moveOnY(moveCP, dist):
	moveCP[:,:,1] += dist
def moveOnZ(moveCP, dist):
	moveCP[:,:,2] += dist
def printO(moveCP, dist):
	print 'move otherwise'
def move(CP, axis_logo='otherwise', dist=0):
	'''
	constructing a base surface by move shifts of above standard conics
	'''
	moveCP = CP.copy()
	
 	{
	'x': moveOnX,
	'y': moveOnY,
	'z': moveOnZ,
	'otherwise': lambda: printO
	}[axis_logo](moveCP,dist)
	return moveCP
