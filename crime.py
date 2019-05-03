import csv
import json
from collections import defaultdict
from ast import literal_eval

csvCrimeTimeIndex = 2
csvCrimePDCodeIndex = 9
csvCrimeKDCodeIndex = 7
csvCrimeLAWCATCD = 12
csvLatLongIndex = 29

FELONY = "FELONY"
CRIMEFILE = "crimeData.json"

# felonies = {
# 		"FELONY ASSAULT" : 106,
# 		"ROBBERY" : 105,
# 		"MISCELLANEOUS PENAL LAW" : 126,
# 		"GRAND LARCENY" : 109,
# 		"DANGEROUS DRUGS" : 235,
# 		"BURGLARY" : 107,

# 		"CRIMINAL MISCHIEF" : 121,
# 		"FORGERY" : 113,
# 		"GRAND LARCENY OF MOTOR VEHICLE" : 110,
# 		"DANGEROUS WEAPONS" : 118,
# 		"DANGEROUS DRUGS" : 235,

# 		"ARSON" : 114,

# 		"SEX CRIMES" : 116,

# 	}

weights = {
		'106' : 120,
		'105' : 360,
		'126' : 14,
		'109' : 105,
		'235' : 14,
		'107' : 120,

		'121' : 14,
		'113' : 1,
		'110' : 20,
		'118' : 60,
		'235' : 10,

		'114' : 20,

		'116' : 180,

	}


class Crime:
	def __init__(self, latLong, pdCode, kdCode, lawCatCD, time):
		self.latLong = latLong #latitude, longitude tuple where crime took place
		self.pdCode = pdCode #crime code
		self.kdCode = kdCode #more granular code
		self.lawCatCD = lawCatCD #misdemeanor, violation, felony, ...
		self.time = time #time that the crime happened

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

#parses the large CSV from NYC database, extracts out the info we want for each crime. Places it in a set of Crime objects
def getCrimes():
	crimes = set()
	f = open("NYPD_Complaint_Data_Historic.csv")
	csv_f = csv.reader(f)
	first_row = next(csv_f)
	for row in csv_f:
		c = Crime(row[csvLatLongIndex], row[csvCrimePDCodeIndex], row[csvCrimeKDCodeIndex], row[csvCrimeLAWCATCD], row[csvCrimeTimeIndex])
		crimes.add(c)

	return crimes

#returns a map of (lat, long): crime weight 
def assignWeights(crimes):
	crimeMap = defaultdict(int)
	for c in crimes:
		key = c.getCoord() #the latitude, longitude
		#need to assign this location a crime weight
		if key == '': continue
		else:
			# key = eval(key)
			if c.getCrimeType() == FELONY:
				kdCode = c.getKDType()
				value = 0
				if kdCode in weights:
					value = weights[kdCode]
				crimeMap[key] += value

	return crimeMap

def writeCrimeMapToJSON(crimeMap):
	with open(CRIMEFILE, 'w') as outfile:  
		json.dump(crimeMap, outfile)


crimes = getCrimes()
crimeMap = assignWeights(crimes)
writeCrimeMapToJSON(crimeMap)


#testing to see if we can read it back as a dictionary
# if CRIMEFILE:
#     with open(CRIMEFILE, 'r') as f:
#         datastore = json.load(f)
#         print(datastore)





















