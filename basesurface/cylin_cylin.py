from scipy import *

from util import transform
from util.Revol_Tangent import Revol_Tangent

from util.rawSurface import RawSurface



def cylin_cylin():	
    #specify subdivision order & initial parameter
    order_u = 3
    order_v = 3
    u = cos(pi/4)

    revol_type1 = 'cylinder'
    tang_alpha1 = 0.3
    blend_num1 = 1
    (baseCP1, v1) = Revol_Tangent(revol_type1, tang_alpha1, blend_num1)

    axis_logo1 = 'x'
    dist1 = 0
    axis_logo2 = 'x'
    theta1 = 0
    size1 = 1

    revol_type2 = 'cylinder'
    tang_alpha2 = 0.3
    blend_num2 = 2

    (baseCP2, v2) = Revol_Tangent(revol_type2, tang_alpha2, blend_num2)

    axis_logo3 = 'y'
    dist2 = 1
    axis_logo4 = 'y'
    theta2 = pi/5
    size2 = 0.8

    baseCP2 = transform.move(baseCP2, 'y', 4)
    baseCP2 = transform.move(baseCP2, 'x', -3)

    baseCP2 = transform.rotate(baseCP2, 'z', -pi/3)
    baseCP2 = transform.stretch(baseCP2, size2)

    blendCP = vstack( (baseCP1, baseCP2) )

    print 'printing blendCP[:,:,0]:'
    print blendCP[:,:,0]
    rawCP = RawSurface(blendCP, 'cylin_cylin')
    rawCP.setSharpEdges([0, -1])

    return rawCP


if __name__ == '__main__':
    '''
    blendCP = cylin_cylin()
    import pylab
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    fig = pylab.figure()
    ax = Axes3D(fig)
    t = transpose
    ax.plot_surface(blendCP[:,:,0], blendCP[:,:,1], blendCP[:,:,2], rstride = 1, cstride = 1, cmap = cm.jet)	#plot3(blendCP[:,:,0], blendCP[:,:,1], blendCP[:,:,2], 'b-')
    #ax.plot_surface(t(blendCP[:,:,0]), t(blendCP[:,:,1]), t(blendCP[:,:,2]), rstride=1, cstride=1,cmap=cm.jet)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    pylab.show()
    '''
    #we write the surface to file
    from util.surfacesToFiles import parseDetail, writeSurfaceToFile

    rawCP = cylin_cylin()

    surface = parseDetail(rawCP)
    writeSurfaceToFile(surface)
