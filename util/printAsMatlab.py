from numpy import ndarray
def printAsMatlab(blendCP):
	if type(blendCP) is not ndarray:
		print 'not ndarray'
		return
	print 'blendCP[:,:,0]'
	print blendCP[:,:,0]
	print '\n'
	print 'blendCP[:,:,1]'
	print blendCP[:,:,1]
	print '\n'
	print 'blendCP[:,:,2]'
	print blendCP[:,:,2]
	print '\n'
