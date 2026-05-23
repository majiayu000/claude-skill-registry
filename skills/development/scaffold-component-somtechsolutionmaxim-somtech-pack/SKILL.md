---
name: scaffold-component
description: |
  Créer un composant React/TypeScript/Tailwind.
  TRIGGERS : créer composant, scaffold-ui, nouveau composant, ajouter composant
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Scaffold Component React

## Procédure

### 1. Vérifier l'existant
```bash
# Chercher composants similaires
find src/components -name "*.tsx" -type f | head -20
```

### 2. Créer le composant

Structure standard :

```tsx
import { useState } from 'react';

interface ${ComponentName}Props {
  // Props typées
}

export function ${ComponentName}({ ...props }: ${ComponentName}Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // États
  if (loading) {
    return <div data-testid="${component-name}-loading">Chargement...</div>;
  }

  if (error) {
    return (
      <div data-testid="${component-name}-error" className="text-red-500">
        {error}
      </div>
    );
  }

  return (
    <div data-testid="${component-name}">
      {/* Contenu */}
    </div>
  );
}
```

### 3. Checklist

- [ ] Props typées avec interface
- [ ] États : loading, vide, erreur, succès
- [ ] `data-testid` sur éléments critiques
- [ ] Pas de secrets dans le code

### 4. Valider

Utiliser `/validate-ui` pour confirmer 0 erreur console.
