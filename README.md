# Northwind DBSCAN Analysis API

Bu proje, Northwind veritabanı üzerinde DBSCAN algoritması kullanarak çeşitli analizler yapan bir REST API'dir. API, müşteri segmentasyonu, tedarikçi analizi, sipariş analizi ve ülke bazlı analizler gibi farklı analizler sunmaktadır.

## Proje Yapısı

```
.
├── analyzers/                 # Analiz modülleri
│   ├── customer_analyzer.py   # Müşteri segmentasyonu
│   ├── supplier_analyzer.py   # Tedarikçi analizi
│   ├── order_analyzer.py      # Sipariş analizi
│   └── country_analyzer.py    # Ülke bazlı analiz
├── images/                    # Analiz görselleri
│   ├── swagger_endpoints.png  # API endpoint'leri görseli
│   ├── customer_dbsan.png     # Müşteri segmentasyonu görseli
│   ├── customer_dbscan_1.png  # Müşteri segmentasyonu detay görseli
│   ├── supplier_dbscan.png    # Tedarikçi analizi görseli
│   ├── suppliers_dbscan.png   # Tedarikçi analizi detay görseli
│   ├── orders_dbscan.png      # Sipariş analizi görseli
│   ├── orders_dbscan_1.png    # Sipariş analizi detay görseli
│   ├── country_dbscan.png     # Ülke analizi görseli
│   └── country_dbscan_1.png   # Ülke analizi detay görseli
├── db_connect.py              # Veritabanı bağlantı yönetimi
├── dbscan_api.py              # FastAPI uygulaması
├── requirements.txt           # Proje bağımlılıkları
├── .env                       # Ortam değişkenleri (git'e gönderilmez)
├── .gitignore                 # Git tarafından yok sayılacak dosyalar
└── README.md                  # Proje dokümantasyonu
```

## Kurulum

1. Projeyi klonlayın:
```bash
git clone [repository-url]
cd [project-directory]
```

2. Sanal ortam oluşturun ve aktif edin:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
.\venv\Scripts\activate  # Windows
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. `.env` dosyasını oluşturun:
```bash
touch .env  # Linux/Mac
# veya
type nul > .env  # Windows
```

5. `.env` dosyasını düzenleyin:
```
# Veritabanı Bağlantı Ayarları
DB_HOST=localhost
DB_PORT=5432
DB_NAME=northwind
DB_USER=your_username
DB_PASSWORD=your_password

# API Ayarları
API_HOST=0.0.0.0
API_PORT=8003
```

6. API'yi başlatın:
```bash
python dbscan_api.py
```

## API Endpoint'leri

![API Endpoint'leri](images/swagger_endpoints.png)

### 1. Müşteri Segmentasyonu
- **Endpoint**: `/customer-segmentation`
- **Metod**: GET
- **Açıklama**: Müşterileri satın alma davranışlarına göre gruplandırır
- **Görsel**: ![Müşteri Segmentasyonu](images/customer_dbsan.png)

### 2. Tedarikçi Analizi
- **Endpoint**: `/supplier-segmentation`
- **Metod**: GET
- **Açıklama**: Tedarikçileri ürün performanslarına göre gruplandırır
- **Görsel**: ![Tedarikçi Analizi](images/supplier_dbscan.png)

### 3. Sipariş Analizi
- **Endpoint**: `/order-analysis`
- **Metod**: GET
- **Açıklama**: Siparişleri çeşitli metrikler üzerinden analiz eder
- **Görsel**: ![Sipariş Analizi](images/orders_dbscan.png)

### 4. Ülke Analizi
- **Endpoint**: `/country-analysis`
- **Metod**: GET
- **Açıklama**: Ülkeleri satış performanslarına göre gruplandırır
- **Görsel**: ![Ülke Analizi](images/country_dbscan.png)

## Analiz Sonuçları

### Müşteri Segmentasyonu
- Müşteriler satın alma davranışlarına göre gruplandırıldı
- Her küme için ortalama sipariş sayısı ve toplam harcama analiz edildi
- Aykırı değerler (sıra dışı müşteriler) tespit edildi

### Tedarikçi Analizi
- Tedarikçiler ürün performanslarına göre segmentlere ayrıldı
- Her segment için ortalama ürün sayısı ve satış performansı analiz edildi
- Sıra dışı performans gösteren tedarikçiler belirlendi

### Sipariş Analizi
- Siparişler çeşitli metrikler üzerinden gruplandırıldı
- Her küme için ortalama sipariş büyüklüğü ve ürün çeşitliliği analiz edildi
- Olağandışı siparişler tespit edildi

### Ülke Analizi
- Ülkeler satış performanslarına göre gruplandırıldı
- Her ülke için ortalama sipariş büyüklüğü ve müşteri sayısı analiz edildi
- Sıra dışı performans gösteren ülkeler belirlendi

## Teknik Detaylar

- **Algoritma**: DBSCAN (Density-Based Spatial Clustering of Applications with Noise)
- **Özellik Seçimi**: Her analiz için özel olarak seçilmiş metrikler
- **Veri Ön İşleme**: StandardScaler ile özellik normalizasyonu
- **Optimal Parametreler**: KneeLocator ile otomatik eps değeri belirleme
- **Veritabanı**: PostgreSQL
- **API Framework**: FastAPI
- **Güvenlik**: Ortam değişkenleri (.env) ile hassas bilgilerin korunması

## Katkıda Bulunma

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request oluşturun 