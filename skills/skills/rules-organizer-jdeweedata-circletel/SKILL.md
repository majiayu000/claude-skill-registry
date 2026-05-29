---
name: rules-organizer
description: Organize Claude Code instructions into modular rule files in .claude/rules/. Use when setting up project standards, adding team conventions, creating domain-specific rules, or managing shared coding guidelines.
---

# Rules Organizer

Skill for organizing Claude Code instructions into modular `.claude/rules/` files.

## When to Use

This skill activates when you:
- Set up coding standards for a project area
- Create team conventions for specific domains
- Add security or compliance rules
- Share rules across projects via symlinks
- Organize a large CLAUDE.md into focused files

**Keywords**: rules, standards, conventions, guidelines, organize instructions, coding style, team rules

## Quick Reference

| Location | Scope | Priority |
|----------|-------|----------|
| `~/.claude/rules/` | All your projects (personal) | Lowest |
| `.claude/rules/` | This project (team) | Higher |
| `.claude/CLAUDE.md` | This project (main) | Highest |

## Directory Structure

```
your-project/
├── .claude/
│   ├── CLAUDE.md           # Main instructions (keep concise)
│   └── rules/
│       ├── code-style.md   # General coding style
│       ├── security.md     # Security requirements
│       ├── testing.md      # Testing conventions
│       ├── frontend/
│       │   ├── react.md    # React patterns
│       │   └── tailwind.md # Tailwind conventions
│       └── backend/
│           ├── api.md      # API route patterns
│           └── database.md # Database conventions
```

## Rule File Format

Each rule file is a simple markdown file (no frontmatter required):

```markdown
# Code Style Rules

## General
- Use 2-space indentation
- No semicolons in TypeScript
- Prefer functional components

## Naming
- Components: PascalCase
- Functions: camelCase
- Constants: SCREAMING_SNAKE_CASE

## Examples

### Good
```typescript
const UserProfile = ({ user }: Props) => {
  return <div>{user.name}</div>
}
```

### Bad
```typescript
function user_profile(props: any) {
  return <div>{props.user.name}</div>;
}
```
```

## CircleTel Rules Organization

### Recommended Structure
```
.claude/rules/
├── general/
│   ├── code-style.md       # TypeScript, naming conventions
│   ├── error-handling.md   # try/catch patterns
│   └── security.md         # OWASP, input validation
├── frontend/
│   ├── react-patterns.md   # Hooks, components, state
│   ├── tailwind.md         # Utility classes, responsive
│   └── forms.md            # Validation, submission
├── backend/
│   ├── api-routes.md       # Next.js 15 patterns
│   ├── supabase.md         # Client usage, RLS
│   └── webhooks.md         # Signature verification
├── domain/
│   ├── payments.md         # NetCash, billing rules
│   ├── coverage.md         # MTN, provider APIs
│   └── b2b-kyc.md          # KYC workflow rules
└── testing/
    ├── unit.md             # Jest patterns
    └── e2e.md              # Playwright patterns
```

## Creating Rule Files

### Step 1: Identify the Category
- Is it general coding style? → `general/`
- Is it framework-specific? → `frontend/` or `backend/`
- Is it business logic? → `domain/`
- Is it about testing? → `testing/`

### Step 2: Create the File
```bash
# Create directory if needed
mkdir -p .claude/rules/backend

# Create rule file
touch .claude/rules/backend/api-routes.md
```

### Step 3: Write Clear Rules
- Start with a heading
- Use bullet points for rules
- Include code examples
- Show both good and bad patterns

## Example Rule Files for CircleTel

### `.claude/rules/backend/api-routes.md`
```markdown
# API Route Conventions

## Next.js 15 Async Params (CRITICAL)

Always await params in dynamic routes:

```typescript
// CORRECT
export async function GET(
  request: NextRequest,
  context: { params: Promise<{ id: string }> }
) {
  const { id } = await context.params
}

// WRONG - Will cause type errors
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params
}
```

## Supabase Client Selection

```typescript
// Server-side (API routes)
import { createClient } from '@/lib/supabase/server'
const supabase = await createClient()

// Client-side (components)
import { createClient } from '@/lib/supabase/client'
const supabase = createClient()
```

## Error Response Format

Always use consistent error responses:

```typescript
// Success
return NextResponse.json({ data, success: true })

// Error
return NextResponse.json(
  { error: 'Description', code: 'ERROR_CODE', success: false },
  { status: 400 }
)
```

## Authentication Check Pattern

```typescript
export async function GET(request: NextRequest) {
  // Check authorization header first
  const authHeader = request.headers.get('authorization')

  if (authHeader?.startsWith('Bearer ')) {
    const token = authHeader.split(' ')[1]
    const { data: { user }, error } = await supabase.auth.getUser(token)
    if (error || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
  }

  // Continue with authenticated request...
}
```
```

### `.claude/rules/domain/payments.md`
```markdown
# Payment System Rules

## NetCash Integration

### Environment Variables
- `NETCASH_SERVICE_KEY` - Never expose in client code
- `NETCASH_WEBHOOK_SECRET` - For signature verification

### Webhook Signature Verification (REQUIRED)
```typescript
import crypto from 'crypto'

function verifyWebhookSignature(
  payload: string,
  signature: string,
  secret: string
): boolean {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex')
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  )
}

// Always verify first
if (!verifyWebhookSignature(payload, signature, secret)) {
  return NextResponse.json({ error: 'Invalid signature' }, { status: 401 })
}
```

### Payment Statuses
| Status | Description |
|--------|-------------|
| `pending` | Awaiting payment |
| `processing` | Payment initiated |
| `completed` | Payment successful |
| `failed` | Payment failed |
| `refunded` | Payment refunded |

### eMandate Flow
1. Create mandate request via API
2. Redirect customer to NetCash authorization
3. Receive webhook confirmation
4. Store mandate reference for future debits
```

### `.claude/rules/frontend/react-patterns.md`
```markdown
# React Patterns for CircleTel

## Loading States (CRITICAL)

Always use try/catch/finally to prevent infinite loading:

```typescript
// CORRECT
useEffect(() => {
  const fetchData = async () => {
    try {
      setLoading(true)
      const data = await api.getData()
      setData(data)
    } catch (error) {
      console.error('Failed:', error)
      setError(error)
    } finally {
      setLoading(false)  // ALWAYS executes
    }
  }
  fetchData()
}, [])

// WRONG - Loading never stops on error
useEffect(() => {
  const fetchData = async () => {
    setLoading(true)
    const data = await api.getData()  // Error here = stuck loading
    setData(data)
    setLoading(false)
  }
  fetchData()
}, [])
```

## Component Organization

```
components/
├── ui/           # Reusable UI primitives
├── forms/        # Form components
├── layout/       # Layout components
├── dashboard/    # Dashboard-specific
├── admin/        # Admin-specific
└── checkout/     # Checkout flow
```

## Props Interface Pattern

```typescript
interface UserCardProps {
  user: User
  onEdit?: (user: User) => void
  className?: string
}

export const UserCard = ({ user, onEdit, className }: UserCardProps) => {
  // Component implementation
}
```

## Custom Hooks Pattern

```typescript
// hooks/use-customer.ts
export function useCustomer(customerId: string) {
  const [customer, setCustomer] = useState<Customer | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    // Fetch logic with try/catch/finally
  }, [customerId])

  return { customer, loading, error }
}
```
```

## Symlink Shared Rules

### Share Rules Across Projects
```bash
# Create shared rules directory
mkdir -p ~/shared-claude-rules

# Create shared security rules
cat > ~/shared-claude-rules/security.md << 'EOF'
# Security Standards

- Never log sensitive data (passwords, tokens, PII)
- Always validate user input
- Use parameterized queries
- Verify webhook signatures
EOF

# Symlink to project
cd /path/to/project
ln -s ~/shared-claude-rules/security.md .claude/rules/security.md
```

### Company-Wide Standards
```bash
# Clone company rules repo
git clone git@github.com:company/claude-rules.git ~/company-claude-rules

# Symlink entire directory
ln -s ~/company-claude-rules .claude/rules/company
```

## User-Level Rules

Personal rules that apply to ALL your projects:

```
~/.claude/rules/
├── preferences.md    # Your coding preferences
├── workflows.md      # Your preferred workflows
└── communication.md  # How you like Claude to respond
```

### Example: `~/.claude/rules/preferences.md`
```markdown
# My Coding Preferences

## Communication
- Be concise, avoid over-explanation
- Use code examples over lengthy descriptions
- Include file:line references

## Code Style
- Prefer early returns
- Use optional chaining (?.)
- Avoid nested ternaries
- Prefer const over let

## When I Ask "Fix This"
1. Read the file first
2. Make minimal changes
3. Explain what changed
```

## Migration from Large CLAUDE.md

### Step 1: Identify Sections
Review your CLAUDE.md and categorize content:
- General coding → `rules/general/`
- Framework-specific → `rules/frontend/` or `rules/backend/`
- Domain logic → `rules/domain/`
- Keep in CLAUDE.md: Project overview, commands, file structure

### Step 2: Extract to Files
```bash
# Create directories
mkdir -p .claude/rules/{general,frontend,backend,domain,testing}

# Create rule files
touch .claude/rules/general/code-style.md
touch .claude/rules/frontend/react.md
touch .claude/rules/backend/api.md
touch .claude/rules/domain/payments.md
```

### Step 3: Slim Down CLAUDE.md
Keep only:
- Project overview
- Quick start commands
- File organization
- Environment setup
- Links to rule files

## Best Practices

1. **Keep rules focused** - One topic per file
2. **Use examples** - Show don't just tell
3. **Include bad patterns** - Show what to avoid
4. **Update regularly** - Rules evolve with project
5. **Version control** - Commit rule changes
6. **Document purpose** - Header explaining when rule applies
7. **Use subdirectories** - Group related rules

## Troubleshooting

### Rules not loading
- Ensure files have `.md` extension
- Check file is in `.claude/rules/` directory
- Restart Claude Code after adding rules

### Too many rules
- Consolidate related rules into fewer files
- Use subdirectories for organization
- Consider what's truly essential

### Conflicting rules
- More specific rules (deeper paths) take priority
- Project rules override user rules
- CLAUDE.md has highest priority

---

**Version**: 1.0.0
**Last Updated**: 2025-12-10
**For**: Claude Code v2.0.64+
