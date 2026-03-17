---
name: ai-video-qa
description: "Validez la qualité de vos vidéos IA avant publication avec une checklist complète couvrant technique, créatif, et positionnement marque. Use when: **Avant publication** - Dernière validation avant mise en ligne; **Revue client** - Préparer les points de feedback anticipés; **Itération qualité** - Identifier les problèmes à corriger; **Go/No-Go decision** - Décider si la vidéo est prête; **Post-mortem** - Analyser pourquoi une vidéo a (ou n'a pas) performé"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# AI Video QA

> Validez la qualité de vos vidéos IA avant publication avec une checklist complète couvrant technique, créatif, et positionnement marque.

## When to Use This Skill

- **Avant publication** - Dernière validation avant mise en ligne
- **Revue client** - Préparer les points de feedback anticipés
- **Itération qualité** - Identifier les problèmes à corriger
- **Go/No-Go decision** - Décider si la vidéo est prête
- **Post-mortem** - Analyser pourquoi une vidéo a (ou n'a pas) performé

## Methodology Foundation

**Source**: PJ Ace best practices + Industry standards + Wistia 2025 State of Video

**Core Principle**: "Une vidéo IA peut être techniquement impressionnante mais échouer commercialement. La QA doit couvrir les trois dimensions: technique, créative, et stratégique."

**Why This Matters**: 41% des pros utilisent l'IA vidéo en 2025, mais beaucoup produisent du "AI slop" qui nuit à leur marque. Une QA rigoureuse fait la différence entre viral et ridicule.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Valide la qualité technique** - Résolution, audio, transitions, artefacts
2. **Évalue l'efficacité créative** - Hook, storytelling, CTA
3. **Vérifie le positionnement marque** - Risque PR, alignement brand
4. **Identifie les red flags IA** - Uncanny valley, mains, incohérences
5. **Génère un rapport actionable** - Issues priorisées avec solutions

## How to Use

### QA complète avant publication
```
J'ai terminé ma vidéo IA de [durée]. Fais une QA complète avec le skill ai-video-qa.
```

### Focus sur un aspect spécifique
```
Vérifie uniquement les aspects techniques / créatifs / brand de ma vidéo.
```

### Préparer une revue client
```
Liste les objections potentielles d'un client pour cette vidéo IA.
```

## Instructions

### Step 1: La Règle des 3 Secondes

```
## Test des 3 Premières Secondes

Regardez la vidéo sur mute. En 3 secondes, l'audience doit pouvoir répondre:

### 1. WHAT IS IT?
**Question:** Le produit ou la marque est-il visible/clair?
[ ] Oui - Immédiatement identifiable
[ ] Partiel - Visible mais pas focal
[ ] Non - Pas clair du tout

**Si Non:** ⚠️ BLOQUANT - Ajouter brand/produit dans le hook

### 2. WHO IS IT FOR?
**Question:** Le public cible est-il évident?
[ ] Oui - Signaux démographiques/psychographiques clairs
[ ] Partiel - Vaguement suggéré
[ ] Non - Audience universelle = personne

**Si Non:** ⚠️ IMPORTANT - Renforcer les signaux d'identification

### 3. WHAT DO I DO?
**Question:** L'action souhaitée est-elle visible?
[ ] Oui - CTA clair dès le début ou anticipé
[ ] Partiel - Suggéré mais pas explicite
[ ] Non - Pas de direction claire

**Si Non:** ⚠️ IMPORTANT - CTA doit être présent ou teasé

### Verdict 3 Secondes
[ ] ✅ PASS - Les 3 questions ont une réponse claire
[ ] ⚠️ NEEDS WORK - 1-2 éléments à renforcer
[ ] ❌ FAIL - Refaire le hook
```

---

### Step 2: Checklist Technique

```
## Validation Technique

### Résolution & Format
- [ ] Résolution correcte (1080p minimum)
- [ ] Aspect ratio approprié (16:9 horizontal, 9:16 vertical)
- [ ] Frame rate stable (24fps cinéma, 30fps digital)
- [ ] Pas de pixelisation visible
- [ ] Export dans le bon codec (H.264/H.265)

### Audio
- [ ] Voix claire et intelligible
- [ ] Niveau audio normalisé (-6dB voix)
- [ ] Pas de clipping ou distorsion
- [ ] Balance voix/musique/SFX correcte
- [ ] Lip-sync acceptable (±2-3 frames max)

### Transitions & Montage
- [ ] Transitions fluides (pas de jump cuts non intentionnels)
- [ ] Continuité de direction de mouvement
- [ ] Éclairage cohérent entre plans
- [ ] Pas de flash frames ou frames noires

### Artefacts IA
- [ ] Pas de morphing de visage visible
- [ ] Pas de membres qui apparaissent/disparaissent
- [ ] Texte lisible (s'il y en a)
- [ ] Arrière-plans stables (pas de "breathing")
- [ ] Pas d'objets flottants ou impossibles

### Durée
- [ ] Durée appropriée pour la plateforme
  - TikTok/Reels: 15-60s
  - YouTube Pre-roll: 6-15s skippable
  - LinkedIn: 30-90s
  - TV/OTT: 15-30s

### Score Technique
____ / 20 points
- 18-20: ✅ Production-ready
- 14-17: ⚠️ Minor fixes needed
- <14: ❌ Significant rework required
```

---

### Step 3: Checklist Créative

```
## Validation Créative

### Hook (0-3 secondes)
- [ ] Capte l'attention immédiatement
- [ ] Pattern interrupt efficace (son, visuel, question)
- [ ] Pas de logo/intro lent (forbidden!)
- [ ] Crée curiosité ou émotion
- [ ] Viewer retention: donnerait-on 5 sec de plus?

### Storytelling
- [ ] Arc narratif clair (début-milieu-fin)
- [ ] Tension/conflit puis résolution
- [ ] Progression logique
- [ ] Payoff satisfaisant
- [ ] Mémorable (passerait le "tell a friend" test)

### Émotion
- [ ] Émotion cible identifiable
- [ ] Cohérence émotionnelle tout au long
- [ ] Pas de dissonance (humour + sérieux mal mixés)
- [ ] Authenticité (pas "AI slop" feeling)

### Message
- [ ] Message principal clair en une phrase
- [ ] Pas de messages contradictoires
- [ ] Bénéfice client évident (pas feature-focused)
- [ ] USP différenciante visible

### CTA
- [ ] Call-to-action explicite
- [ ] Timing approprié (fin, ou teasé + rappelé)
- [ ] Action simple et claire (un seul CTA)
- [ ] Urgence ou raison d'agir maintenant

### Créativité
- [ ] Original (pas un template vu 1000 fois)
- [ ] Approprié au ton de marque
- [ ] Adapté à la culture de la plateforme
- [ ] Shareable potential

### Score Créatif
____ / 24 points
- 20-24: ✅ Excellent creative
- 15-19: ⚠️ Solid but improvable
- <15: ❌ Rethink creative approach
```

---

### Step 4: Red Flags IA Spécifiques

```
## Détection Artefacts IA

### Visages (CRITIQUE)
- [ ] Expressions naturelles (pas de sourire figé)
- [ ] Mouvements de lèvres réalistes
- [ ] Clignements des yeux présents
- [ ] Pas de morphing entre expressions
- [ ] Symétrie faciale raisonnable (pas parfaite)

### Mains & Doigts (HIGH RISK)
- [ ] Nombre de doigts correct (5 par main)
- [ ] Proportions réalistes
- [ ] Pas de fusion entre doigts
- [ ] Mouvements naturels
- [ ] **Si problématique → Recadrer pour éviter**

### Corps & Mouvement
- [ ] Proportions anatomiques correctes
- [ ] Articulations réalistes
- [ ] Pas de membres qui s'étirent
- [ ] Vêtements cohérents (pas de texture morphing)
- [ ] Cheveux naturels (pas de flickering)

### Environnement
- [ ] Perspective cohérente
- [ ] Objets stables (pas de flickering)
- [ ] Ombres correctes et cohérentes
- [ ] Textures stables
- [ ] Pas d'éléments qui apparaissent/disparaissent

### Texte & Logos
- [ ] Texte lisible s'il est généré
- [ ] Logos corrects (pas déformés)
- [ ] **Recommandation: Toujours ajouter en post**

### Score Artefacts IA
____ / 20 points
- 18-20: ✅ Indiscernable de vidéo réelle
- 14-17: ⚠️ AI visible mais acceptable
- 10-13: 🟡 Stylisé/cartoon recommandé
- <10: ❌ Refaire ou changer d'approche
```

---

### Step 5: Évaluation Positionnement Marque

```
## Analyse Risque & Positionnement

### Type de marque
[ ] Challenger brand (peu connue, disruptive)
[ ] Growing brand (en développement)
[ ] Established brand (connue, attentes élevées)
[ ] Heritage/Legacy brand (très connue, sacrée)

### Matrice Risque IA
| Type | Risque PR si "AI visible" | Recommandation |
|------|---------------------------|----------------|
| Challenger | Faible | Oser, innover |
| Growing | Moyen | Qualité++, tests |
| Established | Élevé | Très haute qualité |
| Heritage | Très élevé | Éviter ou hybride |

### Questions critiques
- [ ] L'audience cible est-elle AI-friendly?
- [ ] Le contexte pardonne-t-il les imperfections?
  (Humour oui, Luxe non)
- [ ] Y a-t-il un précédent négatif dans l'industrie?
- [ ] La concurrence utilise-t-elle déjà l'IA vidéo?

### Ton & Authenticité
- [ ] Le ton est cohérent avec la marque
- [ ] Pas de claim impossible/trompeur
- [ ] Transparence sur l'usage IA si nécessaire
- [ ] Pas d'appropriation culturelle involontaire

### Score Brand Risk
[ ] ✅ LOW RISK - Feu vert
[ ] 🟡 MEDIUM RISK - Validation stakeholder recommandée
[ ] 🔴 HIGH RISK - Reconsidérer ou modifier

### Si HIGH RISK, options:
1. Améliorer qualité jusqu'à "indiscernable"
2. Assumer le côté IA (style, ton humoristique)
3. Hybrider avec footage réel
4. Abandonner l'approche IA
```

---

### Step 6: Générer le Rapport QA

```
## QA Report Template

# Rapport QA Vidéo: [Titre]

**Date:** ________________
**Version:** _______________
**Reviewers:** _______________

---

## Résumé Exécutif

| Dimension | Score | Status |
|-----------|-------|--------|
| 3 Secondes Rule | [X/3] | [PASS/FAIL] |
| Technique | [X/20] | [✅/⚠️/❌] |
| Créatif | [X/24] | [✅/⚠️/❌] |
| Artefacts IA | [X/20] | [✅/⚠️/❌] |
| Brand Risk | [Level] | [🟢/🟡/🔴] |

**VERDICT GLOBAL:** [ ] APPROVED [ ] NEEDS REVISION [ ] REJECTED

---

## Issues Identifiées

### Bloquants (P0)
| # | Issue | Timing | Solution |
|---|-------|--------|----------|
| 1 | [Description] | [0:XX] | [Action] |

### Importants (P1)
| # | Issue | Timing | Solution |
|---|-------|--------|----------|
| 1 | [Description] | [0:XX] | [Action] |

### Nice-to-have (P2)
| # | Issue | Timing | Solution |
|---|-------|--------|----------|
| 1 | [Description] | [0:XX] | [Action] |

---

## Recommandations

1. [Recommandation prioritaire]
2. [Recommandation secondaire]
3. [Amélioration optionnelle]

---

## Sign-off

[ ] P0 résolus → Prêt pour publication
[ ] P0 + P1 résolus → Qualité optimale
[ ] Stakeholder approval si risque medium/high
```

## Examples

### Example 1: QA d'une pub SaaS

**Context**: Vidéo 30s pour app de productivité, style décalé

**Input**:
> J'ai une vidéo de 30 secondes pour TaskFlow. Style Office/mockumentaire. Fais la QA.

**Output**:

## QA Report: TaskFlow "Meeting Chaos"

**Date:** 2026-01-25
**Version:** v1.0
**Durée:** 30 secondes

---

### Test 3 Secondes

| Question | Réponse | Status |
|----------|---------|--------|
| What is it? | App visible à 0:18 seulement | ⚠️ |
| Who is it for? | Équipes tech, évident | ✅ |
| What do I do? | CTA à 0:28 "Essai gratuit" | ✅ |

**Verdict:** ⚠️ NEEDS WORK - Ajouter mention TaskFlow dans hook

---

### Scores

| Dimension | Score | Details |
|-----------|-------|---------|
| Technique | 17/20 | -2 audio balance, -1 transition @0:12 |
| Créatif | 21/24 | Hook fort, payoff satisfaisant |
| Artefacts IA | 15/20 | Mains visibles @0:08 problématiques |
| Brand Risk | 🟢 LOW | Challenger brand, ton assumé |

---

### Issues P0 (Bloquants)

| # | Issue | Timing | Solution |
|---|-------|--------|----------|
| 1 | Mains avec 6 doigts | 0:08 | Recadrer en medium shot |
| 2 | App non visible dans hook | 0:00-0:08 | Ajouter écran TaskFlow en overlay |

### Issues P1 (Importants)

| # | Issue | Timing | Solution |
|---|-------|--------|----------|
| 1 | Voix sous musique | 0:14-0:20 | Baisser musique -6dB |
| 2 | Jump cut visible | 0:12 | Ajouter plan intermédiaire |

### Issues P2 (Nice-to-have)

| # | Issue | Timing | Solution |
|---|-------|--------|----------|
| 1 | Logo petit dans CTA | 0:28 | Agrandir 20% |

---

### Verdict

**NEEDS REVISION** - 2 issues P0 à résoudre

Après corrections P0:
- [ ] Re-render scène 0:08 (cadrage)
- [ ] Ajouter overlay TaskFlow dans hook
- [ ] Re-QA puis APPROVED

---

### Example 2: QA pub premium avec high risk

**Context**: Vidéo pour marque de luxe établie

**Input**:
> QA pour une pub de montres Heritage Collection, marque premium établie depuis 130 ans.

**Output**:

## QA Report: Heritage Collection "Timeless"

**Date:** 2026-01-25
**Version:** v2.3
**Durée:** 45 secondes

---

### ⚠️ ALERT: HIGH BRAND RISK

**Type de marque:** Heritage/Legacy (130 ans)
**Risque PR si AI détectée:** TRÈS ÉLEVÉ

**Précédent industrie:** Coca-Cola Christmas AI ad backlash 2024

---

### Test 3 Secondes

| Question | Réponse | Status |
|----------|---------|--------|
| What is it? | Montre visible, marque à 0:02 | ✅ |
| Who is it for? | Executives/collectionneurs | ✅ |
| What do I do? | Implicite (aspiration) | ⚠️ Acceptable pour luxe |

---

### Scores

| Dimension | Score | Details |
|-----------|-------|---------|
| Technique | 19/20 | Quasi parfait |
| Créatif | 23/24 | Excellent storytelling |
| Artefacts IA | 16/20 | Quelques tells subtils |
| Brand Risk | 🔴 HIGH | Legacy brand + artefacts détectables |

---

### Analyse Artefacts Critique

| Timing | Issue | Détectable par public? | Risque |
|--------|-------|------------------------|--------|
| 0:12 | Reflet montre légèrement instable | Oui si freeze-frame | Medium |
| 0:23 | Texture costume "breathing" | Oui, subtil | Medium |
| 0:34 | Transition visage légèrement AI | Oui | HIGH |

**Verdict artefacts:** Un œil entraîné détecte l'IA. Pour une marque heritage, c'est risqué.

---

### Options Recommandées

**Option A: Améliorer (Recommandé)**
- Re-générer scènes 0:12, 0:23, 0:34 avec paramètres plus stricts
- Utiliser Veo 3.1 Standard (qualité max)
- Viser score artefacts 19+/20

**Option B: Hybrider**
- Tourner les plans critiques (visage, mains) en réel
- Garder les plans d'ambiance en IA
- Coût additionnel mais risque réduit à LOW

**Option C: Assumer (Non recommandé)**
- Mentionner "Created with AI" dans credits
- Risque: "Une marque de 130 ans utilise de l'IA cheap"

---

### Verdict

**REJECTED** - Risque PR trop élevé en l'état

**Path to approval:**
1. Re-travailler les 3 scènes problématiques
2. Atteindre score artefacts 19+/20
3. Test blind auprès de 5 personnes non-averties
4. Si 0/5 détecte l'IA → APPROVED
5. Sinon → Option B (hybride)

---

## Checklists & Templates

### Checklist QA Express (2 min)

```
## Quick QA

### Non-négociables
- [ ] 3 Secondes Rule passé
- [ ] Pas de mains/doigts déformés visibles
- [ ] Audio compréhensible
- [ ] CTA présent et clair

### Si TOUT coché → Publication OK pour test
### Si UN non coché → QA complète requise
```

---

### Template Rapport Client

```
## Rapport QA - [Projet]

### Résumé
✅ Vidéo approuvée / ⚠️ Révisions mineures / ❌ Révisions majeures

### Points forts
- [Point 1]
- [Point 2]
- [Point 3]

### Points d'amélioration
| Priorité | Issue | Recommendation |
|----------|-------|----------------|
| Haute | [...] | [...] |
| Medium | [...] | [...] |

### Prochaines étapes
1. [Action 1]
2. [Action 2]

### Timeline estimée pour corrections
[X] jours si révisions mineures
[Y] jours si révisions majeures
```

---

### Scoring Guide

```
## Interprétation des Scores

### Score Global (sur 87 points max)
- 75-87: ✅ APPROVED - Publication immédiate
- 60-74: ⚠️ CONDITIONAL - Fixes mineurs, re-QA rapide
- 45-59: 🟡 NEEDS WORK - Révisions substantielles
- <45: ❌ REJECTED - Refaire ou abandonner approche

### Score Technique (sur 20)
18+: Broadcast quality
14-17: Digital/social quality
10-13: Acceptable pour test
<10: Problèmes techniques majeurs

### Score Créatif (sur 24)
20+: Award-worthy creative
15-19: Solid professional work
10-14: Functional but forgettable
<10: Creative rethink needed

### Score Artefacts (sur 20)
18+: Indiscernable de réel
14-17: AI visible mais acceptable
10-13: Stylisé/assumé recommandé
<10: Uncanny valley territory
```

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

- Wistia. "2025 State of Video Report" - AI video adoption statistics
- PJ Ace. "AI Video Production Workflow" - Quality standards
- [MKTG Skills - Étude Écosystème Vidéo IA](../../docs/etude-ecosysteme-video-ia.md)
- Nielsen Norman Group. "Video UX Guidelines"

## Related Skills

- [ai-video-concept](../ai-video-concept/) - Référence pour évaluer l'alignement concept
- [ai-storyboard-2x2](../ai-storyboard-2x2/) - Vérifier cohérence avec storyboard
- [ai-video-prompting](../ai-video-prompting/) - Pour améliorer les scènes problématiques
- [ai-voice-design](../ai-voice-design/) - Pour les issues audio

---

## Skill Metadata


- **Mode**: cyborg
```yaml
name: ai-video-qa
category: video
subcategory: post-production
version: 1.0
author: MKTG Skills
source_expert: PJ Ace + Wistia + Industry Standards
source_work: AI Video Best Practices
difficulty: intermediate
estimated_value: $500-1500 (professional QA review)
tags: [video, ai, qa, quality, review, checklist, production]
created: 2026-01-25
updated: 2026-01-25
```
