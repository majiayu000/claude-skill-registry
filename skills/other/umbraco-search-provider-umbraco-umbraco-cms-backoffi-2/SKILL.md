---
name: umbraco-search-provider
description: Implement search providers in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Search Provider

## What is it?
A Search Provider integrates custom search functionality into Umbraco's backoffice search bar. It enables users to search custom data sources alongside built-in content, media, and members. The provider implements a `search` method that returns paginated results matching the user's query.

## Documentation
Always fetch the latest docs before implementing:

- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Related Foundation Skills

- **Repository Pattern**: For data access in search providers
  - Reference skill: `umbraco-repository-pattern`

- **Context API**: For accessing contexts within the provider
  - Reference skill: `umbraco-context-api`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What data to search? What fields to return? Custom result display needed?
3. **Generate files** - Create manifest + provider class based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestSearchProvider } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestSearchProvider = {
  type: 'searchProvider',
  alias: 'My.SearchProvider',
  name: 'My Search Provider',
  api: () => import('./my-search-provider.js'),
  meta: {
    label: 'My Items',
  },
};

export const manifests = [manifest];
```

### Provider Implementation (my-search-provider.ts)
```typescript
import type { UmbSearchProvider, UmbSearchResultItemModel, UmbSearchRequestArgs } from '@umbraco-cms/backoffice/search';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';

export class MySearchProvider extends UmbControllerBase implements UmbSearchProvider {
  constructor(host: UmbControllerHost) {
    super(host);
  }

  async search(args: UmbSearchRequestArgs) {
    const { query } = args;

    // Fetch results from your data source
    const results = await this.#fetchResults(query);

    return {
      data: {
        items: results,
        total: results.length,
      },
    };
  }

  async #fetchResults(query: string): Promise<UmbSearchResultItemModel[]> {
    // Your search logic here - API call, local filtering, etc.
    const response = await fetch(`/api/my-items/search?q=${encodeURIComponent(query)}`);
    const data = await response.json();

    return data.items.map((item: any) => ({
      entityType: 'my-entity',
      unique: item.id,
      name: item.name,
      icon: 'icon-document',
      href: `/section/my-section/workspace/my-workspace/edit/${item.id}`,
    }));
  }
}

export default MySearchProvider;
```

### Search Result Item Model
```typescript
// Each result must conform to UmbSearchResultItemModel
interface UmbSearchResultItemModel {
  entityType: string;    // Entity type identifier
  unique: string;        // Unique ID
  name: string;          // Display name
  icon?: string | null;  // Icon to display
  href: string;          // URL to navigate when clicked
}
```

### Provider with Repository
```typescript
import type { UmbSearchProvider, UmbSearchResultItemModel, UmbSearchRequestArgs } from '@umbraco-cms/backoffice/search';
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import { MyRepository } from './my-repository.js';

export class MySearchProvider extends UmbControllerBase implements UmbSearchProvider {
  #repository: MyRepository;

  constructor(host: UmbControllerHost) {
    super(host);
    this.#repository = new MyRepository(this);
  }

  async search(args: UmbSearchRequestArgs) {
    const { data } = await this.#repository.search(args.query);

    const items: UmbSearchResultItemModel[] = data?.items.map((item) => ({
      entityType: 'my-entity',
      unique: item.id,
      name: item.name,
      icon: item.icon ?? 'icon-document',
      href: `/section/my-section/workspace/my-workspace/edit/${item.id}`,
    })) ?? [];

    return {
      data: {
        items,
        total: data?.total ?? 0,
      },
    };
  }
}

export default MySearchProvider;
```

### Search with Context (e.g., search from specific location)
```typescript
async search(args: UmbSearchRequestArgs) {
  const { query, searchFrom } = args;

  // searchFrom contains the entity to search from (if specified)
  const parentId = searchFrom?.unique;

  const results = await this.#fetchResults(query, parentId);

  return {
    data: {
      items: results,
      total: results.length,
    },
  };
}
```

## Search Request Args

| Property | Description |
|----------|-------------|
| `query` | The search term entered by user |
| `searchFrom` | Optional entity to search from (for scoped searches) |

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
