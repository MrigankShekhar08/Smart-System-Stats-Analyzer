from pathlib import Path
import csv
script_p = Path(__file__).parent
script_r = script_p.parent
with open(script_r/"Metrics"/"Container2.csv", mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)