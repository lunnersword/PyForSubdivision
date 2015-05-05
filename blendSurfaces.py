__author__ = 'lunner'
from numpy import *
from topology import Topology
from basesurface.basesurface import *

mode = 'CC'

def blendSixCylinder():
    baseSurfaces = BaseSurface()
    blend0 = baseSurfaces.blendCP('cylinder')
    blend0 = transform.move(blend0, 'y', 3.5)



    raw = RawSurface(blend0, 'cylinder')
    raw.setSharpEdges([-1])
    top1 = Topology.create(raw)


    blend2 = transform.rotate(blend0, 'z', -pi/3)
    raw = RawSurface(blend2, 'cylinder')
    raw.setSharpEdges([-1])

    top2 = Topology.create(raw)

    blend3 = transform.rotate(blend0, 'z', -2*pi/3.0)
    raw = RawSurface(blend3, 'cylinder')
    raw.setSharpEdges([-1])
    top3 = Topology.create(raw)

    blend4 = transform.rotate(blend0, 'z', -pi)
    raw = RawSurface(blend4, 'cylinder')
    raw.setSharpEdges([-1])
    top4 = Topology.create(raw)

    blend5 = transform.rotate(blend0, 'z', -4*pi/3)
    raw = RawSurface(blend5, 'cylinder')
    raw.setSharpEdges([-1])
    top5 = Topology.create(raw)

    blend6 = transform.rotate(blend0, 'z', -5*pi/3)
    raw = RawSurface(blend6, 'cylinder')
    raw.setSharpEdges([-1])
    top6 = Topology.create(raw)

    surfaces = [top1, top2, top3, top4, top5, top6]
    tops = [2, 2, 2, 2, 2, 2]
    bottoms = [0, 0, 0, 0, 0, 0]
    aref = [1.5, 1.5]
    arefs = [0.5, 0.5]
    taref = [0.2, 0.2]
    name = 'sixCylinder' + mode
    #mode = 'DS'
    topology = Topology.blendSurfaces(surfaces,tops, bottoms, aref, arefs, taref, name, mode)

    topology.writeToFile()



def blendThreeCylinder():
    baseSurfaces = BaseSurface()
    blend1 = baseSurfaces.blendCP('cylinder')
    blend1 = transform.rotate(blend1, 'z', -pi/4.0)
    blend1 = transform.move(blend1, 'x', 1.5)
    blend1 = transform.move(blend1, 'y', 2)


    raw = RawSurface(blend1, 'cylinder')
    raw.setSharpEdges([-1])


    top1 = Topology.create(raw)

    blend2 = baseSurfaces.blendCP('cylinder')
    blend2 = transform.rotate(blend2, 'z', -3.0*pi/4.0)
    blend2 = transform.move(blend2, 'x', 1.5)
    blend2 = transform.move(blend2, 'y', -2)


    raw = RawSurface(blend2, 'cylinder')
    raw.setSharpEdges([-1])

    top2 = Topology.create(raw)

    blend3 = baseSurfaces.blendCP('cylinder')
    blend3 = transform.rotate(blend3, 'z', pi/2.0)
    blend3 = transform.move(blend3, 'x', -3)


    raw = RawSurface(blend3, 'cylinder')
    raw.setSharpEdges([-1])

    top3 = Topology.create(raw)

    surfaces = [top1, top2, top3]
    tops = [2, 2, 2]
    bottoms = [0, 0, 0]
    aref = [0.5, 0.5]
    arefs = [0.5, 0.5]
    taref = [0.1, 0.1]
    name = 'threeCylinder' + mode
    #mode = 'DS'
    topology = Topology.blendSurfaces(surfaces,tops, bottoms, aref, arefs, taref, name, mode)

    topology.writeToFile()

def blendThreeCylinderNonFlat():
    baseSurfaces = BaseSurface()
    blend0 = baseSurfaces.blendCP('cylinder')
    blend1 = transform.rotate(blend0, 'x', pi/8.0)
    blend1 = transform.rotate(blend1, 'z', -pi/4.0)
    blend1 = transform.move(blend1, 'x', 1.5)
    blend1 = transform.move(blend1, 'y', 2)


    raw = RawSurface(blend1, 'cylinder')
    raw.setSharpEdges([-1])


    top1 = Topology.create(raw)

    blend2 = transform.rotate(blend0, 'x', pi/8.0)
    blend2 = transform.rotate(blend2, 'z', -3.0*pi/4.0)
    blend2 = transform.move(blend2, 'x', 1.5)
    blend2 = transform.move(blend2, 'y', -2)


    raw = RawSurface(blend2, 'cylinder')
    raw.setSharpEdges([-1])

    top2 = Topology.create(raw)

    '''
    blend3 = transform.rotate(blend0, 'x', pi/8.0)
    blend3 = transform.rotate(blend3, 'z', pi/2.0)
    blend3 = transform.move(blend3, 'x', -3)
    '''
    blend3 = baseSurfaces.blendCP('circular')
    blend3 = transform.rotate(blend3, 'x', pi/8)
    blend3 = transform.rotate(blend3, 'z', pi/2)
    blend3 = transform.move(blend3, 'x', -3)


    raw = RawSurface(blend3, 'circular')
    raw.setSharpEdges([])

    top3 = Topology.create(raw)

    surfaces = [top1, top2, top3]
    tops = [2, 2, 2]
    bottoms = [0, 0, 0]
    aref = [2.1, 1.3]
    arefs = [0.8, 0.5]
    taref = [0.1, 0.2]
    name = 'threeCylinderNonFlat' + mode
    #mode = 'CC'
    topology = Topology.blendSurfaces(surfaces,tops, bottoms, aref, arefs, taref, name, mode)

    topology.writeToFile()


def blendThreeHyperbola():
    baseSurfaces = BaseSurface()
    blend0 = baseSurfaces.blendCP('hyperbola')
    blend1 = transform.rotate(blend0, 'z', -pi/4)
    blend1 = transform.move(blend1, 'x', 70)
    blend1 = transform.move(blend1, 'y', 80)
    raw = RawSurface(blend1, 'hyperbola')
    raw.setSharpEdges([-1])
    top1 = Topology.create(raw)

    blend2 = transform.rotate(blend0, 'z', -3*pi/4)
    blend2 = transform.move(blend2, 'x', 70)
    blend2 = transform.move(blend2, 'y', -80)
    raw = RawSurface(blend2, 'hyperbola')
    raw.setSharpEdges([-1])
    top2 = Topology.create(raw)

    blend3 = transform.rotate(blend0, 'z', pi/2)
    blend3 = transform.move(blend3, 'x', -70)
    raw = RawSurface(blend3, 'hyperbola')
    raw.setSharpEdges([-1])
    top3 = Topology.create(raw)

    surfaces = [top1, top2, top3]

    tops = [0, 0, 0]
    bottoms = [2, 2, 2]
    aref = [3, 3] #centerPoints
    arefs = [1, 1] #grooves
    taref = [0.2, 0.2] #offsetCenterPoints
    name = 'threeHyperbola'+mode
    #mode = 'CC' #'DS'
    topology = Topology.blendSurfaces(surfaces,tops, bottoms, aref, arefs, taref, name, mode)

    topology.writeToFile()


def blendThreeParabola():
    baseSurfaces = BaseSurface()
    blend0 = baseSurfaces.blendCP("parabola")
    blend0 = transform.move(blend0, 'y', 20)
    raw = RawSurface(blend0, 'parabola')
    raw.setSharpEdges([])
    top1 = Topology.create(raw)

    blend2 = transform.rotate(blend0, 'z', -2*pi/3)
    raw = RawSurface(blend2, 'parabola')
    raw.setSharpEdges([])
    top2 = Topology.create(raw)

    blend3 = transform.rotate(blend0, 'z', -4*pi/3)
    raw = RawSurface(blend3, 'parabola')
    raw.setSharpEdges([])
    top3 = Topology.create(raw)

    surfaces = [top1, top2, top3]
    tops = [2, 2, 2]
    bottoms = [0, 0, 0]
    aref = [2.5, 2.5]
    arefs = [0.7, 0.7]
    taref = [0.2, 0.2]
    name = 'threeParabola' + mode
    #mode = 'CC'
    topology = Topology.blendSurfaces(surfaces, tops, bottoms, aref, arefs, taref, name, mode)

    topology.writeToFile()

def blendFiveCone():
    baseSurfaces = BaseSurface()
    blend0 = baseSurfaces.blendCP("cone")
    blend0 = transform.move(blend0, 'y', 12)
    raw = RawSurface(blend0, 'cone')
    raw.setSharpEdges([])
    top1 = Topology.create(raw)

    blend2 = transform.rotate(blend0, 'z', -2*pi/5)
    raw = RawSurface(blend2, 'cone')
    raw.setSharpEdges([])
    top2 = Topology.create(raw)

    blend3 = transform.rotate(blend0, 'z', -4*pi/5)
    raw = RawSurface(blend3, 'cone')
    raw.setSharpEdges([])
    top3 = Topology.create(raw)

    blend4 = transform.rotate(blend0, 'z', -6*pi/5)
    raw = RawSurface(blend4, 'cone')
    raw.setSharpEdges([])
    top4 = Topology.create(raw)

    blend5 = transform.rotate(blend0, 'z', -8*pi/5)
    raw = RawSurface(blend5, 'cone')
    raw.setSharpEdges([])
    top5 = Topology.create(raw)

    # blend6 = transform.rotate(blend0, 'z', -5*pi/3)
    # raw = RawSurface(blend6, 'cone')
    # raw.setSharpEdges([])
    # top6 = Topology.create(raw)

    surfaces = [top1, top2, top3, top4, top5]
    tops = [2, 2, 2, 2, 2]
    bottoms = [0, 0, 0, 0, 0]
    aref = [13, 13]
    arefs = [1.5, 1.5]
    taref = [0.3, 0.3]
    name = 'fiveCone' + mode
    #mode = 'DS'
    topology = Topology.blendSurfaces(surfaces, tops, bottoms, aref, arefs, taref, name, mode)

    topology.writeToFile()

if __name__ == '__main__':
    mode = 'CC'
    blendThreeCylinder()
    blendThreeCylinderNonFlat()
    blendSixCylinder()
    blendThreeHyperbola()
    blendThreeParabola()
    blendFiveCone()

