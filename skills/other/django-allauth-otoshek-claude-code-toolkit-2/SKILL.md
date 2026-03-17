---
name: django-allauth
description: Configure django-allauth with headless API, MFA, social authentication, and CORS for React frontends. This skill should be used when setting up authentication for a new Django project or adding django-allauth to an existing project that needs a React frontend integration. (project)
---


## Overview

This skill configures django-allauth in headless mode for React/Vue/frontend applications. Unlike traditional Django authentication that renders server-side templates, headless mode exposes authentication as REST APIs, making it ideal for single-page applications (SPAs) and mobile apps.

**What this skill provides:**
- Complete django-allauth setup with headless API endpoints
- Multi-factor authentication (TOTP, WebAuthn, recovery codes)
- Social authentication (Google OAuth example included)
- CORS configuration for cross-origin frontend communication
- Email verification and password reset workflows
- Session management for authenticated users

**End result:** A Django backend with secure, production-ready authentication APIs that the React frontend can consume via HTTP requests.

## Prerequisites

Before using this skill, ensure:
- Django project is created
- Virtual environment is created

## Setup Steps

To set up django-allauth in headless mode for React, follow these steps:
1. Install Django-Allauth headless mode Dependencies
2. Configure `settings.py`
3. Create Environment File `.env.development`
4. Add URL routes to `urls.py`
5. Check Django Configuration
6. Run migrations
7. Validate Installation with Tests

---

### Step 1: Activate virtual environment and Install Django-Allauth headless mode Dependencies

Install the required packages for authentication, social login, MFA, and cross-origin requests:

```bash
source venv/bin/activate
pip install 'django-allauth[socialaccount,mfa]' python-dotenv djangorestframework django-cors-headers fido2 python3-openid Pillow pyyaml
```

**Package purposes:**
- `django-allauth[socialaccount,mfa]` - Core authentication with social providers and multi-factor auth
- `python-dotenv` - Load environment variables from `.env` files
- `djangorestframework` - REST API framework (required by allauth headless)
- `django-cors-headers` - Enable cross-origin requests from React frontend
- `fido2` - WebAuthn/passkey support for passwordless authentication
- `python3-openid` - OpenID authentication support for social providers
- `Pillow` - Image processing library (required for avatar/profile images)
- `pyyaml` - YAML parser (required for allauth configuration)

---

### Step 2: Configure `settings.py`

### Find the settings file using Glob tool with pattern "**/*settings.py"

**Editing steps for `settings.py`:**
- Add Environment Variable Loading
- Add FRONTEND_URL, ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS AND CSRF_TRUSTED_ORIGINS
- Ensure 'django.template.context_processors.request' is included in the template context processors list
- Update INSTALLED_APPS
- Update MIDDLEWARE
- Add Django-Allauth Configuration settings to the end of the file

#### Add Environment Variable Loading 

Insert these lines at the end of the existing imports (top of the file):

```python
import os
from dotenv import load_dotenv
load_dotenv('.env.development')
```

#### Ensure 'django.template.context_processors.request' is included in the template context processors list

**Why:** Django-allauth requires access to the request object in templates for authentication flows.

Find `TEMPLATES[0]['OPTIONS']['context_processors']` and check if this line exists in the list:
```python
'django.template.context_processors.request',
```

**If missing:** Add it to the end of the `context_processors` list

#### Update INSTALLED_APPS

Find the `INSTALLED_APPS` list and append the following to the end of the list:
```python

    # Authentication and user management (django-allauth)
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Providers
    'allauth.socialaccount.providers.google',

    # Multi-Factor Authentication (MFA)
    'allauth.mfa',

    # Headless API support for allauth
    'allauth.headless',
    'allauth.usersessions',
```

The end result should look similar to:
```python
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Cross-Origin Resource Sharing
    'corsheaders',

    # REST API support
    'rest_framework',

    # Authentication and user management (django-allauth)
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Providers
    'allauth.socialaccount.providers.google',

    # Multi-Factor Authentication (MFA)
    'allauth.mfa',

    # Headless API support for allauth
    'allauth.headless',
    'allauth.usersessions',
]
```

#### Update MIDDLEWARE

Find the `MIDDLEWARE` list. After `'django.contrib.messages.middleware.MessageMiddleware',`, add:
```python
"allauth.account.middleware.AccountMiddleware",
```

**Critical middleware order requirements:**
- `CorsMiddleware` must come AFTER `SessionMiddleware` and BEFORE `CommonMiddleware` to properly handle CORS headers before request processing
- `AccountMiddleware` must come AFTER `MessageMiddleware` to access session-based authentication state

**Expected result:**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # ← Add here
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

#### Add Django-Allauth Configuration settings to the end of the file

**Location:** At the very end of `settings.py`

**Action:** Append all of the following authentication and MFA configuration:

```python

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Account settings
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # Require email verification before login
ACCOUNT_LOGIN_METHODS = {'email'}  # Use email instead of username for login
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_LOGIN_BY_CODE_ENABLED = True  # Enable passwordless login via email code
ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = True

# Multi-Factor Authentication settings
MFA_SUPPORTED_TYPES = ["totp", "webauthn", "recovery_codes"]
MFA_PASSKEY_LOGIN_ENABLED = True  # Enable passwordless WebAuthn login
MFA_WEBAUTHN_ALLOW_INSECURE_ORIGIN = True if DEBUG else False  # Allow localhost in dev
MFA_PASSKEY_SIGNUP_ENABLED = True

# Headless mode configuration
HEADLESS_ONLY = True  # Disable server-side templates, use API endpoints only
HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": f"{FRONTEND_URL}/account/verify-email/{{key}}",
    "account_reset_password": f"{FRONTEND_URL}/account/password/reset",
    "account_reset_password_from_key": f"{FRONTEND_URL}/account/password/reset/key/{{key}}",
    "account_signup": f"{FRONTEND_URL}/account/signup",
    "socialaccount_login_error": f"{FRONTEND_URL}/account/provider/error",
}

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
            'key': ''
        },
        'FETCH_USERINFO': True,
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'  
```

**Key configuration notes:**
- `HEADLESS_ONLY = True` disables Django's template-based authentication views and forces API-only mode
- `HEADLESS_FRONTEND_URLS` tells the backend where to redirect users in email links (e.g., password reset, email verification)
- Social providers can be added/removed from `SOCIALACCOUNT_PROVIDERS` as needed
- Email backend is set to console for development; change to SMTP for production

---

### Step 3: Create Environment File

**Location:** Project root (same directory as `manage.py`)

**File:** `.env.development`

**Action:** Create file with OAuth credentials (leave empty for now, fill in when setting up social auth):
```
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

**If file exists:** Only add missing keys, don't overwrite existing values

---

### Step 4: Add import and URL routes to `urls.py`

**Location:** Django project package (same directory as `settings.py`)

First add `include` to imports and then add allauth URLs in `urls.py`:

```python
path('accounts/', include('allauth.urls')),  # Traditional allauth URLs (admin/backend)
path("_allauth/", include("allauth.headless.urls")),  # Headless API endpoints for frontend
```

**Why two URL patterns:**
- `accounts/` - Django admin integration and backend management
- `_allauth/` - RESTful API endpoints that the React frontend will call

---

### Step 5: Check Django Configuration

Verify that all settings are correctly configured before running migrations:

```bash
python manage.py check
```

**Expected:** No errors (warnings about unapplied migrations are OK)

---

### Step 6: Run migrations

Create the database tables for authentication, social accounts, and MFA:

```bash
python manage.py migrate
```

**What this creates:**
- User authentication tables
- Social account provider tables
- MFA/WebAuthn tables
- Email verification tables
- Session management tables

---

### Step 7: Validate Installation with Tests

Verify the django-allauth installation by running the official test suite. This ensures all core functionality is working correctly.

#### Clone the django-allauth repository

If not already cloned, clone the official repository to access the test suite:

```bash
git clone https://github.com/pennersr/django-allauth.git
```

#### Install test dependencies

Install pytest and required testing packages:

```bash
pip install 'pytest>=7.4,<9.0' 'pytest-asyncio==0.23.8' pytest-django pytest-cov django-ninja
```

**Note:** Pytest 9.x has compatibility issues with the django-allauth test suite. Using pytest 8.x ensures all tests pass successfully.

#### Update requirements.txt

```bash
pip freeze > requirements.txt
```

#### Run the validation script

Use the validation script to run the core test suite at: `scripts/validate_allauth_tests.sh`

#### Expected test results

**Success criteria:** All 76 tests should pass

**Test coverage:**
- ✅ Login Tests (16 tests) - Basic login, failed attempts, rate limiting, input validation
- ✅ Signup Tests (12 tests) - User registration, email verification, password validation, enumeration prevention
- ✅ Logout Tests (4 tests) - GET and POST logout flows, session management
- ✅ Email Verification Tests (6 tests) - Mandatory/optional verification, cross-user security
- ✅ Password Reset Tests (8 tests) - Reset flow, email handling, rate limiting, invalid keys
- ✅ Password Change Tests (18 tests) - Password change and set workflows with various validation scenarios
- ✅ Session Tests (12 tests) - Session management, token handling, security edge cases

#### What the tests validate

These tests confirm that your installation properly supports:
- User authentication (login/logout)
- User registration with email verification
- Password reset and change workflows
- Security features (rate limiting, unicode protection)
- Multi-factor authentication infrastructure
- Session management
- Email handling
- Async middleware support

**If tests fail:** Review the error messages. Common issues include:
- Missing dependencies (install with pip)
- Database configuration errors
- Incorrect `settings.py` configuration
- Missing URL patterns

**For detailed test information:** See `references/test-validation-guide.md` for:
- Detailed breakdown of each test category
- What each test validates
- Running additional test suites (headless API, social auth, MFA)
- Troubleshooting common test failures
- Continuous validation strategies


### clean up the cloned repository
```bash
rm -rf django-allauth
```