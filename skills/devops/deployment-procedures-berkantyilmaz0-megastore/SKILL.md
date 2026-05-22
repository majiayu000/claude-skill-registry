---
name: deployment-procedures
description: Production deployment principles and decision-making. Safe deployment workflows, rollback strategies, and verification. Teaches thinking, not scripts.
allowed-tools: Read, Glob, Grep, Bash
---

# Dağıtım Prosedürleri

> Güvenli üretim dağıtımları için dağıtım prensipleri ve karar verme.
> **Scriptleri ezberlemeyi değil, DÜŞÜNMEYİ öğrenin.**

---

## ⚠️ Bu Yetenek Nasıl Kullanılır

Bu yetenek kopyalanacak bash scriptlerini değil, **dağıtım prensiplerini** öğretir.

- Her dağıtım benzersizdir
- Her adımın arkasındaki NEDENi anlayın
- Prosedürleri platformunuza uyarlayın

---

## 1. Platform Seçimi

### Karar Ağacı

```
Ne dağıtıyorsunuz?
│
├── Statik site / JAMstack
│   └── Vercel, Netlify, Cloudflare Pages
│
├── Basit web uygulaması
│   ├── Yönetilen → Railway, Render, Fly.io
│   └── Kontrol → VPS + PM2/Docker
│
├── Mikro hizmetler
│   └── Konteyner orkestrasyonu
│
└── Sunucusuz (Serverless)
    └── Edge fonksiyonları, Lambda
```

### Her Platformun Farklı Prosedürleri Vardır

| Platform | Dağıtım Yöntemi |
|----------|------------------|
| **Vercel/Netlify** | Git push, otomatik dağıtım |
| **Railway/Render** | Git push veya CLI |
| **VPS + PM2** | SSH + manuel adımlar |
| **Docker** | Image push + orkestrasyon |
| **Kubernetes** | kubectl apply |

---

## 2. Dağıtım Öncesi Prensipler

### 4 Doğrulama Kategorisi

| Kategori | Ne Kontrol Edilmeli |
|----------|--------------|
| **Kod Kalitesi** | Testler geçiyor, lint temiz, incelendi |
| **Derleme (Build)** | Üretim derlemesi çalışıyor, uyarı yok |
| **Ortam** | Env değişkenleri ayarlı, sırlar güncel |
| **Güvenlik** | Yedekleme yapıldı, geri alma planı hazır |

### Dağıtım Öncesi Kontrol Listesi

- [ ] Tüm testler geçiyor
- [ ] Kod incelendi ve onaylandı
- [ ] Üretim derlemesi başarılı
- [ ] Ortam değişkenleri doğrulandı
- [ ] Veritabanı migrasyonları hazır (varsa)
- [ ] Geri alma planı belgelendi
- [ ] Ekip bilgilendirildi
- [ ] İzleme (monitoring) hazır

---

## 3. Dağıtım İş Akışı Prensipleri

### 5 Aşamalı Süreç

```
1. HAZIRLA (PREPARE)
   └── Kodu, buildi, env değişkenlerini doğrula

2. YEDEKLE (BACKUP)
   └── Değiştirmeden önce mevcut durumu kaydet

3. DAĞIT (DEPLOY)
   └── İzleme açıkken yürüt

4. DOĞRULA (VERIFY)
   └── Sağlık kontrolü, loglar, ana akışlar

5. ONAYLA veya GERİ AL (CONFIRM or ROLLBACK)
   └── Her şey iyi mi? Onayla. Sorun mu var? Geri al.
```

### Aşama Prensipleri

| Aşama | Prensip |
|-------|-----------|
| **Hazırla** | Asla test edilmemiş kodu dağıtma |
| **Yedekle** | Yedek olmadan geri alamazsın |
| **Dağıt** | Olurken izle, uzaklaşma |
| **Doğrula** | Güven ama doğrula |
| **Onayla** | Geri alma tetiğini hazır tut |

---

## 4. Dağıtım Sonrası Doğrulama

### Ne Doğrulanmalı

| Kontrol | Neden |
|-------|-----|
| **Sağlık uç noktası** | Hizmet çalışıyor |
| **Hata logları** | Yeni hata yok |
| **Ana kullanıcı akışları** | Kritik özellikler çalışıyor |
| **Performans** | Yanıt süreleri kabul edilebilir |

### Doğrulama Penceresi

- **İlk 5 dakika**: Aktif izleme
- **15 dakika**: Kararlı olduğunu onayla
- **1 saat**: Son doğrulama
- **Ertesi gün**: Metrikleri incele

---

## 5. Geri Alma (Rollback) Prensipleri

### Ne Zaman Geri Alınmalı

| Belirti | Eylem |
|---------|--------|
| Hizmet kapalı | Derhal geri al |
| Kritik hatalar | Geri al |
| Performans >%50 düştü | Geri almayı düşün |
| Küçük sorunlar | Hızlıysa ileriye doğru düzelt (fix forward) |

### Platforma Göre Geri Alma Stratejisi

| Platform | Geri Alma Yöntemi |
|----------|----------------|
| **Vercel/Netlify** | Önceki commit'i yeniden dağıt |
| **Railway/Render** | Panoda geri al |
| **VPS + PM2** | Yedeği geri yükle, yeniden başlat |
| **Docker** | Önceki image etiketi |
| **K8s** | kubectl rollout undo |

### Geri Alma Prensipleri

1. **Mükemmellik yerine hız**: Önce geri al, sonra hata ayıkla
2. **Hataları birleştirme**: Tek geri alma, birden fazla değişiklik değil
3. **İletişim Kur**: Ekibe ne olduğunu söyle
4. **Post-mortem**: Kararlı hale geldikten sonra nedenini anla

---

## 6. Sıfır Kesinti (Zero-Downtime) Dağıtım

### Stratejiler

| Strateji | Nasıl Çalışır |
|----------|--------------|
| **Yuvarlanan (Rolling)** | Örnekleri birer birer değiştir |
| **Mavi-Yeşil (Blue-Green)** | Trafiği ortamlar arasında değiştir |
| **Kanarya (Canary)** | Kademeli trafik geçişi |

### Seçim Prensipleri

| Senaryo | Strateji |
|----------|----------|
| Standart sürüm | Yuvarlanan (Rolling) |
| Yüksek riskli değişiklik | Mavi-yeşil (kolay geri alma) |
| Doğrulama ihtiyacı | Kanarya (gerçek trafikle test) |

---

## 7. Acil Durum Prosedürleri

### Hizmet Kesintisi Önceliği

1. **Değerlendir**: Belirti nedir?
2. **Hızlı düzeltme**: Belirsizse yeniden başlat
3. **Geri al**: Yeniden başlatma yardımcı olmazsa
4. **Araştır**: Kararlı hale geldikten sonra

### Araştırma Sırası

| Kontrol | Yaygın Sorunlar |
|-------|--------------|
| **Loglar** | Hatalar, istisnalar |
| **Kaynaklar** | Disk dolu, bellek |
| **Ağ** | DNS, güvenlik duvarı |
| **Bağımlılıklar** | Veritabanı, API'ler |

---

## 8. Anti-Desenler

| ❌ Yapma | ✅ Yap |
|----------|-------|
| Cuma günü dağıt | Haftanın başında dağıt |
| Dağıtımı aceleye getir | Süreci takip et |
| Staging'i atla | Her zaman önce test et |
| Yedeksiz dağıt | Dağıtımdan önce yedekle |
| Dağıtımdan sonra uzaklaş | 15+ dk izle |
| Aynı anda birden çok değişiklik | Seferde tek değişiklik |

---

## 9. Karar Kontrol Listesi

Dağıtımdan önce:

- [ ] **Platforma uygun prosedür mü?**
- [ ] **Yedekleme stratejisi hazır mı?**
- [ ] **Geri alma planı belgelendi mi?**
- [ ] **İzleme yapılandırıldı mı?**
- [ ] **Ekip bilgilendirildi mi?**
- [ ] **Sonrasında izlemek için zaman var mı?**

---

## 10. En İyi Uygulamalar

1. Büyük sürümler yerine **küçük, sık dağıtımlar**
2. Riskli değişiklikler için **özellik bayrakları (feature flags)**
3. Tekrarlayan adımları **otomatize et**
4. Her dağıtımı **belgele**
5. Sorunlardan sonra neyin yanlış gittiğini **incele**
6. İhtiyaç duymadan önce **geri almayı test et**

---

> **Unutmayın:** Her dağıtım bir risktir. Riski hızla değil, hazırlıkla en aza indirin.
