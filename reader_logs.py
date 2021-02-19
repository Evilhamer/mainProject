import csv

with open('./data/data.csv', "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["name_data"], "-", row["b_data"])