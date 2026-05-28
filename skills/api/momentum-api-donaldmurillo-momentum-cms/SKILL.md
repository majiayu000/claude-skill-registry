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

@Component({
	selector: 'app-posts',
	template: `
		@if (loading()) {
			<p>Loading...</p>
		} @else {
			@for (post of posts(); track post.id) {
				<article>
					<h2>{{ post.title }}</h2>
					<button (click)="deletePost(post.id)">Delete</button>
				</article>
			}
		}
	`,
	changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PostsComponent {
	private readonly api = injectMomentumAPI();

	readonly posts = signal<any[]>([]);
	readonly loading = signal(true);

	constructor() {
		this.loadPosts();
	}

	async loadPosts(): Promise<void> {
		this.loading.set(true);
		try {
			const result = await this.api.collection('posts').find({
				limit: 20,
				sort: '-createdAt',
			});
			this.posts.set(result.docs);
		} finally {
			this.loading.set(false);
		}
	}

	async deletePost(id: string): Promise<void> {
		await this.api.collection('posts').delete(id);
		this.posts.update((posts) => posts.filter((p) => p.id !== id));
	}
}
```

## Platform Behavior

- **SSR**: Direct database access (no HTTP overhead)
- **Browser**: HTTP calls to `/api/*`
- **Same interface** - code works identically on both platforms

## TransferState (SSR Hydration)

TransferState is **enabled by default** for read operations. Data fetched during SSR is cached and reused on browser hydration.

```typescript
// Default: TransferState enabled (no duplicate fetch on hydration)
const posts = await this.api.collection<Post>('posts').find({ limit: 10 });

// Opt-out: always fetch fresh data
const posts = await this.api.collection<Post>('posts').find({ limit: 10, transfer: false });
```

Requires `provideClientHydration()` in app config.

## Error Handling

```typescript
try {
	await this.api.collection('posts').create({ title: '' });
} catch (error) {
	if (error instanceof ValidationError) {
		console.error('Validation failed:', error.errors);
	}
}
```
