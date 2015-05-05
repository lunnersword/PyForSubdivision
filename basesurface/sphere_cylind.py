from numpy import *

from util import transform
from util.Revol_Tangent import Revol_Tangent
from util.rawSurface import RawSurface
from util.surfacesToFiles import parseDetail, writeSurfaceToFile


def sphere_cylind():
    order_u = 3
    order_v = 3
    u = cos(pi/4)

    revol_type1 = 'circular'
    tang_alpha1 = 0.3
    blend_num1 = 1
    (baseCP1, v1) = Revol_Tangent(revol_type1, tang_alpha1, blend_num1)

    rawCP1 = RawSurface(baseCP1, 'circular')
    rawCP1.blendCP = transform.flipdim(rawCP1.blendCP, 0)
    #rawCP1.blendCP = flipdim(rawCP1.blendCP, 1)
    rawCP1.blendCP = transform.shift(rawCP1.blendCP, 2)
    surface = parseDetail(rawCP1)
    writeSurfaceToFile(surface)

    axis_logo1 = 'x'
    dist1 = 0
    axis_logo2 = 'x'
    theta1 = 0
    size1 = 1

    revol_type2 = 'cylinder'
    tang_alpha2 = 0.3
    blend_num2 = 2
    (baseCP2, v2 ) = Revol_Tangent(revol_type2, tang_alpha2, blend_num2)

    axis_logo3 = 'y'
    dist2 = 2
    axis_logo4 = 'z'
    theta2 = pi/6
    size2 = 0.8

    baseCP2 = transform.move(baseCP2, 'y', 6)
    baseCP2 = transform.move(baseCP2, 'x', -3)

    baseCP2 = transform.stretch(baseCP2, size2)

    rawCP2 = RawSurface(baseCP2, 'cylinder')
    rawCP1.blendCP = vstack( (rawCP1.blendCP, rawCP2.blendCP) )
    rawCP1.name = 'sphere_cylind'
    print rawCP1.sharpEdges
    rawCP1.setSharpEdges([-1])
    print rawCP1.sharpEdges
    return rawCP1
	

if __name__ == '__main__':
    '''
    blendCP = sphere_cylind()
    import pylab
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    fig = pylab.figure()
    ax = Axes3D(fig)
    t = transpose
    ax.plot_surface(blendCP[:,:,0], blendCP[:,:,1], blendCP[:,:,2], rstride = 1, cstride = 1, cmap = cm.jet)#plot3(blendCP[:,:,0], blendCP[:,:,1], blendCP[:,:,2], 'b-')
    ax.plot_surface(t(blendCP[:,:,0]), t(blendCP[:,:,1]), t(blendCP[:,:,2]), rstride=1, cstride=1,cmap=cm.jet)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    pylab.show()
    '''
    #rawCP = RawSurface(sphere_cylind(), 'sphere_cylind')
    #rawCP.setSharpEdges([0,-1])
    rawCP = sphere_cylind()

    surface = parseDetail(rawCP)
    writeSurfaceToFile(surface)
