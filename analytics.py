import pandas as pd
import sqlite3

def run_analytics(db_path='warehouse.db'):
    conn = sqlite3.connect(db_path)

    df = pd.read_sql("SELECT * FROM pres_big_table", conn)

    print("=== RETAIL PERFORMANCE INSIGHTS ===")

    # 1. Price Parity (Average Price per Country)
    # Insight: Understand which market has a higher price point in USD.
    avg_price = df.groupby('source_country')['price_usd'].mean()
    print(f"\n[1] Average Item Price (USD):\n{avg_price.to_frame('Avg Price')}")

    # 2. Inventory Volume (SKU Count)
    # Insight: Identify which region provides the most variety/stock.
    inventory = df['source_country'].value_counts()
    print(f"\n[2] Total Inventory Count:\n{inventory.to_frame('Total SKUs')}")

    # 3. Top 3 Most Expensive Items (Global)
    # Insight: Identify high-value luxury goods across all regions.
    top_items = df.nlargest(3, 'price_usd')[['item_name', 'price_usd', 'source_country']]
    print(f"\n[3] Top 3 Premium Items:\n{top_items}")

    # 4. Currency Impact Summary
    # Insight: Compare raw Japan JPY vs standardized USD to see the conversion scale.
    # (Only applies if you kept the original price column during transformation)
    if 'price' in df.columns:
        jp_sample = df[df['source_country'] == 'Japan'].head(1)
        print(f"\n[4] Currency Check (Japan): {jp_sample['price'].values[0]} JPY -> ${jp_sample['price_usd'].values[0]:.2f} USD")

    # 5. Data Cleanliness Score
    # Insight: Check for any remaining nulls or 'Unknown' placeholders.
    null_count = (df == 'Unknown').sum().sum()
    print(f"\n[5] Data Integrity: {null_count} placeholders found in final dataset.")

    conn.close()

if __name__ == "__main__":
    run_analytics()