---
name: sanity-cms
description: A headless CMS that provides a flexible content model and powerful APIs. Use for structured content management with type-safe queries for Williamstown SC.
---

# sanity-cms

## Instructions

Follow documentation from https://www.sanity.io/learn/llms.txt to implement Sanity CMS in the project. This skill provides project-specific patterns for sports club content modeling, TypeScript integration, and Next.js optimization.

## Content Modeling for Sports Clubs

### Core Schema Types

The Williamstown SC website requires these primary content types:

1. **blogPost** - Club news, announcements, match reports
2. **event** - Matches, training sessions, club events
3. **player** - Team roster and player profiles
4. **fixture** - Match schedule, results, and statistics
5. **sponsor** - Club sponsors and partners
6. **page** - Static pages (About, Contact, etc.)
7. **teamMember** - Coaching staff and committee members

## Schema Best Practices

### Naming Conventions

Follow these conventions for consistency:

```typescript
// Schema files: camelCase.ts
blogPost.ts;
teamMember.ts;
fixtureResult.ts;

// Field names: camelCase
publishedAt;
featuredImage;
homeTeamScore;

// Document types: camelCase
blogPost;
teamMember;
fixtureResult;
```

### Required Fields Pattern

Every document type should include these base fields:

```typescript
{
  name: 'blogPost', // or your document type
  type: 'document',
  fields: [
    {
      name: 'title',
      type: 'string',
      title: 'Title',
      validation: (Rule) => Rule.required()
    },
    {
      name: 'slug',
      type: 'slug',
      title: 'Slug',
      options: {
        source: 'title',
        maxLength: 96,
      },
      validation: (Rule) => Rule.required()
    },
    // _createdAt and _updatedAt are automatic
    // Additional fields...
  ]
}
```

### SEO Metadata Pattern

Reusable SEO object for all content types:

```typescript
// schemas/objects/seo.ts
export default {
  name: 'seo',
  title: 'SEO',
  type: 'object',
  fields: [
    {
      name: 'metaTitle',
      type: 'string',
      title: 'Meta Title',
      description: 'Title for search engines (50-60 characters)',
      validation: (Rule) => Rule.max(60)
    },
    {
      name: 'metaDescription',
      type: 'text',
      title: 'Meta Description',
      description: 'Description for search engines (120-160 characters)',
      validation: (Rule) => Rule.min(120).max(160)
    },
    {
      name: 'ogImage',
      type: 'image',
      title: 'Social Share Image',
      description: 'Recommended: 1200x630px'
    },
  ]
}

// Use in document schemas:
{
  name: 'seo',
  type: 'seo',
  title: 'SEO Settings'
}
```

## Example Document Schemas

### Blog Post Schema

```typescript
// schemas/documents/blogPost.ts
export default {
	name: 'blogPost',
	title: 'Blog Post',
	type: 'document',
	fields: [
		{
			name: 'title',
			type: 'string',
			title: 'Title',
			validation: (Rule) => Rule.required()
		},
		{
			name: 'slug',
			type: 'slug',
			title: 'Slug',
			options: {
				source: 'title',
				maxLength: 96
			},
			validation: (Rule) => Rule.required()
		},
		{
			name: 'publishedAt',
			type: 'datetime',
			title: 'Published At',
			validation: (Rule) => Rule.required()
		},
		{
			name: 'excerpt',
			type: 'text',
			title: 'Excerpt',
			description: 'Short summary for cards and previews',
			rows: 3,
			validation: (Rule) => Rule.max(200)
		},
		{
			name: 'mainImage',
			type: 'image',
			title: 'Main Image',
			options: {
				hotspot: true
			},
			fields: [
				{
					name: 'alt',
					type: 'string',
					title: 'Alternative Text',
					validation: (Rule) => Rule.required()
				}
			]
		},
		{
			name: 'categories',
			type: 'array',
			title: 'Categories',
			of: [{ type: 'reference', to: [{ type: 'category' }] }]
		},
		{
			name: 'body',
			type: 'array',
			title: 'Body',
			of: [
				{ type: 'block' },
				{
					type: 'image',
					options: { hotspot: true },
					fields: [
						{
							name: 'alt',
							type: 'string',
							title: 'Alternative Text'
						}
					]
				}
			]
		},
		{
			name: 'featured',
			type: 'boolean',
			title: 'Featured Post',
			description: 'Display on homepage'
		},
		{
			name: 'seo',
			type: 'seo',
			title: 'SEO Settings'
		}
	],
	preview: {
		select: {
			title: 'title',
			media: 'mainImage',
			subtitle: 'publishedAt'
		}
	}
};
```

### Fixture/Match Result Schema

```typescript
// schemas/documents/fixture.ts
export default {
	name: 'fixture',
	title: 'Fixture',
	type: 'document',
	fields: [
		{
			name: 'matchDate',
			type: 'datetime',
			title: 'Match Date & Time',
			validation: (Rule) => Rule.required()
		},
		{
			name: 'competition',
			type: 'string',
			title: 'Competition',
			options: {
				list: [
					{ title: 'NPL Victoria', value: 'npl' },
					{ title: 'FFA Cup', value: 'ffa-cup' },
					{ title: 'State League', value: 'state-league' }
				]
			}
		},
		{
			name: 'homeTeam',
			type: 'string',
			title: 'Home Team',
			validation: (Rule) => Rule.required()
		},
		{
			name: 'awayTeam',
			type: 'string',
			title: 'Away Team',
			validation: (Rule) => Rule.required()
		},
		{
			name: 'homeScore',
			type: 'number',
			title: 'Home Score',
			description: 'Leave empty for upcoming matches'
		},
		{
			name: 'awayScore',
			type: 'number',
			title: 'Away Score',
			description: 'Leave empty for upcoming matches'
		},
		{
			name: 'venue',
			type: 'string',
			title: 'Venue',
			validation: (Rule) => Rule.required()
		},
		{
			name: 'isHomeGame',
			type: 'boolean',
			title: 'Is Home Game',
			description: 'Is this a Williamstown SC home game?'
		},
		{
			name: 'matchReport',
			type: 'array',
			title: 'Match Report',
			description: 'Detailed match report (optional)',
			of: [{ type: 'block' }]
		},
		{
			name: 'highlights',
			type: 'url',
			title: 'Highlights Video URL',
			description: 'YouTube or other video platform URL'
		}
	],
	preview: {
		select: {
			homeTeam: 'homeTeam',
			awayTeam: 'awayTeam',
			homeScore: 'homeScore',
			awayScore: 'awayScore',
			date: 'matchDate'
		},
		prepare({ homeTeam, awayTeam, homeScore, awayScore, date }) {
			const score =
				homeScore !== undefined && awayScore !== undefined ? `${homeScore}-${awayScore}` : 'vs';
			return {
				title: `${homeTeam} ${score} ${awayTeam}`,
				subtitle: new Date(date).toLocaleDateString()
			};
		}
	}
};
```

### Player Profile Schema

```typescript
// schemas/documents/player.ts
export default {
	name: 'player',
	title: 'Player',
	type: 'document',
	fields: [
		{
			name: 'name',
			type: 'string',
			title: 'Full Name',
			validation: (Rule) => Rule.required()
		},
		{
			name: 'slug',
			type: 'slug',
			title: 'Slug',
			options: {
				source: 'name',
				maxLength: 96
			}
		},
		{
			name: 'number',
			type: 'number',
			title: 'Squad Number',
			validation: (Rule) => Rule.min(1).max(99)
		},
		{
			name: 'position',
			type: 'string',
			title: 'Position',
			options: {
				list: [
					{ title: 'Goalkeeper', value: 'GK' },
					{ title: 'Defender', value: 'DEF' },
					{ title: 'Midfielder', value: 'MID' },
					{ title: 'Forward', value: 'FWD' }
				]
			},
			validation: (Rule) => Rule.required()
		},
		{
			name: 'photo',
			type: 'image',
			title: 'Player Photo',
			options: {
				hotspot: true
			},
			fields: [
				{
					name: 'alt',
					type: 'string',
					title: 'Alternative Text',
					validation: (Rule) => Rule.required()
				}
			]
		},
		{
			name: 'bio',
			type: 'text',
			title: 'Biography',
			rows: 4
		},
		{
			name: 'stats',
			type: 'object',
			title: 'Season Statistics',
			fields: [
				{
					name: 'appearances',
					type: 'number',
					title: 'Appearances',
					initialValue: 0
				},
				{
					name: 'goals',
					type: 'number',
					title: 'Goals',
					initialValue: 0
				},
				{
					name: 'assists',
					type: 'number',
					title: 'Assists',
					initialValue: 0
				}
			]
		}
	],
	preview: {
		select: {
			title: 'name',
			number: 'number',
			position: 'position',
			media: 'photo'
		},
		prepare({ title, number, position, media }) {
			return {
				title: `${number ? `#${number} ` : ''}${title}`,
				subtitle: position,
				media
			};
		}
	}
};
```

## TypeScript Integration

### Generate Types

Add to your `package.json`:

```json
{
	"scripts": {
		"sanity:typegen": "sanity schema extract && sanity typegen generate"
	}
}
```

Run after schema changes:

```bash
npm run sanity:typegen
```

### Use Generated Types

```typescript
// Import generated types
import type {BlogPost, Fixture, Player} from '@/sanity/types'

// Type-safe data fetching
const posts: BlogPost[] = await client.fetch(query)

// Type-safe component props
interface NewsCardProps {
  post: BlogPost
}

const NewsCard = ({post}: NewsCardProps) => {
  return (
    <article>
      <h2>{post.title}</h2>
      <p>{post.excerpt}</p>
    </article>
  )
}
```

### Type-safe GROQ Queries

```typescript
import { groq } from 'next-sanity';
import type { BlogPost } from '@/sanity/types';

const query = groq`
  *[_type == "blogPost"] | order(publishedAt desc) {
    _id,
    title,
    slug,
    publishedAt,
    excerpt,
    "mainImage": mainImage.asset->url,
    "categories": categories[]->title
  }
`;

const posts = await client.fetch<BlogPost[]>(query);
```

## GROQ Query Patterns

### Common Queries

#### Latest Blog Posts

```groq
*[_type == "blogPost"] | order(publishedAt desc)[0...10] {
  _id,
  title,
  slug,
  excerpt,
  publishedAt,
  "image": mainImage.asset->url,
  "imageAlt": mainImage.alt,
  "categories": categories[]->title,
  featured
}
```

#### Upcoming Fixtures

```groq
*[_type == "fixture" && matchDate > now()] | order(matchDate asc) {
  _id,
  matchDate,
  homeTeam,
  awayTeam,
  venue,
  competition,
  isHomeGame
}
```

#### Past Results

```groq
*[_type == "fixture" && matchDate < now() && defined(homeScore)] | order(matchDate desc)[0...10] {
  _id,
  matchDate,
  homeTeam,
  awayTeam,
  homeScore,
  awayScore,
  venue,
  isHomeGame
}
```

#### Team Roster by Position

```groq
*[_type == "player"] | order(position asc, number asc) {
  _id,
  name,
  number,
  position,
  "photo": photo.asset->url,
  "photoAlt": photo.alt,
  stats
}
```

#### Single Post with Full Content

```groq
*[_type == "blogPost" && slug.current == $slug][0] {
  _id,
  title,
  slug,
  publishedAt,
  excerpt,
  body,
  "mainImage": mainImage.asset->url,
  "mainImageAlt": mainImage.alt,
  "categories": categories[]->{
    _id,
    title,
    slug
  },
  seo
}
```

### Reference Expansion

```groq
// Single reference with ->
"author": author->name,
"category": category->title,

// Array of references with []->
"tags": tags[]->title,
"players": players[]-> {
  name,
  number,
  position
},

// Nested references
"author": author-> {
  name,
  "image": image.asset->url
}
```

### Filtering & Sorting

```groq
// Filter by multiple conditions
*[_type == "blogPost" && featured == true && publishedAt < now()]

// Filter with references
*[_type == "blogPost" && references(*[_type == "category" && title == "News"]._id)]

// Date filtering
*[_type == "fixture" && matchDate >= $startDate && matchDate <= $endDate]

// Sorting
| order(publishedAt desc)
| order(matchDate asc)
| order(position asc, number asc) // Multiple fields
```

### Pagination

```groq
// First 10 results
*[_type == "blogPost"] | order(publishedAt desc)[0...10]

// Next 10 results (11-20)
*[_type == "blogPost"] | order(publishedAt desc)[10...20]

// Using variables
*[_type == "blogPost"] | order(publishedAt desc)[$start...$end]
```

## Image Optimization

### Image Schema with Validation

```typescript
{
  name: 'mainImage',
  type: 'image',
  title: 'Main Image',
  options: {
    hotspot: true, // Enable focal point selection
  },
  fields: [
    {
      name: 'alt',
      type: 'string',
      title: 'Alternative Text',
      description: 'Describe the image for accessibility',
      validation: (Rule) => Rule.required().error('Alt text is required for accessibility')
    },
    {
      name: 'caption',
      type: 'string',
      title: 'Caption',
      description: 'Optional caption to display below image'
    }
  ],
  validation: (Rule) => Rule.required()
}
```

### Image URL Builder

```typescript
// lib/sanity/image.ts
import imageUrlBuilder from '@sanity/image-url';

// Usage:
import { urlFor } from '@/lib/sanity/image';

import { client } from './client';

const builder = imageUrlBuilder(client);

export function urlFor(source: any) {
	return builder.image(source);
}

const imageUrl = urlFor(post.mainImage).width(800).height(600).fit('crop').url();
```

### Next.js Image Integration

```tsx
import Image from 'next/image';
import { urlFor } from '@/lib/sanity/image';

<Image
	src={urlFor(post.mainImage).width(800).height(600).url()}
	alt={post.mainImage.alt}
	width={800}
	height={600}
	className="rounded-lg"
/>;
```

### Responsive Images

```typescript
// Generate srcset for responsive images
function getImageSrcSet(image: any, widths: number[] = [400, 800, 1200]) {
  return widths.map(width =>
    `${urlFor(image).width(width).url()} ${width}w`
  ).join(', ')
}

// Usage in component:
<img
  src={urlFor(image).width(800).url()}
  srcSet={getImageSrcSet(image)}
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 800px"
  alt={image.alt}
/>
```

## Portable Text (Rich Text)

### Schema Configuration

```typescript
{
  name: 'body',
  title: 'Body',
  type: 'array',
  of: [
    {
      type: 'block',
      marks: {
        decorators: [
          {title: 'Strong', value: 'strong'},
          {title: 'Emphasis', value: 'em'},
          {title: 'Underline', value: 'underline'},
        ],
        annotations: [
          {
            name: 'link',
            type: 'object',
            title: 'Link',
            fields: [
              {
                name: 'href',
                type: 'url',
                title: 'URL',
                validation: (Rule) => Rule.required()
              }
            ]
          }
        ]
      }
    },
    {
      type: 'image',
      options: {hotspot: true},
      fields: [
        {
          name: 'alt',
          type: 'string',
          title: 'Alternative Text',
          validation: (Rule) => Rule.required()
        },
        {
          name: 'caption',
          type: 'string',
          title: 'Caption'
        }
      ]
    }
  ]
}
```

### Rendering Portable Text

```tsx
import {PortableText} from '@portabletext/react'
import Image from 'next/image'
import {urlFor} from '@/lib/sanity/image'

const components = {
  block: {
    h1: ({children}) => (
      <h1 className="text-4xl font-bold mb-4">{children}</h1>
    ),
    h2: ({children}) => (
      <h2 className="text-3xl font-bold mb-3">{children}</h2>
    ),
    h3: ({children}) => (
      <h3 className="text-2xl font-bold mb-2">{children}</h3>
    ),
    normal: ({children}) => (
      <p className="mb-4 leading-relaxed">{children}</p>
    ),
  },
  marks: {
    link: ({children, value}) => (
      <a
        href={value.href}
        className="text-primary underline hover:text-primary-focus"
        target="_blank"
        rel="noopener noreferrer"
      >
        {children}
      </a>
    ),
  },
  types: {
    image: ({value}) => (
      <figure className="my-8">
        <Image
          src={urlFor(value).width(1200).url()}
          alt={value.alt || 'Blog post image'}
          width={1200}
          height={800}
          className="rounded-lg"
        />
        {value.caption && (
          <figcaption className="text-sm text-center mt-2 text-base-content/70">
            {value.caption}
          </figcaption>
        )}
      </figure>
    ),
  },
}

// Usage:
<PortableText value={post.body} components={components} />
```

## Preview & Draft Mode

### Enable Draft Mode in Next.js

```typescript
// app/api/draft/route.ts
import { draftMode } from 'next/headers';
import { redirect } from 'next/navigation';

export async function GET(request: Request) {
	const { searchParams } = new URL(request.url);
	const secret = searchParams.get('secret');
	const slug = searchParams.get('slug');

	// Verify secret token
	if (secret !== process.env.SANITY_PREVIEW_SECRET) {
		return new Response('Invalid token', { status: 401 });
	}

	// Enable draft mode
	draftMode().enable();

	// Redirect to the path
	redirect(slug || '/');
}
```

### Disable Draft Mode

```typescript
// app/api/exit-draft/route.ts
import { draftMode } from 'next/headers';
import { redirect } from 'next/navigation';

export async function GET() {
	draftMode().disable();
	redirect('/');
}
```

### Fetch with Draft Content

```typescript
import { draftMode } from 'next/headers';
import { client } from '@/lib/sanity/client';

export async function getPosts() {
	const preview = draftMode().isEnabled;

	const posts = await client.fetch(
		query,
		{},
		{
			perspective: preview ? 'previewDrafts' : 'published',
			// Disable caching in preview mode
			cache: preview ? 'no-store' : 'force-cache',
			next: {
				revalidate: preview ? 0 : 3600
			}
		}
	);

	return posts;
}
```

## Schema Organization

### Recommended Directory Structure

```
sanity/
├── schemas/
│   ├── documents/          # Top-level content types
│   │   ├── blogPost.ts
│   │   ├── event.ts
│   │   ├── fixture.ts
│   │   ├── page.ts
│   │   ├── player.ts
│   │   └── sponsor.ts
│   ├── objects/            # Reusable objects
│   │   ├── seo.ts
│   │   ├── socialLinks.ts
│   │   └── stats.ts
│   └── index.ts            # Export all schemas
├── lib/
│   ├── client.ts           # Sanity client config
│   └── image.ts            # Image URL builder
├── env.ts                  # Environment variables
└── types.ts                # Generated TypeScript types
```

### Schema Index File

```typescript
// schemas/index.ts
import blogPost from './documents/blogPost';
import event from './documents/event';
import fixture from './documents/fixture';
import player from './documents/player';
import seo from './objects/seo';

export const schemaTypes = [
	// Documents
	blogPost,
	event,
	fixture,
	player,
	// Objects
	seo
];
```

## Validation Patterns

### Common Validations

```typescript
// Required field
validation: (Rule) => Rule.required();

// String length
validation: (Rule) => Rule.min(50).max(160);

// Number range
validation: (Rule) => Rule.min(0).max(100);

// URL validation
validation: (Rule) =>
	Rule.uri({
		scheme: ['http', 'https']
	});

// Custom validation
validation: (Rule) =>
	Rule.custom((value) => {
		if (!value) {
			return 'This field is required';
		}
		if (value.length < 10) {
			return 'Must be at least 10 characters';
		}
		return true;
	});

// Conditional validation
validation: (Rule) =>
	Rule.custom((value, context) => {
		if (context.document.featured && !value) {
			return 'Featured posts must have an excerpt';
		}
		return true;
	});
```

## Content Relationships

### References

```typescript
// Single reference
{
  name: 'author',
  title: 'Author',
  type: 'reference',
  to: [{type: 'person'}],
  validation: (Rule) => Rule.required()
}

// Multiple references
{
  name: 'categories',
  title: 'Categories',
  type: 'array',
  of: [{type: 'reference', to: [{type: 'category'}]}]
}

// Reference with preview
{
  name: 'relatedPosts',
  title: 'Related Posts',
  type: 'array',
  of: [
    {
      type: 'reference',
      to: [{type: 'blogPost'}],
      options: {
        filter: '_id != $id',
        filterParams: {id: '_id'}
      }
    }
  ]
}
```

### Querying References

```groq
// Expand single reference
"author": author-> {
  name,
  "image": image.asset->url
}

// Expand array of references
"categories": categories[]-> {
  _id,
  title,
  slug
}

// Filter by reference
*[_type == "blogPost" && references(*[_type == "category" && slug.current == $categorySlug]._id)]
```

## Performance Optimization

### Client Configuration

```typescript
// lib/sanity/client.ts
import { createClient } from 'next-sanity';

export const client = createClient({
	projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID!,
	dataset: process.env.NEXT_PUBLIC_SANITY_DATASET!,
	apiVersion: '2024-01-01',
	useCdn: process.env.NODE_ENV === 'production',
	perspective: 'published'
});
```

### Next.js Caching

```typescript
// On-demand revalidation
import { revalidateTag } from 'next/cache';

// Fetch with caching
const posts = await client.fetch(
	query,
	{},
	{
		cache: 'force-cache',
		next: {
			revalidate: 3600, // Revalidate every hour
			tags: ['posts'] // Tag for on-demand revalidation
		}
	}
);

export async function POST(request: Request) {
	revalidateTag('posts');
	return Response.json({ revalidated: true });
}
```

### GROQ Query Optimization

```groq
// Use select() to limit fields
*[_type == "blogPost"]{
  _id,
  title,
  slug,
  publishedAt
}

// Avoid fetching large fields unless needed
*[_type == "blogPost"]{
  ..., // All fields
  body  // Exclude this for list views
}

// Use pagination
*[_type == "blogPost"] | order(publishedAt desc)[0...10]

// Limit reference depth
"author": author->{name} // Only fetch name, not entire document
```

## Webhooks & Real-time Updates

### Sanity Webhook Setup

Configure webhooks in Sanity dashboard:

1. Go to API → Webhooks
2. Add webhook URL: `https://yoursite.com/api/revalidate`
3. Select dataset and events (create, update, delete)

### Next.js Revalidation Endpoint

```typescript
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
	const body = await request.json();
	const secret = request.headers.get('x-sanity-webhook-secret');

	// Verify webhook secret
	if (secret !== process.env.SANITY_WEBHOOK_SECRET) {
		return NextResponse.json({ message: 'Invalid secret' }, { status: 401 });
	}

	// Revalidate based on document type
	const { _type } = body;

	if (_type === 'blogPost') {
		revalidateTag('posts');
		revalidatePath('/news');
	}

	if (_type === 'fixture') {
		revalidateTag('fixtures');
		revalidatePath('/fixtures');
	}

	return NextResponse.json({ revalidated: true });
}
```

## Best Practices

### Content Modeling

1. **Keep schemas focused** - One document type per concern
2. **Use objects for reusability** - SEO, social links, etc.
3. **Add descriptions** - Help content editors understand fields
4. **Set sensible defaults** - Use `initialValue` for common values
5. **Validate thoroughly** - Prevent bad data at input time

### TypeScript

1. **Generate types after schema changes** - Keep types in sync
2. **Use type guards** - Verify data structure at runtime
3. **Type query results** - Add type annotations to fetch calls

### Performance

1. **Use CDN for images** - Sanity automatically serves via CDN
2. **Implement ISR** - Use Next.js revalidation for fresh content
3. **Limit query fields** - Only fetch what you need
4. **Paginate large datasets** - Don't fetch everything at once

### Security

1. **Never expose tokens** - Use environment variables
2. **Validate webhook secrets** - Verify incoming requests
3. **Sanitize user input** - Even from CMS (Portable Text is safe by default)

## Common Pitfalls

❌ **Don't:**

- Fetch entire documents when you only need a few fields
- Store computed values that can be calculated
- Create deeply nested schemas (max 3-4 levels)
- Use references when a simple string field would work
- Skip alt text on images

✅ **Do:**

- Use GROQ projections to limit fields
- Calculate derived values in queries or components
- Keep schemas flat when possible
- Reference only when you need to share/update content
- Always require alt text for accessibility

## Quick Reference

### GROQ Syntax

```groq
*[filter] | order(field direction)[range] {projection}

// Examples:
*[_type == "blogPost"]                    // All blog posts
*[_type == "blogPost" && featured]         // Filtered
| order(publishedAt desc)                  // Sorted
[0...10]                                   // Paginated
{title, slug, "image": mainImage.asset->url}  // Projected
```

### Common Field Types

```
string, text, number, boolean, datetime, date
slug, url, email
image, file
array, object
reference
block (Portable Text)
```

### Validation Methods

```
required(), min(), max(), length(), regex(), email(), url(), custom()
```
