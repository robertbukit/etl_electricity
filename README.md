# End-to-End Real-Time Electricity Data Pipeline (ETL)

## Overview
This project implements a robust, an end-to-end **Data Engineering Pipeline** following the **ELT (Extract, Transform, Load)** architectural pattern. The pipeline automates the collection of real-time electricity data gridhub (wholesale price, demand, carbon intensity, etc) across multiple global zones. Data is fetched via a REST API, securely deposited into a local Data Lake, programmatically flattened and cleaned using pandas, structurally mapped into a PostgreSQL Data Warehouse, and fully automated using Windows Task Scheduler.

This repository serves as a foundational yet production-grade framework for aspiring Data Engineers. It demonstrates core competencies in handling nested JSON structures, managing local storage state (anti-overwrite design), database schema migrations, and local system orchestration.

---

## System Architecture

<img width="1096" height="377" alt="electricity_architect" src="https://github.com/user-attachments/assets/6a303707-ec93-4315-bc8b-46f67bb8d885" />

---


## Tech Stack
*   **Data Ingestion:** REST API Framework (`requests`, `json`)
*   **Data Lake Base Storage:** File System Infrastructure (JSON Architecture)
*   **Data Transformation:** Pandas Data Analysis Engine (`pandas`)
*   **Data Warehouse Target:** PostgreSQL Relational Database Engine (`psycopg2`)
*   **Workflow Orchestration & Scheduling:** Native Windows Task Scheduler Subsystem

---

## Project Structure
Below is the directory architecture of the engineering workspace:

```text
etl_electricity/
│
├── data/
│   ├── processed/          # Clean Zone: Stores unified tabular CSV fact datasets
│   └── raw/                # Data Lake: Houses immutable historical nested JSON data
│
├── scripts/
│   ├── extract.py          # Extraction script: Communicates with API and loads raw data
│   ├── transform.py        # Transformation engine: Dynamically loops files via Pandas
│   └── load.py             # Database connector: Controls automated DDL and Loop Inserts
│
├── .env                    # Secure workspace configuration (PostgreSQL credentials)
|── main.py                 # Central Controller Script (Pipeline Orchestrator)
├── requirement.txt         # All requirement/library dependencies
└── README.md               # Pipeline documentation deployment asset
```
---

## Configuration & Execution Workflow

#### 1. Environment Variable Setup (`.env`)
Create a `.env` deployment file at the project root directory containing your relational database target specifications:
```env
POSTGRES_USER=your_postgres_username
POSTGRES_PASSWORD=our_password
POSTGRES_PORT=5432
```

#### 2. Manual Pipeline Trigger
To execute the automated pipeline sequencing via terminal infrastructure, enter:
```powershell
# Activate local virtual environment
venv\Scripts\Activate

# Run the master workflow controller
python main.py
```

---

## Known Limitations
*   **Local Hardware Dependency:** The pipeline execution sequence is fully bound to the host computer state. If the laptop is shut down or entering sleep mode during the designated trigger threshold (**15:00**), the automation schedule will skip until the device status wakes up.
*   **API Rate Limitations:** The framework consumes a developer-tier public token limited to **500 transaction requests per day**. Increasing target zones or scheduling interval patterns closer than every 15 minutes poses a risk of triggering a `HTTP 402 (Payment Required)` exception block.

---


<img width="960" height="600" alt="Screenshot 2026-10-19 135238" src="https://github.com/user-attachments/assets/242802ed-f3ad-43af-9c0e-33ff6caa11fe" />
<img width="960" height="600" alt="image" src="https://github.com/user-attachments/assets/caedd597-87b4-4f24-ae5c-b307263f7c14" />
<img width="960" height="600" alt="image" src="https://github.com/user-attachments/assets/2e689b2e-5d46-48ef-9605-6406ecfeb90d" />

