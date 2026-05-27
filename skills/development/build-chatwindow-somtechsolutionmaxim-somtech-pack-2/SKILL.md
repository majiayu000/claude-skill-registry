---
name: build-chatwindow
description: Construit des chatwindows avec widgets interactifs ChatWidget. Guide la création de widgets selon le contrat ChatWidget, leur intégration dans ChatWindow, la configuration des workflows (OpenAI Agent / n8n), et la validation via le Playground. Utilise ce skill lorsque l'utilisateur demande de créer, modifier ou intégrer des widgets dans une conversation ChatWindow.
license: MIT
metadata:
  author: somtech-pack
  version: "1.1.0"
  project: generic
---

# Construction de ChatWindows avec Widgets

Ce skill guide la construction de chatwindows avec widgets interactifs `ChatWidget` selon l'architecture ChatWindow. Cette architecture est réutilisable dans tout projet utilisant Supabase, React et des workflows (OpenAI Agent Builder / n8n).

## Quand utiliser ce skill

Utilisez ce skill lorsque :
- L'utilisateur demande de créer un nouveau widget ChatWidget
- Il faut intégrer un widget dans une conversation ChatWindow
- Il faut configurer un workflow pour renvoyer des widgets
- Il faut modifier un widget existant
- Il faut valider le rendu d'un widget dans le Playground
- Il faut comprendre le contrat ChatWidget et les types supportés

## Architecture ChatWindow

ChatWindow est une interface de conversation réutilisable qui s'appuie sur :
- **Frontend** : Composants `ChatWindow` + `ChatWidget` + hook de gestion (ex: `useChatKit`)
- **Stockage** : Threads + messages (Supabase Postgres ou autre base de données)
- **Workflows** : `openai_agent` ou `n8n` (configuration en base de données)
- **Routeur SSE** : Edge Function (ex: `chatkit`) qui stream les réponses + widgets

> **Note pour adaptation** : Les noms de composants et fonctions peuvent varier selon votre projet. Adaptez les chemins et noms selon votre structure de code.

### Flux de données

```
Utilisateur → ChatWindow → useChatKit → Edge Function chatkit → Workflow → SSE → Widget
```

## Contrat ChatWidget

### Format de transport (SSE)

Un widget est envoyé via un événement SSE :

```json
{
  "type": "widget",
  "widget": {
    "id": "w-unique-001",
    "type": "button",
    "label": "Actions disponibles",
    "data": { /* données spécifiques au type */ },
    "actions": [ /* ChatWidgetAction[] */ ]
  }
}
```

### Schéma TypeScript

```typescript
interface ChatWidget {
  id: string;                    // Identifiant unique stable
  type: 'button' | 'form' | 'select' | 'checkbox' | 'radio' | 'summary_confirm';
  label?: string;                 // Libellé affiché
  data?: Record<string, unknown>; // Données spécifiques au type
  actions?: ChatWidgetAction[];   // Actions disponibles
}

interface ChatWidgetAction {
  id: string;                     // Identifiant unique
  label: string;                  // Libellé du bouton
  action: string;                 // Identifiant stable de l'action
  payload?: Record<string, unknown>; // Valeurs fixes fusionnées avec formData
}
```

⚠️ **Important** : `input` existe dans les types mais **n'est pas rendu** actuellement. Éviter ce type.

## Types de widgets supportés

### 1. `button` — Actions rapides

**Usage** : Afficher des boutons d'action rapide sans saisie utilisateur.

**Structure `data`** :
- Pas de `data` requis (ou vide)
- Les actions sont définies dans `actions[]`

**Exemple** :
```json
{
  "id": "w-actions-001",
  "type": "button",
  "label": "Actions disponibles",
  "actions": [
    {
      "id": "a-open-linear",
      "label": "Ouvrir dans Linear",
      "action": "open_url",
      "payload": { "url": "https://linear.app/org/issue/APP-123" }
    },
    {
      "id": "a-navigate",
      "label": "Voir les détails",
      "action": "navigate",
      "payload": { "path": "/requests/uuid-ticket" }
    }
  ]
}
```

### 2. `form` — Collecte d'informations

**Usage** : Formulaire avec champs multiples pour collecter des données.

**Structure `data`** :
```typescript
{
  description?: string;  // Description affichée au-dessus du formulaire
  fields: Array<{
    name: string;        // Nom du champ (clé dans formData)
    type: 'text' | 'textarea' | 'number' | 'email' | ...;
    label: string;       // Libellé affiché
    required?: boolean;  // Champ obligatoire
  }>;
  // Valeurs initiales (optionnel) : clés au même niveau que fields
  titre?: string;
  description?: string;
}
```

**Exemple** :
```json
{
  "id": "w-ticket-form-001",
  "type": "form",
  "label": "Compléter la demande",
  "data": {
    "description": "Merci de compléter ces informations avant création.",
    "fields": [
      { "name": "titre", "type": "text", "label": "Titre", "required": true },
      { "name": "description", "type": "textarea", "label": "Description", "required": true },
      { "name": "impact", "type": "text", "label": "Impact", "required": false }
    ],
    "titre": "Erreur sur fiche client",
    "description": "Quand on ouvre une fiche client, un message d'erreur apparaît.",
    "impact": "Blocage partiel"
  },
  "actions": [
    {
      "id": "a-create-ticket",
      "label": "Créer la demande",
      "action": "create_ticket",
      "payload": { "module": "clients", "priority": "P1" }
    }
  ]
}
```

### 3. `select` — Choix unique (liste déroulante)

**Usage** : Permettre à l'utilisateur de choisir une option parmi plusieurs.

**Structure `data`** :
```typescript
{
  options: Array<{ value: string; label: string }>;
  value?: string;  // Valeur présélectionnée (optionnel)
}
```

**Comportement** : Si `actions.length === 1`, l'action est déclenchée automatiquement lors de la sélection.

**Exemple** :
```json
{
  "id": "w-priority-001",
  "type": "select",
  "label": "Choisir la priorité",
  "data": {
    "options": [
      { "value": "P0", "label": "P0 (Critique)" },
      { "value": "P1", "label": "P1 (Haute)" },
      { "value": "P2", "label": "P2 (Normale)" },
      { "value": "P3", "label": "P3 (Faible)" }
    ],
    "value": "P2"
  },
  "actions": [
    { "id": "a-set-priority", "label": "Confirmer", "action": "set_priority" }
  ]
}
```

### 4. `checkbox` — Choix multiples

**Usage** : Permettre à l'utilisateur de sélectionner plusieurs options.

**Structure `data`** :
```typescript
{
  options: Array<{ value: string; label: string }>;
}
```

**Comportement** : `formData[option.value]` devient un booléen (`true` si coché, `false` sinon).

**Exemple** :
```json
{
  "id": "w-flags-001",
  "type": "checkbox",
  "label": "Informations disponibles",
  "data": {
    "options": [
      { "value": "logs", "label": "Logs" },
      { "value": "steps", "label": "Étapes pour reproduire" },
      { "value": "screenshot", "label": "Capture" }
    ]
  },
  "actions": [
    { "id": "a-submit-flags", "label": "Continuer", "action": "confirm_flags" }
  ]
}
```

### 5. `radio` — Choix unique (boutons radio)

**Usage** : Permettre à l'utilisateur de choisir une option parmi plusieurs (affichage radio).

**Structure `data`** :
```typescript
{
  options: Array<{ value: string; label: string }>;
  value?: string;  // Valeur présélectionnée (optionnel)
}
```

**Comportement** : Comme `select`, auto-trigger si `actions.length === 1`.

**Exemple** :
```json
{
  "id": "w-type-001",
  "type": "radio",
  "label": "Type de demande",
  "data": {
    "options": [
      { "value": "incident", "label": "Incident" },
      { "value": "question", "label": "Question" },
      { "value": "amelioration", "label": "Amélioration" }
    ],
    "value": "incident"
  },
  "actions": [
    { "id": "a-confirm-type", "label": "Confirmer", "action": "set_type" }
  ]
}
```

### 6. `summary_confirm` — Résumé et confirmation

**Usage** : Afficher un résumé lisible avec confirmation avant action finale.

**Structure `data`** :
```typescript
{
  title?: string;           // Titre du résumé
  understood?: string[];    // Liste des points compris
  confirmation?: string;    // Question de confirmation
  next_step?: string;       // Prochaine étape après confirmation
}
```

**Spécificité** : Le renderer envoie un contexte **minimal** à l'action (`{ widget_id: widget.id }`) pour éviter d'envoyer tout `widget.data`.

**Exemple** :
```json
{
  "id": "w-orchestrator-validation-001",
  "type": "summary_confirm",
  "data": {
    "title": "✅ Demande — Bug",
    "understood": [
      "Quand vous cliquez sur \"Client\", vous arrivez sur une page blanche.",
      "Vous vous attendiez à voir la fiche client s'afficher normalement."
    ],
    "confirmation": "Pouvez-vous confirmer que c'est bien ça ? OK / à corriger",
    "next_step": "Parfait, votre demande est prise en charge par l'équipe et sera traitée rapidement."
  },
  "actions": [
    {
      "id": "a-confirm-orchestrator",
      "label": "Confirmé",
      "action": "confirm_orchestrator",
      "payload": { "confirmed": true }
    }
  ]
}
```

## Convention d'exécution des actions

Lorsqu'un utilisateur déclenche une action :

1. **Fusion des données** : `payload` (valeurs fixes) est fusionné avec `formData` (valeurs saisies)
2. **Envoi** : Le frontend appelle `triggerAction(action.action, mergedPayload)`
3. **Traitement** : L'action repasse par le même routeur SSE que les messages

### Bonnes pratiques pour les actions

- **`action`** : Identifiant stable et descriptif (`open_url`, `navigate`, `create_ticket`, `set_priority`, etc.)
- **`payload`** : Valeurs immuables (ex: `{ path: "/requests/..." }`, `{ module: "clients" }`)
- **`formData`** : Valeurs dynamiques saisies par l'utilisateur (fusionnées automatiquement)

## Processus de construction

### Étape 1 : Définir le widget

1. **Choisir le type** : Sélectionner le type de widget approprié selon le besoin
2. **Définir l'ID** : Utiliser un ID stable et descriptif (ex: `w-ticket-form-001`)
3. **Structurer les données** : Préparer `data` selon le type choisi
4. **Définir les actions** : Identifier les actions possibles et leurs `payload`

### Étape 2 : Créer le JSON du widget

Créer le widget selon le contrat ChatWidget :

```json
{
  "id": "w-unique-id",
  "type": "button",
  "label": "Libellé du widget",
  "data": { /* selon le type */ },
  "actions": [ /* ChatWidgetAction[] */ ]
}
```

### Étape 3 : Tester dans le Playground

1. **Accéder au Playground** : Route de votre projet (ex: `/admin/widget-playground` ou `/widgets/playground`)
2. **Copier le JSON** : Coller le widget dans le Playground
3. **Vérifier le rendu** : S'assurer que le widget s'affiche correctement
4. **Tester les actions** : Vérifier que les actions déclenchent les bons événements (toast + log console)
5. **Vérifier la console** : Confirmer **0 erreur console**

> **Note** : Si votre projet n'a pas encore de Playground, créez-en un en vous basant sur les composants `ChatWidget` existants. Voir la section "Sources de vérité" pour les fichiers de référence.

### Étape 4 : Intégrer dans le workflow

#### Pour OpenAI Agent Builder

Dans le prompt de l'agent, inclure le widget dans la réponse :

```json
{
  "type": "widget",
  "widget": { /* ChatWidget */ }
}
```

#### Pour n8n

Dans le webhook n8n, renvoyer :

```json
{
  "content": "Message texte",
  "widget": { /* ChatWidget */ }
}
```

Le routeur SSE convertit automatiquement en événement SSE.

### Étape 5 : Valider dans ChatWindow

1. **Utiliser la bulle de test** : Composant de test ChatWindow (ex: `ChatWindowWidget` ou équivalent)
2. **Sélectionner un workflow** : Choisir un workflow actif dans votre configuration
3. **Envoyer un message** : Déclencher le workflow qui renvoie le widget
4. **Vérifier le rendu** : S'assurer que le widget s'affiche sous le message
5. **Tester les actions** : Vérifier que les actions fonctionnent correctement
6. **Vérifier la console** : Confirmer **0 erreur console**

> **Note** : Adaptez cette étape selon votre mécanisme de test. L'important est de valider le widget dans un contexte de conversation réel.

## Checklist de validation

### Validation Playground (obligatoire)

- [ ] Le widget s'affiche correctement dans votre Playground (route selon votre projet)
- [ ] Les champs/formulaires sont interactifs
- [ ] Les actions déclenchent un toast + log console
- [ ] Le JSON du widget est valide (pas d'erreur de parsing)
- [ ] L'enveloppe SSE (`{ type: "widget", widget: ... }`) est correcte
- [ ] **0 erreur console** dans le navigateur

### Validation ChatWindow (obligatoire)

- [ ] Le widget s'affiche sous le message dans ChatWindow
- [ ] Les interactions utilisateur fonctionnent (saisie, sélection, clics)
- [ ] Les actions renvoient un événement observable (message/action)
- [ ] Le streaming SSE fonctionne correctement
- [ ] Les messages user/assistant sont persistés en base
- [ ] **0 erreur console** dans le navigateur

## Bonnes pratiques

### IDs stables

- Utiliser des IDs déterministes et descriptifs
- Format recommandé : `w-{type}-{purpose}-{number}` (ex: `w-ticket-form-001`)
- Éviter les IDs générés aléatoirement

### Actions stables

- `action` doit être stable et descriptif
- Exemples : `open_url`, `navigate`, `create_ticket`, `set_priority`, `confirm_orchestrator`
- Éviter les actions génériques comme `submit`, `click`, `confirm`

### Données minimales

- Éviter de renvoyer un `widget.data` énorme côté backend
- Préférer `payload` (valeurs fixes) + champs saisis (`formData`)
- Pour `summary_confirm`, utiliser le contexte minimal (`{ widget_id }`)

### Accessibilité

- Associer des labels aux champs
- Gérer le focus correctement (composants shadcn/radix aident)
- Tester au clavier (Tab, Enter, Espace)

## Ajouter un nouveau type de widget

Si vous devez ajouter un nouveau type de widget :

1. **Étendre le type TS** : Ajouter le type dans vos types TypeScript (ex: `src/types/chat.ts`)
2. **Implémenter le rendu** : Ajouter le rendu dans votre composant ChatWidget (ex: `src/components/chat/ChatWidget.tsx`)
3. **Ajouter un exemple** : Ajouter un exemple dans votre Playground (ex: `src/pages/WidgetPlayground.tsx`)
4. **Mettre à jour le contrat** : Documenter dans votre contrat widgets (ex: `agentbuilder/WIDGETS_CONTRACT.md` ou équivalent)
5. **Valider** : Tester dans le Playground + contexte de conversation réel (console = 0 erreur)

> **Note** : Adaptez les chemins de fichiers selon la structure de votre projet.

## Sources de vérité (structure type)

Dans un projet utilisant cette architecture, vous devriez avoir :

- **Contrat widgets** : Documentation du format ChatWidget (ex: `agentbuilder/WIDGETS_CONTRACT.md` ou `docs/widgets-contract.md`)
- **Types TS** : Types TypeScript pour ChatWidget (ex: `src/types/chat.ts` ou équivalent)
- **Renderer widgets** : Composant qui rend les widgets (ex: `src/components/chat/ChatWidget.tsx`)
- **UI conversation** : Composant principal de conversation (ex: `src/components/chat/ChatWindow.tsx`)
- **Hook data/transport** : Hook qui gère les messages et widgets (ex: `src/hooks/useChatKit.ts` ou équivalent)
- **Playground widgets** : Page de test/prévisualisation (ex: `src/pages/WidgetPlayground.tsx`)
- **Bulle de test** : Composant de test ChatWindow (ex: `src/components/chat/ChatWindowWidget.tsx`)
- **Routeur SSE** : Edge Function ou API qui stream les réponses (ex: `supabase/functions/chatkit/index.ts` ou équivalent)
- **Documentation** : Documentation du projet (ex: `docs/chatbot/` ou équivalent)

> **Note pour adaptation** : Ces chemins sont des exemples. Adaptez-les selon la structure de votre projet. L'important est d'avoir ces composants/fichiers quelque part dans votre codebase.

## Références

### Documentation générique

- Ce skill fournit toutes les informations nécessaires pour créer des widgets ChatWidget
- Les exemples dans `references/WIDGET_EXAMPLES.md` sont réutilisables tels quels
- Le guide d'intégration dans `references/WORKFLOW_INTEGRATION.md` est applicable à tout projet

### Documentation associée (pack)

Dans ce pack, une documentation générique est fournie ici :
- `docs/chatwindow/README.md`

> **Note** : Cette doc est conçue pour être réutilisable. Adaptez les chemins/fichiers à votre projet si nécessaire.


## Adaptation pour un nouveau projet

Ce skill est conçu pour être réutilisable dans tout projet. Pour l'adapter :

### 1. Structure de fichiers

Adaptez les chemins mentionnés selon votre structure :
- Types TypeScript : où vous définissez vos types `ChatWidget`
- Composants : où vous avez vos composants `ChatWindow` et `ChatWidget`
- Playground : route et composant de votre Playground
- Routeur SSE : votre Edge Function ou API qui stream les réponses

### 2. Noms de composants

Les noms de composants peuvent varier :
- `ChatWindow` → votre composant de conversation
- `ChatWidget` → votre composant de widget
- `useChatKit` → votre hook de gestion (ou équivalent)

### 3. Configuration

- **Base de données** : Adaptez selon votre système (Supabase, autre)
- **Workflows** : Adaptez selon vos workflows (OpenAI Agent Builder, n8n, autre)
- **Routes** : Adaptez les routes du Playground selon votre routing

### 4. Contrat ChatWidget

Le contrat ChatWidget décrit dans ce skill est **universel** et peut être utilisé tel quel. Seuls les chemins de fichiers et noms de composants doivent être adaptés.

### 5. Validation

Les processus de validation décrits (Playground + ChatWindow) sont applicables à tout projet. Adaptez uniquement les routes et noms de composants.
