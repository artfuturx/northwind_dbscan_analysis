from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analyzers.customer_analyzer import analyze_customers
from analyzers.supplier_analyzer import analyze_suppliers
from analyzers.order_analyzer import analyze_orders
from analyzers.country_analyzer import analyze_countries

app = FastAPI(
    title="Northwind DBSCAN Analysis API",
    description="Northwind veritabanı üzerinde DBSCAN algoritması kullanarak müşteri, tedarikçi, sipariş ve ülke analizleri yapan REST API",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/customer-segmentation", 
         summary="Müşteri Segmentasyonu",
         description="Müşterileri satın alma davranışlarına göre gruplandırır")
async def customer_segmentation():
    return analyze_customers()


@app.get("/supplier-segmentation",
         summary="Tedarikçi Analizi",
         description="Tedarikçileri ürün performanslarına göre gruplandırır")
async def supplier_segmentation():
    return analyze_suppliers()

@app.get("/order-analysis",
         summary="Sipariş Analizi",
         description="Siparişleri çeşitli metrikler üzerinden analiz eder")
async def order_analysis():
    return analyze_orders()

@app.get("/country-analysis",
         summary="Ülke Analizi",
         description="Ülkeleri satış performanslarına göre gruplandırır")
async def country_analysis():
    return analyze_countries()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003) 