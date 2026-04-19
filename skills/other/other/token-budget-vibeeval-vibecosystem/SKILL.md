---
name: token-budget
description: Agent basina token kullanimi takibi, maliyet optimizasyonu, butce limitleri ve ROI analizi. Session ve proje bazinda harcama raporlari. Hangi agent ne kadar token tuketiyor, hangisi verimli, hangisi israf.
---

# Token Budget Management

Her agent cagri token harcar. Butce yonetimi olmadan maliyetler kontrolsuz buyur.

## Maliyet Tablosu (2026 Q2)

| Model | Input (1M token) | Output (1M token) | Cache Read (1M) |
|-------|----------------:|------------------:|----------------:|
| Opus 4.6 | $15.00 | $75.00 | $1.50 |
| Sonnet 4.6 | $3.00 | $15.00 | $0.30 |
| Haiku 4.5 | $0.80 | $4.00 | $0.08 |

### Agent Basina Ortalama Maliyet

| Agent Tipi | Ortalama Token/Cagri | Ortalama Maliyet | Notlar |
|------------|--------------------:|------------------:|--------|
| scout (arastirma) | 15K-50K | $0.15-0.75 | Cok dosya okur |
| code-reviewer | 10K-30K | $0.10-0.45 | Diff boyutuna bagli |
| architect | 20K-60K | $0.30-0.90 | Derin dusunme gerektirir |
| spark (quick fix) | 3K-10K | $0.03-0.15 | En verimli |
| kraken (TDD) | 30K-100K | $0.45-1.50 | Test + implement |
| sleuth (debug) | 20K-80K | $0.30-1.20 | Bug karmasikligina bagli |
| verifier | 5K-15K | $0.05-0.22 | Build + test calistirma |
| security-reviewer | 10K-40K | $0.15-0.60 | Tarama derinligine bagli |
| planner | 15K-40K | $0.22-0.60 | Plan buyuklugune bagli |

## Butce Planlama

### Session Butcesi

```
KUCUK IS (bug fix, kucuk feature):
  Beklenen: 50K-150K token
  Butce: $0.50-2.00
  Agent sayisi: 2-4

ORTA IS (feature, refactoring):
  Beklenen: 200K-500K token
  Butce: $3.00-7.00
  Agent sayisi: 4-8

BUYUK IS (yeni modul, buyuk refactor):
  Beklenen: 500K-2M token
  Butce: $7.00-30.00
  Agent sayisi: 8-15

SWARM (tam ekip):
  Beklenen: 1M-5M token
  Butce: $15.00-75.00
  Agent sayisi: 15-30
```

### Aylik Butce Tahmini

```
Gunluk 3-5 session x 30 gun:

Hafif kullanim (vibe coding):
  ~100K token/gun = $1.50/gun = ~$45/ay

Normal kullanim (aktif gelistirme):
  ~500K token/gun = $7.50/gun = ~$225/ay

Yogun kullanim (tam ekip, swarm):
  ~2M token/gun = $30/gun = ~$900/ay

Claude Max abone ise:
  Sabit $200/ay -- token limiti var ama birim maliyet yok
  ROI: Normal kullanim ustu her sey Max ile karli
```

## Maliyet Optimizasyon Stratejileri

### 1. Model Routing (En Buyuk Tasarruf)

```
Opus kullan:
  - Mimari kararlar (architect)
  - Karmasik debug (sleuth)
  - Guvenlik analizi (security-reviewer)
  - Kritik code review

Sonnet kullan:
  - Genel gelistirme (kraken, spark)
  - Rutin review (code-reviewer)
  - Dokumantasyon (technical-writer)
  - Test yazma (tdd-guide)

Sonuc: %40-60 maliyet dususu, %5-10 kalite kaybı
```

### 2. Context Yonetimi

```
YAPMA: 5 dosyayi tamamen okuyup agent'a gonder
YAP:   Sadece ilgili fonksiyonlari gonder

YAPMA: Her seferinde tum CLAUDE.md'yi inject et
YAP:   Sadece ilgili kurallari sec

YAPMA: Agent'a "her seyi kontrol et" de
YAP:   Spesifik kontrol listesi ver

Token tasarrufu: %30-50
```

### 3. Agent Secimi

```
PAHALI YOLDAN GITME:
  architect (60K) + kraken (100K) + verifier (15K) = 175K token

VERIMLI YOL:
  spark (10K) + verifier (10K) = 20K token
  (Kucuk is icin spark yeterli, architect/kraken gereksiz)

Kural: Is buyuklugune uygun agent sec
```

### 4. Cache Kullanimi

```
Ayni dosyayi tekrar tekrar okuma:
  Ilk okuma: 10K token (tam fiyat)
  Cache hit: 10K token (%90 indirimli)

Strateji: Session basinda ilgili dosyalari bir kere oku,
sonraki agent'lar cache'ten okusun
```

### 5. Paralel vs Sequential

```
PARALEL (daha pahali ama hizli):
  3 agent ayni anda = 3x token ama 3x hizli
  Kullan: Deadline varsa, bagimsiz isler

SEQUENTIAL (daha ucuz):
  Agent 1 bitir → ciktisini Agent 2'ye ver
  Kullan: Butce kisitliysa, bagimli isler
```

## ROI Analizi

### Agent Basina ROI

```
ROI = (Tasarruf edilen sure x saat ucreti) / Agent maliyeti

Ornek: code-reviewer
  Maliyet: ~$0.30/review
  Tasarruf: ~15 dk/review (manual review vs)
  Saat ucreti: $50/saat
  ROI: ($12.50) / ($0.30) = 41x

Ornek: sleuth (bug investigation)
  Maliyet: ~$0.75/investigation
  Tasarruf: ~45 dk/bug (manual debug vs)
  ROI: ($37.50) / ($0.75) = 50x

Ornek: architect (buyuk plan)
  Maliyet: ~$0.90/plan
  Tasarruf: ~2 saat (manual planning vs)
  ROI: ($100) / ($0.90) = 111x
```

### En Yuksek ROI Agent'lar

| Siralama | Agent | ROI | Neden |
|----------|-------|-----|-------|
| 1 | architect | 111x | Buyuk zaman tasarrufu, dusuk maliyet |
| 2 | sleuth | 50x | Bug investigation cok zaman alir |
| 3 | code-reviewer | 41x | Her commit icin gerekli |
| 4 | verifier | 35x | Otomatik quality gate |
| 5 | spark | 30x | Kucuk isler icin cok verimli |

### En Dusuk ROI Agent'lar

| Agent | ROI | Neden | Oneri |
|-------|-----|-------|-------|
| scout (gereksiz arama) | 5x | Bazen cok dosya okur, az bilgi bulur | Spesifik soru sor |
| kraken (kucuk is) | 8x | TDD overhead kucuk isler icin fazla | Kucuk is = spark |
| designer (sadece oneri) | 3x | Oneri verir ama implement etmez | Frontend-dev yeterli |

## Harcama Raporu Sablonu

```markdown
# Token Harcama Raporu - [Tarih]

## Ozet
- Toplam token: XXX,XXX
- Tahmini maliyet: $XX.XX
- Agent sayisi: X
- Session suresi: X saat

## Agent Bazli Dagilim

| Agent | Token | Maliyet | Is | ROI |
|-------|------:|--------:|---|----|
| architect | 45K | $0.67 | Auth redesign plani | 111x |
| kraken | 85K | $1.27 | Implementation | 25x |
| code-reviewer | 20K | $0.30 | Review | 41x |
| verifier | 12K | $0.18 | Final check | 35x |
| **TOPLAM** | **162K** | **$2.42** | | |

## Optimizasyon Onerisi
- kraken yerine spark kullanilabilirdi (-70K token)
- architect ciktisi daha spesifik olabilirdi (-15K token)
- Potansiyel tasarruf: %52
```

## vibecosystem Entegrasyonu

- **cost-tracker agent**: Bu skill'i kullanarak session maliyet raporu uretir
- **smart-model-routing skill**: Model secimini maliyet/kalite dengesine gore yapar
- **swarm-optimizer agent**: Swarm calistirmalarinda butce optimizasyonu yapar
- **session-replay-analyzer agent**: Gecmis session'larin token verimliligini analiz eder
