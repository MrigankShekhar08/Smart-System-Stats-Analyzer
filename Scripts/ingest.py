
from pathlib import Path
import csv
import sqlite3
import sys


def init_db(db_path):
    #Ensures Database is created and tables are created/exist.
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL UNIQUE,
                us_cpu REAL,
                sy_cpu REAL,
                wa_cpu REAL,
                Disk_tot REAL,
                Disk_used REAL,
                Disk_ava REAL,
                tot_ram REAL,
                used_ram REAL,
                ava_ram REAL
            )
        ''')
    conn.commit()
        
 
def import_csv_to_db(csv_fp,db_fp):
    """Reads CSV file and inserts rows into the database."""
    
    init_db(db_fp)  # Ensure the database and table are initialized
    
    with sqlite3.connect(db_fp) as conn:
        cursor = conn.cursor()
        
        with open(csv_fp, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Preparing batch data for efficient insertion
            to_db = [
                (
                    (row['Time_Stamp']),
                    float(row['us_CPU%']),
                    float(row['sy_CPU%']),
                    float(row['wa_CPU%']),
                    float(row['Disk_tot']),
                    float(row['Disk_use']),
                    float(row['Disk_ava']),
                    float(row['tot_RAM']),
                    float(row['used_RAM']),
                    float(row['ava_RAM'])
                ) for row in reader
            ]
            cursor.executemany('''
                    INSERT OR IGNORE INTO system_metrics (timestamp, us_cpu, sy_cpu, wa_cpu, Disk_tot, Disk_used, Disk_ava, tot_ram, used_ram, ava_ram)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', to_db)

        
        conn.commit()

if __name__ == "__main__":
    print("Starting ingestion script...")
    script_dir = Path(__file__).parent  ;  #parent directory of the script
    script_r = script_dir.parent ;        #Absolute parent directory of the script
    metrics_dir = script_r/"Metrics" 
    metrics_dir.mkdir(parents=True, exist_ok=True) ; #Checks if the metrics directory exists, if not creates it
    db_path = metrics_dir/"system_metrics.db"
    csv_fp = metrics_dir/"Container2.csv" ;         #Actual path of the file
    
    import_csv_to_db(csv_fp, db_path)
 