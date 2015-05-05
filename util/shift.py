from numpy import *

def shift(blendCP, step):
	
	if type(blendCP) is not ndarray:
		raise TypeError
	jlen = len(blendCP[0,:,0])
	step = step % jlen
	if step <= 0:
		return blendCP
	'''
	cp = blendCP.copy()
	cp[:,0:step:,:] = blendCP[:,-step::,:]
	cp[:,step::,:] = blendCP[:,0:-step:,:]
	return cp
	'''
	for j in range(step):
		temp = blendCP[:,0,:]
		for i in range(jlen-1):
			blendCP[:,i,:] = blendCP[:,i+1,:]
		blendCP[:,i,:] = temp
	return blendCP
