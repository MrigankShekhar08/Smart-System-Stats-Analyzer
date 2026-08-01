import csv

with open('/home/MridulPathak/Project1/Metrics/Container2.csv', mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)