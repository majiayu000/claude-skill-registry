---
name: Zero Warnings Enforcer
description: Applique la philosophie "Broken Window" avec zéro tolérance pour les warnings/errors ESLint et TypeScript. JAMAIS désactiver les règles, TOUJOURS corriger la cause racine. À utiliser lors de la correction d'erreurs, warnings, ou quand l'utilisateur mentionne "eslint", "typescript error", "warning", "linting", "quality", "broken window", "@ts-ignore", "eslint-disable".
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Zero Warnings Enforcer

## 🎯 Mission

Maintenir une **qualité de code irréprochable** en appliquant la philosophie **Broken Window** : **ZÉRO warning**, **ZÉRO error**, **JAMAIS de désactivation de règles**.

## 🪟 Philosophie : Broken Window Theory

### Le Principe

**Broken Window Theory** (Théorie de la vitre brisée) :
- Une vitre cassée non réparée → Signal d'abandon
- Autres vitres brisées → Dégradation rapide
- Bâtiment entier dégradé en quelques semaines

**Application au code** :
- Un warning ignoré → Signal que la qualité n'est pas prioritaire
- Autres warnings ajoutés → Accumulation de dette technique
- Code base dégradée → Maintenabilité impossible

### La Règle d'Or

> **Un projet de qualité a ZÉRO warning, ZÉRO error, ZÉRO désactivation de règle.**

**Conséquences** :
- ✅ Code maintenable à long terme
- ✅ Onboarding facile (pas de "legacy code" sale)
- ✅ Confiance dans le code (pas de surprises)
- ✅ Refactoring sécurisé (typage strict)
- ✅ Bugs détectés tôt (ESLint + TypeScript)

## 🚫 Règles INTERDITES

### JAMAIS Désactiver ESLint

```typescript
// ❌ INTERDIT - ABSOLUMENT JAMAIS
/* eslint-disable */
const badCode = () => { ... };

// ❌ INTERDIT - ABSOLUMENT JAMAIS
// eslint-disable-next-line no-unused-vars
const unusedVariable = 'bad';

// ❌ INTERDIT - ABSOLUMENT JAMAIS
/* eslint-disable-next-line */
const veryBadCode = () => { ... };
```

**Pourquoi c'est INTERDIT** :
- Cache un problème au lieu de le résoudre
- Crée de la dette technique
- Signal de code de mauvaise qualité
- Accumulation rapide de désactivations

**Exception RARE** (documentée) :
```typescript
// ✅ ACCEPTABLE UNIQUEMENT SI :
// 1. Raison documentée
// 2. Approuvée en code review
// 3. Temporaire avec TODO et date limite
// 4. Aucune alternative possible

/* eslint-disable-next-line no-console */
console.log('Debug log - TODO: Remove before 2024-12-31'); // Ticket JIRA-123
```

### JAMAIS Ignorer TypeScript

```typescript
// ❌ INTERDIT - ABSOLUMENT JAMAIS
// @ts-ignore
const badType: string = 123;

// ❌ INTERDIT - ABSOLUMENT JAMAIS
// @ts-expect-error
const alsoBAD = someFunction();

// ❌ INTERDIT - ABSOLUMENT JAMAIS
const lazyTyping: any = { foo: 'bar' };

// ❌ INTERDIT - ABSOLUMENT JAMAIS
const unknownStuff: unknown = getData();
```

**Pourquoi c'est INTERDIT** :
- Perd le bénéfice du typage statique
- Bugs en production (erreurs de type non détectées)
- Perte de l'autocomplétion
- Refactoring dangereux

### JAMAIS de Types Faibles

```typescript
// ❌ INTERDIT
const data: any = fetchData();

// ❌ INTERDIT
const result: unknown = processData();

// ❌ INTERDIT
function process(input: any): any {
  return input;
}

// ✅ CORRECT
interface UserData {
  id: string;
  name: string;
  email: string;
}

const data: UserData = fetchData();
const result: ProcessedData = processData();
function process(input: UserInput): UserOutput {
  return transform(input);
}
```

## 🔧 ESLint Errors - Comment les Corriger

### 1. `no-unused-vars` - Variables Non Utilisées

```typescript
// ❌ MAUVAIS - Génère un warning
const unusedVariable = 'value';

function Component({ unusedProp, usedProp }: Props) {
  return <div>{usedProp}</div>;
}

// ✅ CORRECT - Supprimer la variable
// (Si vraiment inutile)

// ✅ CORRECT - Utiliser la variable
const usedVariable = 'value';
console.log(usedVariable);

// ✅ CORRECT - Préfixer avec _ si intentionnel (destructuring)
function Component({ _unusedProp, usedProp }: Props) {
  return <div>{usedProp}</div>;
}
```

### 2. `no-console` - Console Logs

```typescript
// ❌ MAUVAIS - console.log en production
console.log('Debug data:', data);
console.error('Error:', error);

// ✅ CORRECT - Utiliser un logger
import { logger } from '@/lib/logger';

logger.debug('Debug data:', data);
logger.error('Error:', error);

// ✅ CORRECT - Créer un logger custom
class Logger {
  debug(message: string, data?: any) {
    if (process.env.NODE_ENV === 'development') {
      console.log(`[DEBUG] ${message}`, data);
    }
  }

  error(message: string, error?: Error) {
    // Log to external service (Sentry, etc.)
    console.error(`[ERROR] ${message}`, error);
  }
}

export const logger = new Logger();
```

### 3. `@typescript-eslint/no-explicit-any` - Type `any`

```typescript
// ❌ MAUVAIS
function process(data: any) {
  return data.value;
}

// ✅ CORRECT - Type explicite
interface InputData {
  value: string;
}

function process(data: InputData): string {
  return data.value;
}

// ✅ CORRECT - Generic si type inconnu
function process<T extends { value: string }>(data: T): string {
  return data.value;
}

// ✅ CORRECT - Union type si plusieurs types possibles
function process(data: string | number | boolean): string {
  return String(data);
}
```

### 4. `react-hooks/exhaustive-deps` - useEffect Dependencies

```typescript
// ❌ MAUVAIS - Missing dependency
useEffect(() => {
  fetchData(userId); // userId is missing from deps
}, []);

// ❌ MAUVAIS - Désactiver la règle
useEffect(() => {
  fetchData(userId);
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, []);

// ✅ CORRECT - Ajouter la dépendance
useEffect(() => {
  fetchData(userId);
}, [userId]); // Correct!

// ✅ CORRECT - Extraire primitive si object
useEffect(() => {
  fetchData(user.id);
}, [user.id]); // Primitive, stable

// ✅ CORRECT - useCallback pour fonctions
const fetchData = useCallback((id: string) => {
  // fetch logic
}, []);

useEffect(() => {
  fetchData(userId);
}, [userId, fetchData]); // Stable function
```

### 5. `@typescript-eslint/no-unused-vars` - Imports Non Utilisés

```typescript
// ❌ MAUVAIS - Import non utilisé
import { useState, useEffect, useMemo } from 'react'; // useMemo unused

// ✅ CORRECT - Supprimer l'import
import { useState, useEffect } from 'react';

// ✅ CORRECT - Utiliser l'import
import { useState, useEffect, useMemo } from 'react';
const memoized = useMemo(() => compute(), []);
```

### 6. `@typescript-eslint/no-non-null-assertion` - Non-null Assertion

```typescript
// ❌ MAUVAIS - Non-null assertion
const value = data!.value;
const user = users.find(u => u.id === id)!;

// ✅ CORRECT - Vérifier null
const value = data?.value;
if (!data) {
  throw new Error('Data is required');
}
const value = data.value;

// ✅ CORRECT - Type guard
function isData(data: Data | null): data is Data {
  return data !== null;
}

if (isData(data)) {
  const value = data.value; // Type safe
}

// ✅ CORRECT - Optional chaining + fallback
const value = data?.value ?? 'default';
```

### 7. `@typescript-eslint/no-floating-promises` - Promises Non Gérées

```typescript
// ❌ MAUVAIS - Promise non await
fetchData(); // Floating promise

async function handler() {
  saveData(); // Promise non await
}

// ✅ CORRECT - Await la promise
await fetchData();

async function handler() {
  await saveData();
}

// ✅ CORRECT - void si intentionnel (fire and forget)
void fetchData(); // Explicit fire-and-forget

// ✅ CORRECT - .catch() si fire-and-forget
fetchData().catch(error => {
  logger.error('Background fetch failed', error);
});
```

## 🔷 TypeScript Errors - Comment les Corriger

### 1. Type 'X' is not assignable to type 'Y'

```typescript
// ❌ MAUVAIS
const id: string = 123; // Error

// ❌ MAUVAIS - @ts-ignore
// @ts-ignore
const id: string = 123;

// ✅ CORRECT - Convertir le type
const id: string = String(123);

// ✅ CORRECT - Changer le type
const id: number = 123;

// ✅ CORRECT - Union type si plusieurs types
const id: string | number = 123;
```

### 2. Object is possibly 'null' or 'undefined'

```typescript
// ❌ MAUVAIS
const name = user.name; // user peut être null

// ❌ MAUVAIS - Non-null assertion
const name = user!.name;

// ✅ CORRECT - Optional chaining
const name = user?.name;

// ✅ CORRECT - Type guard
if (!user) {
  throw new Error('User is required');
}
const name = user.name; // Type safe

// ✅ CORRECT - Nullish coalescing
const name = user?.name ?? 'Anonymous';
```

### 3. Property 'X' does not exist on type 'Y'

```typescript
// ❌ MAUVAIS
const value = obj.unknownProperty; // Property doesn't exist

// ❌ MAUVAIS - any
const obj: any = getData();
const value = obj.unknownProperty;

// ✅ CORRECT - Définir le type correct
interface MyObject {
  knownProperty: string;
  unknownProperty: string; // Add missing property
}

const obj: MyObject = getData();
const value = obj.unknownProperty;

// ✅ CORRECT - Type guard
function hasProperty<T, K extends string>(
  obj: T,
  key: K
): obj is T & Record<K, unknown> {
  return key in obj;
}

if (hasProperty(obj, 'unknownProperty')) {
  const value = obj.unknownProperty; // Type safe
}
```

### 4. Argument of type 'X' is not assignable to parameter of type 'Y'

```typescript
// ❌ MAUVAIS
function greet(name: string) {
  console.log(`Hello ${name}`);
}

greet(123); // Error

// ❌ MAUVAIS - any
greet(123 as any);

// ✅ CORRECT - Convertir le type
greet(String(123));

// ✅ CORRECT - Générique si fonction accepte plusieurs types
function greet<T extends string | number>(name: T) {
  console.log(`Hello ${name}`);
}

greet(123); // OK
greet('John'); // OK
```

### 5. Cannot find name 'X'

```typescript
// ❌ MAUVAIS
const result = unknownFunction(); // Function not imported

// ✅ CORRECT - Importer la fonction
import { unknownFunction } from '@/lib/utils';
const result = unknownFunction();

// ✅ CORRECT - Définir la fonction si manquante
function unknownFunction(): string {
  return 'result';
}

const result = unknownFunction();
```

### 6. Index signature is missing in type 'X'

```typescript
// ❌ MAUVAIS
const obj: { name: string } = { name: 'John' };
const key = 'age';
const value = obj[key]; // Error

// ❌ MAUVAIS - any
const obj: any = { name: 'John' };

// ✅ CORRECT - Index signature
interface User {
  name: string;
  [key: string]: string; // Index signature
}

const obj: User = { name: 'John' };
const value = obj[key]; // OK

// ✅ CORRECT - Type guard
function isValidKey<T extends object>(
  obj: T,
  key: string | number | symbol
): key is keyof T {
  return key in obj;
}

if (isValidKey(obj, key)) {
  const value = obj[key]; // Type safe
}

// ✅ CORRECT - Record type
const obj: Record<string, string> = { name: 'John' };
const value = obj[key]; // OK
```

## ✅ Quality Gates

### 1. Pre-commit Hooks (Husky + lint-staged)

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --max-warnings 0", // ZERO warnings tolerated
      "tsc --noEmit" // Type check
    ]
  }
}
```

### 2. CI/CD Pipeline (Strict Mode)

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: yarn install

      # ESLint - ZERO warnings
      - name: ESLint (Zero Warnings)
        run: yarn lint --max-warnings 0

      # TypeScript - Strict mode
      - name: TypeScript Check
        run: yarn tsc --noEmit

      # Tests - MUST pass
      - name: Run Tests
        run: yarn test

      # Build - MUST succeed
      - name: Build
        run: yarn build
```

### 3. ESLint Configuration (Strict)

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking',
  ],
  rules: {
    // STRICT RULES
    '@typescript-eslint/no-explicit-any': 'error', // any = ERROR
    '@typescript-eslint/no-unused-vars': 'error', // unused = ERROR
    'no-console': 'error', // console.log = ERROR
    '@typescript-eslint/no-floating-promises': 'error',
    '@typescript-eslint/no-non-null-assertion': 'error',
    '@typescript-eslint/strict-boolean-expressions': 'error',

    // NO WARNINGS ALLOWED
    'max-warnings': 0,
  },
};
```

### 4. TypeScript Configuration (Strict)

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true, // Enable ALL strict checks
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

## 📋 Checklist Qualité (Avant Commit)

### ✅ Avant Chaque Commit

- [ ] `yarn lint --max-warnings 0` passe sans erreur
- [ ] `yarn tsc --noEmit` passe sans erreur
- [ ] `yarn test` passe tous les tests
- [ ] `yarn build` réussit sans warnings
- [ ] Aucun `eslint-disable` ajouté
- [ ] Aucun `@ts-ignore` ajouté
- [ ] Aucun `any` ou `unknown` ajouté
- [ ] Aucun `console.log` laissé (utiliser logger)
- [ ] Code review personnel effectuée

### ✅ Avant Chaque PR

- [ ] Tous les commits respectent la checklist
- [ ] CI/CD passe (0 warning, 0 error)
- [ ] Code coverage maintenu ou amélioré
- [ ] Documentation à jour
- [ ] Tests ajoutés pour nouvelles features

## 🚨 Exceptions RARES (Documentées)

### Quand Désactiver une Règle EST Acceptable

**Cas TRÈS RARES** (< 1% du code) :
1. **Bug ESLint/TypeScript** : Règle buggée connue
2. **Code généré** : Fichiers auto-générés (Prisma client, etc.)
3. **Migration legacy** : Code legacy avec date limite de migration

**Template d'exception** :
```typescript
// EXCEPTION DOCUMENTÉE
// Raison: [Explication détaillée]
// Ticket: JIRA-123
// Deadline: 2024-12-31
// Reviewer: @john-doe
/* eslint-disable-next-line no-console */
console.log('Legacy debug - Migration en cours');
```

**Règles pour exceptions** :
- ✅ TOUJOURS documenter la raison
- ✅ TOUJOURS créer un ticket de suivi
- ✅ TOUJOURS fixer une deadline
- ✅ TOUJOURS faire valider en code review
- ✅ TOUJOURS scope minimal (`-next-line`, pas `disable`)

## 🎓 Exemples Complets

### Exemple 1 : Corriger un useEffect avec Dependencies

```typescript
// ❌ AVANT - Warning exhaustive-deps
function Component({ userId }: Props) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData(userId).then(setData);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Missing userId dependency

  return <div>{data?.name}</div>;
}

// ✅ APRÈS - Correction complète
function Component({ userId }: Props) {
  const [data, setData] = useState<UserData | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadData() {
      const result = await fetchData(userId);
      if (!cancelled) {
        setData(result);
      }
    }

    void loadData();

    return () => {
      cancelled = true; // Cleanup
    };
  }, [userId]); // Correct dependency

  return <div>{data?.name}</div>;
}
```

### Exemple 2 : Corriger un Type `any`

```typescript
// ❌ AVANT - Type any
function processData(data: any) {
  return {
    id: data.id,
    name: data.name,
    items: data.items.map((item: any) => item.value),
  };
}

// ✅ APRÈS - Types explicites
interface InputData {
  id: string;
  name: string;
  items: Array<{ value: string }>;
}

interface ProcessedData {
  id: string;
  name: string;
  items: string[];
}

function processData(data: InputData): ProcessedData {
  return {
    id: data.id,
    name: data.name,
    items: data.items.map(item => item.value),
  };
}
```

## 📚 Skills Complémentaires

Pour aller plus loin :
- **refactoring** : Refactoring best practices
- **testing** : Testing standards pour prévenir les régressions
- **code-reviewer** : Code review checklist

---

**Rappel** : **Un warning = Une fenêtre cassée = Début de la dégradation.** Corrigez IMMÉDIATEMENT, ne JAMAIS ignorer.
