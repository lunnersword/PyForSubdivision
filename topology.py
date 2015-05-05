__author__ = 'lunner'
from numpy import *
from util.rawSurface import RawSurface
from util.surfacesToFiles import parseDetail, writeSurfaceToFile

BaseTypes = ['cylinder', 'parabola', 'hyperbola', 'circular', 'cone']
ClockWiseList = ['cylinder', 'parabola', 'hyperbola', 'circular', 'cone']
CounterCWList = []
PoleTypes = ['cone', 'parabola']

class Topology:
    def __init__(self):
        self.name = ""
        self.vertices = []
        self.faces = []
        #self.originalFaces = []
        self.refineFaces = {}
        self.sharpEdges = []
        self.sharpVertex = []
        self.selectedFace = 0
        self.auxiliaryPoints = {}
    @classmethod
    def parseDetail(cls, CP):
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


        ilen = len(P[:,0,0])
        jlen = 4
        if CP.name not in PoleTypes:
            for i in range(ilen):
                for j in range(jlen):
                    vertices.append(P[i,j,:].copy())
            for i in range(ilen-1):
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
            for i in range(ilen-1):
                for j in range(jlen):
                    vertices.append(P[i,j,:].copy())
            vertices.append(P[ilen-1,0,:].copy())
            for i in range(ilen-2):
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
            i = ilen - 2
            for j in range(jlen):
                face = []
                if j == jlen-1:
                    face.append(i*jlen + j)
                    face.append(i*jlen + 0)
                    face.append((i+1)*jlen)

                else:
                    face.append(i*jlen + j)
                    face.append(i*jlen + j+1)
                    face.append((i+1)*jlen)
                faces.append(face)
        if CP.name == 'circular':
            face = []
            k = ilen-1
            for j in range(jlen):
                face.append(k*jlen + j)
            faces.append(face)

        for i in CP.sharpEdges:
            #print '%d\n' % i
            for j in range(jlen):
                if j == jlen-1:
                    sEdges.append([i*jlen+j, i*jlen])
                else:
                    sEdges.append([i*jlen+j, i*jlen+j+1])
        for i in CP.sharpEdges:
            for j in range(jlen):
                sVertices.append([i*jlen+j, 2])

        if CP.name in PoleTypes:
            #not for parabola
            if CP.name == 'cone':
                sVertices.append([len(vertices)-1, 3])

        Dict['name'] = CP.name
        Dict['vertices'] = vertices
        Dict['faces'] = faces
        Dict['sEdges'] = sEdges
        Dict['sVertices'] = sVertices
        return Dict
    @classmethod
    def create(cls, surface):
        #assert type(surface) is RawSurface
        #if type(surface) is not RawSurface:
            #raise TypeError
        '''
        if not isinstance(surface, RawSurface):
            raise TypeError
        '''

        temp = Topology()
        Dict = Topology.parseDetail(surface)
        temp.name = surface.name
        temp.vertices = Dict['vertices']
        'when new vertices append'
        temp.faces = Dict['faces']
        #temp.originalFaces = Dict['faces']
        #temp.refineFaces = {}
        temp.sharpEdges = Dict['sEdges']
        temp.sharpVertex = Dict['sVertices']
        '''
        rows = len(surface.blendCP[:, 0, 0])
        temp.blendCP = zeros((rows, 4, 3))
        temp.blendCP[:, :, :] = surface.blendCP[:, 0:4, :]
        '''
        temp.selectedFace = 0

        #temp.setupRefineFaces()
        #temp.createFaces()

        return temp

    def setSelectedFace(self, index):
        self.selectedFace = index

    def writeToFile(self):
        Dict = {}
        Dict['name'] = self.name
        Dict['vertices'] = self.vertices
        Dict['faces'] = self.faces
        Dict['sEdges'] = self.sharpEdges
        Dict['sVertices'] = self.sharpVertex

        writeSurfaceToFile(Dict, True)

    def verticesLastIndex(self):
        return len(self.vertices) - 1

    def setupAuxiliaryPoints(self, blendTop):
        #print self.selectedFace
        face = self.faces[self.selectedFace]
        #facepoint = self.computeFacepoint(face[0], face[1], face[2], face[3])
        facepoint = Topology.averageOfPoints(blendTop.vertices[face[0]], blendTop.vertices[face[1]], blendTop.vertices[face[2]], blendTop.vertices[face[3]])

        #mid1 = self.computeMidPoint(face[0], face[1])
        #mid2 = self.computeMidPoint(face[1], face[2])
        #mid4 = self.computeMidPoint(face[3], face[0])
        mid1 = Topology.averageOfPoints(blendTop.vertices[face[0]], blendTop.vertices[face[1]])
        mid2 = Topology.averageOfPoints(blendTop.vertices[face[1]], blendTop.vertices[face[2]])
        mid4 = Topology.averageOfPoints(blendTop.vertices[face[3]], blendTop.vertices[face[0]])

        mid10 = Topology.averageOfPoints(blendTop.vertices[face[0]], mid1)
        mid11 = Topology.averageOfPoints(mid1, blendTop.vertices[face[1]])
        mid20 = Topology.averageOfPoints(blendTop.vertices[face[1]], mid2)
        mid40 = Topology.averageOfPoints(blendTop.vertices[face[0]], mid4)

        fp1 = Topology.averageOfPoints(blendTop.vertices[face[0]], mid1, facepoint, mid4)
        fp2 = Topology.averageOfPoints(mid1, blendTop.vertices[face[1]], mid2, facepoint)


        vv1 = Topology.averageOfPoints(fp1, mid1, fp2, facepoint)

        row1 = [face[0], mid10, mid1, mid11, face[1]]
        row2 = [mid40, fp1, vv1, fp2, mid20]
        rows = [row1, row2]
        #print self.selectedFace
        self.auxiliaryPoints[self.selectedFace] = rows
        #print self.auxiliaryPoints[self.selectedFace]

    '''
    def setupRefineFaces(self):
        for i in range(len(self.originalFaces)):
            print str(i) + ':'
            print self.originalFaces[i]
            rows = self.rowsFromABigFace(i)
            self.refineFaces[str(i)] = rows
            #print 'rows:'
            #print rows

        #print 'setupRefineFaces end'

    def createFaces(self):
        for i in self.refineFaces:
            self.createFacesFromRows(self.refineFaces[i])
    '''

    def createFacesFromRows(self, rows):
        #print 'fuck rows:'
        #print rows
        for i in range(len(rows) - 1):
            row1 = rows[i]
            row2 = rows[i+1]

            if len(row1) != len(row2):
                raise IndexError, 'length not equal'

            for j in range(len(row1) - 1):
                face = [row1[j], row1[j+1], row2[j+1], row2[j]]
                self.faces.append(face)

    '''
    def rowsFromABigFace(self, index):
        if index < 0 or index > len(self.originalFaces):
            raise IndexError
        face = self.originalFaces[index]
        facepoint = self.computeFacepoint(face[0], face[1], face[2], face[3])
        self.vertices.append(facepoint)
        facepoint = len(self.vertices) - 1


        mid1 = self.computeMidPoint(face[0], face[1])
        self.vertices.append(mid1)
        mid1 = len(self.vertices) - 1
        mid2 = self.computeMidPoint(face[1], face[2])
        self.vertices.append(mid2)
        mid2 = len(self.vertices) - 1
        mid3 = self.computeMidPoint(face[2], face[3])
        self.vertices.append(mid3)
        mid3 = len(self.vertices) - 1
        mid4 = self.computeMidPoint(face[3], face[0])
        self.vertices.append(mid4)
        mid4 = len(self.vertices) - 1

        mid10 = self.computeMidPoint(face[0], mid1)
        self.vertices.append(mid10)
        mid10 = len(self.vertices) - 1
        mid11 = self.computeMidPoint(mid1, face[1])
        self.vertices.append(mid11)
        mid11 = len(self.vertices) - 1

        mid20 = self.computeMidPoint(face[1], mid2)
        self.vertices.append(mid20)
        mid20 = len(self.vertices) - 1
        mid21 = self.computeMidPoint(mid2, face[2])
        self.vertices.append(mid21)
        mid21 = len(self.vertices) - 1

        mid30 = self.computeMidPoint(face[3], mid3)
        self.vertices.append(mid30)
        mid30 = len(self.vertices) - 1
        mid31 = self.computeMidPoint(mid3, face[2])
        self.vertices.append(mid31)
        mid31 = len(self.vertices) - 1

        mid40 = self.computeMidPoint(face[0], mid4)
        self.vertices.append(mid40)
        mid40 = len(self.vertices) - 1
        mid41 = self.computeMidPoint(mid4, face[3])
        self.vertices.append(mid41)
        mid41 = len(self.vertices) - 1

        fp1 = self.computeFacepoint(face[0], mid1, facepoint, mid4)
        self.vertices.append(fp1)
        fp1 = len(self.vertices) - 1

        fp2 = self.computeFacepoint(mid1, face[1], mid2, facepoint)
        self.vertices.append(fp2)
        fp2 = len(self.vertices) - 1

        fp3 = self.computeFacepoint(facepoint, mid2, face[2], mid3)
        self.vertices.append(fp3)
        fp3 = len(self.vertices) - 1

        fp4 = self.computeFacepoint(mid4, facepoint, mid3, face[3])
        self.vertices.append(fp4)
        fp4 = len(self.vertices) - 1

        vv1 = self.computeFacepoint(fp1, mid1, fp2, facepoint)
        self.vertices.append(vv1)
        vv1 = len(self.vertices) - 1

        vv2 = self.computeFacepoint(facepoint, fp2, mid2, fp3)
        self.vertices.append(vv2)
        vv2 = len(self.vertices) - 1

        vv3 = self.computeFacepoint(facepoint, fp3, mid3, fp4)
        self.vertices.append(vv3)
        vv3 = len(self.vertices) - 1

        vv4 = self.computeFacepoint(facepoint, fp4, mid4, fp1)
        self.vertices.append(vv4)
        vv4 = len(self.vertices) - 1

        row1 = [face[0], mid10, mid1, mid11, face[1]]

        row2 = [mid40, fp1, vv1, fp2, mid20]

        row3 = [mid4, vv4, facepoint, vv2, mid2]

        row4 = [mid41, fp4, vv3, fp3, mid21]

        row5 = [face[3], mid30, mid3, mid31, face[2]]


        rows = [row1, row2, row3, row4, row5]

        return rows
    '''
    @classmethod
    def averageOfPoints(cls, *points):
        temp = zeros(3)
        for point in points:
            for i in range(3):
                temp[i] += point[i]
        num = len(points)
        for i in range(3):
            temp[i] /= num
        return temp

    def computeFacepoint(self, index1, index2, index3, index4):

        if index1 < 0 or index1 >= len(self.vertices):
            raise IndexError, str(index1) + ' ' +str(len(self.vertices))
        if index2 < 0 or index2 >= len(self.vertices):
            raise IndexError, str(index2)
        if index3 < 0 or index3 >= len(self.vertices):
            raise IndexError, index3
        if index4 < 0 or index4 >= len(self.vertices):
            raise IndexError, index4


        facePoint = zeros(3)
        for i in range(3):
            facePoint[i] = (self.vertices[index1][i] + self.vertices[index2][i] + self.vertices[index3][i] + self.vertices[index4][i])/4.0
        return facePoint

    def computeMidPoint(self, vindex1, vindex2):
        if vindex1 < 0 or vindex1 >= len(self.vertices):
            raise IndexError
        if vindex2 < 0 or vindex2 >= len(self.vertices):
            raise IndexError

        midPoint = zeros(3)

        for i in range(3):
            midPoint[i] = (self.vertices[vindex1][i] + self.vertices[vindex2][i]) / 2.0

        return midPoint

    def offsetFaces(self, foreNum):
        for face in self.faces:
            for i in range(len(face)):
                face[i] += foreNum

    def offsetSharpEdges(self, foreNum):
        for edge in self.sharpEdges:
            for i in range(len(edge)):
                edge[i] += foreNum

    def offsetSharpVertex(self, foreNum):
        for sharpVertex in self.sharpVertex:
            sharpVertex[0] += foreNum
    '''
    def offsetRefineFace(self, foreNum):
        rows = self.refineFaces[self.selectedFace]
        for row in rows:
            for i in range(len(row)):
                row[i] += foreNum
    '''


    @classmethod
    def computeCenterPoint(cls, surfaces, aref):
        centerPoint = zeros(3)
        num = len(surfaces)

        for i in range(num):
            faceIndex = surfaces[i].selectedFace
            #v13 = topology.vertices[surfaces[i].refineFaces[faceIndex][0][2]]
            #v23 = topology.vertices[surfaces[i].refineFaces[faceIndex][1][2]]
            v13 = surfaces[i].auxiliaryPoints[faceIndex][0][2]
            v23 = surfaces[i].auxiliaryPoints[faceIndex][1][2]
            for j in range(3):
                centerPoint[j] += v13[j] + aref*(v13[j] - v23[j])
        for i in range(3):
            centerPoint[i] /= num


        return centerPoint
    @classmethod
    def computeCenterPoints(cls, surfaces, aref, taref):
        centerPoint = cls.computeCenterPoint(surfaces, aref)
        print centerPoint
        centerPoints = []
        for i in range(len(surfaces)):
            faceIndex = surfaces[i].selectedFace
            vmid = surfaces[i].auxiliaryPoints[faceIndex][0][2]
            print vmid
            centerPoints.append(centerPoint + taref*(vmid - centerPoint))
        return centerPoints

    @classmethod
    def computeGrooveVertices(cls, topology, surfaces, arefs, beta, istop):
        grooves = []
        bufferGrooves = []

        for i in range(len(surfaces)):
            point1 = zeros(3)
            point2 = zeros(3)
            bpoint1 = zeros(3)
            bpoint2 = zeros(3)
            if istop:
                k = i
            else:
                k = (len(surfaces) - i) % len(surfaces)
            faceIndex = surfaces[k].selectedFace
            grooveVertices = [point1, point2]
            bufferGroove = [bpoint1, bpoint2]
            '''
            v11k = topology.vertices[surfaces[i].refineFaces[faceIndex][0][0]]
            v12k = topology.vertices[surfaces[i].refineFaces[faceIndex][0][1]]
            v21k = topology.vertices[surfaces[i].refineFaces[faceIndex][1][0]]
            v22k = topology.vertices[surfaces[i].refineFaces[faceIndex][1][1]]
            '''
            '''00 04 is index not vertex '''
            rows = surfaces[k].auxiliaryPoints[faceIndex]
            v11k = topology.vertices[rows[0][0]]
            v12k = surfaces[k].auxiliaryPoints[faceIndex][0][1]
            v21k = surfaces[k].auxiliaryPoints[faceIndex][1][0]
            v22k = surfaces[k].auxiliaryPoints[faceIndex][1][1]
            if istop:
                j = (i+1) % len(surfaces)
            else:
                j = (len(surfaces) - i - 1) % len(surfaces)
            faceIndex = surfaces[j].selectedFace

            'v12k1 v14k1 v24k1 v15k1 v11k1 v25k1'
            '''
            v14k1 = topology.vertices[surfaces[j].refineFaces[faceIndex][0][3]]
            v24k1 = topology.vertices[surfaces[j].refineFaces[faceIndex][1][3]]
            v15k1 = topology.vertices[surfaces[j].refineFaces[faceIndex][0][4]]
            v25k1 = topology.vertices[surfaces[j].refineFaces[faceIndex][1][4]]
            '''
            rows = surfaces[j].auxiliaryPoints[faceIndex]
            v14k1 = surfaces[j].auxiliaryPoints[faceIndex][0][3]
            v24k1 = surfaces[j].auxiliaryPoints[faceIndex][1][3]
            #v15k1 = surfaces[j].auxiliaryPoints[faceIndex][0][4]
            v15k1 = topology.vertices[rows[0][4]]
            v25k1 = surfaces[j].auxiliaryPoints[faceIndex][1][4]

            for ax in range(3):
                point1[ax] = (v12k[ax] + v14k1[ax])/2.0 + arefs*(v12k[ax] - v22k[ax] + v14k1[ax] - v24k1[ax])
                point2[ax] = (v11k[ax] + v15k1[ax])/2.0 + arefs*(v11k[ax] - v21k[ax] + v15k1[ax] - v25k1[ax])

                bpoint1[ax] = point2[ax] + beta*(v11k[ax] - point2[ax])
                bpoint2[ax] = point2[ax] + beta*(v15k1[ax] - point2[ax])

            grooves.append(grooveVertices)
            bufferGrooves.append(bufferGroove)

        return grooves, bufferGrooves

    @classmethod
    def combineVertices(cls, blendTopology, surfaces):
        vertices = blendTopology.vertices
        faces = blendTopology.faces
        sharpEdges = blendTopology.sharpEdges
        sharpVertex = blendTopology.sharpVertex

        for i in range(len(surfaces)):
            foreNum = len(vertices)
            for vertex in surfaces[i].vertices:
                vertices.append(vertex)
            "update face, sharp edge, sharpvetex's vertex index"
            surfaces[i].offsetFaces(foreNum)
            faces.extend(surfaces[i].faces)
            surfaces[i].offsetSharpEdges(foreNum)
            sharpEdges.extend(surfaces[i].sharpEdges)
            surfaces[i].offsetSharpVertex(foreNum)
            sharpVertex.extend(surfaces[i].sharpVertex)
            #surfaces[i].offsetRefineFace(foreNum)

    @classmethod
    def blendSinglePatch(cls, blendTopology, surfaces, aref, arefs, istop):
        centerPoint = cls.computeCenterPoint(surfaces, aref)
        #centerPoints = cls.computeCenterPoints(blendTopology, surfaces, aref)
        grooves = cls.computeGrooveVertices(blendTopology, surfaces, arefs, istop)
        'append new vertices to topology'
        blendTopology.vertices.append(centerPoint)
        centerPoint = len(blendTopology.vertices) - 1
        clamps = []
        #clampClusters = []

        'append groove vertices to topology'
        tempGrooves = []
        for groove in grooves:
            tempGroove = []
            for vertex in groove:
                blendTopology.vertices.append(vertex)
                tempGroove.append(len(blendTopology.vertices) - 1)
            tempGrooves.append(tempGroove)
        grooves = tempGrooves


        'create new faces '
        for i in range(len(surfaces)):
            if istop:
                k = i
            else:
                k = (len(surfaces) - i) % len(surfaces)
            first = surfaces[k]

            if istop:
                j = (i+1) % len(surfaces)
            else:
                j = (len(surfaces) - i - 1) % len(surfaces)

            second = surfaces[j]

            #rowk = first.refineFaces[first.selectedFace][0]
            #rowk1 = second.refineFaces[second.selectedFace][0]
            rowk = first.auxiliaryPoints[first.selectedFace][0]
            rowk1 = second.auxiliaryPoints[second.selectedFace][0]
            #clamps is index
            clamp = []

            clamp.append(rowk[0])
            clamp.append(rowk1[4])

            clamps.append(clamp)

            groove = grooves[i]

            # the center point is shared by too many lines
            #extend vertices
            blendTopology.vertices.append(rowk[1])
            rowk01 = len(blendTopology.vertices) - 1
            blendTopology.vertices.append(rowk[2])
            rowk02 = len(blendTopology.vertices) - 1
            blendTopology.vertices.append(rowk[3])
            rowk03 = len(blendTopology.vertices) - 1

            blendTopology.vertices.append(rowk1[1])
            rowk11 = len(blendTopology.vertices) - 1
            blendTopology.vertices.append(rowk1[2])
            rowk12 = len(blendTopology.vertices) - 1
            blendTopology.vertices.append(rowk1[3])
            rowk13 = len(blendTopology.vertices) - 1


            newface1 = [rowk[0], rowk01, groove[0], groove[1]]

            newface2 = [rowk01, rowk02, centerPoint, groove[0]]

            newface3 = [groove[0], centerPoint, rowk12, rowk13]

            newface4 = [groove[1], groove[0], rowk13, rowk1[4]]


            blendTopology.faces.extend([newface1, newface2, newface3, newface4])


        return clamps, grooves


    @classmethod
    def blendConjectedSurface(cls, blendTopology, surfaces, aref, arefs, taref, istop, mode):

        centerPoints = cls.computeCenterPoints(surfaces, aref, taref)
        print centerPoints

        grooves, bufferGrooves = cls.computeGrooveVertices(blendTopology, surfaces, arefs, 0.25, istop)
        'append new vertices to topology'
        for i in range(len(centerPoints)):
            blendTopology.vertices.append(centerPoints[i])
            centerPoints[i] = len(blendTopology.vertices) - 1

        clamps = []

        'append buffer grooves to topology'
        if mode == 'CC':
            tempGrooves = []
            for groove in bufferGrooves:
                tempGroove = []
                for vertex in groove:
                    blendTopology.vertices.append(vertex)
                    tempGroove.append(len(blendTopology.vertices) - 1)
                tempGrooves.append(tempGroove)
            bufferGrooves = tempGrooves

            '''
            'append groove vertices to topology'
            tempGrooves = []
            for groove in grooves:
                tempGroove = []
                for vertex in groove:
                    blendTopology.vertices.append(vertex)
                    tempGroove.append(len(blendTopology.vertices) - 1)
                tempGrooves.append(tempGroove)
            grooves = tempGrooves
            '''


            'create new faces '
            centerFace = []
            for i in range(len(surfaces)):
                if istop:
                    k = i
                else:
                    k = (len(surfaces) - i) % len(surfaces)
                first = surfaces[k]

                if istop:
                    j = (i+1) % len(surfaces)
                else:
                    j = (len(surfaces) - i - 1) % len(surfaces)

                second = surfaces[j]

                #rowk = first.refineFaces[first.selectedFace][0]
                #rowk1 = second.refineFaces[second.selectedFace][0]
                rowk = first.auxiliaryPoints[first.selectedFace][0]
                rowk1 = second.auxiliaryPoints[second.selectedFace][0]
                #clamps is index
                clamp = []

                clamp.append(rowk[0])
                clamp.append(rowk1[4])

                clamps.append(clamp)

                v0 = rowk[0]
                v1 = rowk[4]
                '''
                tempindex = (len(grooves)+i-1) % len(grooves)
                groove0 = grooves[tempindex][1]
                groove1 = grooves[i][1]
                '''
                tempindex = (len(bufferGrooves)+i-1) % len(bufferGrooves)
                grooveCurrent = bufferGrooves[i]
                grooveAhead = bufferGrooves[tempindex]
                bufGrooveCToCurrent = grooveCurrent[0]
                bufGrooveCToNext = grooveCurrent[1]
                bufGrooveAToCurrent = grooveAhead[1]



                # face = [centerPoints[k], groove0, v1, v0, groove1]
                #instead of five edge face by a trangle and a tangle
                #face = [groove0, v1, v0, groove1]
                face = [bufGrooveAToCurrent, v1, v0, bufGrooveCToCurrent]

                blendTopology.faces.append(face)
                #face = [centerPoints[k], groove0, groove1]
                face = [centerPoints[k], bufGrooveAToCurrent, bufGrooveCToCurrent]
                blendTopology.faces.append(face)

                #add triangles


                #grooveP = groove1

                centerPoint1 = centerPoints[k]

                centerPoint2 = centerPoints[j]
                #face = [centerPoint1, grooveP, centerPoint2]
                face = [centerPoint1, bufGrooveCToCurrent, bufGrooveCToNext, centerPoint2]

                blendTopology.faces.append(face)

                centerFace.append(centerPoints[k])


            # face = []
            # for point in centerPoints:
            #     face.append(point)
            blendTopology.faces.append(centerFace)
            '''
            #set sharp vertices
            sharpVertices = []
            for groove in grooves:
                sharpVertices.append([groove[1], 3])

            for cp in centerPoints:
                sharpVertices.append([cp, 2])

            blendTopology.sharpVertex.extend(sharpVertices)
            '''

            return (clamps, bufferGrooves)
        else:


            'append groove vertices to topology'
            tempGrooves = []
            for groove in grooves:
                tempGroove = []
                '''
                for vertex in groove:
                    blendTopology.vertices.append(vertex)
                    tempGroove.append(len(blendTopology.vertices) - 1)
                '''
                blendTopology.vertices.append(groove[1])
                tempGroove.append(len(blendTopology.vertices) -1)

                tempGrooves.append(tempGroove)
            grooves = tempGrooves



            'create new faces '
            centerFace = []
            for i in range(len(surfaces)):
                if istop:
                    k = i
                else:
                    k = (len(surfaces) - i) % len(surfaces)
                first = surfaces[k]

                if istop:
                    j = (i+1) % len(surfaces)
                else:
                    j = (len(surfaces) - i - 1) % len(surfaces)

                second = surfaces[j]

                #rowk = first.refineFaces[first.selectedFace][0]
                #rowk1 = second.refineFaces[second.selectedFace][0]
                rowk = first.auxiliaryPoints[first.selectedFace][0]
                rowk1 = second.auxiliaryPoints[second.selectedFace][0]
                #clamps is index
                clamp = []

                clamp.append(rowk[0])
                clamp.append(rowk1[4])

                clamps.append(clamp)

                v0 = rowk[0]
                v1 = rowk[4]

                tempindex = (len(grooves)+i-1) % len(grooves)
                '''
                groove0 = grooves[tempindex][1]
                groove1 = grooves[i][1]
                '''
                groove0 = grooves[tempindex][0]
                groove1 = grooves[i][0]





                #face = [centerPoints[k], groove0, v1, v0, groove1]
                #instead of five edge face by a trangle and a tangle
                face = [groove0, v1, v0, groove1]
                blendTopology.faces.append(face)

                face = [centerPoints[k], groove0, groove1]

                blendTopology.faces.append(face)

                #add triangles


                grooveP = groove1

                centerPoint1 = centerPoints[k]

                centerPoint2 = centerPoints[j]
                face = [centerPoint1, grooveP, centerPoint2]


                blendTopology.faces.append(face)

                centerFace.append(centerPoints[k])


            # face = []
            # for point in centerPoints:
            #     face.append(point)
            blendTopology.faces.append(centerFace)


            return (clamps, grooves)

    @classmethod
    def blendSurfaces(cls, surfaces, tops, bottoms, aref, arefs, taref, name, mode):
        blendTopology = Topology()
        blendTopology.name = name
        cls.combineVertices(blendTopology, surfaces)
        #return blendTopology   #unCommit here to get surfaces before blending

        'top '
        'here lose some to set selectedFace'
        for i in range(len(tops)):


            surfaces[i].selectedFace = tops[i]
            #surfaces[i].setSelectedFace(tops[i])

            surfaces[i].setupAuxiliaryPoints(blendTopology)

        clamps1, grooves1 = cls.blendConjectedSurface(blendTopology, surfaces, aref[1], arefs[1], taref[1], False, mode)
        #return blendTopology
        'bottom'
        'here lose something to set selectedFace'
        for i in range(len(bottoms)):
            surfaces[i].selectedFace = bottoms[i]
            surfaces[i].setupAuxiliaryPoints(blendTopology)
            #print surfaces[i].auxiliaryPoints[surfaces[i].selectedFace]
        clamps2, grooves2 = cls.blendConjectedSurface(blendTopology, surfaces, aref[0], arefs[0], taref[0], True, mode)

        clamps2.reverse()
        grooves2.reverse()

        if mode == 'CC':
            '''
            'reconstructure grooves'
            grooves = []
            for i in range(len(grooves1)):
                temp = []
                temp.append(grooves1[i][1])
                temp.append(grooves2[i][1])
                grooves.append(temp)

                v0 = clamps1[i]
            '''

            #slide faces


            for i in range(len(grooves1)):
                v0 = clamps1[i][0]
                v1 = clamps1[i][1]
                v2 = clamps2[i][0]
                v3 = clamps2[i][1]
                g00 = grooves1[i][0]
                g01 = grooves1[i][1]
                g10 = grooves2[i][0]
                g11 = grooves2[i][1]

                #face1 = [v0, g0, g1,]
                rows = [[v3, g11, g10, v2],[v0, g00, g01, v1]]
                blendTopology.createFacesFromRows(rows)

            '''
            for i in range(len(grooves)):
                v0 = clamps1[i][1]
                v1 = clamps2[i][1]
                v2 = clamps2[i][0]
                v3 = clamps1[i][0]
                g0 = grooves[i][0]
                g1 = grooves[i][1]

                gv00 = blendTopology.computeMidPoint(v0, g0)
                blendTopology.vertices.append(gv00)
                gv00 = len(blendTopology.vertices) - 1
                gv01 = blendTopology.computeMidPoint(g0, v3)
                blendTopology.vertices.append(gv01)
                gv01 = len(blendTopology.vertices) - 1

                mid1 = blendTopology.computeMidPoint(v0, v1)
                blendTopology.vertices.append(mid1)
                mid1 = len(blendTopology.vertices) - 1

                mid2 = blendTopology.computeMidPoint(v2, v3)
                blendTopology.vertices.append(mid2)
                mid2 = len(blendTopology.vertices) - 1

                gmid = blendTopology.computeMidPoint(g0, g1)
                blendTopology.vertices.append(gmid)
                gmid = len(blendTopology.vertices) - 1

                gmid0 = blendTopology.computeMidPoint(g0, gmid)
                blendTopology.vertices.append(gmid0)
                gmid0 = blendTopology.verticesLastIndex()

                gmid1 = blendTopology.computeMidPoint(gmid, g1)
                blendTopology.vertices.append(gmid1)
                gmid1 = blendTopology.verticesLastIndex()

                fp1 = blendTopology.computeFacepoint(v0, mid1, gmid, g0)
                blendTopology.vertices.append(fp1)
                fp1 = len(blendTopology.vertices) - 1

                fp2 = blendTopology.computeFacepoint(g0, v3, mid2, gmid)
                blendTopology.vertices.append(fp2)
                fp2 = len(blendTopology.vertices) - 1

                fp3 = blendTopology.computeFacepoint(gmid, mid2, v2, g1)
                blendTopology.vertices.append(fp3)
                fp3 = len(blendTopology.vertices) - 1

                fp4 = blendTopology.computeFacepoint(mid1, gmid, g1, v1)
                blendTopology.vertices.append(fp4)
                fp4 = len(blendTopology.vertices) - 1

                mm0 = blendTopology.computeFacepoint(mid1, fp1, gmid, fp4)
                blendTopology.vertices.append(mm0)
                mm0 = len(blendTopology.vertices) - 1

                mm1 = blendTopology.computeFacepoint(gmid, fp2, mid2, fp3)
                blendTopology.vertices.append(mm1)
                mm1 = len(blendTopology.vertices) - 1

                vmid00 = blendTopology.computeMidPoint(v0, mid1)
                blendTopology.vertices.append(vmid00)
                vmid00 = len(blendTopology.vertices) - 1

                vmid01 = blendTopology.computeMidPoint(v3, mid2)
                blendTopology.vertices.append(vmid01)
                vmid01 = blendTopology.verticesLastIndex()

                vmid10 = blendTopology.computeMidPoint(mid1, v1)
                blendTopology.vertices.append(vmid10)
                vmid10 = blendTopology.verticesLastIndex()

                vmid11 = blendTopology.computeMidPoint(mid2, v2)
                blendTopology.vertices.append(vmid11)
                vmid11 = blendTopology.verticesLastIndex()

                gv10 = blendTopology.computeMidPoint(v1, g1)
                blendTopology.vertices.append(gv10)
                gv10 = blendTopology.verticesLastIndex()

                gv11 = blendTopology.computeMidPoint(g1, v2)
                blendTopology.vertices.append(gv11)
                gv11 = blendTopology.verticesLastIndex()


                row1 = [v0, gv00, g0, gv01, v3]
                row2 = [vmid00, fp1, gmid0, fp2, vmid01]
                row3 = [mid1, mm0, gmid, mm1, mid2]
                row4 = [vmid10, fp4, gmid1, fp3, vmid11]
                row5 = [v1, gv10, g1, gv11, v2]
                rows = [row1, row2, row3, row4, row5]

                blendTopology.createFacesFromRows(rows)
            '''
            return blendTopology
        else:

            'reconstructure grooves'
            grooves = []
            for i in range(len(grooves1)):
                temp = []
                temp.append(grooves1[i][0])
                temp.append(grooves2[i][0])
                grooves.append(temp)

            #slide faces

            for i in range(len(grooves1)):
                v0 = clamps1[i][0]
                v1 = clamps1[i][1]
                v2 = clamps2[i][0]
                v3 = clamps2[i][1]
                g0 = grooves[i][0]
                g1 = grooves[i][1]

                #face1 = [v0, g0, g1,]
                rows = [[v3, g1, v2],[v0, g0, v1]]
                blendTopology.createFacesFromRows(rows)


            return blendTopology


