from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.internal import extract, transform, load, analytics

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Retail ETL System Active on Render"}

@app.post("/pipeline/run")
async def trigger_pipeline():
    try:
        extract.load_csv('data/source/japan_store/japan_items.csv', 'japan_items')
        extract.load_csv('data/source/japan_store/sales_data.csv', 'japan_sales')
        extract.load_csv('data/source/myanmar_store/myanmar_items.csv', 'myanmar_items')
        extract.load_csv('data/source/myanmar_store/sales_data.csv', 'myanmar_sales')

        transform.clean_table()

        load.load_presentation()

        analytics.run_analytics()

        return {"status": "success", "message": "Pipeline completed successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}