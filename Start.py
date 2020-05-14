import csv
import numpy as np
import matplotlib.pyplot as plt
import pylab
from pylab import xticks

# The latitude and longitude extent of the provided map.
MAP_TOP = -6.2
MAP_BOTTOM = -36.82
MAP_LEFT = 106.8
MAP_RIGHT = 174.77

EARTH_RADIUS = 6371  # Mean radius of the earth in kilometers.

def is_valid_record(record):

    # To check if central pressure and wind speed are not empty
    if(record[6] != "" and record[8] != ""):
        return True
    else:
        return False


def parse_record(record):
   
    #Converting the data from record into a dictionary called record_dictionary after checking if the value is present
    record_dictionary = dict()

    if record[1] != '':
        record_dictionary['id'] = record[1]
    if record[0] != '':
        record_dictionary['name'] = record[0]
    if record[2] != '':
        record_dictionary["year"]=int(record[2][:4])
        record_dictionary["month"]= int(record[2][5:7])
        record_dictionary["day"]=int(record[2][8:10])
        record_dictionary["hour"]=int(record[2][11:13])
    if record[6] !='':
        record_dictionary["central pressure"]= int(record[6])
    if  record[7] !='':
        record_dictionary["radius"]= float(record[7])
    if record[8] !='':
        record_dictionary["speed"]=float(record[8])
    if record[4] != '':
        record_dictionary["lat"]=float(record[4])
    if record[5] != '':
        record_dictionary["long"]=float(record[5])

    return record_dictionary


def convert_lat_long(lat, long):

    x, y = 0.0, 0.0

    #calculating the width of the map
    width = float(MAP_TOP) - float(MAP_BOTTOM)

    # calculating the height of the map
    height = float(MAP_RIGHT) - float(MAP_LEFT)

    #calculating the coordinates
    x = ((long - MAP_LEFT)/height)
    y = ((lat - MAP_BOTTOM)/width)

    return (x, y)


def pressure_distribution(records):

    distribution_dictionary = dict()

    #calculating the frequency of different central pressure
    for d in records:
        if d['central pressure'] in distribution_dictionary:
            distribution_dictionary[d['central pressure']]+=1
        else:
            distribution_dictionary[d['central pressure']]=1

    return distribution_dictionary


def pressure_histogram(distribution_dictionary):

    if not distribution_dictionary:
        return None

    # Order the data based on the central pressure value.
    frequency_data = sorted(distribution_dictionary.items())

    # Generate the lists of x values and y values.
    x_list = [frequency_data[i][0] for i in range(len(frequency_data))]
    y_list = [frequency_data[i][1] for i in range(len(frequency_data))]

    # Reduced the width from 1 to 0.5
    plt.bar(x_list, y_list,  width=0.5)

    #shows the grid for better readibility of bars
    plt.grid(True)

    #Increased the fontsize of axis labels
    pylab.xticks(fontsize=15)
    pylab.yticks(fontsize=15)

    #To print the title of histogram and increased the fontsize as well
    plt.title("Frequency of Central Pressure", fontsize=20)

    # To print the name of x axis of histogram
    plt.xlabel("Central Pressure (in Pascal)")

    # To print the name of the y axis of histogram
    plt.ylabel("Frequency")

    plt.show()

    return None


def animation_data(cyclone_records):

    cyclone_track = list()

    #Traversing through cyclone records and assigning them to tuples
    for i in cyclone_records:
        cyclone_tup =     (int(i['year']),
                           int(i['month']),
                           int(i['day']),
                           int(i['hour']),
                           float(i['lat']),
                           float(i['long']),
                           float(i['speed']),
                           str(i['name']),)

        #adding tuples to the list cyclone_track
        cyclone_track.append(cyclone_tup)

        #sorting the cyclone_track
        print(sorted(cyclone_track))

    return cyclone_track

def generate_heat_map(records):

    array_size = 50  # y, x dimensions of the heat-map
    heat_map_data = np.zeros(shape=(array_size, array_size))# type = np.float64)

    #traversing through records
    for d in records:
        
        #calculate the value of latitude and longitude into x and y
        x,y = convert_lat_long(d['lat'], d['long'])

        #round off of the values to define absolute value of index in matrix
        x=round(x*49)
        y=round(y*49)

        #counting the number of occurance of cyclones in area
        if 'radius' not in d and x < 50 and y < 50:
            heat_map_data[x][y] += 1
        elif 'radius' in d and x < 50 and y < 50:
            r = round(d['radius'] / EARTH_RADIUS)
            for i in range(r):
                heat_map_data[x+i][y-i] += 1
                heat_map_data[x+i][y+i] += 1
                heat_map_data[x-i][y+i] += 1
                heat_map_data[x-i][y-i] += 1

    return heat_map_data

def read_data_set(file_name):
    """
    Reads in and processes a csv file of the given name.
    :param file_name: The name of the file (string) to process.
    :return: A list of records.
    """

    # Read in the data set
    input_data = open(file_name, mode="r")
    input_reader = csv.reader(input_data)
    next(input_reader)  # Remove the header

    data_set = []

    for record in input_reader:
        if record[1] and record[2] and record[4] and record[5] and is_valid_record(record):
            data_set.append(record)

    input_data.close()

    return data_set

if __name__ == "__main__":

    data_set = read_data_set("Cyclones.csv")

    parsed_data = []

    for record in data_set:
        parsed_record = parse_record(record)
        if parsed_record:
            parsed_data.append(parsed_record)

    if parsed_data:
        histogram_data = pressure_distribution(parsed_data)
        pressure_histogram(histogram_data)
    else:
        print("You need to check the code")
