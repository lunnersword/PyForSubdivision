from numpy import *

from util import move, Revol_Tangent
from util.stretch import stretch
from util.rawSurface import RawSurface
from util.surfacesToFiles import parseDetail, writeSurfaceToFile


def blend1():
	order_u = 3
	order_v = 3
	u = cos(pi/4)

	revol_type1 = 'circular'
	tang_alpha1 = 0.3
	blend_num1 = 1
	(baseCP1, v1) = Revol_Tangent(revol_type1, tang_alpha1, blend_num1)
	(baseCP2, v1) = Revol_Tangent(revol_type1, tang_alpha1, blend_num1)
	
	rawCP1 = RawSurface(baseCP1, 'circular')
	rawCP2 = RawSurface(baseCP2, 'circular')
	
	rawCP1.blendCP = stretch(rawCP1.blendCP, 20)
	rawCP1.blendCP = move(rawCP1.blendCP, 'y', 65)
	
	rawCP2.blendCP = stretch(rawCP2.blendCP, 20)
	rawCP2.blendCP = move(rawCP2.blendCP, 'y', -65)

	revol_type2 = 'hyperbola'
	tang_alpha2 = 0.3
	blend_num2 = 2

	baseCP3, v2 = Revol_Tangent(revol_type2, tang_alpha2, blend_num2)
	
	rawCP1.blendCP = vstack( (rawCP1.blendCP, baseCP3, rawCP2.blendCP) )
	rawCP1.name = 'cir-hyper-cir'
	rawCP1.setSharpEdges([])
	return rawCP1

if __name__ == '__main__':
	rawCP = blend1()
	surface = parseDetail(rawCP)
	writeSurfaceToFile(surface)
