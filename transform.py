import sqlite3
import pandas as pd

def clean_sqlite_table(db_path='warehouse.db'):
    """
    read from staging and perform data cleaning
    Standardize values across datasets (e.g., Japan store item prices in JPY and Myanmar store item prices in USD are converted to a common currency or format).
    """
    conn = sqlite3.connect(db_path)

    JYP_to_USD = 0.0073

    df_japan = pd.read_sql("SELECT * FROM stage_japan", conn)
    df_japan.columns = df_japan.columns.str.strip()
    df_japan = df_japan.drop_duplicates().fillna('Unknown')

    #Standardize Currency: Convert JYP to USD
    df_japan['price_usd'] = df_japan['price'] * JYP_to_USD
    df_japan['source_country'] = 'Japan'
    df_japan.to_sql("trans_japan", conn, if_exists='replace', index=False)

    df_myanmar = pd.read_sql("SELECT * FROM stage_myanmar", conn)
    df_myanmar.columns = df_myanmar.columns.str.strip()
    df_myanmar = df_myanmar.drop_duplicates().fillna('Unknown')

    #Myanmar is already in USD
    df_myanmar['price_usd'] = df_myanmar['price']
    df_myanmar['source_country'] = 'Myanmar'
    df_myanmar.to_sql("trans_myanmar", conn, if_exists='replace', index=False)

    conn.close()
    print("Transformation completed! The data is cleaned and standardized.")

