# Problem 3: 

# Tedarikçi Segmentasyonu Veritabanı tabloları: Suppliers, Products, OrderDetails

# Soru: "Tedarikçileri sağladıkları ürünlerin satış performansına göre gruplandırın. Az katkı sağlayan veya sıra dışı tedarikçileri bulun."

# Özellik vektörleri: 
# Tedarik ettiği ürün sayısı
# Bu ürünlerin toplam satış miktarı
# Ortalama satış fiyatı
# Ortalama müşteri sayısı


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator
from db_connect import engine

def analyze_suppliers():
    query = """
    SELECT 
        s.supplier_id,
        s.company_name,
        COUNT(DISTINCT p.product_id) as total_products,
        SUM(od.quantity) as total_sales_quantity,
        AVG(od.unit_price) as avg_sale_price,
        COUNT(DISTINCT o.customer_id) as unique_customers
    FROM 
        suppliers s
        INNER JOIN products p ON s.supplier_id = p.supplier_id
        INNER JOIN order_details od ON p.product_id = od.product_id
        INNER JOIN orders o ON od.order_id = o.order_id
    GROUP BY 
        s.supplier_id, s.company_name
    HAVING 
        COUNT(DISTINCT p.product_id) > 0
    """
    
    # Veriyi çekme
    df = pd.read_sql_query(query, engine)
    print("Veri önizleme:")
    print(df.head())
    
    # Özellik vektörlerini seçme
    features = ["total_products", "total_sales_quantity", "avg_sale_price", "unique_customers"]
    X = df[features]
    
    # Veriyi ölçeklendirme
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Optimal eps değerini bulma ve görselleştirme
    def find_optimal_eps(X_scaled, min_samples=3):
        neighbors = NearestNeighbors(n_neighbors=min_samples).fit(X_scaled)
        distances, _ = neighbors.kneighbors(X_scaled)
        distances = np.sort(distances[:, min_samples-1])
        
        kneedle = KneeLocator(range(len(distances)), distances, curve='convex', direction='increasing')
        optimal_eps = distances[kneedle.elbow]
        
        plt.figure(figsize=(10, 6))
        plt.plot(distances)
        plt.axvline(x=kneedle.elbow, color='r', linestyle='--', label=f'Optimal eps: {optimal_eps:.2f}')
        plt.xlabel('Points sorted by distance')
        plt.ylabel(f'{min_samples}-th nearest neighbor distance')
        plt.title('Elbow Method for Optimal eps')
        plt.legend()
        plt.grid(True)
        plt.show()
        
        return optimal_eps

    optimal_eps = find_optimal_eps(X_scaled)
    dbscan = DBSCAN(eps=optimal_eps, min_samples=3)
    df["cluster"] = dbscan.fit_predict(X_scaled)
    
    # Kümeleme sonuçlarını görselleştirme
    plt.figure(figsize=(12, 8))
    plt.scatter(df['total_sales_quantity'], df['avg_sale_price'], c=df['cluster'], cmap='plasma', s=60)
    plt.xlabel("Toplam Satış Miktarı")
    plt.ylabel("Ortalama Satış Fiyatı")
    plt.title("Tedarikçi Segmentasyonu (DBSCAN)")
    plt.grid(True)
    plt.colorbar(label='Küme No')
    plt.show()

    # Aykırı değerleri analiz etme
    outliers = df[df["cluster"] == -1]
    print("\nAykırı değer sayısı:", len(outliers))
    print("\nAykırı değerler (sıra dışı tedarikçiler):")
    print(outliers[["company_name", "total_products", "total_sales_quantity", "avg_sale_price", "unique_customers"]])
    
    # Sonuçları hazırlama
    results = {
        "total_clusters": len(df["cluster"].unique()),
        "outliers": df[df["cluster"] == -1].to_dict(orient="records"),
        "clusters": df.to_dict(orient="records")
    }
    
    return results 