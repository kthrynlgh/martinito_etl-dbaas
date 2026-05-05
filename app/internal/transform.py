import pandas as pd
from sqlalchemy import create_engine

DB_URL = "postgresql://martinito_etl_db_user:G8pGEOXUIW0SI9ePZ5WrZYqB8Tb0TNfG@dpg-d7sqcahkh4rs7399qsrg-a.singapore-postgres.render.com/martinito_etl_db"
engine = create_engine(DB_URL)

def clean_table():
    JYP_to_USD = 0.0073

    df_j_items = pd.read_sql("SELECT * FROM stage_japan_items", engine)
    df_j_sales = pd.read_sql("SELECT * FROM stage_japan_sales", engine)
    df_japan = pd.merge(df_j_sales, df_j_items, left_on='product_id', right_on='id', how='left')

    df_japan.columns = df_japan.columns.str.strip().str.lower()
    df_japan = df_japan.drop_duplicates().fillna('Unknown')

    df_japan = df_japan.rename(columns={'product_name': 'item_name', 'category': 'item_category'})
    df_japan['price_usd'] = df_japan['price'] * JYP_to_USD
    df_japan['source_country'] = 'Japan'

    cols_to_keep = ['invoice_id', 'item_name', 'item_category', 'price_usd', 'quantity', 'source_country']
    df_japan[cols_to_keep].to_sql("trans_japan", engine, if_exists='replace', index=False)

    df_m_items = pd.read_sql("SELECT * FROM stage_myanmar_items", engine)
    df_m_sales = pd.read_sql("SELECT * FROM stage_myanmar_sales", engine)
    df_myanmar = pd.merge(df_m_sales, df_m_items, left_on='product_id', right_on='id', how='left')

    df_myanmar.columns = df_myanmar.columns.str.strip().str.lower()
    df_myanmar = df_myanmar.drop_duplicates().fillna('Unknown')

    df_myanmar = df_myanmar.rename(columns={'name': 'item_name', 'type': 'item_category'})
    df_myanmar['price_usd'] = df_myanmar['price']
    df_myanmar['source_country'] = 'Myanmar'

    df_myanmar[cols_to_keep].to_sql("trans_myanmar", engine, if_exists='replace', index=False)

    print("Transformation completed! The data is cleaned and standardized.")

