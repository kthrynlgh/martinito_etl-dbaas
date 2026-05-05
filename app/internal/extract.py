import pandas as pd
from sqlalchemy import create_engine

DB_URL = "postgresql://martinito_etl_db_user:G8pGEOXUIW0SI9ePZ5WrZYqB8Tb0TNfG@dpg-d7sqcahkh4rs7399qsrg-a.singapore-postgres.render.com/martinito_etl_db"
engine = create_engine(DB_URL)

def load_csv(csv_path, table_name):
    try:
        df = pd.read_csv(csv_path)

        df.columns = [col.replace("'", "").strip() for col in df.columns]

        df.to_sql(f"stage_{table_name}", engine, if_exists='replace', index=False)
        print(f"Success! {table_name} loaded into staging area.")
    except Exception as e:
        print(f"Error loading {table_name}: {e}")
