---
name: di-mockable-services
description: Design injectable, mockable services (interfaces + composition root)
compatibility: opencode
license: MIT
metadata:
  stack: node-react-next
  style: solid-clean-code
---
## What I do

Je standardise la **DI** (injection de dépendances) et la conception **mockable**.

## Core rules
- Écrire le contrat d'abord : `IUserApi`, `UserRepository`, etc.
- Les hooks/use-cases dépendent des interfaces.
- Les implémentations concrètes vivent dans `infra/`.
- Le **seul** endroit qui instancie l'infra est le `composition root`.

## Example (frontend service)

```ts
export interface IUserApi {
  getById(id: string): Promise<UserDTO>;
}

export class UserApi implements IUserApi {
  constructor(private readonly http: HttpClient) {}
  getById(id: string) { return this.http.get(`/users/${id}`); }
}

export class FakeUserApi implements IUserApi {
  async getById(id: string) { return { id, name: 'Test' }; }
}
```

## Testing guidance
- En test, remplacer via le container : `container.userApi = new FakeUserApi()`.
- Éviter les mocks globaux non typés.
