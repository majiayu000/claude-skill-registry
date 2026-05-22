---
name: refactor-clean
description: >
  Codebase temizliği için kullan. "/refactor-clean" komutuyla tetiklenir.
  Dead code, kullanılmayan import, loose .md dosyaları, eski TODO'lar
  temizlendiğinde devreye gir. Uzun session sonlarında kullanılması önerilir.
---

# Refactor & Clean Workflow

## Kapsam
Bu skill davranış değiştirmez — sadece temizlik yapar.

## Adımlar

### 1. Dead Code Tarama
```bash
# Kullanılmayan import'ları bul
grep -r "import" src/ | # analiz

# TypeScript unused variables
npx tsc --noEmit 2>&1 | grep "declared but"
```

### 2. TODO / FIXME Tarama
```bash
grep -r "TODO\|FIXME\|HACK\|XXX" src/
```
Listele ve kullanıcıya göster. Hangilerinin çözüleceğini sor.

### 3. Console.log Tarama
```bash
grep -r "console\." src/ --include="*.ts" --include="*.tsx"
```
Bulunanları kaldır veya logger'a çevir.

### 4. Loose .md Dosyaları
`.claude/tmp/` klasöründe 7 günden eski session dosyaları:
```bash
find .claude/tmp/ -name "*.md" -mtime +7
```
Kullanıcıya listele, onay alarak sil.

### 5. Kullanılmayan Dependency Kontrolü
```bash
npx depcheck
```
Sonuçları göster, kullanıcı kararına bırak.

### 6. Test Çalıştır
Temizlik sonrası: `npm test`
Tüm testler geçmeli — hiçbir davranış değişmemeli.

### 7. Sonuç Raporu
- Kaç satır silindi
- Kaç dosya düzenlendi
- Test sonucu
