
import copy
from numpy import *
from util.Revol_Tangent import Revol_Tangent
from util import transform
from util.rawSurface import RawSurface
from util.surfacesToFiles import parseDetail, writeSurfaceToFile



def offsetFaces(offset, faces):
	'''
	for face in faces:
		for point in face:
			point += offset
	'''#value unchanged
	for i in range(len(faces)):
		for j in range(len(faces[i])):
			faces[i][j] += offset

def fourCircular():
	order_u = 3
	order_v = 3
	u = cos(pi/4)

	revol_type1 = 'circular'
	tang_alpha1 = 0.3
	blend_num1 = 1
	(base1, v1) = Revol_Tangent(revol_type1, tang_alpha1, blend_num1)
	
	
	rawCP1 = RawSurface(base1, 'circular')
	rawCP2 = RawSurface(base1, 'circular')
	rawCP3 = RawSurface(base1, 'circular')
	rawCP4 = RawSurface(base1, 'circular')

	rawCP1.blendCP = transform.move(rawCP1.blendCP, 'y', 3)
	rawCP2.blendCP = transform.move(rawCP2.blendCP, 'x', -4)
	rawCP3.blendCP = transform.move(rawCP3.blendCP, 'y', -3)
	rawCP4.blendCP = transform.move(rawCP4.blendCP, 'x', 4)
	
	
	circular1 = parseDetail(rawCP1)
	circular2 = parseDetail(rawCP2)
	circular3 = parseDetail(rawCP3)
	circular4 = parseDetail(rawCP4)

	result = copy.deepcopy(circular1)
	result['vertices'].extend(circular2['vertices'])
	result['vertices'].extend(circular3['vertices'])
	result['vertices'].extend(circular4['vertices'])

	faces1 = copy.copy(circular1['faces'])
	faces2 = copy.copy(circular2['faces'])
	faces3 = copy.copy(circular3['faces'])
	faces4 = copy.copy(circular4['faces'])

	
	#
	vertexCount = len(circular1['vertices'])
	
	offsetFaces(vertexCount, faces2)
	offsetFaces(vertexCount*2, faces3)
	offsetFaces(vertexCount*3, faces4)
	
	
	result['faces'].extend(faces2)
	result['faces'].extend(faces3)
	result['faces'].extend(faces4)
	
	result['name'] = 'BefroeFourCircular'
	return result
	

	objects = [circular1, circular2, circular3, circular4]
	centralPoint = getAverageVertex(objects)
	
	faces = []
	for obj in objects:
		face = getNearestFaceToCentral(centralPoint, obj)
		faces.append(face[0])

	

	vertexCount = len(circular1['vertices'])
	
	offsetFaces(vertexCount, faces2)
	offsetFaces(vertexCount*2, faces3)
	offsetFaces(vertexCount*3, faces4)
	result['faces'] = []

	# the adjacent segments between face1 face2, combine to face
	temp = getAdjacentSegmentsBetweenFaces(faces1[faces[0]], faces2[faces[1]], result['vertices'])
	newFace = []
	topVertices = []
	bottomVertices = []
	newFace.append(temp[0])
	newFace.append(temp[1])
	newFace.append(temp[2])
	newFace.append(temp[3])
	topVertices.append(temp[1])
	topVertices.append(temp[2])
	bottomVertices.append(temp[0])
	bottomVertices.append(temp[3])
	result['faces'].append(newFace)

	# the adjacent segments between face2 face3, combine into face
	temp = getAdjacentSegmentsBetweenFaces(faces2[faces[1]], faces3[faces[2]], result['vertices'])
	newFace = []
	newFace.append(temp[0])
	newFace.append(temp[1])
	newFace.append(temp[3])
	newFace.append(temp[2])
	topVertices.append(temp[1])
	topVertices.append(temp[3])
	bottomVertices.append(temp[0])
	bottomVertices.append(temp[2])
	result['faces'].append(newFace)

	#the adjacent segments between face3 face4, combine into face
	temp = getAdjacentSegmentsBetweenFaces(faces3[faces[2]], faces4[faces[3]], result['vertices'])
	newFace = []
	newFace.append(temp[0])
	newFace.append(temp[1])
	newFace.append(temp[3])
	newFace.append(temp[2])
	topVertices.append(temp[0])
	topVertices.append(temp[2])
	bottomVertices.append(temp[1])
	bottomVertices.append(temp[3])
	result['faces'].append(newFace)

	#the adjacent segments between face4 face1 combine into face
	temp = getAdjacentSegmentsBetweenFaces(faces4[faces[3]], faces1[faces[0]], result['vertices'])
	newFace = []
	newFace.append(temp[0])
	newFace.append(temp[1])
	newFace.append(temp[2])
	newFace.append(temp[3])
	topVertices.append(temp[1])
	topVertices.append(temp[2])
	bottomVertices.append(temp[0])
	bottomVertices.append(temp[3])
	result['faces'].append(newFace)

	#combine the top bottom face
	topFace = [x for x in topVertices]
	bottomFace = [x for x in bottomVertices]
	result['faces'].append(topFace)
	result['faces'].append(bottomFace)

	faces1.pop(faces[0])
	faces2.pop(faces[1])
	faces3.pop(faces[2])
	faces4.pop(faces[3])
	
	
	result['faces'].extend(faces1)
	result['faces'].extend(faces2)
	result['faces'].extend(faces3)
	result['faces'].extend(faces4)

	result['name'] = 'fourCircular'
	
	return result

if __name__ == '__main__':
	writeSurfaceToFile(fourCircular())
