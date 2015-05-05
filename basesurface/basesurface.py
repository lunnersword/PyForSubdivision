__author__ = 'lunner'
from numpy import *
from util import transform
from util.Revol_Tangent import Revol_Tangent
from util.rawSurface import RawSurface
from util.surfacesToFiles import parseDetail, writeSurfaceToFile

class BaseSurface:
    def __init__(self):
        List = ['cone', 'cylinder', 'circular', 'hyperbola', 'parabola']
        dDict = {'cone': [0], 'cylinder': [0,-1], 'circular': [], 'hyperbola': [0, -1], 'parabola': [0]}
        dDict['cone']
        parameters = []
        self.blendCPs = {}
        self.rawSurfaces = {}
        self.surfaces = {}
        for typestr in List:
            Dict = {}
            Dict['revol_type'] = typestr
            Dict['tang_alpha'] = 0.3
            Dict['blend_num'] = 0
            parameters.append(Dict)

        for param in parameters:
            blendCP,u = Revol_Tangent(**param)
            'temp = blendCP.copy()'
            if param['revol_type'] == 'cylinder':
                blendCP = transform.move(blendCP, 'y', 0.785398163397)


            self.blendCPs[param['revol_type']] = blendCP

            rawSurface = RawSurface(blendCP, param['revol_type'])
            rawSurface.setSharpEdges(dDict[rawSurface.name])
            self.rawSurfaces[param['revol_type']] = rawSurface

            self.surfaces[param['revol_type']] = parseDetail(rawSurface)

    def blendCP(self, typestr):
        return self.blendCPs[typestr].copy()

    def rawSurfac(self, typestr):
        return self.rawSurfaces[typestr]

    def surface(self, typestr):
        return self.surfaces[typestr]

    def figure(self, typestr):
        blendCP = self.blendCPs[typestr]
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

    def figureBlendCP(self, blendCP):
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


    def writeToFile(self, typestr):
        writeSurfaceToFile(self.surfaces[typestr])

if __name__ == '__main__':
    surfaces = BaseSurface()
    "for str in ['cone', 'cylinder', 'circular', 'hyperbola', 'parabola']:"
    ttype = 'circular'
    p = surfaces.blendCP('circular')
    print(p)
    surfaces.figure(ttype)
    surfaces.writeToFile(ttype)