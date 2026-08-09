import csv

with open('/home/Mridul/Smart-System-Stats-Analyzer/Metrics/Container2.csv', mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)