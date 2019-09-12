# Parses raw NY intersection data and filters it for incorrect / duplicate
# intersection data points.
#
# Outputs two JSON files that are python dictionaries:
#   (1): intersectionToCrossStreets.json | maps (lat., long.) --> set([street1, street2, ...])
#        This is a mapping from each intersection's coordinate to its corresponding
#        cross streets.
#
#   (2): crossStreetsToIntersections.json | maps set([street1, street2, ...]) --> (lat., long.)
#        This is a mapping from each intersection's cross streets to its corresponding
#        coordinate.
#

import geocoder
import json
import os
import pickle
import threading

'''
# Extracts the geojson data file names.
path_to_geojson = "NY raw intersection data/"
geojson_files = sorted([pos_json for pos_json in os.listdir(path_to_geojson) if pos_json.endswith('.geojson')])

# Extracts the intersection features from each of the geojson data files.
geojson_features = []
for geojson in geojson_files:
    with open(path_to_geojson + geojson) as f:
        geojson_data = json.load(f)
        geojson_features.append(geojson_data['features'])
'''


## -------------------------------------------------------------------------- ##

# Generates "surrounding" coordinates in order to probe for cross streets
# around a given intersection coordinates.
kMod = 0.00001
kModifications = [
    (kMod, kMod), (kMod, -1 * kMod), (-1 * kMod, kMod), (-1 * kMod, -1 * kMod),
    (kMod, 0), (-1 * kMod, 0), (0, kMod), (0, -1 * kMod)
    ]
def getSurroundingCoords(coordinate):
    surrounding = []
    surrounding.append(coordinate)
    latitude = coordinate[0]
    longitude = coordinate[1]
    for mods in kModifications:
        surrounding.append([latitude + mods[0], longitude + mods[1]])

    return surrounding

# Function that uses the geocoder API to reverse lookup the street of a given
# coordinate.
def reverseLookup(coord, streets, streetsLock):
    g = geocoder.mapbox(coord, method='reverse', key='pk.eyJ1IjoiYXBwc2NsYXBwZXIiLCJhIjoiY2p2dzA4ZDZxMnEydjQ1bzF6emttaWtweiJ9.mYwgu-Jp2QpIKcy9cQY7sw')
    g_json = g.json
    with streetsLock:
        if g_json['raw']['text'] != None:
            streets.add(g_json['raw']['text'])


# Probes around the given coordinate and returns a set of potential cross streets
# for the given coordinate.
def getCrossStreets(coord):
    surrounding_coords = getSurroundingCoords(coord)
    streets = set([])
    streetsLock = threading.Lock()
    threads = []
    for near in surrounding_coords:
        t = threading.Thread(target=reverseLookup, args=(near, streets, streetsLock))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    return streets

## -------------------------------------------------------------------------- ##

f_old = open("crossStreetsToIntersections.pickle", "rb")
crossStreetsToIntersections = pickle.load(f_old)
f_old.close()

'''
num = 1
for feature in geojson_features[10]:
    print "DATA POINT #{}".format(num)
    num += 1
    # Gets the coordinate from the feature (lat., long.)
    coord = list(feature["geometry"]["coordinates"])
    coord.reverse()

    # Gets the nearby cross streets of the coordinate.
    cross_streets = getCrossStreets(coord)

    # If we can't find cross streets then its a bad data point (not an
    # intersection) so we skip it.
    if len(cross_streets) <= 1:
        print "TOO SMOLL:"
        print "COORD: {}".format(coord)
        print "CROSS_STREETS: {}".format(cross_streets)
        print " "
        continue

    # Maps coordinate to the cross streets pair.
    cross_streets_key = tuple(sorted(cross_streets))
    crossStreetsToIntersections.setdefault(cross_streets_key, []).append(coord)

    print "COORD ({}, {}) HAS THESE STREETS: {}".format(coord[0], coord[1], cross_streets)
    print "INTERSECTION CROSS STREETS {} HAS THESE COORDINATES: {}".format(cross_streets, crossStreetsToIntersections[cross_streets_key])
    print " "


'''

# For each intersection, we average the coordinates that mapped to
# that given intersection (i.e. its cross streets) and choose that to be the
# coordinate value for that intersection.
intersectionToCrossStreets = {}
for cross_streets_key, intersections in crossStreetsToIntersections.items():
    average_intersection = [0, 0]
    for coord in intersections:
        average_intersection[0] += coord[0]
        average_intersection[1] += coord[1]

    average_intersection[0] = average_intersection[0] / float(len(intersections))
    average_intersection[1] = average_intersection[1] / float(len(intersections))

    intersectionToCrossStreets[tuple(average_intersection)] = cross_streets_key
    crossStreetsToIntersections[cross_streets_key] = tuple(average_intersection)

f1 = open("intersectionToCrossStreets.pickle", "wb")
pickle.dump(intersectionToCrossStreets, f1)
f1.close()

f_new = open("crossStreetsToIntersection.pickle", "wb")
pickle.dump(crossStreetsToIntersections, f_new)
f_new.close()
