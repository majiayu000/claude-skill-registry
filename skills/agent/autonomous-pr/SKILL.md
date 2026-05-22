---
name: autonomous-pr
description: Otonom PR yasam dongusu. PR olustur, CI bekle, hata varsa duzelt, review feedback'i uygula, merge'e hazirla. Budget ve zaman limiti ile kontrol altinda tutulan tam otonom PR pipeline'i.
---

# Autonomous PR Lifecycle

PR'i olusturmaktan merge'e kadar tum sureci otonom yonet. CI basarisiz olursa duzelt, review feedback gelirse uygula, butce asarsa dur.

## PR Pipeline

```
1. BRANCH    → Feature branch olustur
2. IMPLEMENT → Kodu yaz (kraken/spark)
3. VERIFY    → Lokal test + lint + build
4. PR CREATE → gh pr create
5. CI WAIT   → CI pipeline'i bekle
6. CI FIX    → Basarisizsa duzelt, tekrar push (max 3)
7. REVIEW    → Review feedback bekle
8. APPLY     → Feedback'i uygula
9. READY     → Merge'e hazir bildir
```

## Kullanim

### Basit: Tek PR

```bash
# Claude'a otonom PR olusturttir
claude -p "
Feature: kullanici profil sayfasi ekle
Branch: feat/user-profile
PR target: main

Pipeline:
1. Branch olustur
2. Implement et
3. Test yaz
4. PR olustur
5. CI bekle ve fix et
6. Hazir olunca bildir
"
```

### Gelismis: Budget ve Zaman Limiti

```bash
claude -p "
Feature: auth middleware refactor
Branch: refactor/auth-middleware
PR target: main

Limitler:
  --budget 500K tokens    # Max token harcama
  --max-duration 30m      # Max sure
  --max-ci-retries 3      # Max CI fix denemesi
  --auto-merge false      # Merge'i ben onaylayacagim

Basarisiz olursa:
  Draft PR olarak birak, ne yaptigini acikla
"
```

## CI Fix Dongusu

```
CI BASARISIZ
  │
  ├─ Build hatasi?
  │   └─ build-error-resolver agent cagir
  │      └─ Fix → Push → CI tekrar bekle
  │
  ├─ Test basarisiz?
  │   └─ Hata mesajini oku
  │      ├─ Test kodu hatali → Test'i duzelt
  │      └─ Implementation hatali → Kodu duzelt
  │      └─ Push → CI tekrar bekle
  │
  ├─ Lint hatasi?
  │   └─ Otomatik fix (prettier, eslint --fix)
  │      └─ Push → CI tekrar bekle
  │
  ├─ Type hatasi?
  │   └─ Type fix uygula
  │      └─ Push → CI tekrar bekle
  │
  └─ 3. deneme basarisiz?
      └─ DURR → Draft PR olarak birak
         └─ PR body'ye aciklama yaz
```

### CI Fix Script

```bash
#!/bin/bash
# scripts/ci-fix-loop.sh

MAX_RETRIES=3
RETRY=0

while [ $RETRY -lt $MAX_RETRIES ]; do
  echo "=== CI Check (attempt $((RETRY + 1))/$MAX_RETRIES) ==="

  # CI durumunu kontrol et
  STATUS=$(gh pr checks --json state -q '.[].state' | sort -u)

  if echo "$STATUS" | grep -q "SUCCESS"; then
    echo "CI PASSED"
    exit 0
  fi

  if echo "$STATUS" | grep -q "PENDING"; then
    echo "CI bekliyor..."
    sleep 30
    continue
  fi

  # Basarisiz -- fix dene
  RETRY=$((RETRY + 1))
  echo "CI FAILED (attempt $RETRY)"

  # Hata detayini al
  FAILED=$(gh pr checks --json name,state -q '.[] | select(.state=="FAILURE") | .name')

  for check in $FAILED; do
    echo "Fixing: $check"
    # Claude'a fix ettir
    claude -p "CI check '$check' failed. Read the error, fix it, commit." --no-input
  done

  git push
  sleep 60  # CI'in yeniden baslamasini bekle
done

echo "CI FIX BASARISIZ ($MAX_RETRIES deneme)"
exit 1
```

## Review Feedback Dongusu

```
REVIEW GELDI
  │
  ├─ Approval?
  │   └─ MERGE'E HAZIR
  │
  ├─ Changes requested?
  │   └─ Her yorumu oku
  │      ├─ Kod degisikligi isteniyor → Uygula
  │      ├─ Soru soruluyor → Cevapla (PR comment)
  │      └─ Mimari itiraz → DURDUR, kullaniciya bildir
  │   └─ Degisiklikleri push et
  │   └─ Re-review iste
  │
  └─ Comment only?
      └─ Cevaplanmasi gereken varsa cevapla
```

### Review Feedback Uygulama

```bash
# PR review comment'lerini oku
gh pr view <PR_NUMBER> --comments --json comments

# Her comment icin fix uygula
claude -p "
PR #<NUMBER> icin su review feedback geldi:

$(gh api repos/OWNER/REPO/pulls/<NUMBER>/comments | jq -r '.[] | "File: \(.path):\(.line)\nComment: \(.body)\n---"')

Her feedback'i uygula, commit et.
"

git push
gh pr review <PR_NUMBER> --comment --body "Review feedback uygulandı, tekrar bakabilir misiniz?"
```

## Budget Kontrol

### Token Sayaci

```bash
# Session token kullanimi takibi
# Her agent cagrisinda tahmini token sayisini artir
TOKEN_USED=0
TOKEN_BUDGET=500000  # 500K limit

check_budget() {
  if [ $TOKEN_USED -gt $TOKEN_BUDGET ]; then
    echo "BUDGET ASILDI: $TOKEN_USED / $TOKEN_BUDGET tokens"
    echo "Otonom islem durduruluyor."
    # Draft PR olarak birak
    gh pr ready --undo 2>/dev/null
    exit 1
  fi
}
```

### Zaman Kontrol

```bash
START_TIME=$(date +%s)
MAX_DURATION=1800  # 30 dakika

check_time() {
  ELAPSED=$(($(date +%s) - START_TIME))
  if [ $ELAPSED -gt $MAX_DURATION ]; then
    echo "ZAMAN LIMITI: ${ELAPSED}s / ${MAX_DURATION}s"
    echo "Mevcut durumu kaydet ve dur."
    git add -A && git commit -m "WIP: zaman limiti asildi" || true
    gh pr create --draft --title "WIP: $FEATURE" --body "Zaman limiti nedeniyle duraklatildi." 2>/dev/null
    exit 1
  fi
}
```

## Guvenlik Kurallari

```
1. ASLA --force push yapma
2. ASLA main/master'a direkt push yapma
3. ASLA review olmadan merge yapma (auto-merge false default)
4. Secret/credential commit ETME
5. Budget asiminda DURDUR, devam etme
6. CI 3 kez basarisizsa DURDUR, draft birak
7. Mimari itirazda DURDUR, kullaniciya sor
```

## vibecosystem Entegrasyonu

- **shipper agent**: Release PR'lari icin bu pipeline'i kullanir
- **build-error-resolver agent**: CI fix dongusunde build hatalarini cozer
- **code-reviewer agent**: Self-review yapar push oncesi
- **verifier agent**: Lokal verify adiminda calisir
- **kraken agent**: Implementation adiminda TDD ile yazar
- **/commit skill**: PR icindeki commit'leri yonetir
