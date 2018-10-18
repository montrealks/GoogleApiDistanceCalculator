### DESCRIPTION
Micro-app that uses the Google Distance Matrix API to return the distance and the drive-time between a single origin and
as many as 2500 destinations.

### HOW TO USE

Use the config files directly below.
1. Set the path to the CSV file containing the data to be analyzed. Must have a trailing forwardslash '/'
2. Set the origin address. Can be a string or latitude longitude with a comma separating and no spaces
3. Set the departure time using http://www.epochconverter.com/
3. Ensure that the CSV has ALL of the mandatory headers (below)


### NOTES

* The Goole Distancematrix API returns two instances of trip duration. The first assumes light traffic, the second will
use historical traffic data for the time entered as DEPARTURE_TIME to determine the amount of traffic for that time and
thus the trip duration. It is therefore best to input a heavy traffic period so to have the greatest contrast in travel
duration.
* The DEPARTURE_TIME is called 'epoch time' and is measured in seconds since Jan 1 1970 GMT. Use the link to convert
from human time to epoch time
