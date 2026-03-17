---
name: tmdb-integration
displayName: "TMDB Integration"
description: "TMDB (The Movie Database) API integration for React Native TV streaming apps. Use when users need help with movie/TV show data, poster images, search functionality, trending content, video trailers from TMDB, API authentication, rate limiting, or TypeScript types for TMDB responses."
keywords: ["tmdb", "movie-database", "api-integration", "movie-data", "tv-shows", "poster-images", "search", "trending", "trailers", "authentication", "rate-limiting", "typescript", "axios", "react-hooks"]
author: "Giovanni Laquidara"
---

# TMDB Integration Skill

You are an expert in integrating The Movie Database (TMDB) API with React Native TV applications. This skill activates when users ask about:

- Fetching movie or TV show data
- Displaying poster and backdrop images
- Implementing search functionality
- Getting trending content
- Fetching video trailers
- TMDB authentication and API keys
- Rate limiting and optimization
- TypeScript types for TMDB responses

## Authentication

TMDB offers two equivalent authentication methods:

### API Key (Query Parameter)

```typescript
const url = `https://api.themoviedb.org/3/movie/550?api_key=${API_KEY}`;
```

### Bearer Token (Header) - Recommended

```typescript
const headers = {
  'Authorization': `Bearer ${ACCESS_TOKEN}`,
  'Accept': 'application/json'
};
```

**Both tokens are generated in your TMDB account settings.** Bearer token is recommended for production as credentials aren't visible in URLs.

## Image URL Construction

**Base URL:** `https://image.tmdb.org/t/p/`

**Official Sizes (use these for CDN caching):**

| Type | Available Sizes |
|------|-----------------|
| Poster | w92, w154, w185, w342, w500, w780, original |
| Backdrop | w300, w780, w1280, original |
| Logo | w45, w92, w154, w185, w300, w500, original |
| Profile | w45, w185, h632, original |

**Image URL Helper:**

```typescript
const TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/';

type PosterSize = 'w92' | 'w154' | 'w185' | 'w342' | 'w500' | 'w780' | 'original';
type BackdropSize = 'w300' | 'w780' | 'w1280' | 'original';

export function getPosterUrl(path: string | null, size: PosterSize = 'w500'): string | null {
  if (!path) return null;
  return `${TMDB_IMAGE_BASE}${size}${path}`;
}

export function getBackdropUrl(path: string | null, size: BackdropSize = 'w1280'): string | null {
  if (!path) return null;
  return `${TMDB_IMAGE_BASE}${size}${path}`;
}
```

**Important:** Only use official sizes - non-standard sizes bypass CDN caching and are 10-50x slower.

## Essential Endpoints

### Trending Content

```
GET /trending/{media_type}/{time_window}

media_type: movie, tv, person, all
time_window: day, week
```

### Discovery

```
GET /discover/movie
GET /discover/tv

Parameters:
- sort_by: popularity.desc, vote_average.desc, release_date.desc
- with_genres: 28,12 (AND) or 28|12 (OR)
- page: pagination (20 items per page)
```

### Search

```
GET /search/movie?query={term}
GET /search/tv?query={term}
GET /search/multi?query={term}  // Movies, TV, and people
```

### Details with Related Data

```
GET /movie/{id}?append_to_response=videos,credits,images
GET /tv/{id}?append_to_response=videos,credits,images,season/1,season/2
```

**append_to_response** combines multiple requests into one (doesn't count toward rate limits).

### Genres

```
GET /genre/movie/list
GET /genre/tv/list
```

## TypeScript Interfaces

```typescript
// Base types
export interface Movie {
  id: number;
  title: string;
  overview: string;
  poster_path: string | null;
  backdrop_path: string | null;
  release_date: string;
  vote_average: number;
  vote_count: number;
  popularity: number;
  genre_ids?: number[];
  adult: boolean;
}

export interface TVShow {
  id: number;
  name: string;
  overview: string;
  poster_path: string | null;
  backdrop_path: string | null;
  first_air_date: string;
  vote_average: number;
  vote_count: number;
  popularity: number;
  genre_ids?: number[];
  origin_country: string[];
}

export interface TMDBResponse<T> {
  page: number;
  results: T[];
  total_pages: number;
  total_results: number;
}

// Detail types
export interface MovieDetails extends Movie {
  budget: number;
  revenue: number;
  runtime: number;
  status: string;
  tagline: string;
  genres: Genre[];
  production_companies: ProductionCompany[];
  credits?: Credits;
  videos?: { results: Video[] };
  images?: Images;
}

export interface TVDetails extends TVShow {
  number_of_episodes: number;
  number_of_seasons: number;
  episode_run_time: number[];
  seasons: Season[];
  networks: Network[];
  status: string;
  credits?: Credits;
  videos?: { results: Video[] };
}

export interface Genre {
  id: number;
  name: string;
}

export interface Video {
  id: string;
  key: string;           // YouTube/Vimeo video ID
  name: string;
  site: 'YouTube' | 'Vimeo';
  size: number;
  type: 'Trailer' | 'Teaser' | 'Clip' | 'Featurette' | 'Behind the Scenes';
  official: boolean;
  published_at: string;
}

export interface Credits {
  cast: CastMember[];
  crew: CrewMember[];
}

export interface CastMember {
  id: number;
  name: string;
  character: string;
  profile_path: string | null;
  order: number;
}

export interface CrewMember {
  id: number;
  name: string;
  job: string;
  department: string;
  profile_path: string | null;
}

export interface Season {
  id: number;
  season_number: number;
  name: string;
  overview: string;
  air_date: string;
  episode_count: number;
  poster_path: string | null;
}

export interface Episode {
  id: number;
  name: string;
  overview: string;
  episode_number: number;
  season_number: number;
  still_path: string | null;
  air_date: string;
  runtime: number;
  vote_average: number;
}
```

## Axios Client Setup

```typescript
import axios from 'axios';

const TMDB_BASE_URL = 'https://api.themoviedb.org/3';

const tmdbClient = axios.create({
  baseURL: TMDB_BASE_URL,
  timeout: 10000,
  headers: {
    'Accept': 'application/json',
    'Authorization': `Bearer ${process.env.TMDB_ACCESS_TOKEN}`,
  },
});

// Add default language
tmdbClient.interceptors.request.use((config) => {
  config.params = {
    ...config.params,
    language: 'en-US',
  };
  return config;
});

// Error handling
tmdbClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 429) {
      // Rate limited - implement retry with backoff
      console.warn('TMDB rate limit hit');
    }
    return Promise.reject(error);
  }
);

export default tmdbClient;
```

## React Native Hooks

### useTrending Hook

```typescript
import { useState, useEffect } from 'react';
import tmdbClient from '../services/tmdbClient';
import { Movie, TVShow, TMDBResponse } from '../types/tmdb';

type MediaType = 'movie' | 'tv' | 'all';
type TimeWindow = 'day' | 'week';

export function useTrending<T extends Movie | TVShow>(
  mediaType: MediaType = 'movie',
  timeWindow: TimeWindow = 'week'
) {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchTrending() {
      try {
        setLoading(true);
        const response = await tmdbClient.get<TMDBResponse<T>>(
          `/trending/${mediaType}/${timeWindow}`
        );
        if (!cancelled) {
          setData(response.data.results);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err as Error);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchTrending();
    return () => { cancelled = true; };
  }, [mediaType, timeWindow]);

  return { data, loading, error };
}
```

### useMovieDetails Hook

```typescript
export function useMovieDetails(movieId: number) {
  const [movie, setMovie] = useState<MovieDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchDetails() {
      try {
        setLoading(true);
        const response = await tmdbClient.get<MovieDetails>(
          `/movie/${movieId}`,
          {
            params: {
              append_to_response: 'videos,credits,images',
            },
          }
        );
        if (!cancelled) {
          setMovie(response.data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err as Error);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    if (movieId) {
      fetchDetails();
    }
    return () => { cancelled = true; };
  }, [movieId]);

  return { movie, loading, error };
}
```

### useSearch Hook with Debounce

```typescript
import { useState, useCallback, useRef } from 'react';
import { debounce } from 'lodash';

export function useSearch() {
  const [results, setResults] = useState<(Movie | TVShow)[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const searchRef = useRef(
    debounce(async (query: string) => {
      if (!query.trim()) {
        setResults([]);
        return;
      }

      try {
        setLoading(true);
        const response = await tmdbClient.get('/search/multi', {
          params: { query },
        });
        setResults(response.data.results.filter(
          (item: any) => item.media_type === 'movie' || item.media_type === 'tv'
        ));
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    }, 300)
  );

  const search = useCallback((query: string) => {
    searchRef.current(query);
  }, []);

  return { results, loading, error, search };
}
```

## Rate Limiting

**Current Limits:**
- 50 requests per second
- 20 simultaneous connections per IP

**Optimization Strategies:**

1. **Use append_to_response** - Combine requests (free, no rate limit impact)
2. **Implement caching** - Cache responses with TTL
3. **Debounce searches** - Wait 300ms after user stops typing
4. **Batch requests** - Group API calls with small delays

## Common Pitfalls & Solutions

| Pitfall | Solution |
|---------|----------|
| API key in client-side code | Use backend proxy in production |
| Slow image loading | Only use official sizes (w342, w500, w780) |
| Missing images crash app | Always check for null: `poster_path && getPosterUrl(poster_path)` |
| Wrong video displayed | Filter: `videos.filter(v => v.type === 'Trailer' && v.official)` |
| Rate limit errors | Implement exponential backoff, use append_to_response |
| State update on unmounted component | Use cleanup flag in useEffect |
| Search fires too often | Debounce search input (300-500ms) |
| Can't get all TV episodes | Use `append_to_response=season/1,season/2,...` (max 20) |

## Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 7 | Invalid API key | Check for typos, verify key in settings |
| 10 | Suspended API key | Contact TMDB support |
| 34 | Resource not found | May be temporary - retry once |
| 429 | Rate limit exceeded | Implement backoff, reduce request rate |

## Video URL Construction

```typescript
function getVideoUrl(video: Video): string {
  if (video.site === 'YouTube') {
    return `https://www.youtube.com/watch?v=${video.key}`;
  }
  if (video.site === 'Vimeo') {
    return `https://vimeo.com/${video.key}`;
  }
  return '';
}

// Get official trailer
function getOfficialTrailer(videos: Video[]): Video | undefined {
  return videos.find(v => v.type === 'Trailer' && v.official)
      || videos.find(v => v.type === 'Trailer')
      || videos[0];
}
```

## Resources

- [TMDB API Docs](https://developer.themoviedb.org/docs/getting-started)
- [TMDB API Reference](https://developer.themoviedb.org/reference/getting-started)
- [Image Configuration](https://developer.themoviedb.org/docs/image-basics)
- [Rate Limiting](https://developer.themoviedb.org/docs/rate-limiting)
