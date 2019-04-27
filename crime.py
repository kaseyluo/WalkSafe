import csv

csvCrimeTimeIndex = 2
csvCrimePDCodeIndex = 9
csvCrimeKDCodeIndex = 7
csvCrimeLAWCATCD = 12
csvLatLongIndex = 29


class Crime:
	def __init__(self, latLong, pdCode, kdCode, lawCatCD, time):
		self.latLong = latLong
		self.pdCode = pdCode #crime code
		self.kdCode = kdCode #more granular code
		self.lawCatCD = lawCatCD #misdemeanor, violation, felony, ...
		self.time = time

	def getCoord(self):
		return self.latLong

	def getPDType(self):
		return self.pdCode

	def getKDType(self):
		return self.kdCode

	def getCrimeType(self):
		return self.lawCatCD

	def getTime(self):
		return self.time

	def printSelf(self): 
		print("Coord: ", self.latLong, " PD-TYPE: ", self.pdCode, " KD-TYPE: ", self.kdCode, " TYPE: ", self.lawCatCD, ": TIME: ", self.time)


def getCrimes():
	crimes = set()
	f = open("NYPD_Complaint_Data_Historic.csv")
	csv_f = csv.reader(f)

	for row in csv_f:
		c = Crime(row[csvLatLongIndex], row[csvCrimePDCodeIndex], row[csvCrimeKDCodeIndex], row[csvCrimeLAWCATCD], row[csvCrimeTimeIndex])
		crimes.add(c)

	return crimes


crimes = getCrimes()
