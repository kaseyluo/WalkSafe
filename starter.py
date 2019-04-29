import geocoder
import json
import pprint
import threading

# Code that generates "surrounding" coordinates in order to probe for cross streets
# around a given intersection coordinates.
kMod = 0.00001
kModifications = [
    (kMod, kMod), (kMod, -1 * kMod), (-1 * kMod, kMod), (-1 * kMod, -kMod),
    (kMod, 0), (-1 * kMod, 0), (0, kMod), (0, -1 * kMod)
    ]
def getSurrounding(coordinate):
    surrounding = []
    surrounding.append(coordinate)
    latitude = coordinate[0]
    longitude = coordinate[1]
    for mods in kModifications:
        surrounding.append([latitude + mods[0], longitude + mods[1]])

    return surrounding

# "Perfect" Intersection Test Set (latitude, longitude):
perfect = [
    [40.7180338, -74.003043], [40.717449, -74.003533], [40.7162869, -74.0045303],
    [40.718269, -74.007052], [40.719029, -74.008747], [40.715103, -74.0159377],
    [40.7147834, -74.0161825]
    ]

# Function that uses the geocoder API to reverse lookup the street of a given
# coordinate.
def reverseLookup(coord, streets, streetsLock):
    g = geocoder.osm(near, method='reverse')
    with streetsLock:
        if g.street != None:
            streets.add(g.street)

# Perfect Intersection Identification Process
streetsLock = threading.Lock()
for coord in perfect:
    surrounding = getSurrounding(coord)

    streets = set([])
    threads = []
    for near in surrounding:
        t = threading.Thread(target=reverseLookup, args=(near, streets, streetsLock))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    print "COORD ({}, {}) HAS THESE STREETS: {}".format(coord[0], coord[1], streets)

# "Duplicate" Intersection Test Set
duplicate = [
    [40.716871, -74.004026], [40.7167984, -74.0040877], # At least one should map to Leonard St., Broadway
    [40.7128551, -74.0118081], [40.7128206, -74.0117324], [40.7130017, -74.0117733], # Vesey St., Greenwich St.
    [40.707836, -74.00685], [40.707855, -74.0068357] # Platt St, Gold St.
    ]

print " "
for coord in duplicate:
    surrounding = getSurrounding(coord)

    streets = set([])
    threads = []
    for near in surrounding:
        t = threading.Thread(target=reverseLookup, args=(near, streets, streetsLock))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    print "COORD ({}, {}) HAS THESE STREETS: {}".format(coord[0], coord[1], streets)

# "Incorrect" Intersection Test Set --- should have less than two streets associated
# with each coord (since they are not actual intersections)
incorrect = [
    [40.7104515, -74.0139919],
    [40.7104412, -74.014264],
    [40.7102899, -74.0139536],
    [40.7102917, -74.0135162],
    [40.7106822, -74.0141976],
    [40.7103731, -74.0134224],
    [40.707697, -74.006941], # Gold Street.
    [40.707578, -74.007035], # Gold Street.
    [40.707458,  -74.007151], # Gold Street.
    [40.707341, -74.007286] # Gold Street.
    ]

print " "
for coord in incorrect:
    surrounding = getSurrounding(coord)

    streets = set([])
    threads = []
    for near in surrounding:
        t = threading.Thread(target=reverseLookup, args=(near, streets, streetsLock))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    print "COORD ({}, {}) HAS THESE STREETS: {}".format(coord[0], coord[1], streets)
