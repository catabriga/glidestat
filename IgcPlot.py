import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import math

import IgcFlight as ifl
import ImgMaker
import SpeedCalc

def latlon2xy(centerLat, centerLon, lat, lon):
	earthRadius = 6371000.0
	dlat = lat - centerLat
	dlon = lon - centerLon
	
	x = dlat * earthRadius
	y = dlon * earthRadius
	return x,y

def loadFlight(filename):
	flight = ifl.IgcFlight(filename)
	xs = []
	ys = []
	zs = []
	ts = []

	centerPoint = flight.trackpoints[0]
	clat = centerPoint.latitude
	clon = centerPoint.longitude

	for tp in flight.trackpoints:
		x,y = latlon2xy(clat, clon, tp.latitude, tp.longitude)

		xs.append(x)
		ys.append(y)
		zs.append(tp.gpsAltitude)
		ts.append(tp.time)
	return xs, ys, zs, ts

def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

def plotFlight():
	mpl.rcParams['legend.fontsize'] = 10

	fig = plt.figure()
	ax = fig.gca(projection='3d')

	x,y,z,t = loadFlight('pico.igc')

	ax.plot(x, y, z, label='parametric curve')
	ax.legend()

	set_axes_equal(ax)
	plt.show()

def showDeltas():
	xs,ys,zs,ts = loadFlight('pico.igc')
	
	pts = list(zip(xs,ys,zs,ts))
	
	lastPt = pts[0]
	for pt in pts[1:]:
		(x,y,z,t) = pt
		(lx,ly,lz,lt) = lastPt
		dp = math.sqrt((x-lx)**2 + (y-ly)**2 + (z-lz)**2)
		dt = (t-lt).total_seconds()
		print('dp = ', dp, '\tdt = ', dt, '\tdps = ', (z-lz)/dt)
		lastPt = pt


def addFlightToImgMaker(imgMaker, centerCoord, filename):
	flight = ifl.IgcFlight(filename, centerCoord)
	lpt = flight.trackpoints[0]
	for pt in flight.trackpoints[1:]:
		dt = (pt.time-lpt.time).total_seconds()
		if(dt > 0):
			climbRate = (pt.z-lpt.z)/dt
			if(climbRate > -10):
				imgMaker.addSegment(((lpt.x,lpt.y),(pt.x,pt.y)), climbRate)
				lpt = pt

		
def plotMatrix():
	centerCoord = (-22.968575*math.pi/180.0, -45.738685*math.pi/180.0)
	imgMaker = ImgMaker.ImgMaker((20000,20000), 10.0)

	indexFile = 'indexes/pico_agudo.txt'
	#indexFile = 'indexes/pico_small.txt'
	with open(indexFile, 'r') as f:		
		for line in f:
			line = line.rstrip('\n')
			print('Reading file ', line)
			addFlightToImgMaker(imgMaker, centerCoord, line)
		
	imgMaker.showMatrix()
		

def plotVelocities():
	flight = ifl.IgcFlight('pico7.igc')
	
	vxs = []
	vys = []
	
	lpt = flight.trackpoints[0]
	for pt in flight.trackpoints[1:]:
		dx = (pt.x-lpt.x)
		dy = (pt.y-lpt.y)
		dz = (pt.z-lpt.z)
		dt = (pt.time-lpt.time).total_seconds()		
		vx = dx/dt
		vy = dy/dt		
		vxs.append(vx)
		vys.append(vy)
		lpt = pt
		
	speed = SpeedCalc.calcWindSpeed(list(zip(vxs, vys)))
	circle = plt.Circle((speed[0], speed[1]), speed[2], color='r', fill=False)
		
	plt.scatter(vxs, vys)
	ax = plt.gca()
	ax.add_artist(circle)
	plt.show()
		
#showDeltas()
#plotFlight()
plotMatrix()
#plotVelocities()
