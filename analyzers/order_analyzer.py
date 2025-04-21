# Problem 2
# Ürün Kümeleme (Benzer Ürünler) 
# Veritabanı tabloları: Products, OrderDetails

# Soru: "Benzer sipariş geçmişine sahip ürünleri DBSCAN ile gruplandırın. Az satılan ya da alışılmadık kombinasyonlarda geçen ürünleri belirleyin."

# Özellik vektörleri:
# Ortalama satış fiyatı 
# Satış sıklığı 
# Sipariş başına ortalama miktar
# Kaç farklı müşteriye satıldı

# Amaç: Benzer ürünlerin segmentasyonu
# -1 olan ürünler → belki özel ürünler veya niş ihtiyaçlar

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator
from db_connect import engine

def analyze_orders():
    query = """
    SELECT 
        o.order_id,
        o.order_date,
        o.ship_city,
        o.ship_country,
        COUNT(od.product_id) as total_products,
        SUM(od.quantity) as total_quantity,
        SUM(od.quantity * od.unit_price) as total_amount,
        COUNT(DISTINCT od.product_id) as unique_products
    FROM 
        orders o
        INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY 
        o.order_id, o.order_date, o.ship_city, o.ship_country
    """

    # Veriyi çekme
    df = pd.read_sql_query(query, engine)
    print("Veri önizleme:")
    print(df.head())

    # Özellik vektörlerini seçme
    X = df[["total_products", "total_quantity", "total_amount", "unique_products"]]

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
    plt.scatter(df['total_amount'], df['total_quantity'], c=df['cluster'], cmap='plasma', s=60)
    plt.xlabel("Toplam Tutar")
    plt.ylabel("Toplam Miktar")
    plt.title("Sipariş Segmentasyonu (DBSCAN)")
    plt.grid(True)
    plt.colorbar(label='Küme No')
    plt.show()

    # Aykırı değerleri analiz etme
    outliers = df[df["cluster"] == -1]
    print("\nAykırı değer sayısı:", len(outliers))
    print("\nAykırı değerler (özel siparişler):")
    print(outliers[["order_id", "order_date", "ship_city", "ship_country", "total_amount", "total_quantity"]])

    # Sonuçları hazırlama
    results = {
        "total_clusters": len(df["cluster"].unique()),
        "outliers": df[df["cluster"] == -1].to_dict(orient="records"),
        "clusters": df.to_dict(orient="records")
    }
    
    return results 