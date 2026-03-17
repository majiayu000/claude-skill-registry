---
name: github-trending
description: Fetch and display GitHub trending repositories and developers. Use when building dashboards showing trending repos, discovering popular projects, or tracking GitHub trends. Triggers on GitHub trending, trending repos, popular repositories, GitHub discover.
---

# GitHub Trending Data

Access GitHub trending repositories and developers data.

## Important Note

**GitHub does NOT provide an official trending API.** The trending page at `github.com/trending` must be scraped directly or use the GitHub Search API as an alternative.

## Approach 1: Direct Web Scraping (Recommended)

Scrape `github.com/trending` directly using Cheerio:

```typescript
import * as cheerio from 'cheerio';

interface TrendingRepo {
  owner: string;
  name: string;
  fullName: string;
  url: string;
  description: string;
  language: string;
  languageColor: string;
  stars: number;
  forks: number;
  starsToday: number;
}

async function scrapeTrending(options: {
  language?: string;
  since?: 'daily' | 'weekly' | 'monthly';
} = {}): Promise<TrendingRepo[]> {
  // Build URL: github.com/trending or github.com/trending/typescript?since=weekly
  let url = 'https://github.com/trending';
  if (options.language) {
    url += `/${encodeURIComponent(options.language)}`;
  }
  if (options.since) {
    url += `?since=${options.since}`;
  }

  const response = await fetch(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (compatible; TrendingBot/1.0)',
    },
  });
  
  if (!response.ok) {
    throw new Error(`Failed to fetch trending: ${response.status}`);
  }

  const html = await response.text();
  const $ = cheerio.load(html);
  const repos: TrendingRepo[] = [];

  // Each trending repo is in an article.Box-row element
  $('article.Box-row').each((_, element) => {
    const $el = $(element);
    
    // Get repo link (e.g., /owner/repo)
    const repoLink = $el.find('h2 a').attr('href')?.trim() || '';
    const [, owner, name] = repoLink.split('/');
    
    // Get description
    const description = $el.find('p.col-9').text().trim();
    
    // Get language
    const language = $el.find('[itemprop="programmingLanguage"]').text().trim();
    
    // Get language color from the colored dot
    const langColorStyle = $el.find('.repo-language-color').attr('style') || '';
    const langColorMatch = langColorStyle.match(/background-color:\s*([^;]+)/);
    const languageColor = langColorMatch ? langColorMatch[1].trim() : '';
    
    // Get stars (total)
    const starsText = $el.find('a[href$="/stargazers"]').text().trim();
    const stars = parseNumber(starsText);
    
    // Get forks
    const forksText = $el.find('a[href$="/forks"]').text().trim();
    const forks = parseNumber(forksText);
    
    // Get stars today/this week/this month
    const starsTodayText = $el.find('.float-sm-right, .d-inline-block.float-sm-right').text().trim();
    const starsToday = parseNumber(starsTodayText);

    if (owner && name) {
      repos.push({
        owner,
        name,
        fullName: `${owner}/${name}`,
        url: `https://github.com${repoLink}`,
        description,
        language,
        languageColor,
        stars,
        forks,
        starsToday,
      });
    }
  });

  return repos;
}

function parseNumber(text: string): number {
  const clean = text.replace(/,/g, '').trim();
  if (clean.includes('k')) {
    return Math.round(parseFloat(clean) * 1000);
  }
  return parseInt(clean) || 0;
}
```

## Approach 2: GitHub Search API (Official Alternative)

Use GitHub's Search API to find recently created repos with high stars:

```typescript
interface GitHubSearchResult {
  total_count: number;
  items: GitHubRepo[];
}

interface GitHubRepo {
  full_name: string;
  html_url: string;
  description: string;
  language: string;
  stargazers_count: number;
  forks_count: number;
  created_at: string;
}

async function getTrendingViaSearch(options: {
  language?: string;
  days?: number;
  minStars?: number;
} = {}): Promise<GitHubRepo[]> {
  const days = options.days || 7;
  const minStars = options.minStars || 100;
  
  // Calculate date N days ago
  const date = new Date();
  date.setDate(date.getDate() - days);
  const since = date.toISOString().split('T')[0];

  // Build search query
  const queryParts = [
    `created:>${since}`,
    `stars:>=${minStars}`,
  ];
  if (options.language) {
    queryParts.push(`language:${options.language}`);
  }
  const query = queryParts.join(' ');

  const response = await fetch(
    `https://api.github.com/search/repositories?q=${encodeURIComponent(query)}&sort=stars&order=desc&per_page=25`,
    {
      headers: {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`, // Optional but recommended
        'User-Agent': 'TrendingApp/1.0',
      },
    }
  );

  if (!response.ok) {
    throw new Error(`GitHub API error: ${response.status}`);
  }

  const data: GitHubSearchResult = await response.json();
  return data.items;
}
```

**Note:** The Search API has rate limits (10 requests/minute unauthenticated, 30/minute with token).

## Next.js API Route (Server-Side Scraping)

```typescript
// app/api/trending/route.ts
import { NextRequest } from 'next/server';
import * as cheerio from 'cheerio';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const language = searchParams.get('language') || '';
  const since = searchParams.get('since') || 'daily';

  try {
    let url = 'https://github.com/trending';
    if (language) url += `/${encodeURIComponent(language)}`;
    url += `?since=${since}`;

    const response = await fetch(url, {
      headers: { 'User-Agent': 'Mozilla/5.0 (compatible)' },
      next: { revalidate: 3600 }, // Cache for 1 hour
    });

    const html = await response.text();
    const repos = parseGitHubTrending(html);
    
    return Response.json(repos);
  } catch (error) {
    console.error('Trending scrape failed:', error);
    return Response.json(
      { error: 'Failed to fetch trending repos' },
      { status: 500 }
    );
  }
}

function parseGitHubTrending(html: string) {
  const $ = cheerio.load(html);
  const repos: any[] = [];

  $('article.Box-row').each((_, el) => {
    const $el = $(el);
    const repoLink = $el.find('h2 a').attr('href') || '';
    const [, owner, name] = repoLink.split('/');
    
    repos.push({
      owner,
      name,
      fullName: `${owner}/${name}`,
      url: `https://github.com${repoLink}`,
      description: $el.find('p.col-9').text().trim(),
      language: $el.find('[itemprop="programmingLanguage"]').text().trim(),
      stars: parseNumber($el.find('a[href$="/stargazers"]').text()),
      forks: parseNumber($el.find('a[href$="/forks"]').text()),
      starsToday: parseNumber($el.find('.float-sm-right').text()),
    });
  });

  return repos;
}

function parseNumber(text: string): number {
  const clean = text.replace(/,/g, '').trim();
  if (clean.includes('k')) return Math.round(parseFloat(clean) * 1000);
  return parseInt(clean) || 0;
}
```

## React Hook

```tsx
import { useState, useEffect } from 'react';

function useTrending(options: { language?: string; since?: string } = {}) {
  const [repos, setRepos] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchTrending() {
      setIsLoading(true);
      try {
        const params = new URLSearchParams();
        if (options.language) params.set('language', options.language);
        if (options.since) params.set('since', options.since);

        const response = await fetch(`/api/trending?${params}`);
        if (!response.ok) throw new Error('Failed to fetch');
        setRepos(await response.json());
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setIsLoading(false);
      }
    }

    fetchTrending();
  }, [options.language, options.since]);

  return { repos, isLoading, error };
}
```

## Important Considerations

1. **No Official API**: GitHub's trending page has no official API - scraping is the only option
2. **Rate Limiting**: Respect GitHub's servers - cache aggressively
3. **HTML Structure Changes**: GitHub may change their HTML - monitor for breakages
4. **User-Agent**: Always include a User-Agent header
5. **Server-Side Only**: Do scraping server-side to avoid CORS issues

## Resources

- **GitHub Trending Page**: https://github.com/trending
- **GitHub Search API**: https://docs.github.com/en/rest/search
