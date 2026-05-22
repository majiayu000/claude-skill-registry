---
name: lint-and-validate
description: Automatic quality control, linting, and static analysis procedures. Use after every code modification to ensure syntax correctness and project standards. Triggers onKeywords: lint, format, check, validate, types, static analysis.
allowed-tools: Read, Glob, Grep, Bash
---

# Lint ve Doğrulama Yeteneği

> **ZORUNLU:** HER kod değişikliğinden sonra uygun doğrulama araçlarını çalıştırın. Kod hatasız olana kadar bir görevi bitirmeyin.

### Ekosisteme Göre Prosedürler

#### Node.js / TypeScript
1. **Lint/Düzelt:** `npm run lint` veya `npx eslint "yol" --fix`
2. **Tipler:** `npx tsc --noEmit`
3. **Güvenlik:** `npm audit --audit-level=high`

#### Python
1. **Linter (Ruff):** `ruff check "yol" --fix` (Hızlı & Modern)
2. **Güvenlik (Bandit):** `bandit -r "yol" -ll`
3. **Tipler (MyPy):** `mypy "yol"`

## Kalite Döngüsü
1. **Kodu Yaz/Düzenle**
2. **Denetimi Çalıştır:** `npm run lint && npx tsc --noEmit`
3. **Raporu Analiz Et:** "FINAL AUDIT REPORT" bölümünü kontrol et.
4. **Düzelt & Tekrarla:** "FINAL AUDIT" başarısızlıklarıyla kod göndermeye izin VERİLMEZ.

## Hata Yönetimi
- `lint` başarısız olursa: Stil veya sözdizimi sorunlarını hemen düzeltin.
- `tsc` başarısız olursa: Devam etmeden önce tip uyuşmazlıklarını düzeltin.
- Hiçbir araç yapılandırılmamışsa: Proje kök dizininde `.eslintrc`, `tsconfig.json`, `pyproject.toml` olup olmadığını kontrol edin ve oluşturulmasını önerin.

---
**Katı Kural:** Hiçbir kod bu kontrolleri geçmeden "bitti" olarak commit edilmemeli veya raporlanmamalıdır.

---

## Scriptler

| Script | Amaç | Komut |
|--------|---------|---------|
| `scripts/lint_runner.py` | Birleşik lint kontrolü | `python scripts/lint_runner.py <project_path>` |
| `scripts/type_coverage.py` | Tip kapsamı analizi | `python scripts/type_coverage.py <project_path>` |
