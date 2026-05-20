---
name: turkce-kod
description: Türkçe yazılım projeleri için kod dokümantasyonu, yorum satırları, README ve commit mesajları yazma rehberi. Teknik terimlerin Türkçe karşılıkları ve Türk geliştirici topluluğu standartları.
tags: [türkçe, dokümantasyon, kod, readme, yorum]
related_skills: [turkce-asistan]
version: 1.0.0
---

# Türkçe Kod Dokümantasyonu Rehberi

Bu skill, Türkçe yazılım projelerinde tutarlı, okunabilir ve profesyonel dokümantasyon yazmanı sağlar.

---

## 1. Yorum Satırı Standartları

### Genel Kurallar
- Yorumlar **Türkçe** yazılır, yabancı kelimeler italik veya tırnak içinde gösterilir.
- Yorum satırları büyük harfle başlar, nokta ile biter.
- Kod ne **yaptığını** değil, **neden** yaptığını açıklar.

### Python Örneği
```python
# Kullanıcı oturumunu doğrula ve yetki seviyesini belirle.
def oturum_dogrula(kullanici_id: int) -> dict:
    """
    Verilen kullanıcı kimliğine göre oturum bilgilerini döndürür.

    Args:
        kullanici_id: Veritabanındaki benzersiz kullanıcı numarası.

    Returns:
        Kullanıcı bilgisi ve yetki seviyesini içeren sözlük.

    Raises:
        KullaniciBulunamadi: Kullanıcı veritabanında yoksa.
    """
    ...
```

### JavaScript / TypeScript Örneği
```typescript
/**
 * Sepetteki ürünlerin toplam fiyatını hesaplar.
 * KDV dahil tutar için `kdvDahilFiyat()` fonksiyonunu kullan.
 *
 * @param urunler - Fiyat bilgisi içeren ürün dizisi
 * @returns Toplam fiyat (kuruş cinsinden, virgülsüz tam sayı)
 */
function toplamFiyatHesapla(urunler: Urun[]): number {
    // Boş sepet kontrolü — backend doğrulamasına güvenmiyoruz.
    if (urunler.length === 0) return 0;
    return urunler.reduce((toplam, urun) => toplam + urun.fiyat, 0);
}
```

### Go Örneği
```go
// SiparisOlustur yeni bir sipariş kaydı oluşturur ve veritabanına ekler.
// Stok kontrolü bu fonksiyon içinde yapılmaz; çağırmadan önce StokKontrol() çalıştır.
func SiparisOlustur(ctx context.Context, istek SiparisIstegi) (*Siparis, error) {
    ...
}
```

---

## 2. Değişken ve Fonksiyon İsimlendirme

### Türkçe mi, İngilizce mi?
- **Tercih:** Projenin diline göre tutarlı ol. Karma kullanımdan kaçın.
- **Türkçe kullan:** İş mantığı (domain) değişkenlerinde — `musteri`, `siparis`, `fatura`.
- **İngilizce bırak:** Framework/kütüphane terimleri — `request`, `response`, `callback`, `index`.

### Adlandırma Örnekleri

| İngilizce (kaçın) | Türkçe (tercih) |
|-------------------|-----------------|
| `user` | `kullanici` |
| `order` | `siparis` |
| `invoice` | `fatura` |
| `product` | `urun` |
| `cart` | `sepet` |
| `address` | `adres` |
| `payment` | `odeme` |
| `employee` | `calisan` |
| `company` | `sirket` |
| `report` | `rapor` |

### Türkçe Karakter Uyarısı
Dil destekleyen ortamlarda (Python 3, modern JS/TS) Türkçe karakter kullanılabilir:
```python
müşteri_adı = "Ali"   # Geçerli Python 3
ürün_listesi = []     # Geçerli Python 3
```
Ancak terminal uyumsuzluğu riski nedeniyle **ASCII karşılıklarını tercih et:**
```python
musteri_adi = "Ali"   # Daha güvenli
urun_listesi = []     # Daha güvenli
```

---

## 3. Commit Mesajı Yazımı

### Format
```
<tür>: <kısa açıklama> (max 72 karakter)

<detay — opsiyonel, neden değiştirildi>

Refs: #123
```

### Tür Etiketleri
| Etiket | Kullanım |
|--------|----------|
| `ekle` | Yeni özellik |
| `düzelt` | Hata giderme |
| `güncelle` | Mevcut özellik iyileştirme |
| `sil` | Kod/dosya silme |
| `yeniden-düzenle` | Davranış değiştirmeden kod temizliği |
| `test` | Test ekleme/güncelleme |
| `belge` | Sadece dokümantasyon |
| `yapılandır` | Config/CI değişikliği |

### Örnekler
```
ekle: kullanıcı profil fotoğrafı yükleme özelliği

Cloudinary entegrasyonu ile resim yükleme ve boyutlandırma eklendi.
5MB sınırı ve JPEG/PNG/WebP formatı destekleniyor.

Refs: #87
```

```
düzelt: boş sepette toplam fiyat hesabı sıfır gösterilmiyor
```

```
yeniden-düzenle: fatura modülünü servis katmanına taşı
```

---

## 4. README.md Şablonu

```markdown
# Proje Adı

Projenin ne yaptığını tek cümlede açıkla.

## Kurulum

\```bash
pip install proje-adi
# veya
npm install proje-adi
\```

## Hızlı Başlangıç

\```python
from proje import AnaModul

modul = AnaModul(api_anahtari="...")
sonuc = modul.calistir()
print(sonuc)
\```

## Özellikler

- **Özellik 1:** Açıklama
- **Özellik 2:** Açıklama

## Yapılandırma

| Parametre | Tür | Varsayılan | Açıklama |
|-----------|-----|-----------|----------|
| `api_anahtari` | `str` | — | Zorunlu |
| `zaman_asimi` | `int` | `30` | Saniye cinsinden |

## Katkı Sağlama

1. Fork oluştur
2. Özellik dalı aç: `git checkout -b ozellik/yeni-ozellik`
3. Değişikliklerini commit et: `ekle: yeni özellik açıklaması`
4. Pull Request aç

## Lisans

MIT — Ayrıntılar için [LICENSE](LICENSE) dosyasına bakın.
```

---

## 5. Hata Mesajları ve Log Yazımı

### Türkçe Hata Mesajları
```python
# Kötü — İngilizce hata, Türkçe projede tutarsız
raise ValueError("User not found")

# İyi — Türkçe ve açıklayıcı
raise KullaniciBulunamadi(f"'{kullanici_id}' numaralı kullanıcı sistemde kayıtlı değil.")
```

### Log Seviyeleri ve Türkçe Kullanım
```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Oturum doğrulama başlatıldı. kullanici_id=%s", kullanici_id)
logger.info("Sipariş oluşturuldu. siparis_no=%s tutar=%s", siparis.no, siparis.tutar)
logger.warning("Stok azalıyor. urun_id=%s kalan=%d", urun.id, urun.stok)
logger.error("Ödeme işlemi başarısız. hata=%s", str(hata))
```

---

## 6. Teknik Terim Hızlı Referans

Tam liste için `references/teknik-terimler.md` dosyasına bakın.

| İngilizce | Türkçe Karşılık |
|-----------|----------------|
| Authentication | Kimlik doğrulama |
| Authorization | Yetkilendirme |
| Deployment | Dağıtım / Kurulum |
| Refactoring | Yeniden düzenleme |
| Repository | Depo |
| Pull Request | Birleştirme isteği |
| Branch | Dal |
| Merge | Birleştirme |
| Dependency | Bağımlılık |
| Middleware | Ara katman |
| Cache | Önbellek |
| Thread | İş parçacığı |
| Callback | Geri çağırım |
| Instance | Örnek / Nesne |
| Endpoint | Uç nokta |

---

## 7. Kontrol Listesi

Kodu göndermeden önce:

- [ ] Yorum satırları Türkçe ve nokta ile bitiyor
- [ ] Değişken isimleri proje diline göre tutarlı
- [ ] Commit mesajı `<tür>: <açıklama>` formatında
- [ ] README.md güncel
- [ ] Hata mesajları kullanıcıya anlamlı
- [ ] Log mesajları yeterli bağlam içeriyor
