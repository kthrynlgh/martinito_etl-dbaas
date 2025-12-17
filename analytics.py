import pandas as pd
import sqlite3

def run_analytics(db_path='warehouse.db'):
    conn = sqlite3.connect(db_path)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)

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

    # 4. Category Revenue Contribution
    # Insight: Calculates which category generates the most potential revenue (Price * Quantity)
    df['total_value'] = df['price_usd'] * df['quantity']
    cat_perf = df.groupby(['source_country', 'item_category'])['total_value'].sum().unstack().fillna(0)
    print("\n[4] Category Value Contribution per Country (USD):")
    print(cat_perf)

    # 5. Strategic Category Gap Analysis
    # Insight: Identifies which categories exist in one country but are missing in the other
    pivot_count = df.groupby(['item_category', 'source_country']).size().unstack(fill_value=0)
    gaps = pivot_count[(pivot_count['Japan'] == 0) | (pivot_count['Myanmar'] == 0)]

    print("\n[5] Strategic Growth: Category Gaps Identified")
    if not gaps.empty:
        print("The following categories are exclusive to one region and represent expansion opportunities:")
        print(gaps)
    else:
        print("Inventory Synergy: Both regions currently carry all the same categories.")

    conn.close()

if __name__ == "__main__":
    run_analytics()