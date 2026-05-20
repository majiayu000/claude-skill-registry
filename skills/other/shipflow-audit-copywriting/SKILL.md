---
name: shipflow-audit-copywriting
description: Audit copywriting & marketing — analyse le parcours client depuis le persona jusqu'à la conversion. Évalue la stratégie de persuasion, pas la qualité rédactionnelle.
argument-hint: [file-path | "global"] (omit for full project)
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -100 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- All pages: !`find src/pages src/app -name "*.astro" -o -name "*.tsx" -o -name "*.vue" 2>/dev/null | grep -v node_modules | sort`
- Content collections: !`find src/content -type f 2>/dev/null | head -20 || echo "no content dir"`
- Pricing/checkout pages: !`find src -path "*pric*" -o -path "*checkout*" -o -path "*offre*" -o -path "*tarif*" 2>/dev/null | head -10 || echo "none found"`

## Distinction avec shipflow-audit-copy

| | audit-copy (rédactionnel) | audit-copywriting (ce skill) |
|---|---|---|
| Question | "Est-ce bien écrit ?" | "Est-ce que ça vend ?" |
| Focus | Voix, ton, grammaire, clarté | Persona, parcours, objections, conversion |
| Point de départ | Le texte | Le client cible |
| Mesure | Qualité linguistique | Efficacité persuasive |

Ne PAS refaire le travail de audit-copy. Ce skill suppose que le texte est correct. Il évalue la **stratégie**.

## Mode detection

- **`$ARGUMENTS` is "global"** → GLOBAL MODE: audit tous les projets.
- **`$ARGUMENTS` is a file path** → PAGE MODE: audit une page.
- **`$ARGUMENTS` is empty** → PROJECT MODE: audit complet du projet.

---

## PAGE MODE

### Step 1: Comprendre la page dans le parcours

1. Lire la page cible.
2. Lire les pages qui **pointent vers** cette page (navigation, CTAs entrants).
3. Lire les pages vers lesquelles cette page **envoie** (CTAs sortants, liens).
4. Identifier le rôle dans le funnel : **Découverte** (TOFU) / **Considération** (MOFU) / **Décision** (BOFU) / **Rétention**.

### Step 2: Audit copywriting

Score chaque catégorie **A/B/C/D**. Standard : copywriter senior spécialisé conversion.

#### 1. Alignement Persona
- [ ] Le persona cible est identifiable dès les 3 premières phrases
- [ ] Le vocabulaire est celui du persona (pas le jargon interne du produit)
- [ ] Le problème adressé est un vrai pain point du persona (pas une feature déguisée)
- [ ] Le niveau d'awareness est adapté : Unaware → Problem-aware → Solution-aware → Product-aware → Most aware (Schwartz)
- [ ] Le "tu" / "vous" est cohérent avec la relation souhaitée

#### 2. Proposition de valeur
- [ ] Le bénéfice principal est exprimé en termes de résultat pour le client, pas en features
- [ ] La promesse est crédible (ni exagérée, ni timorée)
- [ ] Le différenciateur vs alternatives est clair (pourquoi ici et pas ailleurs ?)
- [ ] La transformation promise (avant → après) est concrète
- [ ] La preuve de la promesse est présente (data, témoignage, mécanisme expliqué)

#### 3. Structure de persuasion
- [ ] Le hook (titre + sous-titre) crée une tension ou une curiosité
- [ ] Le body suit un framework de persuasion reconnaissable (PAS, AIDA, BAB, 4P, StoryBrand)
- [ ] Chaque section a un rôle clair dans la séquence de persuasion
- [ ] La montée en engagement est progressive (pas de "achète" dès le premier scroll)
- [ ] La longueur est adaptée au niveau d'awareness (plus unaware = plus long)

#### 4. Traitement des objections
- [ ] Les 3-5 objections principales du persona sont adressées
- [ ] Les objections sont traitées AVANT le CTA principal (pas après)
- [ ] Le traitement est empathique ("on comprend que...") pas défensif ("mais non...")
- [ ] La preuve sociale répond aux objections spécifiques (pas juste "5000 clients")
- [ ] La réversibilité du risque est explicite (garantie, essai gratuit, pas d'engagement)

#### 5. Parcours émotionnel
- [ ] L'émotion dominante est identifiable et cohérente avec le persona
- [ ] La séquence émotionnelle est : douleur → espoir → confiance → action
- [ ] L'empathie précède la solution (le persona se sent compris AVANT d'entendre la solution)
- [ ] Les témoignages sont de personnes dans lesquelles le persona se reconnaît
- [ ] Le ton ne culpabilise pas, ne fait pas peur inutilement, ne manipule pas

#### 6. Appels à l'action (stratégie, pas rédaction)
- [ ] Le CTA principal est aligné avec le niveau d'awareness de la page
- [ ] Le CTA propose la bonne prochaine étape (pas un saut trop grand)
- [ ] Il y a un CTA alternatif plus léger pour les indécis
- [ ] La friction perçue autour du CTA est minimisée (pas de formulaire monstre)
- [ ] Le CTA est positionné après la preuve, pas avant

#### 7. Cohérence du parcours
- [ ] La promesse faite en amont (SEO, pub, nav) est tenue sur la page
- [ ] La transition vers la page suivante est fluide (pas de rupture de ton ou de promesse)
- [ ] Le message se renforce au fil du parcours (pas de contradiction entre pages)
- [ ] Les micro-engagements sont valorisés (newsletter, quiz, téléchargement)

### Step 3: Recommandations

Pour chaque catégorie notée B ou moins :
1. Diagnostic précis du problème
2. Recommandation stratégique (pas une réécriture — c'est le job de audit-copy)
3. Exemple de direction à prendre
4. Impact estimé sur la conversion : 🔴 fort / 🟠 moyen / 🟡 faible

### Step 4: Report

```
AUDIT COPYWRITING: [page]
─────────────────────────────────────
Persona cible identifié : [persona]
Position funnel : [TOFU/MOFU/BOFU/Rétention]
Niveau awareness : [Schwartz level]
─────────────────────────────────────
Alignement Persona     [A/B/C/D]
Proposition de valeur  [A/B/C/D]
Structure persuasion   [A/B/C/D]
Objections             [A/B/C/D]
Parcours émotionnel    [A/B/C/D]
Appels à l'action      [A/B/C/D]
Cohérence parcours     [A/B/C/D]
─────────────────────────────────────
OVERALL                [A/B/C/D]

Recommandations stratégiques : X
Impact conversion estimé : [fort/moyen/faible]
```

---

## PROJECT MODE

### Workspace root detection

Si le répertoire courant n'a pas de marqueurs projet mais contient des sous-répertoires — on est au **workspace root**.

Utiliser **AskUserQuestion** :
- Question : "Quel(s) projet(s) auditer en copywriting ?"
- `multiSelect: true`
- Options depuis `/home/claude/shipflow_data/PROJECTS.md`

Puis passer en **GLOBAL MODE**.

### Phase 1 : Définir le Persona

Avant toute analyse, extraire ou construire le persona depuis le projet :

1. Chercher des docs existants : `docs/copywriting/persona.md`, ou `persona*`, `avatar*`, `icp*`, `target*`
2. Si un persona existe déjà, le présenter à l'utilisateur pour validation — ne pas repartir de zéro
3. Sinon, analyser CLAUDE.md et la homepage pour déduire le persona
4. Documenter :
   - **Qui** : démographie, situation, identité
   - **Douleur** : le problème #1 qui l'amène ici
   - **Désir** : ce qu'il veut vraiment (pas le produit — le résultat)
   - **Objections** : ses 3-5 raisons de ne pas agir
   - **Déclencheur** : qu'est-ce qui l'amène aujourd'hui (pas hier, pas demain)
   - **Alternatives** : que fait-il s'il ne choisit pas ce produit ?

Utiliser **AskUserQuestion** pour valider le persona avec l'utilisateur avant de continuer.

### Phase 2 : Cartographier le parcours client

Mapper TOUTES les pages du site sur le parcours client :

```
DÉCOUVERTE (TOFU)         CONSIDÉRATION (MOFU)      DÉCISION (BOFU)         RÉTENTION
─────────────────         ────────────────────      ─────────────           ─────────
[pages SEO/blog]    →     [pages features]     →   [pricing/offre]    →   [dashboard]
[landing pages]     →     [témoignages]        →   [checkout]         →   [emails]
[homepage]          →     [comparatifs]        →   [inscription]      →   [communauté]
```

Identifier :
- **Trous dans le funnel** : étapes sans page dédiée
- **Culs-de-sac** : pages sans CTA vers l'étape suivante
- **Sauts** : pages qui passent de TOFU à BOFU sans MOFU
- **Pages orphelines** : du contenu sans lien dans le parcours

### Phase 3 : Analyse par étape du funnel

Pour chaque étape du parcours, évaluer les pages regroupées :

**TOFU — Découverte** :
- Le contenu attire les bonnes personnes ? (pas juste du trafic)
- Le pain point est-il validé dès l'arrivée ?
- Y a-t-il un hook vers l'étape suivante ?

**MOFU — Considération** :
- La solution est-elle présentée comme LA réponse au pain point ?
- La preuve sociale est-elle adaptée au persona ?
- Les objections sont-elles traitées ici ?

**BOFU — Décision** :
- Le pricing est-il framé en valeur (pas en coût) ?
- La friction du checkout est-elle minimale ?
- L'urgence est-elle authentique (pas des fake timers) ?

**Rétention** :
- Le onboarding tient-il la promesse marketing ?
- Le persona retrouve-t-il le vocabulaire qu'il a vu avant l'inscription ?

### Phase 4 : Stratégie de conversion globale

Évaluer la stratégie d'ensemble :

1. **Cohérence promesse ↔ produit** : le marketing promet-il ce que le produit délivre ?
2. **Positionnement** : le produit est-il clairement différencié ? De quoi ?
3. **Pricing psychology** : ancrage, decoy, framing — utilisés correctement ?
4. **Trust signals** : suffisants à chaque point de friction ?
5. **Content-market fit** : le contenu attire-t-il le persona ou des curieux sans intention ?

### Phase 5 : Recommandations prioritisées

Produire un plan d'action par impact sur la conversion :

| Pri | Recommandation | Pages impactées | Impact estimé |
|-----|---------------|-----------------|---------------|
| 🔴 | [action stratégique] | [pages] | Fort — [raison] |
| 🟠 | [action] | [pages] | Moyen — [raison] |
| 🟡 | [action] | [pages] | Faible — [raison] |

Règle : les recommandations sont **stratégiques** (quoi changer et pourquoi), pas **rédactionnelles** (comment réécrire). La réécriture est le job de l'utilisateur ou de audit-copy.

### Phase 6 : Report

```
AUDIT COPYWRITING: [project name]
═══════════════════════════════════════

PERSONA
  Qui : [description courte]
  Douleur : [pain point #1]
  Désir : [résultat souhaité]
  Objections : [top 3]

PARCOURS CLIENT
  Découverte   [X pages]  [A/B/C/D]
  Considération [X pages]  [A/B/C/D]
  Décision     [X pages]  [A/B/C/D]
  Rétention    [X pages]  [A/B/C/D]

  Trous funnel : [X]
  Culs-de-sac : [X]
  Pages orphelines : [X]

STRATÉGIE DE CONVERSION
  Cohérence promesse/produit  [A/B/C/D]
  Positionnement              [A/B/C/D]
  Pricing psychology          [A/B/C/D]
  Trust signals               [A/B/C/D]
  Content-market fit          [A/B/C/D]

═══════════════════════════════════════
OVERALL                       [A/B/C/D]

Recommandations : X (🔴 Y critical, 🟠 Z high, 🟡 W medium)
Top 3 quick wins conversion :
  1. [action] → [impact]
  2. [action] → [impact]
  3. [action] → [impact]
```

### Phase 7 : Persister les livrables

Sauvegarder les analyses dans `docs/copywriting/` à la racine du projet. Ces fichiers servent de **référence partagée** pour les autres skills (audit-copy, audit-seo, enrich, market-study, etc.).

Créer le dossier si absent : `mkdir -p docs/copywriting`

#### `docs/copywriting/persona.md`

```markdown
# Persona — [Nom du persona]

> Dernière mise à jour : [date]
> Généré par : /shipflow-audit-copywriting

## Identité
- **Qui** : [démographie, situation, identité]
- **Contexte** : [ce qui se passe dans sa vie]

## Psychologie
- **Douleur #1** : [le problème qui l'amène]
- **Désir profond** : [ce qu'il veut vraiment — pas le produit]
- **Déclencheur** : [pourquoi aujourd'hui et pas hier]

## Objections
1. [objection principale]
2. [objection #2]
3. [objection #3]
4. [objection #4 si pertinent]
5. [objection #5 si pertinent]

## Alternatives
- [ce qu'il fait s'il ne choisit pas ce produit]

## Niveau d'awareness (Schwartz)
- **Entrée typique** : [Unaware / Problem-aware / Solution-aware / Product-aware]
- **Cible sortie** : [Most aware → conversion]

## Vocabulaire du persona
- [mots et expressions qu'il utilise pour parler de son problème]
- [termes à utiliser dans le copy — pas notre jargon]
```

#### `docs/copywriting/parcours-client.md`

```markdown
# Parcours Client — [Projet]

> Dernière mise à jour : [date]

## Funnel

| Étape | Pages | Score | Diagnostic |
|-------|-------|-------|------------|
| Découverte (TOFU) | [liste pages] | [A/B/C/D] | [résumé] |
| Considération (MOFU) | [liste pages] | [A/B/C/D] | [résumé] |
| Décision (BOFU) | [liste pages] | [A/B/C/D] | [résumé] |
| Rétention | [liste pages] | [A/B/C/D] | [résumé] |

## Problèmes de parcours
- **Trous** : [étapes sans page]
- **Culs-de-sac** : [pages sans CTA sortant]
- **Sauts** : [TOFU → BOFU sans MOFU]
- **Orphelines** : [pages hors parcours]

## Flux de conversion principal
[page entrée] → [page 2] → [page 3] → [conversion]
```

#### `docs/copywriting/strategie.md`

```markdown
# Stratégie Copywriting — [Projet]

> Dernière mise à jour : [date]

## Positionnement
- **Promesse principale** : [en une phrase]
- **Différenciateur** : [pourquoi ici et pas ailleurs]
- **Transformation** : [avant → après]

## Scores

| Dimension | Score | Diagnostic |
|-----------|-------|------------|
| Cohérence promesse/produit | [A/B/C/D] | [résumé] |
| Positionnement | [A/B/C/D] | [résumé] |
| Pricing psychology | [A/B/C/D] | [résumé] |
| Trust signals | [A/B/C/D] | [résumé] |
| Content-market fit | [A/B/C/D] | [résumé] |

## Recommandations prioritisées

| Pri | Action | Pages | Impact |
|-----|--------|-------|--------|
| 🔴 | [action] | [pages] | [impact] |
| 🟠 | [action] | [pages] | [impact] |
| 🟡 | [action] | [pages] | [impact] |

## Quick wins
1. [action] → [impact attendu]
2. [action] → [impact attendu]
3. [action] → [impact attendu]
```

**Règles de persistance :**
- Si les fichiers existent déjà, les **mettre à jour** (pas les écraser complètement — garder l'historique avec la date)
- Les autres skills doivent lire ces fichiers quand ils existent : `docs/copywriting/persona.md` est la source de vérité persona pour tout le projet
- Ne pas dupliquer le contenu du report dans ces fichiers — le report va dans AUDIT_LOG.md, les fichiers sont la **référence vivante**

---

## GLOBAL MODE

1. Lire `/home/claude/shipflow_data/PROJECTS.md`. Identifier les projets avec site web.

2. **AskUserQuestion** : "Quels projets auditer en copywriting ?" — `multiSelect: true`.

3. Lancer un agent par projet sélectionné (en parallèle). Chaque agent exécute le PROJECT MODE complet.

4. Compiler un rapport cross-projet :
   ```
   GLOBAL COPYWRITING AUDIT — [date]
   ═══════════════════════════════════════
   PROJECT SCORES
     [project]  [A/B/C/D] — [persona] — [top issue]
     ...
   CROSS-PROJECT PATTERNS
     [Patterns communs entre projets]
   TOP 5 ACTIONS CONVERSION
     1. 🔴 [project] — [action] → [impact]
     ...
   ═══════════════════════════════════════
   ```

5. Mettre à jour AUDIT_LOG.md et TASKS.md.

---

## Tracking (all modes)

### Log the audit

Append à :
1. **Global `/home/claude/shipflow_data/AUDIT_LOG.md`** : remplir la colonne Copywriting.
2. **Local `./AUDIT_LOG.md`** : idem sans la colonne Project.

### Update TASKS.md

1. **Local TASKS.md** : ajouter `### Audit: Copywriting` avec les recommandations comme tâches.
2. **Master `/home/claude/shipflow_data/TASKS.md`** : même chose dans la section du projet.

---

## Important (all modes)

- **Partir du persona, pas du produit.** Toujours. Le persona d'abord, le produit ensuite.
- **Jamais de manipulation.** Urgence fausse, fake social proof, dark patterns = note F automatique.
- **Population vulnérable = éthique renforcée.** Si le produit s'adresse à des personnes en souffrance (santé, addiction, deuil), le copywriting doit être empathique et honnête. Jamais de peur, jamais de culpabilité, jamais de promesses irréalistes.
- Les recommandations sont stratégiques, pas rédactionnelles. Dire "il faut traiter l'objection prix avant le CTA", pas "réécrivez ce paragraphe comme ça".
- Détecter la langue automatiquement. Auditer dans cette langue.
- **Accents français obligatoires.** Lors de toute création ou modification de contenu en français, vérifier systématiquement que TOUS les accents sont présents et corrects (é, è, ê, à, â, ù, û, ô, î, ï, ç, œ, æ). Les accents manquants sont une faute d'orthographe.
