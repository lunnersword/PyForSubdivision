from scipy import *

from util import transform

from util.rawSurface import RawSurface
from util.Revol_Tangent import Revol_Tangent

def hyper_hyper():
	order_u = 3
	order_v = 3
	u = cos(pi/4)

	revol_type1 = 'hyperbola'
	tang_alpha1 = 0.3
	blend_num1 = 1
	baseCP1, v1 = Revol_Tangent(revol_type1, tang_alpha1, blend_num1)
	
	
	axis_logo1 = 'x'
	dist1 = 0
	axis_logo2 = 'x'
	theta1 = 0
	size1 = 1
	
	moveCP1 = transform.move(baseCP1, axis_logo1, dist1)
	rotateCP1 = transform.rotate(moveCP1, axis_logo2, theta1)
	baseCP1 = transform.stretch(rotateCP1, size1)
	
	
	revol_type2 = 'hyperbola'
	tang_alpha2 = 0.3
	blend_num2 = 2
	baseCP2, v2 = Revol_Tangent(revol_type2, tang_alpha2, blend_num2)
	

	axis_logo3 = 'y'
	dist2 = -45
	axis_logo4 = 'z'
 	theta2 = pi
	size2 = 1
	rotateCP2 = transform.rotate(baseCP2, axis_logo4, theta2)
	moveCP2 = transform.move(rotateCP2, axis_logo3, dist2)
	baseCP2 = transform.stretch(moveCP2, size2)
	
	baseCP2 = transform.flipdim(baseCP2,1)
	
	blendCP = vstack( (baseCP1, baseCP2) )

	return blendCP
	


if __name__ == '__main__':
	'''
	blendCP = hyper_hyper()
	printAsMatlab(blendCP)	

	import pylab
	from mpl_toolkits.mplot3d import Axes3D
	from matplotlib import cm
	fig = pylab.figure()
	ax = Axes3D(fig)
	t = transpose
	ax.plot_surface(blendCP[:,:,0], blendCP[:,:,1], blendCP[:,:,2], rstride=1, cstride=1, cmap=cm.jet)
	ax.plot_surface(t(blendCP[:,:,0]), t(blendCP[:,:,1]), t(blendCP[:,:,2]), rstride=1, cstride=1, cmap=cm.jet)
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	pylab.show()
	'''
	rawCP = RawSurface(hyper_hyper(), 'hyper_hyper')
	rawCP.setSharpEdges([0, -1])
	from util.surfacesToFiles import parseDetail, writeSurfaceToFile
	surface = parseDetail(rawCP)
	writeSurfaceToFile(surface)
