---
name: agent-linter
description: Agent ve skill dosyalarinin yapisal dogrulamasi. Frontmatter kontrol, naming convention, zorunlu bolum kontrolu, tutarlilik denetimi. Yeni agent/skill eklendiginde veya mevcut dosyalar duzenlediginde otomatik calistirilir.
---

# Agent & Skill Linter

Agent ve skill dosyalarinin kalite kontrolu. Yanlis yapilandirilmis dosyalar runtime'da sessizce basarisiz olur -- linter bunu onler.

## Agent Dosyasi Kurallari

### Frontmatter (ZORUNLU)

```yaml
---
name: agent-adi          # kebab-case, dosya adiyla AYNI olmali
description: Tek satir   # 20-200 karakter arasi
tools: ["Read", "Bash"]  # Gecerli tool listesi
model: opus              # Opsiyonel: opus | sonnet
---
```

### Frontmatter Validasyonu

| Kural | Kontrol | Hata Seviyesi |
|-------|---------|---------------|
| `name` mevcut | Frontmatter'da name var mi? | ERROR |
| `name` = dosya adi | `name: sleuth` == `sleuth.md` | ERROR |
| `name` kebab-case | `code-reviewer` OK, `codeReviewer` FAIL | ERROR |
| `description` mevcut | Bos olmamali | ERROR |
| `description` uzunlugu | 20-200 karakter | WARN |
| `tools` array | String array olmali | ERROR |
| `tools` gecerli | Sadece bilinen tool isimleri | WARN |
| `model` gecerli | opus, sonnet veya bos | ERROR |

### Body Kurallari

| Kural | Kontrol | Hata Seviyesi |
|-------|---------|---------------|
| System prompt var | Frontmatter'dan sonra icerik var | ERROR |
| 50+ satir | Cok kisa agent tanimlari yetersiz | WARN |
| 2000 satir max | Cok uzun dosyalar token israf eder | WARN |
| Markdown basliklar | En az 1 `##` basligi var | WARN |

## Skill Dosyasi Kurallari

### Frontmatter (ZORUNLU)

```yaml
---
name: skill-adi          # kebab-case
description: Aciklama    # 20-300 karakter
---
```

### Skill Validasyonu

| Kural | Kontrol | Hata Seviyesi |
|-------|---------|---------------|
| Dosya adi | `SKILL.md` veya `skill.md` | ERROR |
| `name` mevcut | Frontmatter'da | ERROR |
| `name` = klasor adi | `name: tdd-workflow` == `skills/tdd-workflow/` | WARN |
| `description` mevcut | Bos olmamali | ERROR |
| Icerik var | Frontmatter'dan sonra en az 20 satir | WARN |
| Kod ornegi var | En az 1 code block | INFO |

## Lint Calistirma

### Bash Script

```bash
#!/bin/bash
# scripts/lint-agents.sh

ERRORS=0
WARNS=0

lint_agent() {
  local file="$1"
  local name=$(basename "$file" .md)

  # Frontmatter kontrolu
  if ! head -1 "$file" | grep -q "^---"; then
    echo "ERROR: $file - frontmatter yok"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # name field kontrolu
  local fm_name=$(sed -n '/^---$/,/^---$/p' "$file" | grep "^name:" | sed 's/name: *//')
  if [ -z "$fm_name" ]; then
    echo "ERROR: $file - name field yok"
    ERRORS=$((ERRORS + 1))
  elif [ "$fm_name" != "$name" ]; then
    echo "ERROR: $file - name '$fm_name' != dosya adi '$name'"
    ERRORS=$((ERRORS + 1))
  fi

  # description kontrolu
  local desc=$(sed -n '/^---$/,/^---$/p' "$file" | grep "^description:")
  if [ -z "$desc" ]; then
    echo "ERROR: $file - description yok"
    ERRORS=$((ERRORS + 1))
  fi

  # Uzunluk kontrolu
  local lines=$(wc -l < "$file")
  if [ "$lines" -lt 10 ]; then
    echo "WARN: $file - cok kisa ($lines satir)"
    WARNS=$((WARNS + 1))
  elif [ "$lines" -gt 2000 ]; then
    echo "WARN: $file - cok uzun ($lines satir)"
    WARNS=$((WARNS + 1))
  fi
}

echo "=== Agent Linter ==="
for f in agents/*.md; do
  lint_agent "$f"
done

echo ""
echo "=== Skill Linter ==="
for f in skills/*/SKILL.md skills/*/skill.md; do
  [ -f "$f" ] && lint_agent "$f"
done

echo ""
echo "Sonuc: $ERRORS error, $WARNS warning"
[ "$ERRORS" -gt 0 ] && exit 1 || exit 0
```

### CI Entegrasyonu

```yaml
# .github/workflows/lint-agents.yml
name: Agent & Skill Lint
on:
  pull_request:
    paths: ['agents/**', 'skills/**']

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: bash scripts/lint-agents.sh
```

## Yaygin Hatalar

| Hata | Ornek | Cozum |
|------|-------|-------|
| name/dosya uyumsuzlugu | `name: codeReviewer` dosya: `code-reviewer.md` | name'i kebab-case yap |
| Description cok kisa | `description: Reviews code` | Ne yaptigini detayla |
| Tools yanlis format | `tools: Read, Bash` | `tools: ["Read", "Bash"]` |
| Bos agent dosyasi | Sadece frontmatter, body yok | System prompt ekle |
| Duplicate name | 2 agent ayni name'e sahip | Benzersiz isim ver |
| Skill klasor/name uyumsuz | `name: tdd` klasor: `tdd-workflow/` | Eslestir |

## Toplu Lint Raporu

```bash
# Tum agent'lari tara, rapor uret
cd ~/vibecosystem
bash scripts/lint-agents.sh 2>&1 | tee lint-report.txt

# Sadece ERROR'lari goster
grep "^ERROR" lint-report.txt

# Istatistik
echo "Agents: $(ls agents/*.md | wc -l)"
echo "Skills: $(ls skills/*/SKILL.md skills/*/skill.md 2>/dev/null | wc -l)"
echo "Errors: $(grep -c ERROR lint-report.txt)"
echo "Warnings: $(grep -c WARN lint-report.txt)"
```

## vibecosystem Entegrasyonu

- **verifier agent**: Lint'i final quality gate'e ekle
- **qa-engineer agent**: Yeni agent/skill PR'larinda lint calistir
- **self-learner agent**: Lint hatalari pattern olarak ogren
- **catalyst agent**: Scaffold sırasinda lint-uyumlu dosya uret
- **/commit skill**: Commit oncesi agent/skill dosyalarini lint'le
