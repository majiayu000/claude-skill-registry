---
name: umbraco-repository-pattern
description: Understand and use repositories in Umbraco backoffice (foundational concept)
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Repository Pattern

## What is it?
Repositories are the Backoffice's entry point for data requests and update notifications, abstracting data access from various sources (server, offline database, store, Signal-R). They provide a structured way to manage data operations, separating business logic from direct data access for easier maintenance and scalability. Repositories use data sources behind the scenes, allowing consumers to work with data without knowing where or how it's stored.

## CRITICAL: API Authentication

**NEVER use raw `fetch()` for custom API calls.** This will result in 401 Unauthorized errors.

**ALWAYS use a generated OpenAPI client** configured with Umbraco's auth context. See the `umbraco-openapi-client` skill for setup instructions.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/repositories
- **Working with Data**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Store**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What data to manage? CRUD operations needed? Data source type?
3. **Generate code** - Implement repository and data source based on latest docs
4. **Explain** - Show what was created and how to use it

## Minimal Examples

### Repository Registration
```typescript
import { umbExtensionsRegistry } from '@umbraco-cms/backoffice/extension-registry';
import { MyRepository } from './my-repository.js';

const repositoryManifest = {
  type: 'repository',
  alias: 'My.Repository',
  name: 'My Repository',
  api: MyRepository,
};

umbExtensionsRegistry.register(repositoryManifest);
```

### Basic Repository Implementation (Using OpenAPI Client)
```typescript
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';
// Import from generated OpenAPI client (see umbraco-openapi-client skill)
import { MyExtensionService } from '../api/index.js';

export class MyRepository extends UmbControllerBase {
  constructor(host: UmbControllerHost) {
    super(host);
  }

  async getAll() {
    // Use generated OpenAPI client - handles auth automatically
    const response = await MyExtensionService.getAll();
    return response.data;
  }

  async getById(id: string) {
    const response = await MyExtensionService.getById({ path: { id } });
    return response.data;
  }

  async create(data: any) {
    const response = await MyExtensionService.create({ body: data });
    return response.data;
  }

  async update(id: string, data: any) {
    const response = await MyExtensionService.update({
      path: { id },
      body: data,
    });
    return response.data;
  }

  async delete(id: string) {
    await MyExtensionService.delete({ path: { id } });
  }
}
```

### Using Repository in Context
```typescript
import { UmbContextBase } from '@umbraco-cms/backoffice/class-api';
import { UmbArrayState } from '@umbraco-cms/backoffice/observable-api';
import { MyRepository } from './my-repository.js';

export class MyContext extends UmbContextBase<MyContext> {
  #repository = new MyRepository(this);
  #items = new UmbArrayState([]);

  readonly items = this.#items.asObservable();

  async loadItems() {
    const data = await this.#repository.getAll();
    this.#items.setValue(data);
  }

  async createItem(item: any) {
    const newItem = await this.#repository.create(item);
    this.#items.setValue([...this.#items.getValue(), newItem]);
  }

  async deleteItem(id: string) {
    await this.#repository.delete(id);
    this.#items.setValue(
      this.#items.getValue().filter(item => item.id !== id)
    );
  }
}
```

### Repository with Data Source (Using OpenAPI Client)
```typescript
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import { MyDataSource } from './my-data-source.js';

export class MyRepository extends UmbControllerBase {
  #dataSource = new MyDataSource(this);

  async getAll() {
    return await this.#dataSource.getAll();
  }

  async getById(id: string) {
    return await this.#dataSource.getById(id);
  }
}

// Data Source - uses generated OpenAPI client
import { MyExtensionService } from '../api/index.js';

export class MyDataSource extends UmbControllerBase {
  async getAll() {
    // Use OpenAPI client - NEVER raw fetch()
    const response = await MyExtensionService.getAll();
    return response.data;
  }

  async getById(id: string) {
    const response = await MyExtensionService.getById({ path: { id } });
    return response.data;
  }
}
```

### Tree Repository Example
```typescript
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import { UmbTreeDataSource } from '@umbraco-cms/backoffice/tree';

export class MyTreeRepository extends UmbControllerBase {
  #dataSource: UmbTreeDataSource;

  constructor(host: UmbControllerHost) {
    super(host);
    this.#dataSource = new MyTreeDataSource(this);
  }

  async getRootItems() {
    return await this.#dataSource.getRootItems();
  }

  async getChildrenOf(parentKey: string) {
    return await this.#dataSource.getChildrenOf(parentKey);
  }

  async getAncestorsOf(key: string) {
    return await this.#dataSource.getAncestorsOf(key);
  }
}
```

## Key Concepts

**Repository**: Entry point for data operations, abstracts data access

**Data Source**: Underlying mechanism that actually fetches/stores data

**Store**: Optional layer that holds data throughout the session using State objects

**Host Element**: Repository must be instantiated with a host for proper context rendering

**Separation of Concerns**:
- Repository = what operations are available
- Data Source = how data is fetched/stored
- Store = where data is cached
- Context = who coordinates it all

**Benefits**:
- Loose coupling between UI and data layer
- Swappable data sources
- Easier testing and maintenance
- Consistent data access patterns

**Usage Pattern**:
1. Define repository with CRUD methods
2. Implement data source for actual I/O
3. Instantiate repository in context
4. Context coordinates state and repository
5. UI observes state from context

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
