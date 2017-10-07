import IgcFlight
import math

class FileIndexer:

	def __init__(self):
		self.DIST_THRESHOLD = 20000	# threshold distance for classification at a location (meters)

		self.locations = {}
		self.locations['pico_agudo'] = (-22.863544, -45.651280)
		self.locations['santa_rita'] = (-22.195853, -45.742658)

		self.convertCoordsToRadians()

	def convertCoordsToRadians(self):
		for k,l in self.locations.items():
			self.locations[k] = (deg2rad(l[0]), deg2rad(l[1]))

	def openIndexFiles(self):
		self.files = {}
		for loc in self.locations:
			self.files[loc] = open('indexes/' + loc + '.txt', 'w')

	def closeIndexFiles(self):
		for loc in self.locations:
			self.files[loc].close()

	def getFileLocation(self, filename):
		try:
			with open(filename, 'r') as f:
				for line in f:
					if(line[0] == 'B'):
						tp = IgcFlight.IgcFlight.TrackPointRecord(line)
						return (tp.latitude, tp.longitude)
					elif(line.startswith('HFDTE')):
						pass #Date of flight
		except FileNotFoundError:
			pass
		except:
			print('Error parsing file: ', filename)
		return None

	def getDistance(self, location, fileLocation):
		dlat = location[0] - fileLocation[0]
		dlon = location[1] - fileLocation[1]
		earthRadius = 6371000.0
		dx = dlon * earthRadius		
		dy = dlat * earthRadius
		dist = math.sqrt(dx*dx + dy*dy)
		return dist
		
	def addFileToIndex(self, filename, indexName):
		self.files[indexName].write(filename + '\n')
		print('Adding ', filename, ' to ', indexName)

	def indexFile(self, filename):
		fileLoc = self.getFileLocation(filename)
		if(fileLoc != None):
			for key,loc in self.locations.items():
				if(self.getDistance(loc, fileLoc) < self.DIST_THRESHOLD):
					self.addFileToIndex(filename, key)					

	def indexFiles(self):
		self.openIndexFiles()
		startId = 0
		endId = 300000
		for i in range(endId, startId, -1):
			filename = 'igc/' + str(i) + '.igc'
			self.indexFile(filename)

		self.closeIndexFiles()

def deg2rad(deg):
		return deg*math.pi/180.0
	

indexer = FileIndexer()
indexer.indexFiles()
