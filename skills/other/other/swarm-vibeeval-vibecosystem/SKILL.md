---
name: swarm
description: Tum ekibi ayni anda devreye sok. Agent'lar paralel calisir, birbirine soru sorar, birlikte gelistirir. Kullanim: /swarm <gorev>
---

# /swarm - Collaborative Swarm Mode

Tum ana ekibi ayni anda devreye sokar. Agent'lar paralel calisir, shared dosyalar uzerinden haberlesir.

## Kullanim

```
/swarm Kullanici authentication sistemi ekle
/swarm Bu projeyi bastan incele ve iyilestir
/swarm Yeni e-commerce modulu gelistir
```

## Adim 1: Proje Tespiti

Once mevcut dizini tara:
- Tech stack ne?
- CLAUDE.md var mi?
- Mevcut kod ne durumda?

Yoksa `/project-detect` calistir.

## Adim 2: Shared Klasor Hazirla

```bash
mkdir -p .claude/shared
touch .claude/shared/swarm-questions.md
touch .claude/shared/swarm-answers.md
touch .claude/shared/swarm-review.md
```

Her dosyanin basina header ekle:

```markdown
# Swarm Communication Log
Gorev: <gorev aciklamasi>
Baslangic: <tarih>
```

## Adim 3: Phase 1 - Paralel Kesif

3 agent'i PARALEL calistir (Task tool ile):

### Agent 1: scout
```
Gorevi: Codebase'i tara, mevcut pattern'leri bul, dosya yapisini cikar.
Cikti: .claude/shared/swarm-phase1-scout.md
```

### Agent 2: project-manager (Sofia)
```
Gorevi: Gorevi alt gorevlere parcala, oncelik sir, bagimlilik belirle.
Sprint backlog olustur.
Cikti: .claude/shared/swarm-phase1-pm.md
```

### Agent 3: architect
```
Gorevi: Mimari plan ciz, tech decisions yap, ADR yaz.
Cikti: .claude/shared/swarm-phase1-architect.md
```

Phase 1 tamamlaninca: 3 ciktiyi oku, sentezle, Phase 2'ye gec.

## Adim 4: Phase 2 - Paralel Gelistirme

Phase 1 ciktilarini her agent'a ver, PARALEL calistir:

### Agent 4: backend-dev (Dmitri)
```
Gorevi: API endpoints, database schema, business logic implement et.
Input: Phase 1 sentezi + PM sprint backlog'u
Cikti: .claude/shared/swarm-phase2-backend.md
Sorulari: .claude/shared/swarm-questions.md'ye yaz
```

### Agent 5: frontend-dev (Aria)
```
Gorevi: UI components, pages, state management implement et.
Input: Phase 1 sentezi + Designer ciktisi (varsa)
Cikti: .claude/shared/swarm-phase2-frontend.md
Sorulari: .claude/shared/swarm-questions.md'ye yaz
```

### Agent 6: designer (Marcus)
```
Gorevi: Design system, component specs, color/typography kararlari.
Input: Phase 1 sentezi
Cikti: .claude/shared/swarm-phase2-designer.md
```

### Agent 7: devops (Kai)
```
Gorevi: CI/CD, Docker, deployment config, monitoring.
Input: Phase 1 sentezi
Cikti: .claude/shared/swarm-phase2-devops.md
```

Phase 2 tamamlaninca:
1. Sorulari oku (.claude/shared/swarm-questions.md)
2. Cevaplanmamis sorulari ilgili agent'a yonlendir
3. Cevaplari .claude/shared/swarm-answers.md'ye yaz
4. Catismalari coz

## Adim 5: Phase 3 - Paralel Review

Tum Phase 2 ciktilarini 4 review agent'a ver:

### Agent 8: code-reviewer
```
Gorevi: Kod kalitesi, best practices, maintainability.
Cikti: .claude/shared/swarm-review-code.md
```

### Agent 9: security-analyst (Zara)
```
Gorevi: OWASP top 10, secrets, input validation, auth.
Cikti: .claude/shared/swarm-review-security.md
```

### Agent 10: qa-engineer (Priya)
```
Gorevi: Test stratejisi, edge cases, test plani yaz.
Cikti: .claude/shared/swarm-review-qa.md
```

### Agent 11: data-analyst (Yuna)
```
Gorevi: Analytics events, metrik tanimlama, A/B test plani.
Cikti: .claude/shared/swarm-review-data.md
```

Phase 3 tamamlaninca: Review bulgularini topla, CRITICAL olanlari listele.

## Adim 6: Phase 4 - Duzeltme + Test

Review'dan gelen CRITICAL ve HIGH bulgulari duzelt:

### Agent 12-13: backend-dev + frontend-dev
```
Gorevi: Review fix'lerini implement et.
Input: Phase 3 review bulgulari
```

### Agent 14: tdd-guide
```
Gorevi: QA engineer'in test planina gore testleri yaz.
Input: Phase 3 QA ciktisi + Phase 2 implementasyon
```

### Agent 15: verifier
```
Gorevi: Son quality gate - build, test, lint, security.
Input: Tum Phase 4 ciktilari
Cikti: PASS / FAIL raporu
```

## Adim 7: Phase 5 - Finalizasyon

### Agent 16: self-learner
```
Gorevi: Tum swarm'dan ogrenimleri cikar, CLAUDE.md'ye kaydet.
Input: Tum phase ciktilari + review bulgulari
```

### Agent 17: technical-writer (Noah)
```
Gorevi: README, API docs, changelog guncelle.
Input: Phase 2 implementasyon + Phase 1 mimari
```

### Agent 18: growth (Camille) [opsiyonel]
```
Gorevi: Launch notu, feature announcement, GTM.
Input: Phase 1 + Phase 5 docs
```

## Swarm Raporu

Her swarm sonunda su raporu uret:

```markdown
# SWARM RAPORU
Gorev: <gorev>
Tarih: <tarih>
Sure: <toplam sure>

## Katilimcilar
| Agent | Phase | Durum |
|-------|-------|-------|
| scout | 1 | Tamamlandi |
| ... | ... | ... |

## Iletisim Ozeti
- Toplam soru: X
- Cevaplanan: Y
- Catisma cozulen: Z

## Review Bulgulari
- CRITICAL: X (hepsi cozuldu)
- HIGH: Y (Z tanesi cozuldu)
- MEDIUM: W

## Verifier Sonucu
PASS / FAIL

## Ogrenimler
- <self-learner ciktisi>

## Sonraki Adimlar
- <kalan isler>
```

## Kurallar

1. Her phase bitmeden sonrakine gecme
2. CRITICAL review bulgulari MUTLAKA duzeltilmeli
3. Verifier FAIL verirse Phase 4'e don
4. Agent'lar arasi catismada maestro karar verir
5. Her agent kendi alaninin disina karismasin
6. Paralel calistirilabilecek agent'lari MUTLAKA paralel calistir
