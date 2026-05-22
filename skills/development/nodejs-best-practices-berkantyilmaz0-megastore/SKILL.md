---
name: nodejs-best-practices
description: Node.js development principles and decision-making. Framework selection, async patterns, security, and architecture. Teaches thinking, not copying.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Node.js En İyi Uygulamalar

> 2025'te Node.js geliştirmesi için prensipler ve karar verme.
> **Kod kalıplarını ezberlemeyi değil, DÜŞÜNMEYİ öğrenin.**

---

## ⚠️ Bu Yetenek Nasıl Kullanılır

Bu yetenek kopyalanacak sabit kodları değil, **karar verme prensiplerini** öğretir.

- Belirsiz olduğunda kullanıcıya tercihlerini SORUN
- BAĞLAMA göre çerçeve/desen seçin
- Her seferinde aynı çözümü varsayılan yapmayın

---

## 1. Çerçeve (Framework) Seçimi (2025)

### Karar Ağacı

```
Ne inşa ediyorsunuz?
│
├── Edge/Sunucusuz (Cloudflare, Vercel)
│   └── Hono (sıfır bağımlılık, ultra hızlı soğuk başlangıç)
│
├── Yüksek Performanslı API
│   └── Fastify (Express'ten 2-3 kat daha hızlı)
│
├── Kurumsal/Ekip aşinalığı
│   └── NestJS (yapılandırılmış, DI, dekoratörler)
│
├── Eski (Legacy)/Kararlı/Maksimum ekosistem
│   └── Express (olgun, en çok ara yazılım)
│
└── Full-stack ile frontend
    └── Next.js API Routes veya tRPC
```

### Karşılaştırma Prensipleri

| Faktör | Hono | Fastify | Express |
|--------|------|---------|---------|
| **En iyisi** | Edge, sunucusuz | Performans | Eski sistemler, öğrenme |
| **Soğuk başlangıç** | En hızlı | Hızlı | Orta |
| **Ekosistem** | Büyüyor | İyi | En büyük |
| **TypeScript** | Yerel (Native) | Mükemmel | İyi |
| **Öğrenme eğrisi** | Düşük | Orta | Düşük |

### Seçim Soruları:
1. Dağıtım hedefi nedir?
2. Soğuk başlangıç süresi kritik mi?
3. Ekibin mevcut deneyimi var mı?
4. Bakımı yapılacak eski kod var mı?

---

## 2. Çalışma Zamanı (Runtime) Hususları (2025)

### Yerel (Native) TypeScript

```
Node.js 22+: --experimental-strip-types
├── .ts dosyalarını doğrudan çalıştır
├── Basit projeler için derleme adımına gerek yok
└── Şunlar için düşünün: scriptler, basit API'ler
```

### Modül Sistemi Kararı

```
ESM (import/export)
├── Modern standart
├── Daha iyi tree-shaking
├── Asenkron modül yükleme
└── Şunlar için kullanın: yeni projeler

CommonJS (require)
├── Eski uyumluluk
├── Daha fazla npm paketi desteği
└── Şunlar için kullanın: mevcut kod tabanları, bazı uç durumlar
```

### Çalışma Zamanı Seçimi

| Çalışma Zamanı | En İyisi |
|---------|----------|
| **Node.js** | Genel amaçlı, en büyük ekosistem |
| **Bun** | Performans, yerleşik paketleyici |
| **Deno** | Önce güvenlik, yerleşik TypeScript |

---

## 3. Mimari Prensipleri

### Katmanlı Yapı Kavramı

```
İstek Akışı:
│
├── Controller/Rota Katmanı
│   ├── HTTP detaylarını işler
│   ├── Sınırda girdi doğrulama
│   └── Servis katmanını çağırır
│
├── Servis Katmanı
│   ├── İş mantığı
│   ├── Çerçeveden bağımsız
│   └── Depo (repository) katmanını çağırır
│
└── Depo (Repository) Katmanı
    ├── Sadece veri erişimi
    ├── Veritabanı sorguları
    └── ORM etkileşimleri
```

### Bu Neden Önemli:
- **Test Edilebilirlik**: Katmanları bağımsız olarak mockla
- **Esneklik**: İş mantığına dokunmadan veritabanını değiştir
- **Netlik**: Her katmanın tek sorumluluğu var

### Ne Zaman Basitleştirilmeli:
- Küçük scriptler → Tek dosya TAMAM
- Prototipler → Daha az yapı kabul edilebilir
- Her zaman sor: "Bu büyüyecek mi?"

---

## 4. Hata Yönetimi Prensipleri

### Merkezi Hata Yönetimi

```
Desen:
├── Özel hata sınıfları oluştur
├── Herhangi bir katmandan fırlat (throw)
├── En üst seviyede yakala (ara yazılım - middleware)
└── Tutarlı yanıt formatla
```

### Hata Yanıt Felsefesi

```
İstemci şunları alır:
├── Uygun HTTP durumu
├── Programatik işleme için hata kodu
├── Kullanıcı dostu mesaj
└── Dahili ayrıntı YOK (güvenlik!)

Loglar şunları alır:
├── Tam yığın izi (stack trace)
├── İstek bağlamı
├── Kullanıcı ID (varsa)
└── Zaman damgası
```

### Durum Kodu Seçimi

| Durum | Statü | Ne Zaman |
|-----------|--------|------|
| Kötü girdi | 400 | İstemci geçersiz veri gönderdi |
| Kimlik doğrulama yok | 401 | Eksik veya geçersiz kimlik bilgileri |
| İzin yok | 403 | Kimlik doğrulama geçerli, ancak izin yok |
| Bulunamadı | 404 | Kaynak mevcut değil |
| Çakışma | 409 | Kopya veya durum çakışması |
| Doğrulama | 422 | Şema geçerli ancak iş kuralları başarısız |
| Sunucu hatası | 500 | Bizim hatamız, her şeyi logla |

---

## 5. Asenkron Desenler Prensipleri

### Her Birini Ne Zaman Kullanmalı

| Desen | Ne Zaman Kullanılır |
|---------|----------|
| `async/await` | Sıralı asenkron işlemler |
| `Promise.all` | Paralel bağımsız işlemler |
| `Promise.allSettled` | Bazılarının başarısız olabileceği paralel işlemler |
| `Promise.race` | Zaman aşımı veya ilk yanıt kazanır |

### Olay Döngüsü (Event Loop) Farkındalığı

```
I/O-sınırlı (async yardımcı olur):
├── Veritabanı sorguları
├── HTTP istekleri
├── Dosya sistemi
└── Ağ işlemleri

CPU-sınırlı (async yardımcı olmaz):
├── Kripto işlemleri
├── Görüntü işleme
├── Karmaşık hesaplamalar
└── → Çalışan iş parçacıkları (worker threads) kullan veya yükü devret (offload)
```

### Olay Döngüsünü Bloklamaktan Kaçınma

- Üretimde asla senkron metodlar kullanma (fs.readFileSync, vb.)
- CPU yoğun işleri devret
- Büyük veriler için akış (streaming) kullan

---

## 6. Doğrulama Prensipleri

### Sınırlarda Doğrula

```
Nerede doğrulanmalı:
├── API giriş noktası (istek gövdesi/parametreleri)
├── Veritabanı işlemlerinden önce
├── Harici veriler (API yanıtları, dosya yüklemeleri)
└── Ortam değişkenleri (başlangıçta)
```

### Doğrulama Kütüphanesi Seçimi

| Kütüphane | En İyisi |
|---------|----------|
| **Zod** | Önce TypeScript, çıkarım (inference) |
| **Valibot** | Daha küçük paket (tree-shakeable) |
| **ArkType** | Performans kritik |
| **Yup** | Mevcut React Form kullanımı |

### Doğrulama Felsefesi

- Hızlı başarısız ol: Erken doğrula
- Belirli ol: Net hata mesajları
- Güvenme: "Dahili" verilere bile

---

## 7. Güvenlik Prensipleri

### Güvenlik Kontrol Listesi (Kod Değil)

- [ ] **Girdi doğrulama**: Tüm girdiler doğrulandı
- [ ] **Parametreli sorgular**: SQL için dize birleştirme yok
- [ ] **Şifre hashleme**: bcrypt veya argon2
- [ ] **JWT doğrulama**: İmzayı ve süreyi her zaman doğrula
- [ ] **Hız sınırlama (Rate limiting)**: Kötüye kullanımdan koru
- [ ] **Güvenlik başlıkları**: Helmet.js veya eşdeğeri
- [ ] **HTTPS**: Üretimde her yerde
- [ ] **CORS**: Düzgün yapılandırılmış
- [ ] **Sırlar**: Sadece ortam değişkenleri
- [ ] **Bağımlılıklar**: Düzenli olarak denetlendi

### Güvenlik Zihniyeti

```
Hiçbir şeye güvenme:
├── Sorgu parametreleri → doğrula
├── İstek gövdesi → doğrula
├── Başlıklar → doğrula
├── Çerezler → doğrula
├── Dosya yüklemeleri → tara
└── Harici API'ler → yanıtı doğrula
```

---

## 8. Test Prensipleri

### Test Stratejisi Seçimi

| Tür | Amaç | Araçlar |
|------|---------|-------|
| **Birim** | İş mantığı | node:test, Vitest |
| **Entegrasyon** | API uç noktaları | Supertest |
| **E2E** | Tam akışlar | Playwright |

### Ne Test Edilmeli (Öncelikler)

1. **Kritik yollar**: Auth, ödemeler, çekirdek iş
2. **Uç durumlar**: Boş girdiler, sınırlar
3. **Hata yönetimi**: İşler ters gittiğinde ne olur?
4. **Test etmeye değmez**: Çerçeve kodu, önemsiz getter'lar

### Yerleşik Test Çalıştırıcı (Node.js 22+)

```
node --test src/**/*.test.ts
├── Harici bağımlılık yok
├── İyi kapsam raporlaması
└── İzleme (watch) modu mevcut
```

---

## 10. Kaçınılması Gereken Anti-Desenler

### ❌ YAPMA:
- Yeni edge projeleri için Express kullanma (Hono kullan)
- Üretim kodunda senkron metodlar kullanma
- Controller'lara iş mantığı koyma
- Girdi doğrulamasını atlama
- Sırları sabit kodla
- Doğrulama olmadan harici verilere güven
- CPU işiyle olay döngüsünü blokla

### ✅ YAP:
- Bağlama göre çerçeve seç
- Belirsiz olduğunda kullanıcıya tercihleri sor
- Büyüyen projeler için katmanlı mimari kullan
- Tüm girdileri doğrula
- Sırlar için ortam değişkenleri kullan
- Optimize etmeden önce profille

---

## 11. Karar Kontrol Listesi

Uygulamadan önce:

- [ ] **Kullanıcıya yığın (stack) tercihi soruldu mu?**
- [ ] **BU bağlam için çerçeve seçildi mi?** (sadece varsayılan değil)
- [ ] **Dağıtım hedefi düşünüldü mü?**
- [ ] **Hata yönetimi stratejisi planlandı mı?**
- [ ] **Doğrulama noktaları belirlendi mi?**
- [ ] **Güvenlik gereksinimleri düşünüldü mü?**

---

> **Unutmayın**: Node.js en iyi uygulamaları desenleri ezberlemek değil, karar vermekle ilgilidir. Her proje gereksinimlerine göre taze bir değerlendirmeyi hak eder.
