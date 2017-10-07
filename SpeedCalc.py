import numpy as np

def calcWindSpeed(speeds):
	B = solveGaussNewton(speeds)
	centerX = B[0]
	centerY = B[1]
	radius = B[2]
	
	return (centerX, centerY, radius)
	
def residualFunc(x, B):
	r = (x[0] - B[0])**2 + (x[1] - B[1])**2 - B[2]**2
	return r
	
def updateResidualVec(R, X, B):
	for i in range(len(X)):
		R[i][0] = residualFunc(X[i], B)
	
def updateJacobian(Jr, X, B):	
	for i in range(len(X)):
		Jr[i,0] = 2*B[0] - 2*X[i][0]
		Jr[i,1] = 2*B[1] - 2*X[i][1]
		Jr[i,2] = -2*B[2]
	
def solveGaussNewton(pts):
	
	X = pts
	B = np.matrix([[0], [0], [1]])
	Jr = np.matrix(np.zeros((len(X), 3)))
	R = np.matrix(np.zeros((len(X), 1)))
	
	for i in range(10):
		updateJacobian(Jr, X, B)
		updateResidualVec(R, X, B)
		JrT = Jr.getT()
		B = B - (JrT * Jr).getI() * JrT * R
	
	print('B: ', B)
	return B