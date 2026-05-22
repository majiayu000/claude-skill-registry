---
name: implement-feature
description: >
  Yeni bir feature implement edilmek istendiğinde otomatik devreye gir.
  "yeni feature", "ekle", "implement et", "geliştir" ifadeleri geçtiğinde
  ya da kullanıcı açıkça bir özellik talep ettiğinde bu skill'i kullan.
  TDD pipeline'ını başlatır: planner → architect → tdd-guide → implement → review.
---

# Feature Implementation Pipeline

Bu skill, yeni bir feature'ı uçtan uca geliştirir.
CLAUDE.md ve rules/ klasörüne göre çalışır.

## Pipeline Adımları

### Adım 1: Plan (@planner subagent)
@planner subagent'ını şu context ile çağır:
- Kullanıcının isteği
- Mevcut codebase yapısı (CLAUDE.md'den)
- İlgili mevcut dosyalar

@planner'ın planı çıkmasını bekle.
Kullanıcıdan onay al. Onay gelmeden Adım 2'ye geçme.

### Adım 2: Mimari (@architect subagent)
@architect subagent'ını @planner'ın onaylı planı ile çağır.
Blueprint çıkana kadar bekle.

### Adım 3: Test Yaz (@tdd-guide subagent)
@tdd-guide subagent'ını @architect'in blueprint'i ile çağır.
Test dosyaları yazılana kadar bekle. (RED aşaması)

### Adım 4: Implementation (Ana Agent)
Sırayla implement et — her adımdan sonra testleri çalıştır:
1. Type/interface tanımları
2. Service/storage katmanı
3. Store (Zustand)
4. Component(ler)
5. Ekrana entegrasyon
6. `npm test` çalıştır → GREEN aşaması

### Adım 5: Refactor
GREEN'e ulaşıldıktan sonra:
- Kodun okunabilirliğini artır (davranışı değiştirmeden)
- Tekrar eden kod varsa extract et
- `npm test` tekrar çalıştır — hâlâ GREEN mi?

### Adım 6: Review (@code-reviewer subagent)
@code-reviewer subagent'ını tüm değişen dosyalarla çağır.
CRITICAL veya MAJOR bulgu varsa önce düzelt.

### Adım 7: Codemap Güncelle
implement-feature bittikten sonra /codemap-update'i çalıştır.

### Adım 8: Deploy (Onay Gerekli)
Kullanıcıya sor: "Değişiklikleri commit/push/deploy etmek ister misin?"
- Evet → /deploy-pipeline skill'ini tetikle
- Hayır → Pipeline'ı burada sonlandır

## Önemli Kurallar
- Her adımda kullanıcıyı bilgilendir ("Şu an Adım 2'deyiz...")
- Adımları atlatma — sıralamaya uy
- Bir adım başarısız olursa duraksama ve kullanıcıya rapor ver
- Deploy adımında HER alt-adım için ayrı onay al
