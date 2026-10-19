import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

pg_user = os.getenv("POSTGRES_USER")
pg_port = int(os.getenv("POSTGRES_PORT"))
pg_password = os.getenv("POSTGRES_PASSWORD")

pg_conn = psycopg2.connect(
    user=pg_user,
    password=pg_password,
    host="localhost",
    port=pg_port,
    database="postgres"
)

pg_conn.autocommit = True
pg_curr = pg_conn.cursor()

# check and create database for electricity
try:
    pg_curr.execute("CREATE DATABASE db_electricity")
    print("db_electricity successfully created")

except psycopg2.errors.DuplicateDatabase:
    print("Database db_electricity already exist")

pg_curr.close()
pg_conn.close()


# Create table into db_electricity

conn = psycopg2.connect(
    user=pg_user,
    password=pg_password,
    host="localhost",
    port=pg_port,
    database="db_electricity"
)
conn.autocommit = True
curr = conn.cursor()

curr.execute("""
CREATE TABLE IF NOT EXISTS ELECTRICITIES_5ZONE 
(Zone varchar(20), Metric varchar(200), Value numeric, Unit varchar(20), Timestamp timestamp,
Resolution varchar(10), Updated bigint, Attribution text, License varchar(50))
""")

print("Table ELECTRICITIES_5ZONE successfully created")

# Run firstly the query of creating database
conn.commit()

# Insert data into ELECTRICITIES_5ZONE 
csv_file_path = "data/processed/master_data_electricity_latest.csv"

if os.path.exists(csv_file_path):
    df = pd.read_csv(csv_file_path)

    for i, row in df.iterrows():
        insert_query = """
        INSERT INTO ELECTRICITIES_5ZONE (Zone, Metric, Value, Unit, Timestamp, Resolution,
        Updated, Attribution, License)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data_to_insert = (
            row['Zone'],
            row['Metric'],
            row['Value'],
            row['Unit'],
            row['Timestamp'],
            row['Resolution'],
            row['Updated'],
            row['Attribution'],
            row['License']
        )

        curr.execute(insert_query, data_to_insert)

    conn.commit()
    print("Load success! all datas successfully migrated to postgres")

else:
    print(f"File {csv_file_path} not found!")


curr.close()
conn.close()


