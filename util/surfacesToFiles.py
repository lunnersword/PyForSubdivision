from numpy import *
from rawSurface import RawSurface

BaseTypes = ['cylinder', 'parabola', 'hyperbola', 'circular', 'cone']
ClockWiseList = ['cylinder', 'parabola', 'hyperbola', 'circular', 'cone']
CounterCWList = []
PoleTypes = ['cone', 'parabola'] #removed 'parabola'

def parseDetail(CP):
    Dict = {}
    vertices = []
    faces = []

    sEdges = []
    sVertices = []
    #if type(CP) is not RawSurface: #why is true?
    if not isinstance(CP, RawSurface):
        raise TypeError
    #collect vertices
    P = CP.blendCP

    def poleLastFaceCW():
        face = []
        face.append(i*jlen + j)
        face.append(i*jlen + j+1)
        face.append((i+1)*jlen)
        faces.append(face)
    def poleLastFaceCW0():
        face = []
        face.append(i*jlen + j)
        face.append(i*jlen + 0)
        face.append((i+1)*jlen)
        faces.append(face)
    def poleLastFaceCCW():
        face = []
        face.append(i*jlen + j)
        face.append((i+1)*jlen)
        face.append(i*jlen + j+1)
        faces.append(face)

    def poleLastFaceCCW0():
        face = []
        face.append(i*jlen +j)
        face.append((i+1)*jlen)
        face.append(i*jlen + 0)
        faces.append(face)


    ilen = len(P[:,0,0])
    jlen = 4
    if CP.name in PoleTypes:
        for i in range(ilen-1):
            for j in range(jlen):
                vertices.append(P[i,j,:].copy())
        vertices.append(P[ilen-1,0,:].copy())
    else:
        for i in range(ilen):
            for j in range(jlen):
                vertices.append(P[i,j,:].copy())



    if CP.name in ClockWiseList:
        for i in range(ilen-1):
            if i == ilen-2 and CP.name in PoleTypes:
                for j in range(jlen):

                    if j == jlen-1:
                        poleLastFaceCW0()
                    else:
                        poleLastFaceCW()

            else:
                for j in range(jlen):
                    face = []
                    if j == jlen-1:
                        face.append(i*jlen + j)
                        face.append(i*jlen + 0)
                        face.append((i+1)*jlen + 0)
                        face.append((i+1)*jlen + j)
                    else:
                        face.append(i*jlen + j)
                        face.append(i*jlen + j+1)
                        face.append((i+1)*jlen + j+1)
                        face.append((i+1)*jlen + j)

                    faces.append(face)
    else:
        for i in range(ilen - 1):
            if i == ilen-2 and CP.name in PoleTypes:
                for j in range(jlen):
                    if j == jlen-1:
                        poleLastFaceCCW0()
                    else:
                        poleLastFaceCCW()
            else:
                for j in range(jlen):
                    face = []
                    if j == jlen-1:
                        face.append(i*jlen + j)
                        face.append((i+1)*jlen + j)
                        face.append((i+1)*jlen + 0)
                        face.append(i*jlen + 0)
                    else:
                        face.append(i*jlen + j)
                        face.append((i+1)*jlen + j)
                        face.append((i+1)*jlen + j+1)
                        face.append(i*jlen + j+1)
                    faces.append(face)
    def endFace():
        if len(CP.sharpEdges) == 0:
            face = []
            if CP.name in CounterCWList:
                for j in range(jlen):
                    face.append(j)
            else:
                a = range(jlen)
                a.reverse()
                for j in a:
                    face.append(j)
            faces.append(face)

            i = ilen-1
            if CP.name not in PoleTypes:
                face = []

                if CP.name in CounterCWList:
                    a = range(jlen)
                    a.reverse()
                    for j in a:
                        face.append(i*jlen + j)
                else:
                    for j in range(jlen):
                        face.append(i*jlen + j)
                faces.append(face)
        elif len(CP.sharpEdges) == 1:
            temp = CP.sharpEdges[0]
            if CP.name in CounterCWList:
                if temp == ilen - 1:
                    #print 'here it is!'
                    face = []
                    for j in range(jlen):
                        face.append(j)
                    faces.append(face)
                elif temp == 0 and CP.name not in PoleTypes:
                    i = ilen-1
                    face = []
                    a = range(jlen)
                    a.reverse()
                    for j in a:
                        face.append(i*jlen + j)

                    faces.append(face)
            else:
                if temp == ilen-1:
                    print('fuck'+str(temp))
                    face = []
                    a = range(jlen)
                    a.reverse()
                    for j in a:
                        face.append(j)
                    faces.append(face)
                elif temp == 0 and CP.name not in PoleTypes:
                    print('fuck 0')
                    i = ilen-1
                    face = []

                    for j in range(jlen):
                        face.append(i*jlen + j)
                    faces.append(face)
    endFace()


    for i in CP.sharpEdges:
        #print '%d\n' % i
        for j in  range(jlen):
            if j == jlen-1:
                sEdges.append([i*jlen+j, i*jlen])
            else:
                sEdges.append([i*jlen+j, i*jlen+j+1])
    for i in CP.sharpEdges:
        for j in  range(jlen):
            sVertices.append([i*jlen+j, 2])

    if CP.name in PoleTypes:
        #not for parabola
        if CP.name == 'cone':
            sVertices.append([len(vertices) - 1, 3])

    Dict['name'] = CP.name
    Dict['vertices'] = vertices
    Dict['faces'] = faces
    Dict['sEdges'] = sEdges
    Dict['sVertices'] = sVertices
    return Dict

def writeSurfaceToFile(surfaces, out=False):
    #out = open(surfaces['name']+'.txt', 'w')
    if out:
        filename = './surfaceTxt/' + surfaces['name'] + '.txt'
    else:
        filename = '../surfaceTxt/' + surfaces['name'] + '.txt'
    out = open(filename, 'w')

    out.write(surfaces['name'])
    out.write('\n')
    out.write('3\n')
    out.write('#ORIGINAL\n')

    out.write(str( len(surfaces['vertices']) ) )
    out.write('\n')

    for j in range(len(surfaces['vertices'])):

        x = surfaces['vertices'][j][0]
        y = surfaces['vertices'][j][1]
        z = surfaces['vertices'][j][2]
        out.write(str(x))
        out.write('\t')
        out.write(str(y))
        out.write('\t')
        out.write(str(z))
        out.write('\n')

        #'\t'.join(str(su
    out.write(str(len(surfaces['faces'])))
    out.write('\n')
    for j in range(len(surfaces['faces'])):
        out.write(str(len(surfaces['faces'][j])))
        out.write('\t')
        for k in range(len(surfaces['faces'][j])):
            out.write(str(surfaces['faces'][j][k]))
            out.write('\t')
        out.write('\n')

    out.write(str(len(surfaces['sEdges'])))
    out.write('\n')
    for j in range(len(surfaces['sEdges'])):
        out.write(str(surfaces['sEdges'][j][0]))
        out.write('\t')
        out.write(str(surfaces['sEdges'][j][1]))
        out.write('\n')

    out.write(str(len(surfaces['sVertices'])))
    out.write('\n')
    for j in range(len(surfaces['sVertices'])):
        out.write(str(surfaces['sVertices'][j][0]))
        out.write('\t')
        out.write(str(surfaces['sVertices'][j][1]))
        out.write('\n')
    out.write('#END')
    out.flush()
    out.close()


if __name__ == '__main__':
    from Revol_Tangent import Revol_Tangent
    List = ['cone', 'cylinder', 'circular', 'hyperbola', 'parabola']
    dDict = {'cone': [0], 'cylinder': [0,-1], 'circular': [], 'hyperbola': [0, -1], 'parabola': [0]}
    dDict['cone']
    parameters = []
    surfaces = []
    for typestr in List:
        Dict = {}
        Dict['revol_type'] = typestr
        Dict['tang_alpha'] = 0.3
        Dict['blend_num'] = 0
        parameters.append(Dict)

    for param in parameters:
        blendCP,u = Revol_Tangent(**param)
        if param['revol_type'] == 'parabola':

            print("to f")
            print(blendCP)
        temp = blendCP.copy()

        rawSurface = RawSurface(blendCP, param['revol_type'])
        dDict[rawSurface.name]
        rawSurface.setSharpEdges(dDict[rawSurface.name])

        surfaces.append(parseDetail(rawSurface))

    for i in range(len(surfaces)):
        writeSurfaceToFile(surfaces[i], False)
		
