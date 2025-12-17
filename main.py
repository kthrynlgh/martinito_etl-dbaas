import extract
import transform
import load
import analytics

def run_pipeline():
    print("Starting ETL Pipeline...")

    # 1. Extract
    extract.load_csv('data/japan_sales.csv', 'japan')
    extract.load_csv('data/myanmar_sales.csv', 'myanmar')

    # 2. Transform
    transform.clean_sqlite_table()

    # 3. Load
    load.load_presentation()

    # 4. Analytics
    analytics.generate_insights()

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()