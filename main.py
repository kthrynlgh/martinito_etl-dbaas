import extract
import transform
import load
import analytics

def run_pipeline():
    print("Starting ETL Pipeline...")

    # 1. Extract
    extract.load_csv('data/source/japan_store/japan_items.csv', 'japan_items')
    extract.load_csv('data/source/japan_store/sales_data.csv', 'japan_sales')
    extract.load_csv('data/source/myanmar_store/myanmar_items.csv', 'myanmar_items')
    extract.load_csv('data/source/myanmar_store/sales_data.csv', 'myanmar_sales')

    # 2. Transform
    transform.clean_sqlite_table()

    # 3. Load
    load.load_presentation()

    # 4. Analytics
    analytics.run_analytics()

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()