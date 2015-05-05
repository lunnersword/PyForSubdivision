import math
import sys

def averageVertices(vertices):
	result = [0.0, 0.0, 0.0]
	count = len(vertices)
	for vertex in vertices:
		result[0] += vertex[0]
		result[1] += vertex[1]
		result[2] += vertex[2]
	result[0] /= count
	result[1] /= count
	result[2] /= count
	return result

def averageVertices(indices, vertices):
	result = [0.0, 0.0, 0.0]
	for index in indices:
		result[0] += vertices[index][0]
		result[1] += vertices[index][1]
		result[2] += vertices[index][2]

	count = len(indices)
	result[0] /= count
	result[1] /= count
	result[2] /= count
	return result

def getAverageVertex(objects):
	result = [0.0, 0.0 ,0.0]
	count = 0
	for obj in objects:
		count += len(obj['vertices'])
		for vertex in obj['vertices']:
			result[0] += vertex[0]
			result[1] += vertex[1]
			result[2] += vertex[2]
	result[0] /= count
	result[1] /= count
	result[2] /= count
	return result

def distanceBetweenPoints(point1, point2):
	return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2 + (point1[2]-point2[2])**2)

def getFacePoint(face, vertices):
	result =[0.0, 0.0, 0.0]
	#print face
	for vertex in face:
		print vertex
		result[0] += vertices[vertex][0]
		result[1] += vertices[vertex][1]
		result[2] += vertices[vertex][2]
	count = len(face)
	result[0] /= count
	result[1] /= count
	result[2] /= count
	return result

def distanceBetweenPointAndFace(point, face, vertices):

	facePoint = getFacePoint(face, vertices)
	return distanceBetweenPoints(point, facePoint)	

def getNearestFaceToCentral(centralPoint, obj):
	maxint = sys.maxint
	result = [-1, maxint]
	faces = obj['faces']
	index = 0
	for face in faces:
		distance = distanceBetweenPointAndFace(centralPoint, face, obj['vertices'])
		if distance < result[1]:
			result[0] = index
			result[1] = distance
		
		index+=1
	
	return result

def distanceBetweenSegments(segment1, segment2, vertices):
	midpoint1 = averageVertices(segment1, vertices)
	midpoint2 = averageVertices(segment2, vertices)
	return distanceBetweenPoints(midpoint1, midpoint2)

def getAdjacentSegmentsBetweenFaces(face1, face2, vertices):
	segments1 = []
	segments2 = []
	for i in range(len(face1)):
		segments1.append( (face1[i], face1[(i+1)%len(face1)]) )
	
	for i in range(len(face2)):
		segments2.append( (face2[i], face2[(i+1)%len(face2)]) )
	result = [-1,-1,-1,-1, sys.maxint]
	for segment1 in segments1:
		for segment2 in segments2:
			distance = distanceBetweenSegments( segment1, segment2, vertices)
			if distance < result[4]:
				result[4] = distance
				result[0] = segment1[0]
				result[1] = segment1[1]
				result[2] = segment2[0]
				result[3] = segment2[1]

	return result
	
