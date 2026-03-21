---
name: learn
description: Hizlica kural/ogrenim kaydet. CLAUDE.md'ye ve memory'ye yazar. Kullanim: /learn <kural>
---

# /learn - Hizli Ogrenim Kaydi

Kullanici `/learn <kural>` yazdiginda su adimlari takip et:

## Adim 1: Argumani Parse Et

Kullanicinin verdigi metni analiz et:
- Ne ogrenilmeli?
- Severity: CRITICAL / IMPORTANT / MINOR
- Kategori: code / react / api / git / security / performance / testing / workflow

## Adim 2: CLAUDE.md'ye Kaydet

Mevcut dizinde CLAUDE.md var mi kontrol et.

### CLAUDE.md VARSA:

"LEARNED MISTAKES" bolumune ekle:

```markdown
- [TARIH] HATA: <ogrenim> | COZUM: <ne yapilmali> | ONLEM: <kural>
```

"ERROR TRACKING" tablosuna ekle:

```markdown
| TARIH | kategori | - | 1 | Learned | Yes |
```

### CLAUDE.md YOKSA:

Kullaniciya sor: "Bu dizinde CLAUDE.md yok. Olusturayim mi? (template: ~/.claude/templates/CLAUDE-TEMPLATE.md)"

## Adim 3: Memory'ye Kaydet

Genel bir ogrenim ise (sadece bu projeye ozel degilse), memory sistemine de kaydet:

```bash
cd ~/.claude && PYTHONPATH=scripts python3 scripts/core/store_learning.py \
  --session-id "learn-command" \
  --content "<ogrenim>" \
  --context "<baglam>" \
  --tags "learn,<kategori>" \
  --confidence high
```

## Adim 4: Onay Ver

```
OGRENILDI:
  Kural: <kural>
  Severity: CRITICAL/IMPORTANT/MINOR
  Kaydedildi: CLAUDE.md + memory
  Kategori: <kategori>
```

## Ornekler

```
/learn API route'larda try-catch sart
-> CLAUDE.md'ye IMPORTANT/api olarak kaydeder

/learn .env dosyasini ASLA commit'leme
-> CLAUDE.md'ye CRITICAL/security olarak kaydeder

/learn React'ta useEffect cleanup unutma
-> CLAUDE.md'ye IMPORTANT/react olarak kaydeder

/learn Bu projede port 3737 kullaniliyor
-> CLAUDE.md'ye MINOR/workflow olarak kaydeder (memory'ye kaydetmez, proje-ozel)
```

## Kurallar

1. Kisa ve net yaz - gereksiz uzatma
2. Her ogrenim actionable olmali (ne yapilmali acik)
3. Ornek kod ekle mumkunse
4. Tekrar kontrolu yap - ayni kural varsa "tekrar" sayisini artir
5. Tarih otomatik eklenir (bugunun tarihi)
