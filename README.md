# S³A — Smart Server Stats Analyzer

A CLI tool that runs in the background at regular, short intervals to quietly track server health, detect anomalies, and flag issues before they become problems.

## Overview

S³A is built as a three-layer pipeline:

**Bash → SQLite → Python**

| Layer | Role | Status |
|---|---|---|
| 🖥️ Bash | Collects server metrics at set intervals, logs to CSV | ✅ Working |
| 🗄️ SQLite | Ingests CSV data into a rolling database, clears old entries | 🔜 In progress |
| 🐍 Python | Analyzes trends, computes median/average, detects anomalies, triggers notifications | 🔜 Planned |

Structurally, this is a small-scale ETL pipeline — bash extracts, Python transforms, SQLite loads.

## Design Philosophy

- **No GUI.** Built with headless servers in mind — this needs to run where there's no screen to look at.
- **Observe-only, not autonomous.** S³A flags issues; it does not touch running processes. A tool that kills processes on its own judgment can cause more damage than the problem it's watching for.

## Current Status

The bash metric-collection layer is complete and has run successfully multiple times, collecting required data and logging it correctly to CSV. Next up: SQLite ingestion.

## Roadmap

- [x] Bash metric-collection layer
- [ ] SQLite ingestion layer
- [ ] Python anomaly-detection layer (median/average-based)
- [ ] Notification system (`notify-send`) with severity-based triggers
- [ ] Weekly cron reports

## Author
Mridul Pathak      
