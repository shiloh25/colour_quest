import csv
import random

# retrieve colours from csv file and put them in a list
file = open("00_colour_list_hex_v3.csv", "r")
all_colours = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row
all_colours.pop(0)
print(all_colours)
