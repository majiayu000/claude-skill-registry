---
name: gate-check
description: Phase transition validation with artifact checklists, PASS/FAIL/CONDITIONAL gates for workflows
---

# Gate Check

Faz gecis validasyonu. Bir sonraki faza gecmeden once gerekliliklerin tamam oldugundan emin ol.

## Standart Fazlar

```
Planning ──▶ Development ──▶ Testing ──▶ Staging ──▶ Production
   G1            G2            G3          G4           G5
```

## Gate Tanimlari

### G1: Planning ──▶ Development

| # | Kriter | Kanit |
|---|--------|-------|
| 1 | Requirements dokumani var | PRD/spec dosyasi |
| 2 | Teknik plan onaylandi | Plan dosyasi + onay |
| 3 | Task'lar olusturuldu | Task listesi |
| 4 | Dependency'ler belirlendi | Dependency listesi |
| 5 | Risk analizi yapildi | Risk matrisi (opsiyonel) |

### G2: Development ──▶ Testing

| # | Kriter | Kanit |
|---|--------|-------|
| 1 | Tum task'lar implement edildi | Task durumlari |
| 2 | Code review tamamlandi | Review onaylari |
| 3 | Build basarili | Build log |
| 4 | Unit test coverage >= 80% | Coverage raporu |
| 5 | Lint/type check temiz | Lint raporu |
| 6 | Security review (auth/data isleri) | Security raporu |

### G3: Testing ──▶ Staging

| # | Kriter | Kanit |
|---|--------|-------|
| 1 | Unit testler PASS | Test raporu |
| 2 | Integration testler PASS | Test raporu |
| 3 | E2E critical path testleri PASS | Playwright raporu |
| 4 | Bug'lar triaged (P0/P1 yok) | Bug listesi |
| 5 | Performance baseline karsilandi | Metrikler |

### G4: Staging ──▶ Production

| # | Kriter | Kanit |
|---|--------|-------|
| 1 | Staging'de 24h+ stabil | Monitoring |
| 2 | Smoke testler PASS | Test raporu |
| 3 | Rollback plani hazir | Rollback dokumani |
| 4 | Changelog yazildi | CHANGELOG.md |
| 5 | Stakeholder onay | Onay kaydi |

## Karar Tipleri

| Karar | Anlam | Aksiyon |
|-------|-------|---------|
| **PASS** | Tum kriterler saglanmis | Sonraki faza gec |
| **FAIL** | Kritik kriter(ler) saglanmamis | Mevcut fazda kal, eksikleri tamamla |
| **CONDITIONAL** | Minor eksikler var, ilerlenebilir | Sonraki faza gec, eksikleri paralel tamamla |

## Gate Check Ciktisi

```
GATE CHECK: G2 (Development -> Testing)
Date: [tarih]

[PASS] Build basarili
[PASS] Code review tamamlandi
[PASS] Lint/type check temiz
[FAIL] Unit test coverage 72% (min 80%)
[PASS] Security review temiz
[PASS] Tum task'lar implement edildi

KARAR: FAIL
NEDEN: Test coverage yetersiz (72% < 80%)
AKSIYON: Test ekle, %80 ustune cik, gate check'i tekrarla
```

## Custom Gate Tanimlama

Projeye ozel gate tanimlamak icin:

```markdown
### Custom Gate: [Isim]

| # | Kriter | Zorunlu | Kanit |
|---|--------|---------|-------|
| 1 | [Kriter] | Evet/Hayir | [Ne bekleniyor] |
```

Zorunlu=Evet olan kriterler FAIL'de FAIL, Zorunlu=Hayir olan CONDITIONAL'a duser.

## Entegrasyon

- **/swarm** workflow'unda her phase gecisinde otomatik gate check
- **verifier** agent'i G2/G3 icin build+test kontrolleri yapar
- **code-reviewer** agent'i G2 icin review kontrolu yapar
- **security-reviewer** agent'i G2 icin security kontrolu yapar
