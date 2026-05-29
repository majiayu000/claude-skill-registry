---
name: changelog-page
description: |
  Scaffold public changelog page for Next.js apps.
  Creates page, RSS feed, and GitHub API client.
---

# Changelog Page

Scaffold a public changelog page that displays releases.

## Branching

Assumes you start on `master`/`main`. Before scaffolding:

```bash
git checkout -b feat/changelog-page-$(date +%Y%m%d)
```

## Objective

Create a public `/changelog` route that:
- Fetches releases from GitHub Releases API
- Groups releases by minor version
- Provides RSS feed
- Requires no authentication
- Matches app's design

## Components

### 1. GitHub API Client

Create `lib/github-releases.ts`:

```typescript
// See references/github-releases-client.md for full implementation

export interface Release {
  id: number;
  tagName: string;
  name: string;
  body: string;
  publishedAt: string;
  htmlUrl: string;
}

export interface GroupedReleases {
  [minorVersion: string]: Release[];
}

export async function getReleases(): Promise<Release[]> {
  const res = await fetch(
    `https://api.github.com/repos/${process.env.GITHUB_REPO}/releases`,
    {
      headers: {
        Accept: 'application/vnd.github.v3+json',
        // Optional: add token for higher rate limits
        ...(process.env.GITHUB_TOKEN && {
          Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
        }),
      },
      next: { revalidate: 300 }, // Cache for 5 minutes
    }
  );

  if (!res.ok) throw new Error('Failed to fetch releases');
  return res.json();
}

export function groupReleasesByMinor(releases: Release[]): GroupedReleases {
  return releases.reduce((acc, release) => {
    // Extract minor version: v1.2.3 -> v1.2
    const match = release.tagName.match(/^v?(\d+\.\d+)/);
    const minorVersion = match ? `v${match[1]}` : 'other';

    if (!acc[minorVersion]) acc[minorVersion] = [];
    acc[minorVersion].push(release);
    return acc;
  }, {} as GroupedReleases);
}
```

### 2. Changelog Page

Create `app/changelog/page.tsx`:

```tsx
// See references/changelog-page-component.md for full implementation

import { getReleases, groupReleasesByMinor } from '@/lib/github-releases';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Changelog',
  description: 'Latest updates and improvements',
};

export default async function ChangelogPage() {
  const releases = await getReleases();
  const grouped = groupReleasesByMinor(releases);

  return (
    <div className="max-w-3xl mx-auto py-12 px-4">
      <header className="mb-12">
        <h1 className="text-3xl font-bold mb-2">Changelog</h1>
        <p className="text-muted-foreground">
          Latest updates and improvements to {process.env.NEXT_PUBLIC_APP_NAME}
        </p>
        <a
          href="/changelog.xml"
          className="text-sm text-primary hover:underline"
        >
          RSS Feed
        </a>
      </header>

      {Object.entries(grouped)
        .sort(([a], [b]) => b.localeCompare(a, undefined, { numeric: true }))
        .map(([minorVersion, versionReleases]) => (
          <section key={minorVersion} className="mb-12">
            <h2 className="text-xl font-semibold mb-4 sticky top-0 bg-background py-2">
              {minorVersion}
            </h2>

            {versionReleases.map((release) => (
              <article key={release.id} className="mb-8 pl-4 border-l-2 border-border">
                <header className="mb-2">
                  <h3 className="font-medium">
                    {release.name || release.tagName}
                  </h3>
                  <time className="text-sm text-muted-foreground">
                    {new Date(release.publishedAt).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })}
                  </time>
                </header>

                <div
                  className="prose prose-sm dark:prose-invert"
                  dangerouslySetInnerHTML={{ __html: parseMarkdown(release.body) }}
                />
              </article>
            ))}
          </section>
        ))}
    </div>
  );
}
```

### 3. RSS Feed

Create `app/changelog.xml/route.ts`:

```typescript
// See references/rss-feed-route.md for full implementation

import { getReleases } from '@/lib/github-releases';

export async function GET() {
  const releases = await getReleases();
  const appName = process.env.NEXT_PUBLIC_APP_NAME || 'App';
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://example.com';

  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${appName} Changelog</title>
    <link>${siteUrl}/changelog</link>
    <description>Latest updates and improvements</description>
    <language>en</language>
    <atom:link href="${siteUrl}/changelog.xml" rel="self" type="application/rss+xml"/>
    ${releases.slice(0, 20).map(release => `
    <item>
      <title>${escapeXml(release.name || release.tagName)}</title>
      <link>${release.htmlUrl}</link>
      <guid isPermaLink="true">${release.htmlUrl}</guid>
      <pubDate>${new Date(release.publishedAt).toUTCString()}</pubDate>
      <description><![CDATA[${release.body}]]></description>
    </item>`).join('')}
  </channel>
</rss>`;

  return new Response(rss, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=300',
    },
  });
}

function escapeXml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}
```

### 4. Environment Variables

Add to `.env.local` and deployment:

```bash
# Required
GITHUB_REPO=owner/repo  # e.g., "acme/myapp"

# Optional (for higher API rate limits)
GITHUB_TOKEN=ghp_xxx

# For page metadata
NEXT_PUBLIC_APP_NAME=MyApp
NEXT_PUBLIC_SITE_URL=https://myapp.com
```

## Styling

The page should match the app's design. Key considerations:

1. **Use existing design tokens** - Colors, spacing, typography from the app
2. **Prose styling** - Use Tailwind Typography or similar for release notes markdown
3. **Responsive** - Mobile-friendly layout
4. **Dark mode** - Support both themes if app does
5. **Minimal** - Focus on content, not decoration

## No Auth

**Important:** This page must be public. Do not wrap in:
- Clerk's `<SignedIn>`
- Middleware auth checks
- Any session requirements

Users should be able to view changelog without signing in.

## Delegation

For complex styling or app-specific customization:
1. Research the app's existing design patterns
2. Delegate implementation to Codex with clear design requirements
3. Reference `aesthetic-system` and `design-tokens` skills

## Output

After running this skill:
- `/app/changelog/page.tsx` - Main page
- `/app/changelog.xml/route.ts` - RSS feed
- `/lib/github-releases.ts` - API client
- Environment variables documented

Verify by:
1. Running dev server
2. Visiting `/changelog`
3. Checking RSS at `/changelog.xml`
4. Confirming releases display correctly
