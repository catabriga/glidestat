import datetime
import numpy as np

class IgcFlight:

	class TrackPointRecord:
		
		def __init__(self, recordStr):
			assert recordStr[0] == 'B'
			self.time = self.timeFromStr(recordStr[1:7])
			self.latitude = self.latitudeFromStr(recordStr[7:15])
			self.longitude = self.longitudeFromStr(recordStr[15:24])
			self.fixValidity = self.fixValidityFromStr(recordStr[24])
			self.pressureAltitude = self.altitudeFromStr(recordStr[25:30])
			self.gpsAltitude = self.altitudeFromStr(recordStr[30:35])
		
		def timeFromStr(self, timeStr):
			hour = int(timeStr[0:2])
			minute = int(timeStr[2:4])
			second = int(timeStr[4:6])
			t = datetime.time(hour, minute, second)
			return t

		def latitudeFromStr(self, latStr):
			degrees = int(latStr[0:2])
			minutes = int(latStr[2:7]) / 1000.0
			northSouthStr = latStr[7]
			lat = degrees + (minutes/60.0)
			if(northSouthStr == 'S'):
				lat = -lat
			lat = lat * np.pi / 180.0				
			return lat

		def longitudeFromStr(self, lonStr):
			degrees = int(lonStr[0:3])
			minutes = int(lonStr[3:8]) / 1000.0
			eastWestStr = lonStr[8]
			lon = degrees + (minutes/60.0)
			if(eastWestStr == 'W'):
				lon = -lon
			lon = lon * np.pi / 180.0			
			return lon

		def fixValidityFromStr(self, fixValStr):
			return fixValStr == 'A'

		def altitudeFromStr(self, altStr):
			alt = int(altStr[0:5])
			return alt
	
	def __init__(self, filename, centerCoord=None):
		self.filename = filename
		self.day = 1
		self.month = 1
		self.year = 1
		self.trackpoints = []

		self.readFile(filename)
		self.addDateToTimes()
		self.calcXYZcoords(centerCoord)
	
	
	def readFile(self, filename):
		with open(filename, 'r') as f:
			for line in f:
				try:
					if(line[0] == 'B'):					
						self.trackpoints.append(IgcFlight.TrackPointRecord(line))
					elif(line.startswith('HFDTE')):
						self.readDateLine(line)
				except Exception as e:
					print('Exception on file ', filename, ' at line:')
					print(line)
					print(e)
					
	def readDateLine(self, dateline):
		try:
			self.day = int(dateline[5:7])
			self.month = int(dateline[7:9])
			self.year = int(dateline[9:11])
		except:
			print('Invalid date on file ', self.filename)
			
	def addDateToTimes(self):
		flightDate = datetime.date(self.year, self.month, self.day)			
		for i in range(len(self.trackpoints)):
			pointTime = self.trackpoints[i].time
			self.trackpoints[i].time = datetime.datetime.combine(flightDate, pointTime)
		
	def latlon2xy(self, coord, centerCoord):
		earthRadius = 6371000.0
		(lat,lon) = coord
		(centerLat, centerLon) = centerCoord
		dlat = lat - centerLat
		dlon = lon - centerLon
		
		x = dlon * earthRadius
		y = dlat * earthRadius

		return x,y
			
	def calcXYZcoords(self, centerCoord):
		if(centerCoord == None):
			centerCoord = (self.trackpoints[0].latitude, self.trackpoints[0].longitude)
	
		for tp in self.trackpoints:
			x,y = self.latlon2xy((tp.latitude, tp.longitude),centerCoord)
			tp.x = x
			tp.y = y
			tp.z = tp.gpsAltitude
			
#flight = IgcFlight('pico.igc')

#print(flight.__dict__)
