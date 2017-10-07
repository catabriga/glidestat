import requests

igcFolder = 'igc/'

def getFlight(flighId):
	postParams = {'flightID':flighId, 'type':'igc'}
	r = requests.post('http://novo.xcbrasil.com.br/download_igc.php', data = postParams)
	return (r.text)


def writeFlightIgc(flightId, igcData):
	f = open(igcFolder+str(flightId)+'.igc', 'w')
	f.write(igcData)
	f.close()
	


for i in range(108003,0,-4):
	print('Downloading flight %d' % i)
	igcData = getFlight(i)
	writeFlightIgc(i, igcData)
