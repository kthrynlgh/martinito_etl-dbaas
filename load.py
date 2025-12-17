import pandas as pd
import sqlite3
import os

def load_presentation(db_path='warehouse.db'):
   """
   This creates the final consolidated “BIG TABLE”.
   Loads all cleaned Japan + Myanmar tables from the transformation DB.
   """
   conn = sqlite3.connect(db_path)

   df_j = pd.read_sql("SELECT * FROM trans_japan", conn)
   df_m = pd.read_sql("SELECT * FROM trans_myanmar", conn)

   big_table = pd.concat([df_j, df_m], ignore_index=True)

   big_table.to_sql("pres_big_table", conn, if_exists='replace', index=False)
   conn.close()
   print("BIG TABLE created successfully! Presentation layer is now ready.")