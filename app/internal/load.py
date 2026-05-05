import pandas as pd
from sqlalchemy import create_engine

DB_URL = "postgresql://martinito_etl_db_user:G8pGEOXUIW0SI9ePZ5WrZYqB8Tb0TNfG@dpg-d7sqcahkh4rs7399qsrg-a.singapore-postgres.render.com/martinito_etl_db"
engine = create_engine(DB_URL)

def load_presentation():
   df_j = pd.read_sql("SELECT * FROM trans_japan", engine)
   df_m = pd.read_sql("SELECT * FROM trans_myanmar", engine)

   big_table = pd.concat([df_j, df_m], ignore_index=True)

   big_table.to_sql("pres_big_table", engine, if_exists='replace', index=False)

   print("BIG TABLE created successfully! Presentation layer is now ready.")