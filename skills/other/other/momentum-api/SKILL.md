---
name: momentum-api
description: Work with Momentum API for data operations in Angular components
argument-hint: <operation> [collection]
---

# Momentum API Usage

Guide for using `injectMomentumAPI()` in Angular components.

## Arguments

- `$ARGUMENTS` - Operation type: "query", "crud", "typed", or collection name

## Quick Reference

### Inject the API

```typescript
import { injectMomentumAPI } from '@momentumcms/admin';

@Component({...})
export class MyComponent {
  private readonly api = injectMomentumAPI();
}
```

### Query Data (Observables)

```typescript
// In constructor or with toSignal()
this.api
	.collection<Post>('posts')
	.find$({ limit: 10 })
	.subscribe((result) => {
		this.posts.set(result.docs);
	});
```

### Query Data (Promises)

```typescript
async loadData(): Promise<void> {
  const result = await this.api.collection<Post>('posts').find({ limit: 10 });
  this.posts.set(result.docs);
}
```

### CRUD Operations

```typescript
// Create
const post = await this.api.collection<Post>('posts').create({ title: 'New Post' });

// Read
const post = await this.api.collection<Post>('posts').findById('123');

// Update
const updated = await this.api.collection<Post>('posts').update('123', { title: 'Updated' });

// Delete
const result = await this.api.collection<Post>('posts').delete('123');
```

### With Generated Types

1. Generate types: `nx run example-angular:generate-types`
2. Import and use:

```typescript
import type { Post, User } from '../types/momentum.generated';

const posts = await this.api.collection<Post>('posts').find();
const users = await this.api.collection<User>('users').find();
```

## Find Options

```typescript
interface FindOptions {
	where?: Record<string, unknown>; // Filter conditions
	sort?: string; // Sort field (prefix with - for desc)
	limit?: number; // Max results (default: 10)
	page?: number; // Page number (default: 1)
}
```

## Full Component Example

```typescript
import { Component, signal, ChangeDetectionStrategy } from '@angular/core';
import { injectMomentumAPI } from '@momentumcms/admin';
import type { Post } from '../types/momentum.generated';

@Component({
	selector: 'app-posts',
	template: `
		@if (loading()) {
			<p>Loading...</p>
		} @else {
			@for (post of posts(); track post.id) {
				<article>
					<h2>{{ post.title }}</h2>
					<p>{{ post.content }}</p>
					<button (click)="deletePost(post.id)">Delete</button>
				</article>
			}
		}

		<form (submit)="createPost($event)">
			<input #titleInput placeholder="Title" />
			<button type="submit">Create Post</button>
		</form>
	`,
	changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PostsComponent {
	private readonly api = injectMomentumAPI();

	readonly posts = signal<Post[]>([]);
	readonly loading = signal(true);

	constructor() {
		this.loadPosts();
	}

	async loadPosts(): Promise<void> {
		this.loading.set(true);
		try {
			const result = await this.api.collection<Post>('posts').find({
				limit: 20,
				sort: '-createdAt',
			});
			this.posts.set(result.docs);
		} finally {
			this.loading.set(false);
		}
	}

	async createPost(event: Event): Promise<void> {
		event.preventDefault();
		const form = event.target as HTMLFormElement;
		const input = form.querySelector('input') as HTMLInputElement;

		const post = await this.api.collection<Post>('posts').create({
			title: input.value,
		});

		this.posts.update((posts) => [post, ...posts]);
		input.value = '';
	}

	async deletePost(id: string): Promise<void> {
		await this.api.collection<Post>('posts').delete(id);
		this.posts.update((posts) => posts.filter((p) => p.id !== id));
	}
}
```

## Platform Behavior

- **SSR**: Direct database access (no HTTP overhead)
- **Browser**: HTTP calls to `/api/*`
- **Same interface** - code works identically on both platforms

## Error Handling

```typescript
import {
	CollectionNotFoundError,
	DocumentNotFoundError,
	AccessDeniedError,
	ValidationError,
} from '@momentumcms/server-core';

try {
	await this.api.collection('posts').create({ title: '' });
} catch (error) {
	if (error instanceof ValidationError) {
		// Handle validation errors
		console.error('Validation failed:', error.errors);
	}
}
```

## Type Generation

Generate types from your collections:

```bash
# Generate types
nx run example-angular:generate-types

# Watch mode (auto-regenerate on changes)
nx run example-angular:generate-types --watch
```

Output file: `src/types/momentum.generated.ts`

## TransferState (SSR Hydration)

TransferState is **enabled by default** for all read operations (`find`, `findById`, `findSignal`, `findByIdSignal`). Data fetched during SSR is automatically cached and reused on browser hydration, eliminating duplicate HTTP calls.

### Default Behavior (TransferState enabled)

```typescript
// SSR: Fetches and caches | Browser: Reads from cache (no HTTP)
const posts = await this.api.collection<Post>('posts').find({ limit: 10 });
const post = await this.api.collection<Post>('posts').findById(id);
```

### Opt-out

Use `transfer: false` to disable TransferState for a specific call:

```typescript
// Always makes HTTP call on browser (no caching)
const posts = await this.api.collection<Post>('posts').find({
	limit: 10,
	transfer: false,
});
```

### Signal Methods

```typescript
// Signals also use TransferState by default
readonly posts = this.api.collection<Post>('posts').findSignal({ limit: 10 });
readonly post = this.api.collection<Post>('posts').findByIdSignal(id);
```

### Requirements

Ensure `provideClientHydration()` is in your app config:

```typescript
// app.config.ts
export const appConfig: ApplicationConfig = {
	providers: [provideClientHydration()],
};
```
