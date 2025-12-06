# 📦 DESTECH CHALLENGE README

## 🧩 Giriş

#### 🧩 CASE-1:
Destech_final.drawio -> draw.io ya import edilir ve incelenebilir.


#### 🧩 CASE-2: 
Mümkün mertebe scale edilmeye uygun moduler mimaride kodlar yazıldı. Dockerize hem staging hem production için ayrı ayrı uygulandı. Ek olarak Celery workerin işlerini incelemek için Flower tool eklendi. Django, Redis, PostgreSQL ve Celery loglarrını Prometheus ile metric toplayıp Grafana ile monitorize ettim. Giriş bilgileri aşağıda mevcuttur. Staging ve Prod ortamlarının dashboardları farklıdır docker ayağa kalkında dashboard otomatik olarak yüklenecektir. Herhangi ek işlem gerekmez. Kolaylık ve linux/mac ortamlarına uygun olacak şekilde Makefile yazıldı. Komut listesini "make help" yazarak görebilirsiniz. Ben MacOS ta çalışarak hazırladım Linux içinde ayarlarını yaptım ama eğer Linux ta deneyipte make komutlarında hata alırsanız Makefile kulanmadan docker-compose -f docker-compose.prod.yml -d --build kullanaraktaa ayağa kaldırabilirsiniz. Makefile help resmini aşağıya ekledim.


#### 🧩 CASE-3: 
Main root içinde case_3_code_review.py dosyası mevcut. Yorumlarımı ve olması gereken kodlamaları ekledim. sadece o dosyayı inceleyerek deeğerlendirebilirsiniz.


---


### Gereksinimler

- Docker & Docker Compose
- Make (MacOS ve Linux destekli)
- Python 3.x (geliştirme aşamasında)



## 🚀 Kullanım

### Uygulama Arayüzleri:

- **Swagger (API Dokümantasyonu):** [http://localhost:8000/api/docs/swagger](http://localhost:8000/api/docs/swagger)
- **Grafana Dashboard:** [http://localhost:3000/dashboards](http://localhost:3000/dashboards)
  - Kullanıcı: `admin`  
  - Şifre: `admin`
- **Flower (Celery İzleyici):** [http://localhost:5555](http://localhost:5555)

---

## 🌟 Özellikler

- Docker ile containerize edilmiş yapı (Staging & Production ayrı ortamlar)
- Redis + PostgreSQL + Celery entegrasyonu
- Flower ile Celery monitoring
- Prometheus + Grafana ile log ve metrik takibi
- Modüler ve ölçeklenebilir kod yapısı
- Platform bağımsız `Makefile` ile kolay kullanım
- Swagger tabanlı otomatik API dökümantasyonu

---

## 🏗️ Mimari

- Django (backend)
- PostgreSQL (veritabanı)
- Redis (queue broker)
- Celery (asenkron görev işleme)
- Flower (görev monitörü)
- Prometheus & Grafana (log & metrik izleme)
- Docker Compose (servis orkestrasyonu)

Draw.io üzerinden mimariyi incelemek için: `Destech_final.drawio` dosyasını [https://draw.io](https://draw.io)'ya import edin.

---

## ⚙️ Yapılandırma

Tüm ortam değişkenleri `.env` dosyalarında tanımlanmıştır.

Dashboard’lar otomatik olarak yüklenir. Ekstra bir işlem yapmanıza gerek yoktur.

---

## 📖 Dokümantasyon

- API Swagger: `/api/docs/swagger`
- Kod inceleme notları için: `case_3_code_review.py`

---

## 💡 Örnekler

**Makefile Komutları:**

![Makefile Komutları](makefile.png)

**Swagger Arayüzü:**

![Swagger](swagger.png)

**Grafana Dashboard:**

![Grafana](grafana.png)

---

## 🛠️ Geliştirici Notları

- Proje MacOS ortamında geliştirilmiştir.
- Linux ortamında test edilmiştir. Ancak `make` ile hata alırsanız doğrudan `docker-compose` komutları ile çalıştırabilirsiniz.
- `case_3_code_review.py` dosyası, kod kalitesi ve iyileştirme önerileri için hazırlanmıştır.
- Daha çok özellik eklenebilir geliştirilebilir. 
---

## 🐞 Troubleshooting

| Problem | Çözüm |
|--------|-------|
| `make` komutu çalışmıyor | Linux ortamında `docker-compose` komutu ile çalıştırın |
| Dashboard gözükmüyor | Docker container'ların doğru şekilde ayağa kalktığından emin olun |
| Swagger erişimi yok | Backend servisi doğru portta çalışıyor mu kontrol edin |

