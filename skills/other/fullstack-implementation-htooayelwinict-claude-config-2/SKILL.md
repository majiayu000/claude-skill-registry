---
name: fullstack-implementation
description: |
  Implement features end-to-end in Laravel 12 + Inertia.js + React 19 + TypeScript OR Python + FastAPI + LangChain. Use when building
  new features, wiring controllers to pages, or implementing CRUD operations. EXCLUSIVE to fullstack-developer agent.
allowed-tools: Read, Edit, Bash, Grep, Glob, Write, mcp_context7
---
# Fullstack Implementation

**Exclusive to:** `fullstack-developer` agent

## 📚 Context7 (Memory) — Up-to-Date Docs

Before implementing unfamiliar APIs, lookup the latest documentation:
```
mcp_context7_resolve-library-id(libraryName="[library]", query="[feature]")
mcp_context7_query-docs(libraryId="/[resolved-id]", query="[specific API]")
```

**Common lookups:**
- React hooks, Server Components, Suspense
- Laravel Eloquent, Inertia responses
- FastAPI dependencies, Pydantic models
- LangChain chains, agents, tools

## 💻 Codex-Bridge — Code Implementation Helper
```
mcp_codex-bridge_consult_codex(
  query="Generate a Laravel controller for [feature] or React component for [UI]",
  directory="."
)
```

## Validation Loop (MANDATORY)

Before completing ANY implementation, run this verification sequence:
```bash
composer test           # All PHP tests pass
npm run types          # No TypeScript errors
npm run lint           # No linting errors
./vendor/bin/pint      # PHP code styled
python -m pytest       # Python tests pass
ruff check .           # Python lint clean
mypy .                 # Python typing clean
```

**Do NOT report completion until all checks pass.**

## Instructions

1. Review `docs/code-standards.md` for naming conventions
2. Check `docs/codebase-summary.md` for current structure
3. Follow patterns in `docs/system-architecture.md`
4. Implement backend first, then frontend
5. Run verification commands before committing

## Implementation Order

### Backend First (Laravel)
1. **Route** → `routes/web.php` or `routes/api.php`
2. **Controller** → `app/Http/Controllers/`
3. **FormRequest** → `app/Http/Requests/`
4. **Model** → `app/Models/`
5. **Policy** → `app/Policies/`

### Backend First (FastAPI)
1. **Router** → `src/api/`
2. **Schema** → `src/schemas/`
3. **Model** → `src/models/`
4. **Service** → `src/services/`
5. **Migration** → Alembic revision (if applicable)

### Frontend Second
1. **Types** → `resources/js/types/`
2. **Page** → `resources/js/pages/`
3. **Components** → `resources/js/components/`
4. **Hooks** → `resources/js/hooks/`

## Laravel 12 Patterns

### Controllers
```php
// Invokable for single action
class ShowDashboardController
{
    public function __invoke(): Response
    {
        return Inertia::render('Dashboard', [...]);
    }
}

// Resource for CRUD
class PostController extends Controller
{
    public function store(StorePostRequest $request) { ... }
}
```

### Form Requests
```php
class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Post::class);
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
        ];
    }
}
```

## React 19 Patterns

### Inertia Form
```tsx
const { data, setData, post, processing, errors } = useForm({
    title: '',
});

const submit = (e: FormEvent) => {
    e.preventDefault();
    post(route('posts.store'));
};
```

### TypeScript Types
```tsx
interface Post {
    id: number;
    title: string;
    created_at: string;
}

interface Props {
    posts: Post[];
}
```

## Verification
```bash
composer test            # PHP tests
npm run types           # TypeScript
npm run lint            # ESLint
./vendor/bin/pint       # PHP style
python -m pytest        # Python tests
ruff check .            # Python lint
mypy .                  # Python typing
```

## Instructions
1. Read project docs for context and conventions
2. Identify entry points (routes/controllers/pages)
3. Follow patterns in `docs/code-standards.md`
4. Keep changes minimal and cohesive
5. Add or update tests when behavior changes
6. Update `docs/codebase-summary.md` if adding new files

## Examples
- "Add a new CRUD page with validation and tests"
- "Wire a form to a controller endpoint and handle errors"
- "Add a FastAPI router, schema, service, and tests"
