---
name: react-setup
description: Use when initializing a new React frontend with Vite to connect to a Django backend over HTTPS. Sets up routing, CSRF protection, Axios config, and validates the build. Not for existing React projects.
allowed-tools: Bash, Write, Edit, Read, Glob, Grep, TodoWrite, Task
---

## Overview
Sets up a production-ready React + Vite frontend configured for Django backend integration with:
- HTTPS local development (using mkcert certificates)
- CSRF token handling for Django session auth
- Axios interceptors for automatic CSRF injection
- React Router with layout structure
- Production build validation

**When to use:** New React projects that need Django backend connectivity
**When NOT to use:** Existing React projects, non-Django backends, or projects not using session auth

## Prerequisites
- Django backend configured with HTTPS
- mkcert certificates in `/certs/` directory (use `mkcert-https-setup` skill)
- Node.js 18+ installed

---

Copy this checklist and track your progress:

- [ ] 1. Initialize React + Vite Project
- [ ] 2. Configure vite.config.js:
- [ ] 3. Create API Configuration
- [ ] 4. Create CSRF Service
- [ ] 5. Create Axios Configuration
- [ ] 6. Create Navbar and Footer Components
- [ ] 7. Create `src/layouts/Root.jsx`:
- [ ] 8. Create Page Components
- [ ] 9. Create `src/router/AppRoutes.jsx`
- [ ] 10. Create Router Wrapper
- [ ] 11. Update App.jsx
- [ ] 12. Verify Setup

---

1. Initialize React + Vite Project

- `npm create vite@latest frontend -- --template react --yes`
- `npm --prefix ./frontend install react-router-dom axios`

---

2. Configure vite.config.js:

1. List cert files in `certs/` to find actual filenames
2. Read existing `frontend/vite.config.js` (created by Vite)
3. Add imports: `fs`, `path`
4. Add server config:
   - server.https: Load key/cert from `certs/` using found filenames
   - server.port: 5173
   - server.proxy: `/api` → `https://localhost:8000` (changeOrigin: true, secure: false)

---

3. Create API Configuration

src/config/api.js:
```javascript
export const API_BASE_URL = '';  // Empty string uses Vite proxy

export const ENDPOINTS = {
  CSRF: '/api/csrf/',
  // Add your API endpoints here as you build features
  // Example: PRODUCTS: '/api/products/',
};
```
---

4. Create CSRF Service

src/services/csrf.js:
```javascript
import { ENDPOINTS } from '../config/api';

let csrfToken = null;

/**
 * Fetches and caches the CSRF token from Django backend
 * The token is stored in a cookie by Django after the first request
 */
export async function getCsrfToken() {
  // Return cached token if available
  if (csrfToken) {
    return csrfToken;
  }

  try {
    const response = await fetch(ENDPOINTS.CSRF, {
      credentials: 'include',
      headers: {
        'Accept': 'application/json',
      }
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch CSRF token: ${response.status}`);
    }

    // Django sets the token in a cookie after this request
    const cookies = document.cookie.split(';');
    const csrfCookie = cookies.find(cookie => cookie.trim().startsWith('csrftoken='));

    if (!csrfCookie) {
      throw new Error('CSRF token not found in cookies');
    }

    csrfToken = csrfCookie.split('=')[1].trim();
    return csrfToken;
  } catch (error) {
    console.error('CSRF token fetch error:', error);
    throw error;
  }
}

/**
 * Clears the cached CSRF token (useful for logout or token refresh)
 */
export function clearCsrfToken() {
  csrfToken = null;
}
```
---

5. Create Axios Configuration

src/services/api.js:
```javascript
import axios from 'axios';
import { API_BASE_URL } from '../config/api';
import { getCsrfToken } from './csrf';  // ADD THIS

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// REQUEST INTERCEPTOR
axiosInstance.interceptors.request.use(
  async (config) => {
    if (['post', 'put', 'patch', 'delete'].includes(config.method.toLowerCase())) {
      const csrfToken = await getCsrfToken();
      config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
  }
);

// Response interceptor
axiosInstance.interceptors.response.use(
  response => response,
  error => {
    console.error('API request failed:', error);
    return Promise.reject(error);
  }
);

export default axiosInstance;
```
---

6. Create Navbar and Footer Components

Create `src/components/Navbar.jsx`:
```javascript
export default function Navbar() {
  return (
    <nav>
      <h1>My App</h1>
    </nav>
  );
}
```

Create `src/components/Footer.jsx`:
```javascript
export default function Footer() {
  return (
    <footer>
      <p>&copy; {new Date().getFullYear()} My App. All rights reserved.</p>
    </footer>
  );
}
```

---

7. Create `src/layouts/Root.jsx`:

```javascript
import { Outlet } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

export default function Root() {
  return (
    <div>
      <Navbar />
      <main>
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
```

---

8. Create Page Components

Create `src/components/BackendStatus.jsx`:
1. Import axios from `../services/api`, useState, useEffect
2. Initialize state: `status = "checking..."`, `error = null`
3. useEffect hook (runs on mount):
   - First: `axios.get('/api/csrf/')` to initialize cookies
   - Second: `axios.get('/api/health/')` using same axios instance
   - Success path: update status with backend message
   - Error path: set error state, display "Backend unreachable"
4. Component is presentational only (no routing/layout logic)

Create `src/pages/Home.jsx`:
1. Render `<BackendStatus />` 
2. Add heading + text explaining the backend connectivity check

---

9. Create `src/router/AppRoutes.jsx`:

1. Export `createAppRouter()` function
2. Returns route config array: Root layout at "/" with Home page as nested "/" child route
3. Imports: `Root` from `../layouts/Root`, `Home` from `../pages/Home`

---

10. Create `src/router/index.jsx`:

1. Export default `AppRouter` component
2. Create browser router from `createAppRouter()` config
3. Return `<RouterProvider router={router} />`
4. Imports: `createBrowserRouter`, `RouterProvider` from react-router-dom, `createAppRouter` from `./AppRoutes`

---

11. Update `src/App.jsx`:
- Remove: All useState, demo imports (reactLogo, viteLogo, App.css), counter UI
- Add imports: `Router` from `./router`
- Render: `<Router />`

---

12. Verify Setup

Run `npm --prefix ./frontend run build` to validate imports, dependencies, and syntax

**Common issues:**
- Missing certs: Check `/certs/` directory exists with .pem files
- Module not found: Verify all imports use correct paths
- CSRF errors: Ensure Django backend is running at `https://localhost:8000`
