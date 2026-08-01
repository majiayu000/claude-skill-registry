---
name: smart-routing
description: Automatically determine the best location, handler, or approach for files,
  requests, and tasks.
---

# 🛤️ Smart Routing Skill

---
name: smart-routing
description: Intelligently route files, requests, and tasks to appropriate handlers
---

## 🎯 Purpose

Automatically determine the best location, handler, or approach for files, requests, and tasks.

## 📋 When to Use

- Creating new files
- Organizing codebase
- Routing API requests
- Assigning tasks to agents

## 🗂️ File Routing

### By File Type
| Extension | Location | Purpose |
|-----------|----------|---------|
| `.tsx`, `.jsx` | `src/components/` | React components |
| `.ts`, `.js` | `src/utils/` | Utility functions |
| `.css`, `.scss` | `src/styles/` | Stylesheets |
| `.test.ts` | Same dir as source | Tests |
| `.md` | `docs/` | Documentation |
| `.json` | `config/` or root | Configuration |

### By Purpose
| Purpose | Location |
|---------|----------|
| Page component | `src/pages/` or `app/` |
| Shared component | `src/components/` |
| API route | `src/api/` or `app/api/` |
| Hook | `src/hooks/` |
| Context | `src/contexts/` |
| Type definitions | `src/types/` |
| Constants | `src/constants/` |

## 🔀 Request Routing

### API Patterns
```javascript
// RESTful routing
GET    /api/users        → List users
GET    /api/users/:id    → Get user
POST   /api/users        → Create user
PUT    /api/users/:id    → Update user
DELETE /api/users/:id    → Delete user
```

### Route Naming
```javascript
// Naming conventions
/api/v1/resource           // Versioned API
/api/resource/:id/subresource  // Nested resource
/api/resource?filter=value     // Query params
```

## 🤖 Task Routing

### To Appropriate Skill
| Task Type | Route To |
|-----------|----------|
| Bug fix | `debugging` |
| New feature | `code-generation` |
| UI work | `design-mastery` |
| Testing | `testing` |
| Deployment | `deployment` |
| Security | `security-audit` |

### By Complexity
| Complexity | Approach |
|------------|----------|
| Simple | Direct implementation |
| Medium | Plan then implement |
| Complex | Design doc → Review → Implement |

## 📁 Project Structure Templates

### Web App (Vite/React)
```
src/
├── components/    ← UI components
├── pages/         ← Page components
├── hooks/         ← Custom hooks
├── utils/         ← Helper functions
├── services/      ← API calls
├── stores/        ← State management
├── types/         ← TypeScript types
└── assets/        ← Static assets
```

### Next.js App Router
```
app/
├── (auth)/        ← Auth routes group
├── api/           ← API routes
├── dashboard/     ← Dashboard pages
├── layout.tsx     ← Root layout
└── page.tsx       ← Home page
```

## 🔧 Routing Logic

```javascript
function routeFile(filename, purpose) {
  // By extension
  if (filename.endsWith('.test.ts')) {
    return 'alongside source';
  }

  // By purpose
  const routes = {
    'component': 'src/components/',
    'page': 'src/pages/',
    'hook': 'src/hooks/',
    'util': 'src/utils/',
    'type': 'src/types/',
    'api': 'src/api/'
  };

  return routes[purpose] || 'src/';
}
```

## 💡 Best Practices

1. **Consistent naming**: Use same pattern throughout
2. **Group by feature**: When project grows
3. **Flat when possible**: Avoid deep nesting
4. **Co-locate related**: Tests near source
5. **Clear boundaries**: Separate concerns

## 🔗 Related Skills

- `project-setup` - Initial structure
- `refactoring` - Reorganize existing code
- `documentation` - Document routing decisions
