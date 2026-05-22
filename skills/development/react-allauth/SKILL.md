---
name: react-allauth
description: Configure React frontend with django-allauth headless API integration, including authentication UI, auth state management, protected routes, and social authentication flows
---

## Purpose

Configure a React frontend application to integrate with django-allauth's headless API, enabling complete authentication workflows including signup, login, email verification, password reset, and social authentication. This skill handles the entire setup process from copying authentication modules to validating flows with automated testing.

## Prerequisites

Before starting this configuration, ensure the following requirements are met:

- **React project with Vite** - A React frontend application initialized with Vite
- **Django backend with django-allauth** - Django backend configured with django-allauth headless API  (in settings.py - Look for allauth in INSTALLED_APPS)
- **HTTPS development environment** - Both frontend and backend running over HTTPS (mkcert recommended for local SSL certificates)
- **React Router** - Project uses `react-router-dom` for routing
- **API configuration** - An `API_BASE_URL` constant exported from a config file (typically `src/config/api.js` or `src/config/api.jsx`)
- **Project structure** - Frontend source code located in `frontend/src/` with standard Vite directory structure

## Steps Overview

1. Clone Repository and Copy Authentication Modules
2. Install Required Dependencies
3. Update App.jsx to Include Authentication Context
4. Configure API Base URL in allauth.jsx
5. Update Redirect URLs
6. Copy Authentication Router and Integrate Routes
7. Fix Social Authentication Callback URL
8. Configure Vite Proxy for Authentication Endpoints
9. Add Auth-Aware Navigation Link
10. Enable Flow-Based Signup Navigation
11. Validate Authentication Flows with Automated Testing
12. Copy Styling Reference Guide
13. Stop Background Tasks

---

### Step 1: Clone Repository and Copy Authentication Modules

Clone the django-allauth repository at the project root:

```bash
git clone https://github.com/pennersr/django-allauth
```

Refactor authentication components by renaming `.js` files to `.jsx`:

```bash
find django-allauth/examples/react-spa/frontend/src/ -name "*.js" -exec bash -c 'mv "$0" "${0%.js}.jsx"' {} \;
```

Copy the authentication modules into the React project:

```bash
mkdir -p frontend/src/user_management
find django-allauth/examples/react-spa/frontend/src/ -mindepth 1 -maxdepth 1 -type d -exec cp -r {} frontend/src/user_management/ \;
```

This creates a `user_management` directory in the React project and copies all authentication-related folders from the cloned repository. The `django-allauth/` directory remains available for later steps in this skill.

---

### Step 2: Install Required Dependencies

Install the WebAuthn dependency required by the authentication modules:

```bash
npm --prefix ./frontend install @github/webauthn-json
```

---

### Step 3: Update App.jsx to Include Authentication Context

**File:** `frontend/src/App.jsx`

Import the `AuthContextProvider` and wrap the app's content with it:

```jsx
import { AuthContextProvider } from './user_management/auth'
```

Wrap the existing app content (typically the router) with `<AuthContextProvider>`:

```jsx
<AuthContextProvider>
  {/* Existing app content */}
</AuthContextProvider>
```

---

### Step 4: Configure API Base URL in allauth.jsx

**File:** `frontend/src/user_management/lib/allauth.jsx`

After the `getCSRFToken` import, add:
```jsx
import { API_BASE_URL } from '../../config/api'
```

Then update the API endpoint path from:
```jsx
`/_allauth/${Client.BROWSER}/v1`
```

To:
```jsx
`${API_BASE_URL}/_allauth/${Client.BROWSER}/v1`
```

---

### Step 5: Update Redirect URLs

Update redirect paths from `/calculator` to `/dashboard`:

**File:** `frontend/src/user_management/auth/routing.jsx`

Change the `LOGIN_REDIRECT_URL` path to:
```jsx
LOGIN_REDIRECT_URL: '/'
```

**File:** `frontend/src/user_management/account/ChangePassword.jsx`

Replace any occurrence of `'/calculator'` with `'/dashboard'`

---

### Step 6: Copy Authentication Router and Integrate Routes

Copy the authentication router file and clean up the cloned repository:

```bash
cp django-allauth/examples/react-spa/frontend/src/Router.jsx frontend/src/router/AuthRouter.jsx && rm -rf django-allauth
```

**File:** `frontend/src/router/AuthRouter.jsx`

Update all import paths to use the `user_management` directory:

Change:
```jsx
import { AuthChangeRedirector, AnonymousRoute, AuthenticatedRoute } from './auth'
```

To:
```jsx
import { AuthChangeRedirector, AnonymousRoute, AuthenticatedRoute } from '../user_management/auth'
```

Update all component imports (like `Login`, `Signup`, `ChangeEmail`, etc.) from relative paths to use `user_management`:

Change:
```jsx
import Login from './account/Login'
import Signup from './account/Signup'
// ... etc
```

To:
```jsx
import Login from '../user_management/account/Login'
import Signup from '../user_management/account/Signup'
// ... etc
```

Update the `Root` import:
```jsx
import Root from '../layouts/Root'
```

Update the `useConfig` import:
```jsx
import { useConfig } from '../user_management/auth/hooks'
```

**File:** `frontend/src/router/AppRoutes.jsx`

Import and integrate authentication routes into `createAppRouter`:

```jsx
import Root from "../layouts/Root";
import Home from "../pages/Home";
import { createAuthRoutes } from './AuthRouter';

export function createAppRouter(config) {
  const authRoutes = createAuthRoutes(config);

  return [
    {
      path: "/",
      element: <Root />,
      children: [
        {
          path: "/",
          element: <Home />,
        },
        ...authRoutes
      ],
    },
  ];
}
```

**File:** `frontend/src/router/AuthRouter.jsx`

Rename the exported function and export the routes array:

Change:
```jsx
function createRouter (config) {
  return createBrowserRouter([
    {
      path: '/',
      element: <AuthChangeRedirector><Root /></AuthChangeRedirector>,
      children: [
        // ... routes
      ]
    }
  ])
}

export default function Router () {
  const [router, setRouter] = useState(null)
  const config = useConfig()
  useEffect(() => {
    setRouter(createRouter(config))
  }, [config])
  return router ? <RouterProvider router={router} /> : null
}
```

To:
```jsx
export function createAuthRoutes (config) {
  return [
    // ... all the route objects from the children array
  ]
}
```

Remove the `/calculator` route as it's not needed.

---

### Step 7: Fix Social Authentication Callback URL

**File:** `frontend/src/user_management/lib/allauth.jsx`

Find the `redirectToProvider` function and update the `callback_url` parameter.

Change:
```jsx
callback_url: window.location.protocol + '//' + window.location.host + callbackURL,
```

To:
```jsx
callback_url: callbackURL,
```

This configuration ensures social authentication callbacks use the correct backend URL instead of the frontend host.

---

### Step 8: Configure Vite Proxy for Authentication Endpoints

**File:** `frontend/vite.config.js`

Add the `/_allauth` proxy configuration to forward authentication requests to the Django backend.

Add to the `proxy` object:
```js
'/_allauth': {
  target: 'https://localhost:8000',
  changeOrigin: true,
  secure: false,  // Allow self-signed certificates
},
```

**Expected result:**
```js
proxy: {
  '/api': {
    target: 'https://localhost:8000',
    changeOrigin: true,
    secure: false,
  },
  '/_allauth': {
    target: 'https://localhost:8000',
    changeOrigin: true,
    secure: false,
  },
}
```

---

### Step 9: Add Auth-Aware Navigation Link

First, search the project to determine if a navbar or header component exists.

#### If a navbar component exists:

Import the auth status helper and toggle the navigation link based on whether the user is logged in:

```jsx
import { useAuthStatus } from "@/user_management/auth";
import { Link } from "react-router-dom";

const [, authInfo] = useAuthStatus();

{authInfo.isAuthenticated ? (
  <Link to="/account/logout">
    <NavigationMenuLink className={navigationMenuTriggerStyle()}>
      Logout
    </NavigationMenuLink>
  </Link>
) : (
  <Link to="/account/login">
    <NavigationMenuLink className={navigationMenuTriggerStyle()}>
      Login
    </NavigationMenuLink>
  </Link>
)}
```

#### If NO navbar component exists:

Add auth-aware navigation links to the landing page.

**File:** `frontend/src/pages/Home.jsx`

Import the required dependencies at the top:

```jsx
import { useAuthStatus } from "@/user_management/auth";
import { Link } from "react-router-dom";
```

Add the navigation links in the component JSX:

```jsx
const [, authInfo] = useAuthStatus();

return (
  <div>
    <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
      {authInfo.isAuthenticated ? (
        <Link to="/account/logout" style={{ marginRight: '1rem' }}>
          Logout
        </Link>
      ) : (
        <Link to="/account/login" style={{ marginRight: '1rem' }}>
          Login
        </Link>
      )}
    </nav>
    {/* Rest of Home page content */}
  </div>
);
```

**Note:** Linking to `/account/logout` ensures authenticated users reach the confirmation screen before finalizing the logout. Anonymous visitors continue to see the Login link.

---

### Step 10: Enable Flow-Based Signup Navigation

This step configures multi-step signup flows (like email verification + passkey creation) to navigate correctly between steps without intermediate redirects.

#### Step 10.1: Configure Signup Screens to Handle Pending Flows

**Files:**
- `frontend/src/user_management/account/Signup.jsx`
- `frontend/src/user_management/mfa/SignupByPasskey.jsx`

Add the following imports at the top of each signup component:

```jsx
import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { pathForFlow } from '../auth'
```

Inside each component, instantiate the navigate function:

```jsx
const navigate = useNavigate()
```

Add a `useEffect` hook that watches for pending flows in the response:

```jsx
useEffect(() => {
  if (response.content) {
    const pending = response.content?.data?.flows?.find(flow => flow.is_pending)
    if (pending) {
      navigate(pathForFlow(pending), { replace: true })
    }
  }
}, [response.content, navigate])
```

This configuration ensures users are redirected to the next step in the signup flow (e.g., email verification) without leaving the signup page in the history stack.

#### Step 10.2: Update Authentication Redirector for Pending Flows

**File:** `frontend/src/user_management/auth/routing.jsx`

Update the `AuthChangeRedirector` component to check for pending flows before redirecting to the default login redirect URL.

In the `LOGGED_IN` branch, add logic to call `pathForPendingFlow(auth)` before defaulting to `LOGIN_REDIRECT_URL`:

```jsx
if (auth.status === AuthStatus.LOGGED_IN) {
  const pendingPath = pathForPendingFlow(auth)
  if (pendingPath) {
    navigate(pendingPath, { replace: true })
  } else {
    navigate(LOGIN_REDIRECT_URL, { replace: true })
  }
}
```

This logic prevents users from being redirected to the dashboard when pending authentication steps remain.

#### Step 10.3: Configure Email Verification to Handle Flows

**File:** `frontend/src/user_management/account/VerifyEmailByCode.jsx`

Replace the static `<Navigate>` component return with a `useEffect` hook that handles flow-based redirects.

Add the required imports:

```jsx
import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { pathForFlow } from '../auth'
```

Instantiate navigate:

```jsx
const navigate = useNavigate()
```

Replace the `<Navigate>` return with a `useEffect` that redirects based on the response:

```jsx
useEffect(() => {
  const content = response.content
  if (!content) {
    return
  }

  const flows = content.data?.flows
  if (flows?.length) {
    const pending = flows.find(flow => flow.is_pending)
    if (pending) {
      navigate(pathForFlow(pending), { replace: true })
      return
    }
  }

  if (content.status === 200) {
    navigate('/account/email', { replace: true })
  } else if (content.status === 401) {
    navigate('/account/login', { replace: true })
  }
}, [response.content, navigate])
```

This configuration ensures email verification redirects to the next pending flow step (e.g., passkey creation) or falls back to the appropriate default page.

---

### Step 11: Validate Authentication Flows with Automated Testing

Run the comprehensive authentication flow test suite to validate the entire integration. This step confirms all authentication flows work correctly end-to-end.

#### Step 11.1: Install Testing Dependencies

Activate the Django virtual environment and install Playwright for browser automation testing:

```bash
source venv/bin/activate

# Install pytest only if missing
python -c "import pytest" 2>/dev/null || pip install 'pytest>=7.4,<9.0'

# Install playwright only if missing
python -c "import playwright" 2>/dev/null || pip install playwright

# Install chromium only if Playwright hasn't installed it yet
playwright show-browsers | grep -q "chromium" \
  || playwright install chromium
```

#### Step 11.2: Check and Start Servers, Then Run the Test Suite

Before running tests, verify both servers are running and start them if needed.

**Check if backend is running on port 8000:**

```bash
lsof -i :8000
```

**If backend is not running, start it:**

Activate the virtual environment, and run the startup script in the background:

```bash
source venv/bin/activate && \
uvicorn backend.asgi:application \
  --host 127.0.0.1 \
  --port 8000 \
  --ssl-keyfile ./certs/localhost+2-key.pem \
  --ssl-certfile ./certs/localhost+2.pem
```

**Check if frontend is running on port 5173:**

```bash
lsof -i :5173
```

**If frontend is not running, start it:**

Start the development server in the background:

```bash
npm --prefix ./frontend run dev
```

**Wait for servers to be ready:**

Allow a few seconds for both servers to fully initialize before proceeding with tests.

**Execute the test suite:**

From the Django project root with the virtual environment activated:
Activate the virtual environment `source venv/bin/activate` and run the test script at: `scripts/test_auth_flows.py`


The test suite includes:

1. **test_01_signup** - User signup flow validation
2. **test_02_email_verification** - Email verification workflow
3. **test_03_password_login** - Password-based authentication
4. **test_04_logout** - Logout functionality
5. **test_05_code_login** - Passwordless code-based login
6. **test_06_password_reset** - Password reset workflow

**Prerequisites for testing:**
- Django backend running on `https://localhost:8000`
- React frontend running on `https://localhost:5173`
- Email backend configured to save emails to `sent_emails/` directory
- Clean database state (tests create unique users with timestamps)

**Test execution:**
- Tests run with visible browser (`headless=False`) for debugging
- Each test is independent and creates its own test user
- Tests clean up email files between runs
- Verbose output (`verbosity=2`) shows detailed test progress

**Note:** Tests run sequentially and may take several minutes to complete due to browser automation and wait times for email delivery.

---

### Step 12: Copy Styling Reference Guide

Read the styling reference guide from the skill's bundled resources and write it to the project root for later use.

The styling guide is located at `references/styling-guide.md` within this skill's directory. Read this file and write its contents to `react-allauth-styling-reference.md` in the project root.

This file lists all 35 authentication components that require styling and can be referenced by styling skills. Delete this file after styling is complete.

---

### Step 13: Stop Background Tasks

Terminate any background commands or servers started during the configuration process.
