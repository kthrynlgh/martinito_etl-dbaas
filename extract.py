import pandas as pd
import sqlite3
import os

def load_csv(csv_path, table_name, db_path='warehouse.db'):
    """
    write a script that loads source csv data to sqlite file in the staging area
    """
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_csv(csv_path)
        df.to_sql(f"stage_{table_name}", conn, if_exists='replace', index=False)
        print(f"Success! {table_name} loaded into staging area.")
    except Exception as e:
        print(f"Error loading {table_name}: {e}")
    finally:
        conn.close()