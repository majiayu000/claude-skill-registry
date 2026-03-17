---
name: notion_integration
router_kit: FullStackKit
description: Notion workspace entegrasyonu - bilgi yönetimi, toplantı hazırlığı, araştırma dokümantasyonu ve spec-to-implementation workflow'ları.
metadata:
  skillport:
    category: documentation
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, notion integration, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - integration
---

# 📝 Notion Integration

> Notion workspace ile kapsamlı entegrasyon rehberi.

---

## 📋 İçindekiler

1. [Knowledge Capture](#1-knowledge-capture)
2. [Meeting Intelligence](#2-meeting-intelligence)
3. [Research Documentation](#3-research-documentation)
4. [Spec to Implementation](#4-spec-to-implementation)

---

## 1. Knowledge Capture

Sohbetleri ve tartışmaları yapılandırılmış dokümantasyona dönüştürme.

### Workflow
```
1. İçerik çıkar → 2. Yapılandır → 3. Konum belirle → 4. Sayfa oluştur → 5. Bağla
```

### İçerik Türleri
| Tür | Yapı |
|-----|------|
| **Concept** | Tanım → Özellikler → Örnekler → Kullanım |
| **How-To** | Önkoşullar → Adımlar → Doğrulama → Sorun Giderme |
| **Decision** | Bağlam → Karar → Gerekçe → Sonuçlar |
| **FAQ** | Kısa Cevap → Detay → Örnekler |

### Hedef Konumlar
- Wiki sayfası (genel bilgi)
- Proje sayfası (proje spesifik)
- Database (yapılandırılmış veri)

---

## 2. Meeting Intelligence

Toplantı hazırlığı ve doküman oluşturma.

### Workflow
```
1. Notion'da ara → 2. İçerik getir → 3. Claude ile zenginleştir → 4. Pre-read oluştur → 5. Agenda oluştur
```

### Doküman Türleri

| Doküman | Hedef Kitle | İçerik |
|---------|-------------|--------|
| **Pre-Read** | İç ekip | Tam bağlam, metrikler, stratejik düşünceler |
| **Agenda** | Tüm katılımcılar | Hedef, gündem, tartışma konuları |

### Toplantı Tipleri
- **Karar toplantısı**: Seçenekler → Öneri → Tartışma → Karar
- **Durum toplantısı**: İlerleme → Gelecek iş → Engelleyiciler
- **Beyin fırtınası**: Hedef → Kısıtlar → Fikirler → Sonraki adımlar

---

## 3. Research Documentation

Notion workspace'te araştırma ve dokümantasyon.

### Workflow
```
1. Ara → 2. Sayfaları getir → 3. Analiz et → 4. Sentezle → 5. Doküman oluştur
```

### Çıktı Formatları
- **Araştırma Özeti**: Kısa, odaklı bulgular
- **Kapsamlı Rapor**: Detaylı analiz ve öneriler
- **Hızlı Brief**: Ana noktalar ve aksiyonlar

### Best Practices
1. Geniş arama yap, sonra daralt
2. Kaynaklara her zaman bağlantı ver
3. Güncellik kontrolü yap
4. Çapraz doğrulama yap

---

## 4. Spec to Implementation

Spesifikasyonları uygulama planlarına dönüştürme.

### Workflow
```
1. Spec bul → 2. Getir ve analiz et → 3. Plan oluştur → 4. Task database bul → 5. Görevler oluştur → 6. İlerleme takibi
```

### Spec Analizi
| Tip | İçerik |
|-----|--------|
| **Fonksiyonel** | User stories, özellikler, veri gereksinimleri |
| **Non-Fonksiyonel** | Performans, güvenlik, ölçeklenebilirlik |
| **Kabul Kriterleri** | Test edilebilir koşullar, benchmarklar |

### Task Breakdown Patterns
- **Bileşene göre**: DB, API, Frontend, Test
- **Özelliğe göre**: Dikey dilimler (auth, data entry)
- **Önceliğe göre**: P0, P1, P2

---

## 🔧 Ortak Araçlar

```
Notion:notion-search     → Sayfa/database ara
Notion:notion-fetch      → İçerik getir
Notion:notion-create-pages → Sayfa oluştur
Notion:notion-update-page  → Sayfa güncelle
```

---

*Notion Integration v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Notion API Documentation](https://developers.notion.com/)

### Aşama 1: Integration Design
- [ ] **Capabilities**: Integration'ın yeteneklerini (Read/Update/Insert/Comment) en az yetki prensibiyle (Least Privilege) ayarla.
- [ ] **Database ID**: Hedef veritabanlarının ID'lerini environment variable olarak sakla.
- [ ] **Mapping**: Harici veri modeli ile Notion property'leri (Rich Text, Select, Date) arasındaki eşlemeyi yap.

### Aşama 2: Robust Operations
- [ ] **Rate Limiting**: Notion API saniyede 3 istek sınırı koyar. Exponential Backoff ile retry mekanizması kur.
- [ ] **Pagination**: 100 kayıttan fazla veri çekerken `next_cursor` kullanmayı unutma.
- [ ] **Rich Text**: Markdown -> Notion Block dönüşümünü doğru yap (paragraflar, listeler, başlıklar).

### Aşama 3: Maintenance
- [ ] **Orphaned Content**: Silinmesi gereken ama API ile erişilemeyen sayfaları (Trash) periyodik kontrol et.
- [ ] **Webhooks**: Veri değişimini anlık algılamak için (resmi webhook yoksa) polling aralığını optimize et.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Notion sorguları property tiplerine (Select vs Multi-select) uygun mu? |
| 2 | 429 (Too Many Requests) hatası doğru yönetiliyor mu? |
| 3 | Sayfa içerikleri (Block children) hiyerarşisi bozulmadan aktarılıyor mu? |
