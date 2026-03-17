---
name: api-client-patterns
description: HTTP client patterns, API integration, request/response handling, error handling, retry logic, axios usage. Use when building API clients, integrating external services, handling API errors, or making HTTP requests.
allowed-tools: Read, Grep, Glob
---

# API Client Patterns

## Core Principles

1. **Single Responsibility** - One client per service
2. **Centralized Configuration** - Base URL, headers, timeouts in one place
3. **Comprehensive Error Handling** - Catch and transform errors appropriately
4. **Type Safety** - Define request/response interfaces
5. **Retry Logic** - Handle transient failures gracefully

---

## API Client Structure

### CORRECT: Well-Structured API Client

```javascript
// client/src/utils/api.js
import axios from 'axios';

// Configuration
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:3001/api';
const TIMEOUT = 30000; // 30 seconds

// Create axios instance with defaults
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor (optional - for auth, logging, etc.)
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor (optional - for error transformation)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Transform errors to consistent format
    const message = error.response?.data?.error || error.message || 'Unknown error';
    return Promise.reject(new Error(message));
  }
);

// API Methods

/**
 * Verify faculty password
 */
export const verifyPassword = async (password) => {
  const response = await apiClient.post('/auth/verify', { password });
  return response.data;
};

/**
 * Generate or update instructional page
 */
export const generatePage = async (config, message, history = []) => {
  const response = await apiClient.post('/generate', {
    config,
    message,
    history
  });
  return response.data;
};

/**
 * Generate AI image using DALL-E
 */
export const generateImage = async (prompt) => {
  const response = await apiClient.post('/images/generate', { prompt });
  return response.data;
};

/**
 * Upload image to Cloudinary
 */
export const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append('image', file);

  const response = await apiClient.post('/images/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  return response.data;
};

export default apiClient;
```

### WRONG: Scattered API Calls

```javascript
// ❌ DON'T DO THIS: Direct axios calls scattered across components
import axios from 'axios';

// In Component 1
const handleLogin = async () => {
  const res = await axios.post('http://localhost:3001/api/auth/verify', {
    password: pwd
  });
};

// In Component 2
const handleGenerate = async () => {
  const res = await axios.post('http://localhost:3001/api/generate', data);
};

// ❌ Issues:
// - Repeated base URL strings
// - No centralized error handling
// - No configuration reuse
// - Hard to test
```

---

## Error Handling Patterns

### CORRECT: Comprehensive Error Handling

```javascript
// API client with error transformation
export const generatePage = async (config, message, history) => {
  try {
    const response = await apiClient.post('/generate', {
      config,
      message,
      history
    });
    return response.data;
  } catch (error) {
    // Check different error types
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const message = error.response.data?.error || 'Server error';

      if (status === 400) {
        throw new Error(`Validation error: ${message}`);
      } else if (status === 401) {
        throw new Error('Authentication failed');
      } else if (status === 429) {
        throw new Error('Rate limit exceeded. Please try again later.');
      } else if (status >= 500) {
        throw new Error('Server error. Please try again.');
      } else {
        throw new Error(message);
      }
    } else if (error.request) {
      // Request made but no response received
      throw new Error('Network error. Please check your connection.');
    } else {
      // Something else happened
      throw new Error(error.message || 'Request failed');
    }
  }
};
```

### Component Error Handling

```javascript
// In component
export default function ChatInterface() {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await generatePage(config, message, history);
      // Handle success
    } catch (err) {
      // Error is already transformed by API client
      setError(err.message);

      // Optional: Report to error tracking service
      console.error('Generation failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <p>{error}</p>
          <button onClick={() => setError(null)}>Dismiss</button>
        </div>
      )}
      {/* Rest of component */}
    </div>
  );
}
```

---

## Request Configuration Patterns

### With Timeout

```javascript
export const generatePageWithTimeout = async (config, message, history, timeout = 60000) => {
  const response = await apiClient.post('/generate', {
    config,
    message,
    history
  }, {
    timeout // Override default timeout for long operations
  });
  return response.data;
};
```

### With Abort Controller (Cancellation)

```javascript
export const generatePageCancellable = async (config, message, history, signal) => {
  const response = await apiClient.post('/generate', {
    config,
    message,
    history
  }, {
    signal // Pass AbortController signal
  });
  return response.data;
};

// Usage in component
const abortController = useRef(null);

const handleGenerate = async () => {
  // Cancel previous request if exists
  if (abortController.current) {
    abortController.current.abort();
  }

  abortController.current = new AbortController();

  try {
    const result = await generatePageCancellable(
      config,
      message,
      history,
      abortController.current.signal
    );
    // Handle result
  } catch (err) {
    if (err.name === 'AbortError') {
      console.log('Request cancelled');
    } else {
      setError(err.message);
    }
  }
};

// Cleanup on unmount
useEffect(() => {
  return () => {
    if (abortController.current) {
      abortController.current.abort();
    }
  };
}, []);
```

---

## Streaming Responses Pattern

For long-running AI generation with streaming:

```javascript
/**
 * Generate page with streaming response
 */
export const generatePageStream = async (config, message, history, onChunk) => {
  const response = await fetch(`${API_BASE}/generate/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ config, message, history })
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();

    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop(); // Keep incomplete line in buffer

    for (const line of lines) {
      if (line.trim()) {
        try {
          const data = JSON.parse(line);
          onChunk(data);
        } catch (err) {
          console.error('Failed to parse chunk:', err);
        }
      }
    }
  }
};

// Usage in component
const handleStreamingGenerate = async () => {
  let fullText = '';

  try {
    await generatePageStream(config, message, history, (chunk) => {
      // Process each chunk as it arrives
      if (chunk.type === 'text') {
        fullText += chunk.content;
        setPreview(fullText); // Update UI in real-time
      } else if (chunk.type === 'done') {
        setComplete(true);
      }
    });
  } catch (err) {
    setError(err.message);
  }
};
```

---

## Retry Logic Pattern

For handling transient failures:

```javascript
/**
 * Retry a function with exponential backoff
 */
const retryWithBackoff = async (fn, maxRetries = 3, baseDelay = 1000) => {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      const isLastAttempt = attempt === maxRetries - 1;

      // Don't retry on 4xx errors (client errors)
      if (error.response?.status >= 400 && error.response?.status < 500) {
        throw error;
      }

      if (isLastAttempt) {
        throw error;
      }

      // Exponential backoff: 1s, 2s, 4s, 8s, etc.
      const delay = baseDelay * Math.pow(2, attempt);
      console.log(`Retry attempt ${attempt + 1}/${maxRetries} after ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
};

// Usage
export const generatePageWithRetry = async (config, message, history) => {
  return retryWithBackoff(async () => {
    const response = await apiClient.post('/generate', {
      config,
      message,
      history
    });
    return response.data;
  });
};
```

---

## File Upload Pattern

### With Progress Tracking

```javascript
export const uploadImageWithProgress = async (file, onProgress) => {
  const formData = new FormData();
  formData.append('image', file);

  const response = await apiClient.post('/images/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    onUploadProgress: (progressEvent) => {
      const percentCompleted = Math.round(
        (progressEvent.loaded * 100) / progressEvent.total
      );
      onProgress(percentCompleted);
    }
  });

  return response.data;
};

// Usage in component
const handleFileUpload = async (file) => {
  setProgress(0);
  try {
    const result = await uploadImageWithProgress(file, (percent) => {
      setProgress(percent);
    });
    setImageUrl(result.url);
  } catch (err) {
    setError(err.message);
  } finally {
    setProgress(0);
  }
};
```

---

## Environment-Based Configuration

```javascript
// client/src/utils/api.js

// Different base URLs for different environments
const getApiBase = () => {
  const env = import.meta.env.MODE;

  switch (env) {
    case 'production':
      return 'https://api.yourapp.com';
    case 'staging':
      return 'https://staging-api.yourapp.com';
    case 'development':
    default:
      return import.meta.env.VITE_API_BASE || 'http://localhost:3001/api';
  }
};

const apiClient = axios.create({
  baseURL: getApiBase(),
  timeout: 30000
});
```

---

## Testing API Clients

```javascript
// client/src/utils/api.test.js
import { describe, it, expect, vi } from 'vitest';
import axios from 'axios';
import { generatePage, verifyPassword } from './api';

// Mock axios
vi.mock('axios');

describe('API Client', () => {
  it('should call generatePage endpoint with correct data', async () => {
    const mockResponse = {
      data: {
        html: '<div>Test</div>',
        message: 'Generated successfully'
      }
    };

    axios.create.mockReturnValue({
      post: vi.fn().mockResolvedValue(mockResponse)
    });

    const result = await generatePage(
      { depth: 2 },
      'Create a page about React',
      []
    );

    expect(result.html).toBe('<div>Test</div>');
  });

  it('should handle errors correctly', async () => {
    axios.create.mockReturnValue({
      post: vi.fn().mockRejectedValue(new Error('Network error'))
    });

    await expect(
      generatePage({}, 'Test', [])
    ).rejects.toThrow('Network error');
  });
});
```

---

## Checklist

### Before Creating an API Client
- [ ] What endpoints will this client access?
- [ ] What base URL and configuration is needed?
- [ ] What error cases need handling?
- [ ] Does it need retry logic?
- [ ] Does it need request/response interceptors?

### After Creating an API Client
- [ ] Base URL configured correctly
- [ ] Timeout set appropriately
- [ ] Errors transformed to consistent format
- [ ] All endpoints have JSDoc comments
- [ ] Request/response types documented
- [ ] Error cases handled in consuming components
- [ ] Tested with mock responses

---

## Integration with Other Skills

- **react-component-patterns**: Using API clients in components
- **express-api-patterns**: Understanding backend endpoints
- **systematic-debugging**: Debugging API integration issues
- **testing-patterns**: Testing API clients

---

## Common Mistakes to Avoid

1. ❌ Scattered axios calls across components
2. ❌ Hard-coded API URLs
3. ❌ Not handling network errors
4. ❌ Not transforming error responses
5. ❌ Missing timeout configuration
6. ❌ Not cancelling requests on unmount
7. ❌ Retry logic on non-retryable errors (4xx)
8. ❌ Not using environment variables for base URL
