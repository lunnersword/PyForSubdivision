from numpy import *

from util import transform
from util.shift import shift
from util.rawSurface import RawSurface
from util.surfacesToFiles import parseDetail, writeSurfaceToFile
from util.Revol_Tangent import Revol_Tangent


def blend2():
	order_u = 3
	order_v = 3
	u = cos(pi/4)

	revol_type1 = 'circular'
	tang_alpha1 = 0.3
	blend_num1 = 1
	(baseCP1, v1) = Revol_Tangent(revol_type1, tang_alpha1, blend_num1)

	rawCP1 = RawSurface(baseCP1, 'circular')
	rawCP1.blendCP = transform.move(rawCP1.blendCP, 'y', 2.5)

	revol_type1 = 'cone'
	baseCP1, v1 = Revol_Tangent(revol_type1, tang_alpha1, blend_num1)

	revol_type1 = 'hyperbola'
	baseCP2, v1 = Revol_Tangent(revol_type1, tang_alpha1, blend_num1)
	baseCP2 = transform.stretch(baseCP2, 0.1)
	baseCP2 = transform.move(baseCP2, 'y', -8)
	baseCP2 = shift(baseCP2, 2)
	
	revol_type1 = 'cylinder'
	baseCP3, v1 = Revol_Tangent(revol_type1, tang_alpha1, blend_num1)
	baseCP3 = transform.stretch(baseCP3, 5)
	baseCP3 = transform.flipdim(baseCP3, 0)
	baseCP3 = transform.move(baseCP3, 'y', -16.5)
	
	revol_type1 = 'parabola'
	baseCP4, v1 = Revol_Tangent(revol_type1, tang_alpha1, blend_num1)
	rawCP2 = RawSurface(baseCP1, 'parabola')
	rawCP2.blendCP = transform.flipdim(rawCP2.blendCP, 0)
	rawCP2.blendCP = transform.move(rawCP2.blendCP, 'y', -43.5)

	rawCP1.blendCP = vstack( (rawCP1.blendCP, baseCP1, baseCP2, baseCP3, rawCP2.blendCP) )
	rawCP1.name = 'allkinds'
	rawCP1.setSharpEdges([])
	rawCP1.blendCP = transform.move(rawCP1.blendCP, 'y', 30)
	return rawCP1

if __name__ == '__main__':
	rawCP = blend2()
	surface = parseDetail(rawCP)
	writeSurfaceToFile(surface)
