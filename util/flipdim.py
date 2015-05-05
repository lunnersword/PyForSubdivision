from numpy import *

def flipdim(array, dim):
	'''
	
	'''
	if dim >= array.ndim or dim < 0:
		return
	
	'''
	codestr =    ':,'*dim + '::-1,...' 
	code = 'print ' + codestr
	exec code
	dest = array.copy()
	m = array.shape[dim]
	if m <= 1:
		return dest
	#dest[...] = array[code]
	return dest
	'''
	m = array.shape[dim]
	if m <= 1:
		return array.copy()
	#dest = array.copy()
	if dim == 0:
		 
		dest[...] = array[::-1,...]
		return dest
	if dim == 1:
		
		dest[...] = array[:,::-1,...]
		return dest
		
		

	

	
