---
name: solid-meta-patterns
description: "Solid Meta patterns: wrap app with MetaProvider, use Title/Meta/Link components for head tags, useHead for custom tags. Meta tags with same name/property override each other."
metadata:
  globs:
    - "**/app.tsx"
    - "**/layout*.tsx"
---

# Solid Meta Coding Patterns

## Setup

Wrap app with `<MetaProvider>`:

```tsx
import { MetaProvider, Title, Meta, Link } from "@solidjs/meta";

function App() {
  return (
    <MetaProvider>
      <Title>My App</Title>
      <Meta name="description" content="My app description" />
      <Link rel="canonical" href="https://example.com" />
      {/* Your app content */}
    </MetaProvider>
  );
}
```

## Components

### Title

```tsx
import { Title } from "@solidjs/meta";

<Title>Home - My App</Title>
// Multiple Title components can exist, last one wins
```

### Meta

```tsx
import { Meta } from "@solidjs/meta";

<Meta charset="utf-8" />
<Meta name="viewport" content="width=device-width, initial-scale=1" />
<Meta name="description" content="Page description" />

{/* Open Graph */}
<Meta property="og:title" content="Page Title" />
<Meta property="og:description" content="Page description" />
<Meta property="og:image" content="/og-image.jpg" />

{/* Twitter */}
<Meta name="twitter:card" content="summary_large_image" />
<Meta name="twitter:title" content="Page Title" />
```

**Important:** Meta tags with the same `name` or `property` override each other (last rendered wins).

### Link

```tsx
import { Link } from "@solidjs/meta";

<Link rel="canonical" href="https://example.com/page" />
<Link rel="stylesheet" href="/styles.css" />
<Link rel="preconnect" href="https://fonts.googleapis.com" />
```

### Style

```tsx
import { Style } from "@solidjs/meta";

<Style>{`
  body {
    margin: 0;
  }
`}</Style>
```

### Base

```tsx
import { Base } from "@solidjs/meta";

<Base href="https://example.com/" />
// Set once in root layout
```

## useHead Hook

For custom head tags:

```tsx
import { useHead } from "@solidjs/meta";

function Page() {
  useHead({
    tag: "script",
    props: {
      type: "application/ld+json",
      id: "structured-data"
    },
    setting: {
      close: true, // Required for script/style tags
      escape: false
    },
    id: "structured-data", // Stable ID for SSR hydration
    children: JSON.stringify({
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "Article Title"
    })
  });
  
  return <div>Content</div>;
}
```

## Dynamic Meta Tags

Use signals for reactive content:

```tsx
import { createSignal } from "solid-js";
import { Title, Meta } from "@solidjs/meta";

function ProductPage({ product }) {
  const title = () => `Product: ${product.name}`;
  
  return (
    <>
      <Title>{title()}</Title>
      <Meta name="description" content={product.description} />
      <Meta property="og:title" content={title()} />
      <Meta property="og:image" content={product.image} />
    </>
  );
}
```

## SEO Template

```tsx
function SEO({ title, description, image, url }) {
  return (
    <>
      <Title>{title}</Title>
      <Meta name="description" content={description} />
      <Link rel="canonical" href={url} />
      
      {/* Open Graph */}
      <Meta property="og:title" content={title} />
      <Meta property="og:description" content={description} />
      <Meta property="og:image" content={image} />
      <Meta property="og:url" content={url} />
      
      {/* Twitter */}
      <Meta name="twitter:card" content="summary_large_image" />
      <Meta name="twitter:title" content={title} />
      <Meta name="twitter:description" content={description} />
      <Meta name="twitter:image" content={image} />
    </>
  );
}
```

## SolidStart-Specific Patterns

### Route-Specific Metadata

In SolidStart routes, metadata is automatically scoped to the route:

```tsx
// routes/about.tsx
import { Title, Meta } from "@solidjs/meta";

export default function About() {
  return (
    <>
      <Title>About - My Site</Title>
      <Meta name="description" content="Learn about us" />
      <h1>About</h1>
    </>
  );
}
```

**Key points:**
- Metadata is route-scoped
- Automatically removed when navigating away
- Can use route data for dynamic metadata

### Using Route Data

```tsx
// routes/users/[id].tsx
import { Title, Meta } from "@solidjs/meta";
import { useParams } from "@solidjs/router";
import { createResource } from "solid-js";

export default function UserProfile() {
  const params = useParams();
  const [user] = createResource(() => params.id, fetchUser);

  return (
    <Show when={user()}>
      <Title>{user()!.name} - Profile</Title>
      <Meta name="description" content={user()!.bio} />
      <Meta property="og:image" content={user()!.avatar} />
      <h1>{user()!.name}</h1>
    </Show>
  );
}
```

### Global Metadata in Root

Add site-wide metadata in root layout:

```tsx
// routes/_layout.tsx or app.tsx
import { Meta, Link } from "@solidjs/meta";

export default function RootLayout(props) {
  return (
    <>
      <Meta property="og:site_name" content="My Site" />
      <Meta property="og:image" content="/default-og.jpg" />
      <Link rel="icon" href="/favicon.ico" />
      {props.children}
    </>
  );
}
```

## Best Practices

1. Wrap app with MetaProvider once at root level
2. Use components (`<Title>`, `<Meta>`, `<Link>`) when possible over `useHead`
3. Provide unique IDs for `useHead` tags (important for hydration)
4. Set `close: true` for script/style tags in `useHead`
5. Override meta tags strategically (last rendered wins)
6. Use reactive values for dynamic meta tags
7. Set canonical URLs for SEO
8. Include Open Graph tags for social sharing
9. Use route-scoped metadata for page-specific tags
10. Combine global and route-specific metadata

