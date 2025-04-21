import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator
from db_connect import engine

def analyze_countries():
    query = """
    SELECT 
        c.country,
        COUNT(DISTINCT o.order_id) as total_orders,
        AVG(od.unit_price * od.quantity) as avg_order_value,
        AVG(od.quantity) as avg_products_per_order
    FROM 
        customers c
        INNER JOIN orders o ON c.customer_id = o.customer_id
        INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY 
        c.country
    HAVING 
        COUNT(DISTINCT o.order_id) > 0
    """

    # Veriyi çekme
    df = pd.read_sql_query(query, engine)
    print("Veri önizleme:")
    print(df.head())

    # Özellik vektörlerini seçme
    X = df[["total_orders", "avg_order_value", "avg_products_per_order"]]

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
    plt.scatter(df['total_orders'], df['avg_order_value'], c=df['cluster'], cmap='plasma', s=60)
    plt.xlabel("Toplam Sipariş Sayısı")
    plt.ylabel("Ortalama Sipariş Tutarı")
    plt.title("Ülke Bazlı Satış Deseni Analizi (DBSCAN)")
    plt.grid(True)
    plt.colorbar(label='Küme No')
    plt.show()

    # Aykırı değerleri analiz etme
    outliers = df[df["cluster"] == -1]
    print("\nAykırı değer sayısı:", len(outliers))
    print("\nAykırı değerler (sıra dışı sipariş alışkanlığı olan ülkeler):")
    print(outliers[["country", "total_orders", "avg_order_value", "avg_products_per_order"]])

    # Sonuçları hazırlama
    results = {
        "total_clusters": len(df["cluster"].unique()),
        "outliers": df[df["cluster"] == -1].to_dict(orient="records"),
        "clusters": df.to_dict(orient="records")
    }
    
    return results 