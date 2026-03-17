---
name: figma-to-code
description: Génère du code à partir d'une sélection Figma en utilisant les composants existants et Code Connect. Utiliser quand l'utilisateur fournit une URL Figma, dit "convertir ce design", "figma to code", "générer depuis figma", ou veut transformer un design en code.
model: opus
context: fork
agent: Plan
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - WebFetch
argument-hint: <figma-url>
user-invocable: true
knowledge:
  core:
    - figma/mcp-tools-reference.md
    - figma/tokens-mapping.md
  advanced:
    - figma/code-connect-guide.md
---

# Figma to Code

## 📥 Contexte à charger

**Au démarrage, vérifier l'environnement Figma et les composants existants.**

| Contexte | Pattern/Action | Priorité |
|----------|----------------|----------|
| Code Connect | `Read: figma.config.json` | Recommandé |
| Composants existants | `Glob: src/components/ui/*.{tsx,jsx,vue}` | Requis |
| Mappings Figma | `Glob: src/components/**/*.figma.tsx` | Optionnel |
| Framework | `Grep: package.json` pour react/vue/angular/next | Requis |
| Design tokens | `Read: src/styles/tokens.css` ou `docs/planning/ui/tokens.css` | Optionnel |

### Instructions de chargement
1. Vérifier si Code Connect est configuré (figma.config.json)
2. Scanner les composants UI existants pour réutilisation
3. Identifier les mappings .figma.tsx existants
4. Détecter le framework pour générer le bon code

---

## Activation

> **Au démarrage :**
> 1. Parser l'URL Figma fournie
> 2. Vérifier si Code Connect est configuré
> 3. Détecter le framework du projet
> 4. Identifier les composants mappés disponibles

## Rôle & Principes

**Rôle** : Transformer un design Figma en code fonctionnel en utilisant les composants existants du projet. Privilégier la réutilisation plutôt que la création de nouveaux composants.

**Principes** :
- **Réutilisation first** - Utiliser les composants mappés existants
- **Tokens first** - Utiliser les design tokens du projet
- **Clean code** - Générer du code lisible et maintenable
- **Framework-aware** - Respecter les conventions du framework détecté

**Règles** :
- ⛔ Ne JAMAIS créer de nouveaux composants de base (Button, Input, etc.)
- ⛔ Ne JAMAIS hardcoder des valeurs de style (utiliser les tokens)
- ⛔ Ne JAMAIS ignorer les composants mappés existants
- ✅ Toujours vérifier les mappings avant de générer
- ✅ Toujours utiliser les tokens CSS existants
- ✅ Toujours proposer de créer les mappings manquants

---

## Process

### 1. Parsing de l'URL Figma

```markdown
🔗 **Analyse URL Figma**

**URL** : [URL fournie]

**Extraction** :
| Élément | Valeur |
|---------|--------|
| File Key | [file_key] |
| Node ID | [node_id ou "page entière"] |
| File Name | [nom si disponible] |

**Type de sélection** :
- [ ] Composant unique
- [ ] Frame / Screen
- [ ] Page complète

Je récupère les informations du design ?
```

**⏸️ STOP** - Validation avant appel API

---

### 2. Vérification des mappings existants

```markdown
🔍 **Mappings Code Connect**

**Composants mappés disponibles** :
| Composant Figma | Composant Code | Mapping |
|-----------------|----------------|---------|
| Button | `<Button>` | ✅ |
| Input | `<Input>` | ✅ |
| Card | `<Card>` | ✅ |
| [Autre] | - | ❌ |

**Composants dans le design** :
[Liste des composants détectés dans la sélection Figma]

**Match** : [X/Y] composants ont un mapping existant

[Si mappings manquants]
⚠️ [N] composants sans mapping. Options :
- [C] Continuer avec composants génériques
- [M] Créer les mappings d'abord (`/figma-setup`)
```

**⏸️ STOP** - Décision sur les mappings manquants

---

### 3. Extraction du design

Utiliser les outils MCP Figma :

```markdown
📐 **Design extrait**

**Structure** :
```
[Frame Name]
├── Header
│   ├── Logo (Image)
│   └── Navigation (→ mapped: NavBar)
├── Hero Section
│   ├── Title (Text)
│   ├── Description (Text)
│   └── CTA (→ mapped: Button)
└── Content
    └── Cards Grid
        ├── Card 1 (→ mapped: Card)
        ├── Card 2 (→ mapped: Card)
        └── Card 3 (→ mapped: Card)
```

**Tokens utilisés** :
| Token Figma | Token CSS local |
|-------------|-----------------|
| Primary/500 | --color-primary-500 |
| Spacing/lg | --space-lg |
| Radius/md | --radius-md |

**Dimensions** : [W] × [H]

Je génère le code ?
```

**⏸️ STOP** - Validation structure avant génération

---

### 4. Génération du code

```markdown
💻 **Code généré**

**Fichier** : `src/components/[name].tsx`

```tsx
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

interface [ComponentName]Props {
  // Props extraites du design
}

export function [ComponentName]({ ...props }: [ComponentName]Props) {
  return (
    <div className="[styles utilisant tokens]">
      {/* Structure générée depuis Figma */}
    </div>
  );
}
```

**Composants utilisés** :
- `Button` (mapped) ✅
- `Card` (mapped) ✅
- `Input` (mapped) ✅

**Tokens utilisés** :
- `--color-primary-500`
- `--space-lg`
- `--radius-md`

Ce code te convient ?
```

**⏸️ STOP** - Validation code généré

---

### 5. Proposition de mappings manquants

Si des composants Figma n'ont pas de mapping :

```markdown
🔗 **Mappings manquants**

Ces composants Figma n'ont pas de mapping Code Connect :

| Composant Figma | Composant code suggéré | Action |
|-----------------|------------------------|--------|
| [FigmaComponent] | `src/components/ui/[name].tsx` | Créer mapping |
| [Autre] | `src/components/ui/[name].tsx` | Créer mapping |

**Créer les mappings maintenant ?**
- [Y] Oui, créer les fichiers .figma.tsx
- [N] Non, utiliser les composants génériques
- [S] Setup complet (`/figma-setup`)
```

**⏸️ STOP** - Décision mappings

Si oui, créer les fichiers .figma.tsx :

```tsx
// src/components/ui/[name].figma.tsx
import figma from "@figma/code-connect";
import { ComponentName } from "./[name]";

figma.connect(ComponentName, "[FIGMA_URL_NODE]", {
  props: {
    // Props détectées
  },
  example: (props) => <ComponentName {...props} />,
});
```

---

### 6. Écriture du fichier

```markdown
📝 **Fichier créé**

**Path** : `src/components/[path]/[name].tsx`

**Contenu** : [résumé du composant]

**Imports** :
- [X] composants UI mappés
- [Y] tokens CSS
- [Z] types

Le fichier a été créé. Vérifications :
- [ ] Pas d'erreurs TypeScript
- [ ] Imports corrects
- [ ] Tokens utilisés (pas de hardcode)
```

Écrire le fichier avec Write.

---

### 7. Validation & Résumé

```markdown
## ✅ Code généré depuis Figma

**Source** : [URL Figma]
**Fichier créé** : `src/components/[name].tsx`

**Résumé** :
| Métrique | Valeur |
|----------|--------|
| Composants mappés utilisés | [N] |
| Tokens CSS utilisés | [N] |
| Lignes de code | [N] |
| Props typées | [N] |

**Composants réutilisés** :
- `Button` ✅
- `Card` ✅
- `Input` ✅

**Nouveaux mappings créés** : [N] (si applicable)

---

**Prochaine étape ?**
- [A] Générer un autre composant (`/figma-to-code [url]`)
- [T] Écrire les tests (`/test-runner`)
- [R] Review le code (`/code-reviewer`)
```

**⏸️ STOP** - Fin de génération

---

## Détection du framework

### React / Next.js

```tsx
// Imports
import { ComponentName } from "@/components/ui/component";

// Styles
className="flex gap-4 p-6"  // Tailwind si détecté
className={styles.container} // CSS Modules si détecté

// Props
interface Props {
  title: string;
  onClick?: () => void;
}
```

### Vue

```vue
<template>
  <div class="container">
    <ComponentName :prop="value" />
  </div>
</template>

<script setup lang="ts">
import ComponentName from '@/components/ui/ComponentName.vue';

defineProps<{
  title: string;
}>();
</script>
```

### HTML / Web Components

```html
<div class="container">
  <custom-button variant="primary">Click me</custom-button>
</div>

<style>
.container {
  display: flex;
  gap: var(--space-md);
}
</style>
```

---

## Mapping des styles Figma → Code

### Couleurs

| Figma | Tailwind | CSS Variable |
|-------|----------|--------------|
| `Primary/500` | `bg-primary-500` | `var(--color-primary-500)` |
| `Neutral/100` | `bg-gray-100` | `var(--color-neutral-100)` |

### Spacing

| Figma | Tailwind | CSS Variable |
|-------|----------|--------------|
| `8` | `p-2` | `var(--space-sm)` |
| `16` | `p-4` | `var(--space-md)` |
| `24` | `p-6` | `var(--space-lg)` |

### Typography

| Figma | Tailwind | CSS Variable |
|-------|----------|--------------|
| `Heading/H1` | `text-3xl font-bold` | `var(--font-heading-1)` |
| `Body/Regular` | `text-base` | `var(--font-body)` |

---

## Output Validation

Avant de terminer, valider :

```markdown
### ✅ Checklist Output Figma to Code

| Critère | Status |
|---------|--------|
| URL Figma parsée correctement | ✅/❌ |
| Design extrait | ✅/❌ |
| Composants mappés utilisés | ✅/❌ |
| Tokens CSS utilisés (pas hardcode) | ✅/❌ |
| Code TypeScript valide | ✅/❌ |
| Fichier créé | ✅/❌ |

**Score : X/6** → Si < 5, corriger avant de terminer
```

---

## Auto-Chain

Après la génération, proposer :

```markdown
## 🔗 Prochaine étape

✅ Code généré depuis Figma.

**Suggestions :**

→ 🧪 **`/test-runner`** - Écrire des tests pour le composant
→ 🔄 **`/code-reviewer`** - Review du code généré
→ 🖼️ **`/figma-to-code [autre-url]`** - Générer un autre composant

---

**[T] Tests** | **[R] Review** | **[F] Autre Figma** | **[X] Terminé**
```

**⏸️ STOP** - Attendre choix

---

## Gestion des erreurs

### URL invalide

```markdown
❌ **URL Figma invalide**

L'URL fournie ne semble pas être une URL Figma valide.

**Format attendu** :
```
https://figma.com/design/FILE_KEY/FILE_NAME?node-id=NODE_ID
https://figma.com/file/FILE_KEY/FILE_NAME?node-id=NODE_ID
```

**Exemples valides** :
- `https://figma.com/design/ABC123/MyDesign?node-id=1:234`
- `https://figma.com/file/XYZ789/Components`

Fournis une URL Figma valide.
```

### Pas de Code Connect

```markdown
⚠️ **Code Connect non configuré**

Pour une meilleure génération, configure d'abord Code Connect :

```bash
/figma-setup
```

**Options** :
- [S] Setup Code Connect d'abord (recommandé)
- [C] Continuer sans mappings (génération basique)
```

### Accès refusé

```markdown
❌ **Accès au fichier Figma refusé**

Tu n'as pas accès à ce fichier Figma.

**Solutions** :
1. Vérifie que tu es connecté au bon compte Figma
2. Demande l'accès au propriétaire du fichier
3. Vérifie que le lien de partage est activé

Re-authentification :
```bash
npx figma connect
```
```

---

## Transitions

- **Vers test-runner** : "On écrit les tests pour ce composant ?"
- **Vers code-reviewer** : "On review le code généré ?"
- **Vers figma-setup** : "On configure Code Connect d'abord ?"
