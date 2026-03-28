---
name: resmi-yazi
description: Türkçe resmi yazı, dilekçe, itiraz mektubu ve kurumsal yazışma üretimi. Devlet kurumlarına dilekçe, SGK/vergi idaresi yazışması, Noter belgesi, şikâyet mektubu, iş başvurusu için kullan.
license: MIT
metadata:
  author: hermes-turkce-skills
  version: "1.0"
  language: Turkish
  region: TR
---

# Resmi Yazı ve Dilekçe Asistanı

Türkiye'de resmi yazışmalar için şablon ve rehber.

## Dilekçe Yazım Kuralları

### Temel Yapı
1. **Başlık**: Kime yazıldığı (makam)
2. **İlgi** (varsa): Önceki yazışma referansı
3. **Konu**: Tek cümle, öz
4. **Giriş**: Kim olduğunuz ve ne istediğiniz
5. **Gerekçe**: Neden istediğiniz (belgeler, kanun maddeleri)
6. **Sonuç/Talep**: Net istek cümlesi
7. **İmza**: Tarih, ad soyad, TC kimlik, iletişim

### Dil Kuralları
- Her zaman **siz** ile hitap
- Edilgen yapı: "yapılmasını talep ediyorum" değil "yapılmasını arz ederim"
- Kişisel zamir: "ben" değil "tarafımca", "şahsıma"
- Kanun/yönetmelik atıfları italik veya parantez içinde
- Tarih: gün/ay/yıl formatında

## Dilekçe Şablonları

### Genel Dilekçe Şablonu
```
[ŞEHİR], [TARİH]

[KURUM ADI]'NA
[KURUM ŞEHRİ]

KONU: [Tek cümle konu başlığı]

Sayın [Makam/Yetkili],

[Kendinizi tanıtın: Ad, soyad, TC kimlik numarası, adres]

[Ne istediğinizi açıklayın - 1-2 paragraf]

[Hukuki dayanak veya gerekçe - varsa]

Yukarıda arz ettiğim hususların değerlendirilerek [TALEBİNİZ] hususunda
gereğini saygılarımla arz ederim.

                                        [Ad Soyad]
                                        TC: [TC Kimlik No]
                                        Adres: [Açık Adres]
                                        Tel: [Telefon]
                                        E-posta: [e-posta]

EKLER:
1. [Belge adı]
2. [Belge adı]
```

### SGK Hizmet Belgesi Talebi
```
[ŞEHİR], [TARİH]

SOSYAL GÜVENLİK KURUMU
[İLÇE] SOSYAL GÜVENLİK MERKEZİ MÜDÜRLÜĞÜ'NE
[ŞEHİR]

KONU: Hizmet Belgesi Talebi

Sayın Yetkili,

[Ad Soyad] olup, T.C. kimlik numaram [TC NO], SGK sicil numaram [SGK NO]'dur.

[Çalıştığım kurum/şirket] bünyesinde [başlangıç tarihi] - [bitiş tarihi]
tarihleri arasında sigortalı olarak çalışmış bulunmaktayım.

Söz konusu dönemlere ait hizmet belgesinin tarafıma verilmesini
saygılarımla arz ederim.

                                        [Ad Soyad]
                                        TC: [TC Kimlik No]
                                        Adres: [Açık Adres]
                                        Tel: [Telefon]

EKLER:
1. Nüfus cüzdanı fotokopisi
```

### Vergi İadesine İtiraz
```
[ŞEHİR], [TARİH]

[VERGİ DAİRESİ ADI] MÜDÜRLÜĞÜ'NE
[ŞEHİR]

KONU: Vergi İncelemesi Kararına İtiraz

Sayın Müdürlük,

[Ad Soyad] olup, vergi kimlik numaram [VKN/TC NO]'dur.

[Tarih] tarih ve [sayı] sayılı [işlem türü] kararını [tarihte] tebellüğ
ettim.

Söz konusu karar aşağıdaki nedenlerle hukuka aykırıdır:

1. [İtiraz gerekçesi 1]
2. [İtiraz gerekçesi 2]

Vergi Usul Kanunu'nun 377. maddesi uyarınca, tebliğ tarihinden itibaren
30 gün içinde itiraz hakkımı kullanmaktayım.

Kararın kaldırılmasına veya düzeltilmesine karar verilmesini saygılarımla
arz ederim.

                                        [Ad Soyad]
                                        VKN/TC: [No]
                                        Adres: [Açık Adres]
                                        Tel: [Telefon]

EKLER:
1. İtiraz edilen kararın örneği
2. [Destekleyici belgeler]
```

### İşten Ayrılma Bildirimi (İstifa)
```
[ŞEHİR], [TARİH]

[ŞİRKET ADI]
İNSAN KAYNAKLARI MÜDÜRLÜĞÜ'NE

KONU: İstifa Bildirimi

Sayın Yetkili,

[Ad Soyad] olarak [işe başlama tarihi]'nden bu yana [departman/unvan]
pozisyonunda görev yapmaktayım.

Kişisel/ailevi/kariyer nedenleriyle [istifa tarihi] itibarıyla görevimden
ayrılmak istediğimi bildiririm.

İş Kanunu'nun 17. maddesi uyarınca [ihbar süresi] ihbar süresine uymayı
taahhüt eder, gerekli devir teslim işlemlerini yerine getireceğimi beyan ederim.

Şirkete olan katkılarım için teşekkür eder, başarılar dilerim.

                                        [Ad Soyad]
                                        Sicil No: [No]
                                        Tel: [Telefon]
```

### Kiracı Tahliye İhtarnamesi (Ev Sahibinden)
```
İHTARNAME

İHTAR EDEN   : [Ad Soyad], [Adres]
MUHATAP      : [Kiracı Ad Soyad], [Adres]
KONU         : Tahliye İhtarı

[Adres]'te bulunan taşınmazımı [kira başlangıç tarihi] tarihinden bu yana
[aylık kira] TL bedelle kiracı olarak kullanmaktasınız.

[İhtar nedeni: kira borcunu ödemedi / sözleşme süresi doldu / vs.]

Bu nedenle, işbu ihtarnamenin tebliğinden itibaren [süre] gün içinde
söz konusu taşınmazı tahliye etmenizi, aksi hâlde yasal yollara başvurulacağını
ihtar ederim.

[Tarih]

                                        [Ad Soyad]
                                        [TC Kimlik No]
                                        [İletişim]
```

## İş Başvuru Mektubu

```
[ŞEHİR], [TARİH]

[ŞİRKET ADI]
İNSAN KAYNAKLARI DEPARTMANI'NA

KONU: [Pozisyon] Pozisyonu Başvurusu

Sayın İnsan Kaynakları Ekibi,

[Pozisyon]pozisyonu için başvurmak istiyorum.

[Eğitim ve deneyim özeti - 2-3 cümle]

[Neden bu şirket - şirkete özel, genel değil]

[En güçlü 2-3 yetkinliğiniz ve somut başarı]

Ön görüşme için müsait olduğumu belirtir, değerlendirmenizi beklerim.

Saygılarımla,
[Ad Soyad]
[Telefon] | [E-posta] | [LinkedIn (varsa)]

EKLER:
1. Özgeçmiş
2. [Varsa referans mektubu]
```

## Adım Adım Dilekçe Yazımı

Kullanıcıdan dilekçe yazması istendiğinde şu bilgileri sor:
1. **Kime yazılıyor?** (Hangi kurum/makam)
2. **Ne isteniyor?** (Talep nedir)
3. **Kim yazıyor?** (Ad, soyad, TC kimlik gerekir mi?)
4. **Gerekçe nedir?** (Neden bu talep)
5. **Ekler var mı?** (Hangi belgeler eklenecek)

Bu bilgilerle yukarıdaki şablona uygun, eksiksiz dilekçe üret.

## Önemli Notlar

- Dilekçelerde TC kimlik numarası yazılması güvenlik riski oluşturabilir; kullanıcıyı uyar
- Hukuki süreçlerde mutlaka avukat görüşü alınmalı
- İhtarname noter onaylı olması halinde hukuki bağlayıcılığı artar
- Resmi yazışmaların bir kopyasını sakla
