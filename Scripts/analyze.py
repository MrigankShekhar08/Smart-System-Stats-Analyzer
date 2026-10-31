import sqlite3
import statistics
from datetime import datetime
from pathlib import Path
import subprocess

script_dir = Path(__file__).parent  ;  #parent directory of the script
script_r = script_dir.parent ; #absolute parent directory
DB_PATH = script_r/"Metrics"/"system_metrics.db"  ; #path to the database file

#DB query and IN-SQL ARITHMETIC

def fetch_metrics():
    
    #Reads metric records from SQLITE and calculates raw percentage columns
    
    #Checking whether the database file exists
    if not DB_PATH.exists():
        print(f"Database file not found at {DB_PATH}")
        return[]
    
    #A temporary read connection to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = """SELECT
    timestamp, (us_cpu + sy_cpu) AS cpu_busy,
    wa_cpu AS cpu_wait,
    (used_ram / tot_ram * 100.0) AS ram_used,
    (Disk_used / Disk_tot * 100.0) AS disk_used,
    Disk_used,
    Disk_tot
    FROM system_metrics
    ORDER BY timestamp ASC;"""
    
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def calculate_p95(data):
    """Calculates the 95th percentile from a numeric list."""
    if not data:
        return 0.0
    
    sorted_data=sorted(data)
    idx = int(0.95 * len(sorted_data))
    return sorted_data[min(idx, len(sorted_data) - 1)]


def check_alerts(rows):
    """Checks the most recent metric row for abnormal spikes and sends desktop alert"""
    if not rows :
        return
    
    latest = rows[-1]
    timestamp = latest[0]
    cpu_busy = latest[1]
    ram_used = latest[3]
    
    alerts = []
    if cpu_busy > 85.0:
        alerts.append(f"High CPU Usage Alert: {cpu_busy:.1f}%")
    if ram_used > 90.0:
        alerts.append(f"High RAM Usage Alert: {ram_used:.1f}%")
        
    if alerts:
        alert_msg = " | ".join(alerts)
        try:
            subprocess.run(["notify-send",
                            "-u", "critical","System Stats Alert",
                            f"[{timestamp}]\n{alert_msg}"], check=True)
        except Exception as e:
            print(f"Failed to send desktop alert: {e}")



def generate_report():
    """Parses data, computes statistical metrics and forecasts disk exhaustion"""
    
    rows = fetch_metrics()
    if not rows: 
        print("No metric records availiable for analysis")
        return
    
    timestamps = [datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S") for r in rows]
    cpu_busy = [r[1] for r in rows]
    cpu_wait = [r[2] for r in rows]
    ram_used = [r[3] for r in rows]
    disk_used = [r[4] for r in rows]
    
    print ("=" * 55)
    print("    SYSTEM STATS ANALYZER REPORT (StdLib v1)   ")
    print ("=" * 55)
    print(f"Total Logged Records : {len(rows)}")
    print(f"Time Range           : {timestamps[0]} to {timestamps[-1]}\n")
    
    metrics = {
        "CPU Busy %" : cpu_busy,
        "CPU Wait %" : cpu_wait,
        "RAM Used %" : ram_used,
        "Disk Used %" : disk_used
    }
    
    for name, values in metrics.items():
        
        avg_val = statistics.mean(values)
        max_val = max(values)
        p95_val = calculate_p95(values)
        std_val = statistics.stdev(values) if len(values) > 1 else 0.0
        
        print(f"--- {name.upper()} ---")
        print(f"  Average (Mean) : {avg_val:.2f}%")
        print(f"  95th Percentile: {p95_val:.2f}%")
        print(f"  Peak (Max)     : {max_val:.2f}%")
        print(f"  Volatility (σ) : {std_val:.2f}\n")
        
    if len(timestamps) > 1:
        
        time_diff_hours = (timestamps[-1] - timestamps[0]).total_seconds() / 3600.0
        bytes_growth = rows[-1][5] - rows[0][5] 
        latest_disk_used = rows[-1][5]
        latest_disk_tot = rows[-1][6]
        
        print("--- DISK CAPACITY PROJECTION ---")
        if time_diff_hours > 0 and bytes_growth > 0:
            bytes_per_hour = bytes_growth / time_diff_hours
            remaining_bytes = latest_disk_tot - latest_disk_used
            hours_remaining = remaining_bytes / bytes_per_hour
            
            print(f"  Current Growth Rate : {bytes_per_hour / (1024**2):.2f} MB/hour")
            print(f"  Estimated Full In   : {hours_remaining / 24.0:.1f} days\n")
        else:
            print("  Disk usage is stable or decreasing. No capacity breach predicted.\n")
            
            
            
if __name__ == "__main__":
    data_rows = fetch_metrics()
    check_alerts(data_rows)
    generate_report()