import re
import csv
from random import *

# run this script to generate a table that also has ratings pulled from reviews and clicks, an artificial measure which we will keep updating
file1 = open('RAW_recipes_clean.csv', "r")
lines = file1.readlines()
file1.close()
file2 = open('final_data.csv', "w")

num_lines = len(lines)
for i in range(num_lines):
    row = lines[i]
    if i % 50 == 0:
        print(i)
    cols = re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", row)
    r_id = cols[1]
    rating = 0
    n = 1
    with open('RAW_interactions.csv') as ratings_csvfile:
        ratings_dict = csv.DictReader(ratings_csvfile)
        for line in ratings_dict:
            if r_id == line['recipe_id']:
                rating = (rating + int(line['rating']))/n
                n += 1
    if i == 0:
        file2.write(row[:-2] + "," + "rating, clicks" + "\n")
    else:
        file2.write(row[:-2] + "," + str(rating) + "," +
                    str(randrange(0, 1000)) + "\n")
