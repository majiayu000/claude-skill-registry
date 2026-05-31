---
name: github
description: >
  Manages all git operations (commit, push, branch management, PR creation)
  in a standardized, safe, and consistent way. Automatically runs the code-review
  skill before any commit. Enforces Conventional Commits standard. Handles the
  full lifecycle: branch → review → commit → push → PR.
---

<!--
  TÜRKÇE AÇIKLAMA
  ───────────────
  Bu skill, tüm git işlemlerini (commit, push, branch yönetimi, PR oluşturma)
  standart, güvenli ve tutarlı biçimde yönetir. Commit öncesi otomatik olarak
  `code-review` skill'ini çalıştırır. Conventional Commits standardını uygular.
  "Çalışıyor, attım" yerine "incelendi, standarda uygun, dokümante edildi, atıldı" der.

  NE ZAMAN: Herhangi bir git işlemi yapılacağında — commit, push, branch oluşturma,
            PR açma, tag. Bu skill atlanarak doğrudan git komutu çalıştırılmaz.
  ÇIKTI:    Clean commit history, PR açıklaması, güncellenmiş CHANGELOG.
-->


# GitHub Skill

## Temel Kural

**Hiçbir commit `code-review` skill çalıştırılmadan atılmaz.**  
Bu kural ihlal edilemez. "Küçük değişiklik" veya "sadece bir satır" istisnası yoktur.

---

## Commit Standardı — Conventional Commits

### Format

```
<type>(<scope>): <subject>

[body — opsiyonel]

[footer — opsiyonel]
```

### Type Listesi

| Type | Ne Zaman Kullanılır |
|------|-------------------|
| `feat` | Yeni özellik |
| `fix` | Bug düzeltmesi |
| `refactor` | Davranış değişmeden kod düzenlemesi |
| `style` | Formatlama, boşluk (işlevsel değişiklik yok) |
| `test` | Test ekleme veya düzenleme |
| `docs` | Dokümantasyon değişikliği |
| `chore` | Build, dependency, config güncellemesi |
| `perf` | Performans iyileştirmesi |
| `ci` | CI/CD pipeline değişikliği |
| `revert` | Önceki commit'i geri alma |

### Scope (Opsiyonel ama Önerilir)

Etkilenen modül, komponent veya katman:
```
feat(auth): add refresh token rotation
fix(userService): handle null email in validation
refactor(Button): extract loading state to hook
chore(deps): upgrade react to 19.2.0
```

### Subject Kuralları

- **İmperative mood** kullan (Türkçe: emir kipi): "add" not "added", "fix" not "fixed"
- **Küçük harf** ile başla
- **Nokta ile bitirme**
- **72 karakter** sınırı
- **Ne** değiştiğini yaz, **neden** body'de açıkla

### Body (Neden Değişti?)

```
feat(auth): add refresh token rotation

Statik refresh token'lar çalınırsa süresiz erişim sağlar.
Rotation ile her kullanımda yeni token üretilir, eskisi geçersiz kılınır.
RFC 6749 güvenlik önerisi doğrultusunda implement edildi.
```

### Breaking Change

```
feat(api)!: change user ID format from integer to UUID

BREAKING CHANGE: Tüm /api/users/:id endpoint'leri artık UUID string
bekliyor. Integer ID kullanan client'lar güncellenmeli.

Migration guide: docs/migrations/integer-to-uuid.md
```

---

## Tam İş Akışı

### 1. Branch Oluştur

```bash
# Format: <type>/<kısa-açıklama>
git checkout -b feat/user-registration
git checkout -b fix/token-refresh-null-check
git checkout -b refactor/button-loading-state
```

Branch isimlendirme kuralları:
- Lowercase, kebab-case
- Type ile başlar (`feat/`, `fix/`, `refactor/`, `hotfix/`)
- `main` veya `master`'a direkt commit atılmaz

---

### 2. Code Review Çalıştır

Commit atmadan önce **`code-review` skill'ini aç ve MOD A'yı uygula**.

```bash
# Önce ne değiştiğini kontrol et
git status
git diff --staged
```

Code review checklist tamamlanmadan 3. adıma geçilmez.

---

### 3. Stage ve Commit

```bash
# İlgili dosyaları stage'e al — hepsini değil, mantıklı gruplar halinde
git add src/services/userService.ts src/services/userService.test.ts

# Commit at — standarda göre
git commit -m "feat(userService): add createUser with password hashing

Yeni kullanıcı kaydı için service katmanı eklendi.
bcrypt ile password hash'leniyor (saltRounds: 12).
Duplicate email durumunda DuplicateEmailError fırlatılıyor.

Testler: userService.test.ts — 8 test, hepsi geçiyor"
```

**Atomik commit'ler:**
- Bir commit, bir mantıksal değişiklik
- Migration + model + service = 3 ayrı commit
- "misc fixes" veya "wip" commit'leri yasak

---

### 4. Her Commit Sonrası Kontrol

```bash
git log --oneline -5    # Son commit'lere bak
git show HEAD           # Son commit'in diff'ini kontrol et
```

Commit mesajı yanlışsa hemen düzelt (push öncesinde):
```bash
git commit --amend -m "fix(auth): handle null refresh token in rotation"
```

---

### 5. Push

```bash
# İlk push — upstream set et
git push -u origin feat/user-registration

# Sonraki push'lar
git push
```

**Push öncesi:**
```bash
# Testler son kez çalıştırılır
npm test

# Main'den geride mi? Rebase et
git fetch origin
git rebase origin/main
```

---

### 6. Pull Request Oluştur

GitHub CLI ile (PR şablonu inline — `.github/PR_TEMPLATE.md` yoksa aşağıdakini kullan):

```bash
gh pr create \
  --title "feat(auth): user registration with email verification" \
  --base main \
  --label "feature" \
  --body "## Ne Değişti?
<2-3 cümle: ne yapıldı, neden>

## Nasıl Test Edildi?
- [ ] Unit testler: \`npm test\` — X/X geçiyor
- [ ] Integration test: manuel doğrulandı
- [ ] Edge case'ler test edildi

## Checklist
- [ ] Code review (MOD A) tamamlandı
- [ ] Testler geçiyor
- [ ] Breaking change varsa CHANGELOG güncellendi
- [ ] Yeni env variable varsa \`.env.example\`'a eklendi
- [ ] \`documentation-sync\` skill çalıştırıldı (API değişikliği varsa)

## İlgili
- Closes #İSSUE_NUMARASI"
```

> **Not:** Ekip `.github/PR_TEMPLATE.md` oluşturursa, body kısmını `--body "$(cat .github/PR_TEMPLATE.md)"` ile değiştir.

---

### 7. CHANGELOG Güncelle

Her PR için `CHANGELOG.md`'nin `[Unreleased]` bölümüne ekle:

```markdown
## [Unreleased]

### Added
- User registration endpoint (POST /api/auth/register) with email verification

### Fixed
- Null refresh token causing 500 error on token rotation

### Changed
- User ID format migrated from integer to UUID (breaking)
```

---

## Özel Durumlar

### Hotfix (Production Emergency)
```bash
# Main'den hotfix branch aç
git checkout -b hotfix/null-pointer-login main

# Düzelt → test → commit
git commit -m "fix(auth): prevent null pointer when user session expires"

# Hem main'e hem aktif development branch'e merge
git checkout main && git merge hotfix/null-pointer-login
git checkout develop && git merge hotfix/null-pointer-login
```

### Commit Geri Alma (Push Öncesi)
```bash
git reset HEAD~1 --soft    # Commit geri al, değişiklikler staged kalır
```

### Tag ve Release
```bash
git tag -a v1.2.0 -m "Release v1.2.0 — user registration feature"
git push origin v1.2.0
```

---

## Yasaklar

- `git push --force` (force push) — sadece personal branch'te, hiçbir zaman `main`'e
- `git commit -m "fix"` — anlamsız commit mesajı
- `git add .` — staging kontrol edilmeden hepsini ekleme
- `git commit --no-verify` — pre-commit hook'ları atlama
- Direkt `main`'e push — pull request olmadan

---

## Hızlı Referans

```bash
# Tam iş akışı
git checkout -b feat/my-feature           # 1. Branch
# → code-review skill (MOD A)             # 2. Review
git add <ilgili dosyalar>                  # 3. Stage
git commit -m "feat(scope): description"  # 4. Commit
git push -u origin feat/my-feature        # 5. Push
gh pr create --title "..." --body "..."   # 6. PR
```
