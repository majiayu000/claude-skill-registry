---
name: times-square-integration
description: Times Square notebook execution system integration patterns. Use this skill when working with Times Square pages, implementing SSE updates, handling URL parameters, setting up GitHub PR previews, or working with the Times Square API. Covers context providers, data fetching hooks, mock API endpoints, and page routing patterns.
---

# Times Square Integration

Times Square is a notebook execution system integrated into the squareone app for displaying computational notebooks.

## Core Concepts

- **Pages**: Notebooks that can be executed and displayed
- **Parameters**: URL-based parameters for notebook execution
- **SSE (Server-Sent Events)**: Real-time updates during execution
- **GitHub PR Previews**: Preview notebooks from pull requests

## Context Providers

### TimesSquareUrlParametersContext

Manages URL-based state for Times Square pages.

```typescript
import { TimesSquareUrlParametersContext } from '../contexts/TimesSquareUrlParametersContext';

// Provider setup (usually in page)
<TimesSquareUrlParametersContext.Provider value={urlParams}>
  <TimesSquarePage />
</TimesSquareUrlParametersContext.Provider>

// Usage in components
const { getParameter, setParameter } = useContext(TimesSquareUrlParametersContext);

const value = getParameter('myParam');
setParameter('myParam', 'newValue');
```

### TimesSquareHtmlEventsContext

Manages real-time SSE (Server-Sent Events) updates.

```typescript
import { TimesSquareHtmlEventsContext } from '../contexts/TimesSquareHtmlEventsContext';

// Provider setup
<TimesSquareHtmlEventsContext.Provider value={eventSource}>
  <TimesSquarePage />
</TimesSquareHtmlEventsContext.Provider>

// Usage
const events = useContext(TimesSquareHtmlEventsContext);
// events provides real-time updates from notebook execution
```

## Data Fetching Hooks

### useTimesSquarePage

Custom hook for fetching Times Square page data.

```typescript
import { useTimesSquarePage } from '../hooks/useTimesSquarePage';

function MyComponent({ pageSlug }) {
  const { data, error, isLoading } = useTimesSquarePage(pageSlug);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>{data.displayName}</div>;
}
```

Pattern uses SWR for caching and revalidation.

## Routing Patterns

### Regular Pages

```
/times-square/{page-slug}
```

### GitHub PR Previews

```
/times-square/github-pr/{owner}/{repo}/{commit}
```

Example:
```
/times-square/github-pr/lsst-sqre/times-square-demo/abc123
```

### API Routes

Mock API endpoints in development (`/pages/api/dev/times-square/`):

- `GET /times-square/api/v1/pages` - List pages
- `GET /times-square/api/v1/pages/:page` - Page metadata
- `GET /times-square/api/v1/pages/:page/html` - Rendered HTML
- `GET /times-square/api/v1/pages/:page/htmlstatus` - Execution status
- `GET /times-square/api/v1/pages/:page/htmlevents` - SSE endpoint

## Mock API Endpoints

For local development without Times Square backend:

```typescript
// pages/api/dev/times-square/v1/pages/[page]/html.ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { page } = req.query;

  // Return mock HTML
  res.status(200).json({
    html: '<div>Mock Times Square page</div>',
    parameters: {},
  });
}
```

## Page Component Pattern

```typescript
import { GetServerSideProps } from 'next';
import { useTimesSquarePage } from '../hooks/useTimesSquarePage';
import { TimesSquareUrlParametersContext } from '../contexts/TimesSquareUrlParametersContext';
import { loadAppConfig } from '../lib/config/loader';

type Props = {
  pageSlug: string;
};

export default function TimesSquarePage({ pageSlug }: Props) {
  const { data, error, isLoading } = useTimesSquarePage(pageSlug);

  if (isLoading) return <div>Loading notebook...</div>;
  if (error) return <div>Error loading notebook</div>;

  return (
    <div>
      <h1>{data.displayName}</h1>
      <div dangerouslySetInnerHTML={{ __html: data.html }} />
    </div>
  );
}

export const getServerSideProps: GetServerSideProps<Props> = async (context) => {
  const appConfig = await loadAppConfig();
  const pageSlug = context.params?.page as string;

  return {
    props: {
      appConfig,
      pageSlug,
    },
  };
};
```

## SSE Integration

```typescript
function TimesSquareLivePage({ pageSlug }) {
  const [eventSource, setEventSource] = useState(null);

  useEffect(() => {
    const es = new EventSource(
      `/times-square/api/v1/pages/${pageSlug}/htmlevents`
    );

    es.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Handle real-time updates
      console.log('New data:', data);
    };

    setEventSource(es);

    return () => es.close();
  }, [pageSlug]);

  return (
    <TimesSquareHtmlEventsContext.Provider value={eventSource}>
      {/* Page content */}
    </TimesSquareHtmlEventsContext.Provider>
  );
}
```

## Configuration

Times Square URL configured in AppConfig:

```yaml
# squareone.config.yaml
timesSquareUrl: 'http://localhost:3000/times-square/api'  # Dev
# timesSquareUrl: 'https://data.lsst.cloud/times-square/api'  # Prod
```

Access in components:

```typescript
import { useAppConfig } from '../contexts/AppConfigContext';

const config = useAppConfig();
const timesSquareUrl = config.timesSquareUrl;
```

## Best Practices

1. **Use context providers** for shared state
2. **Cache with SWR** for performance
3. **Mock APIs** for development
4. **Handle loading states** gracefully
5. **Clean up SSE connections** on unmount
6. **Validate parameters** before execution
7. **Show execution progress** with SSE
8. **Handle errors** appropriately
