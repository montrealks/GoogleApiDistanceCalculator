__author__ = "Kris"

from urllib.parse import urlencode
from urllib.request import urlopen
import simplejson
import csv


# DESCRIPTION
"""
Micro-app that uses the Google Distance Matrix API to return the distance and the drive-time between a single origin and
as many as 2500 destinations.
"""

# HOT TO USE
"""
Use the config files directly below.
1.) Set the path to the CSV file containing the data to be analyzed. Must have a trailing forwardslash '/'
2.) Set the origin address. Can be a string or latitude longitude with a comma separating and no spaces
3.) Set the departure time using http://www.epochconverter.com/
3.) Ensure that the CSV has ALL of the mandatory headers (below)
"""

# NOTES
"""
-The Goole Distancematrix API returns two instances of trip duration. The first assumes light traffic, the second will
use historical traffic data for the time entered as DEPARTURE_TIME to determine the amount of traffic for that time and
thus the trip duration. It is therefore best to input a heavy traffic period so to have the greatest contrast in travel
duration.
-The DEPARTURE_TIME is called 'epoch time' and is measured in seconds since Jan 1 1970 GMT. Use the link to convert
from human time to epoch time
"""

# variables
ORIGIN = "209 rue maria, montreal, QC"
DEPARTURE_TIME = "1471276837"
CSV_LOCATION = 'C:\python_apps\distancematrix\project\src\csvs/'
CSV_IN_NAME = 'ccc.CSV'
CSV_OUT_NAME = CSV_IN_NAME[0:-4] + '_out.csv'
TEST_MODE = True  # when True limits rows in the result file to 4

# mandatory CSV headers. Others will be ignored. DO NOT EDIT ANYTHING HERE
DWT = 'duration with traffic'
DNT = 'duration no traffic'
D = 'distance'
LAT = 'latitude'
LON = 'longitude'

# API components. DO NOT EDIT ANYTHING HERE
GEOCODE_BASE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"
API_KEY = 

# Constants. DO NOT EDIT ANYTHING HERE
TRAFFIC_MODEL = 'pessimistic'  # Options are 'pessimistic', 'optimistic', and 'best_guess
MODE = 'driving'  # options are 'driving', 'walking', 'cycling', 'transit'


def distance_api(destination, **geo_args):
    geo_args.update({

        'origins': ORIGIN,
        'destinations': destination,
        'traffic_model': TRAFFIC_MODEL,
        'departure_time': DEPARTURE_TIME,
        'mode': MODE
    })

    url = GEOCODE_BASE_URL + '?' + urlencode(geo_args) + '&key=' + API_KEY
    print(url)
    result = simplejson.load(urlopen(url))
    distance = round(result['rows'][0]['elements'][0]['distance']['value'] / 1000, 2)  # km
    duration = int(result['rows'][0]['elements'][0]['duration']['value'] / 60)  # minutes
    duration_in_traffic = int(result['rows'][0]['elements'][0]['duration_in_traffic']['value'] / 60)  # minutes

    durations = {"distance": distance,
                 "duration no traffic": duration,
                 "duration with traffic": duration_in_traffic}

    return durations


def csv_updater():
    with open(CSV_LOCATION + CSV_IN_NAME, newline='') as csv_in:
        with open(CSV_LOCATION + CSV_OUT_NAME, 'w+', newline='') as csv_out:
            reader = csv.reader(csv_in)
            writer = csv.writer(csv_out)

            # turn reader into a list where the first item is the list of headers. Get the proper header positions
            all_rows = list(reader)
            col_lat = all_rows[0].index(LAT)  # latitude
            col_lon = all_rows[0].index(LON)  # longitude
            col_d = all_rows[0].index(D)  # checks the header for 'distance' and assigns column position
            col_dnt = all_rows[0].index(DNT)  # duration no traffic
            col_dwt = all_rows[0].index(DWT)  # duration with traffic

            writer.writerow(all_rows[0])

            escaper = 0
            for row in all_rows[1:]:
                latitude = row[col_lat]
                longitude = row[col_lon]

                api = distance_api(destination = latitude + "," + longitude)

                row[col_dnt] = api[DNT]
                row[col_dwt] = api[DWT]
                row[col_d] = api[D]

                """print("distance: ", row[col_d],
                      "duration with traffic: ",
                      row[col_dwt],
                      "duration no traffic ",
                      row[col_dnt])"""

                writer.writerow(row)
                escaper += 1

                if escaper > 3 and TEST_MODE:
                    break

csv_updater()
