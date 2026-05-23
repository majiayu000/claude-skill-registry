---
name: reitz-api-design
description: Write Python code in the style of Kenneth Reitz, creator of Requests. Emphasizes beautiful API design, simplicity for users, and the "for humans" philosophy. Use when designing libraries, APIs, or any interface that other developers will consume.
---

# Kenneth Reitz Style Guide

## Overview

Kenneth Reitz created `requests`, the HTTP library that replaced Python's `urllib2` by being dramatically simpler. His "for humans" philosophy prioritizes user experience above all—APIs should be intuitive, beautiful, and require minimal documentation.

## Core Philosophy

> "API design is UI design for developers."

> "Simplicity is always better than functionality."

> "Fit the 90% use case. Ignore the naysayers."

Reitz believes that **the user's experience is paramount**. If your API requires reading documentation for basic tasks, it has failed.

## Design Principles

1. **For Humans**: Design for human beings first, not for edge cases or theoretical purity.

2. **Beautiful is Better**: Code should be a pleasure to read and write. Aesthetics matter.

3. **Sensible Defaults**: The common case should require zero configuration.

4. **Refuse to Add Features**: Simplicity requires saying no. A lot.

## When Writing Code

### Always

- Provide sensible defaults for every parameter
- Make the common case trivially easy
- Return useful objects, not raw data structures
- Provide helpful error messages that guide users
- Keep the API surface small
- Write beautiful, readable code

### Never

- Require configuration for basic usage
- Expose internal complexity to users
- Add features "just in case" someone needs them
- Break backward compatibility casually
- Make users read documentation for basic operations

### Prefer

- One obvious way to do something
- Keyword arguments over positional (after the first few)
- Method chaining for fluent interfaces
- Meaningful exceptions over error codes
- Immutable objects where possible

## Code Patterns

### The "For Humans" API Design

```python
# BAD: Complex, requires documentation
from urllib2 import Request, urlopen
from urllib import urlencode

url = 'https://api.example.com/data'
data = urlencode({'key': 'value'})
req = Request(url, data.encode('utf-8'))
req.add_header('Authorization', 'Bearer token123')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
response = urlopen(req)
content = response.read().decode('utf-8')

# GOOD: Intuitive, self-documenting (requests style)
import requests

response = requests.post(
    'https://api.example.com/data',
    data={'key': 'value'},
    headers={'Authorization': 'Bearer token123'}
)
content = response.json()
```

### Sensible Defaults

```python
class HTTPClient:
    """An HTTP client with sensible defaults."""
    
    def __init__(
        self,
        base_url='',
        timeout=30,           # Sensible default
        verify_ssl=True,      # Safe default
        max_retries=3,        # Resilient default
        headers=None,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.max_retries = max_retries
        self.headers = headers or {}
    
    def get(self, path, **kwargs):
        # Merge defaults with overrides
        kwargs.setdefault('timeout', self.timeout)
        kwargs.setdefault('verify', self.verify_ssl)
        return self._request('GET', path, **kwargs)
    
    # 90% of users just need:
    # client = HTTPClient('https://api.example.com')
    # data = client.get('/users').json()
```

### Rich Response Objects

```python
# BAD: Return raw data, user figures it out
def fetch_user(user_id):
    data = api_call(f'/users/{user_id}')
    return data  # dict? string? who knows?

# GOOD: Return a rich, useful object
class User:
    def __init__(self, data):
        self._data = data
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
    
    @property
    def display_name(self):
        return self.name or self.email
    
    def __repr__(self):
        return f'<User {self.id}: {self.display_name}>'
    
    def __str__(self):
        return self.display_name


class UserNotFound(Exception):
    """Helpful, specific exception."""
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f'User {user_id} not found')


def fetch_user(user_id):
    response = api_call(f'/users/{user_id}')
    if response.status == 404:
        raise UserNotFound(user_id)
    return User(response.data)


# User experience:
user = fetch_user(123)
print(user)           # John Doe
print(user.email)     # john@example.com
print(repr(user))     # <User 123: John Doe>
```

### Fluent Interface Design

```python
class QueryBuilder:
    """Chainable query builder."""
    
    def __init__(self):
        self._filters = []
        self._order = None
        self._limit = None
    
    def filter(self, **conditions):
        self._filters.append(conditions)
        return self  # Enable chaining
    
    def order_by(self, field, descending=False):
        self._order = (field, descending)
        return self
    
    def limit(self, count):
        self._limit = count
        return self
    
    def execute(self):
        # Build and run query
        return self._run_query()


# Beautiful, readable usage:
users = (
    QueryBuilder()
    .filter(active=True)
    .filter(role='admin')
    .order_by('created_at', descending=True)
    .limit(10)
    .execute()
)
```

### Helpful Error Messages

```python
# BAD: Cryptic errors
class ConfigError(Exception):
    pass

if not api_key:
    raise ConfigError()

# GOOD: Errors that help users fix the problem
class ConfigurationError(Exception):
    """Raised when configuration is missing or invalid."""
    pass


class MissingAPIKey(ConfigurationError):
    def __init__(self):
        super().__init__(
            "API key not found. Set the MYLIB_API_KEY environment "
            "variable or pass api_key='...' to the client constructor.\n"
            "Get your API key at: https://example.com/api-keys"
        )


if not api_key:
    raise MissingAPIKey()
```

### Package Entry Point Design

```python
# mylib/__init__.py

# Make the common case dead simple
from .client import Client
from .exceptions import MyLibError, AuthError, NotFoundError

# Users can just do:
# import mylib
# client = mylib.Client()

# Or for the simplest case:
from .shortcuts import get, post, download

# Now users can do:
# import mylib
# data = mylib.get('https://api.example.com/users')
```

## Mental Model

Reitz designs APIs by asking:

1. **What does the user want to accomplish?** (Not: what can the system do?)
2. **What's the simplest code that could work?** Write that first, then implement it.
3. **What would a new user try first?** Make that work without documentation.
4. **What errors might occur?** Make them helpful, not cryptic.

## The "Requests" Test

When designing an API, ask:
- Can a beginner use it in 5 minutes?
- Does the common case require zero configuration?
- Is the code beautiful when written correctly?
- Would you be proud to show this code to others?

