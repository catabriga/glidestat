import math
import matplotlib.pyplot as plt
import numpy as np

class ImgMaker:

	def __init__(self, center, dimension, resolution):
		(dimX, dimY) = dimension
		numCellsX = int(dimX / resolution)
		numCellsY = int(dimY / resolution)
		self.resolution = resolution
		self.cells = [[[] for x in range(numCellsX)] for y in range(numCellsY)]
		self.center = center
		
	
	def cross(v1, v2):
		cross = v1[0] * v2[1] - v1[1] * v2[0]
		return cross
	
	def lineIntersection(segment1, segment2):
		# considering two segments p + t * r = q + u * s
		# where p and q are points, r and s vectors,
		# t and u are scalar factors
		
		p = segment1[0]
		r = (segment1[1][0] - segment1[0][0], segment1[1][1] - segment1[0][1])
		
		q = segment2[0]
		s = (segment2[1][0] - segment2[0][0], segment2[1][1] - segment2[0][1])
		
		rxs = ImgMaker.cross(r, s)
		
		zeroTolerance = 1e-6
		if(abs(rxs) < zeroTolerance):
			return (0.0, 0.0), False	# segments are parallel
		
		pq = (q[0] - p[0], q[1] - p[1])
		
		pqxs = ImgMaker.cross(pq, s)
		pqxr = ImgMaker.cross(pq, r)
				
		t = pqxs / rxs
		u = pqxr / rxs
		
		# test t to be bigger than tolerance to avoid returning an
		# intersection if first point is at the intersection
		if( t>=zeroTolerance and t<1.0 and u>=0.0 and u<1.0):
			intersection = (p[0] + t*r[0], p[1] + t*r[1])
			return intersection, True
		else:
			return (0.0, 0.0), False	# segments do not intersect
	
	def segmentLength(p1,p2):
		return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
	
	def addSegment(self, segment, climbRate):
		(p1, p2) = segment		
		(x,y) = p1
		res = self.resolution
		
		cellX = int(x / res)
		cellY = int(y / res)
		
		squareSegments = []
		squareSegments.append((( cellX    * res,  cellY    * res), ((cellX+1) * res,  cellY    * res)))
		squareSegments.append((((cellX+1) * res,  cellY    * res), ((cellX+1) * res, (cellY+1) * res)))
		squareSegments.append((((cellX+1) * res, (cellY+1) * res), ( cellX    * res, (cellY+1) * res)))
		squareSegments.append((( cellX    * res, (cellY+1) * res), ( cellX    * res,  cellY    * res)))
		
		endPoint = p2
		for squareSegment in squareSegments:		
			intersectPoint, hasIntersected = ImgMaker.lineIntersection((p1, p2), squareSegment)
			if(hasIntersected):
				endPoint = intersectPoint
				self.addSegment((intersectPoint,p2), climbRate)
				break
		
		length = ImgMaker.segmentLength(p1, endPoint)
		
		if(cellX >= 0 and cellX < len(self.cells) and cellY >= 0 and cellY < len(self.cells[cellX])):
			self.cells[cellX][cellY].append((climbRate,length))
		else:
			print('Point outside matrix: (', cellX, ', ', cellY, ')')
		
	def getAverageClimb(self, climbList):
		totalLength = 0.0
		totalClimb = 0.0
		for c in climbList:			
			(climbRate, length) = c			
			totalClimb = totalClimb + climbRate*length
			totalLength = totalLength + length
		averageClimb = totalClimb / totalLength
		return averageClimb
		
	def showMatrix(self):
		mat = np.zeros((len(self.cells), len(self.cells[0])))
	
		for i in range(len(self.cells)):
			for j in range(len(self.cells[i])):
				if(len(self.cells[i][j]) > 0):
					mat[i][j] = self.getAverageClimb(self.cells[i][j])				
					
		fig = plt.figure()
		ax = fig.add_subplot(111)
		cax = ax.matshow(mat, interpolation='nearest')
		fig.colorbar(cax)
		plt.show()
		