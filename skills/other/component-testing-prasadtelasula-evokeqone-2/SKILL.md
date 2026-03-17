---
name: component-testing
description: Test React components with React Testing Library and Playwright. Use when building UI components or verifying frontend functionality.
allowed-tools: Read, Write, Bash, Glob
---

You help test React components and pages for the QA Team Portal frontend using React Testing Library and Playwright.

## When to Use This Skill

- Testing React components after creation
- Writing unit tests for component logic
- Testing user interactions (clicks, typing, form submission)
- E2E testing of complete user flows
- Accessibility testing
- Visual regression testing

## Testing Approaches

### 1. Unit Tests with React Testing Library

#### Basic Component Test

```typescript
// tests/unit/components/TeamMemberCard.test.tsx
import { render, screen } from '@testing-library/react'
import { TeamMemberCard } from '@/components/public/TeamIntro/TeamMemberCard'

const mockMember = {
  id: '123',
  name: 'John Doe',
  role: 'QA Lead',
  email: 'john@example.com',
  profilePhotoUrl: '/path/to/photo.jpg'
}

describe('TeamMemberCard', () => {
  it('renders member name and role', () => {
    render(<TeamMemberCard member={mockMember} />)

    expect(screen.getByText('John Doe')).toBeInTheDocument()
    expect(screen.getByText('QA Lead')).toBeInTheDocument()
  })

  it('displays profile photo with alt text', () => {
    render(<TeamMemberCard member={mockMember} />)

    const img = screen.getByRole('img', { name: /john doe/i })
    expect(img).toHaveAttribute('src', mockMember.profilePhotoUrl)
  })

  it('shows email link when provided', () => {
    render(<TeamMemberCard member={mockMember} />)

    const emailLink = screen.getByRole('link', { name: /email/i })
    expect(emailLink).toHaveAttribute('href', 'mailto:john@example.com')
  })
})
```

#### Testing User Interactions

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { UpdatesModal } from '@/components/public/Updates/UpdateModal'

describe('UpdatesModal', () => {
  it('closes modal when close button clicked', async () => {
    const onClose = vi.fn()
    render(<UpdatesModal isOpen={true} onClose={onClose} update={mockUpdate} />)

    const closeButton = screen.getByRole('button', { name: /close/i })
    await userEvent.click(closeButton)

    expect(onClose).toHaveBeenCalledTimes(1)
  })

  it('closes modal on escape key press', async () => {
    const onClose = vi.fn()
    render(<UpdatesModal isOpen={true} onClose={onClose} update={mockUpdate} />)

    fireEvent.keyDown(document, { key: 'Escape' })

    expect(onClose).toHaveBeenCalled()
  })
})
```

#### Testing Forms

```typescript
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { LoginForm } from '@/components/admin/auth/LoginForm'

describe('LoginForm', () => {
  it('submits form with valid data', async () => {
    const onSubmit = vi.fn()
    render(<LoginForm onSubmit={onSubmit} />)

    await userEvent.type(
      screen.getByLabelText(/email/i),
      'admin@test.com'
    )
    await userEvent.type(
      screen.getByLabelText(/password/i),
      'password123'
    )

    await userEvent.click(screen.getByRole('button', { name: /login/i }))

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'admin@test.com',
        password: 'password123'
      })
    })
  })

  it('shows validation errors for invalid email', async () => {
    render(<LoginForm onSubmit={vi.fn()} />)

    await userEvent.type(
      screen.getByLabelText(/email/i),
      'invalid-email'
    )
    await userEvent.click(screen.getByRole('button', { name: /login/i }))

    await waitFor(() => {
      expect(screen.getByText(/invalid email/i)).toBeInTheDocument()
    })
  })
})
```

#### Testing API Integration

```typescript
import { render, screen, waitFor } from '@testing-library/react'
import { TeamList } from '@/components/public/TeamIntro/TeamList'
import { rest } from 'msw'
import { setupServer } from 'msw/node'

const mockTeamMembers = [
  { id: '1', name: 'John Doe', role: 'QA Lead' },
  { id: '2', name: 'Jane Smith', role: 'QA Engineer' }
]

const server = setupServer(
  rest.get('/api/v1/team-members', (req, res, ctx) => {
    return res(ctx.json(mockTeamMembers))
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('TeamList', () => {
  it('displays loading state initially', () => {
    render(<TeamList />)
    expect(screen.getByRole('status')).toBeInTheDocument()
  })

  it('displays team members after loading', async () => {
    render(<TeamList />)

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument()
      expect(screen.getByText('Jane Smith')).toBeInTheDocument()
    })
  })

  it('displays error message on API failure', async () => {
    server.use(
      rest.get('/api/v1/team-members', (req, res, ctx) => {
        return res(ctx.status(500))
      })
    )

    render(<TeamList />)

    await waitFor(() => {
      expect(screen.getByText(/error loading/i)).toBeInTheDocument()
    })
  })
})
```

### 2. E2E Tests with Playwright

#### Setup Playwright

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  use: {
    baseURL: 'http://localhost:5173',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  webServer: {
    command: 'npm run dev',
    port: 5173,
    reuseExistingServer: !process.env.CI,
  },
})
```

#### Basic E2E Test

```typescript
// tests/e2e/landing-page.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Landing Page', () => {
  test('displays all sections', async ({ page }) => {
    await page.goto('/')

    // Check all sections are visible
    await expect(page.getByRole('heading', { name: /team introduction/i })).toBeVisible()
    await expect(page.getByRole('heading', { name: /latest updates/i })).toBeVisible()
    await expect(page.getByRole('heading', { name: /tools/i })).toBeVisible()
    await expect(page.getByRole('heading', { name: /resources/i })).toBeVisible()
    await expect(page.getByRole('heading', { name: /research/i })).toBeVisible()
  })

  test('navigation links scroll to sections', async ({ page }) => {
    await page.goto('/')

    // Click tools nav link
    await page.getByRole('link', { name: /tools/i }).click()

    // Check tools section is in view
    const toolsSection = page.getByRole('heading', { name: /tools/i })
    await expect(toolsSection).toBeInViewport()
  })
})
```

#### Testing User Flows

```typescript
// tests/e2e/admin-login.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Admin Login', () => {
  test('admin can login and access dashboard', async ({ page }) => {
    // Navigate to login page
    await page.goto('/admin/login')

    // Fill login form
    await page.getByLabel(/email/i).fill('admin@test.com')
    await page.getByLabel(/password/i).fill('testpass123')

    // Submit form
    await page.getByRole('button', { name: /login/i }).click()

    // Wait for redirect to dashboard
    await expect(page).toHaveURL('/admin/dashboard')

    // Check dashboard loads
    await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible()
  })

  test('shows error for invalid credentials', async ({ page }) => {
    await page.goto('/admin/login')

    await page.getByLabel(/email/i).fill('wrong@test.com')
    await page.getByLabel(/password/i).fill('wrongpass')

    await page.getByRole('button', { name: /login/i }).click()

    // Check error message appears
    await expect(page.getByText(/invalid credentials/i)).toBeVisible()
  })
})
```

#### Testing CRUD Operations

```typescript
// tests/e2e/team-management.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Team Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login as admin
    await page.goto('/admin/login')
    await page.getByLabel(/email/i).fill('admin@test.com')
    await page.getByLabel(/password/i).fill('testpass123')
    await page.getByRole('button', { name: /login/i }).click()
    await page.waitForURL('/admin/dashboard')

    // Navigate to team management
    await page.getByRole('link', { name: /team members/i }).click()
  })

  test('can create new team member', async ({ page }) => {
    await page.getByRole('button', { name: /add member/i }).click()

    // Fill form
    await page.getByLabel(/name/i).fill('New Member')
    await page.getByLabel(/role/i).fill('QA Engineer')
    await page.getByLabel(/email/i).fill('new@test.com')

    // Upload photo
    await page.getByLabel(/photo/i).setInputFiles('./tests/fixtures/profile.jpg')

    // Submit
    await page.getByRole('button', { name: /save/i }).click()

    // Verify success message
    await expect(page.getByText(/member created successfully/i)).toBeVisible()

    // Verify appears in list
    await expect(page.getByText('New Member')).toBeVisible()
  })

  test('can edit existing team member', async ({ page }) => {
    // Click edit button for first member
    await page.getByRole('row').first().getByRole('button', { name: /edit/i }).click()

    // Update name
    await page.getByLabel(/name/i).clear()
    await page.getByLabel(/name/i).fill('Updated Name')

    // Save
    await page.getByRole('button', { name: /save/i }).click()

    // Verify updated
    await expect(page.getByText('Updated Name')).toBeVisible()
  })

  test('can delete team member', async ({ page }) => {
    // Get initial count
    const initialCount = await page.getByRole('row').count()

    // Delete first member
    await page.getByRole('row').first().getByRole('button', { name: /delete/i }).click()

    // Confirm deletion
    await page.getByRole('button', { name: /confirm/i }).click()

    // Verify count decreased
    const newCount = await page.getByRole('row').count()
    expect(newCount).toBe(initialCount - 1)
  })
})
```

### 3. Accessibility Testing

```typescript
// tests/e2e/accessibility.spec.ts
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test.describe('Accessibility', () => {
  test('landing page has no accessibility violations', async ({ page }) => {
    await page.goto('/')

    const accessibilityScanResults = await new AxeBuilder({ page }).analyze()

    expect(accessibilityScanResults.violations).toEqual([])
  })

  test('admin dashboard has no accessibility violations', async ({ page }) => {
    // Login first
    await page.goto('/admin/login')
    await page.getByLabel(/email/i).fill('admin@test.com')
    await page.getByLabel(/password/i).fill('testpass123')
    await page.getByRole('button', { name: /login/i }).click()

    await page.waitForURL('/admin/dashboard')

    const accessibilityScanResults = await new AxeBuilder({ page }).analyze()

    expect(accessibilityScanResults.violations).toEqual([])
  })
})
```

## Running Tests

### Vitest (Unit Tests)

```bash
cd frontend

# Run all unit tests
npm run test

# Run in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage

# Run specific file
npm run test -- TeamMemberCard.test.tsx

# Run with UI
npm run test:ui
```

### Playwright (E2E Tests)

```bash
cd frontend

# Install browsers (first time)
npx playwright install

# Run all E2E tests
npx playwright test

# Run in UI mode
npx playwright test --ui

# Run specific test file
npx playwright test tests/e2e/landing-page.spec.ts

# Run in headed mode (see browser)
npx playwright test --headed

# Run in debug mode
npx playwright test --debug

# Run on specific browser
npx playwright test --project=chromium

# Generate test code
npx playwright codegen http://localhost:5173
```

## Test Configuration

### Vitest Setup (vitest.config.ts)

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './tests/setup.ts',
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### Test Setup File (tests/setup.ts)

```typescript
import '@testing-library/jest-dom'
import { cleanup } from '@testing-library/react'
import { afterEach, vi } from 'vitest'

// Cleanup after each test
afterEach(() => {
  cleanup()
})

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})
```

## Test Checklist

For each component, verify:

- [ ] **Rendering** - Component renders without errors
- [ ] **Props** - Handles different prop combinations
- [ ] **User interactions** - Clicks, typing, form submission work
- [ ] **Loading states** - Shows loading indicators
- [ ] **Error states** - Shows error messages
- [ ] **Empty states** - Handles no data gracefully
- [ ] **Accessibility** - ARIA labels, keyboard navigation, screen readers
- [ ] **Responsiveness** - Works on mobile/tablet/desktop
- [ ] **Edge cases** - Null values, long text, special characters

## Common Testing Patterns

### Testing Hooks

```typescript
import { renderHook, waitFor } from '@testing-library/react'
import { useTeamMembers } from '@/hooks/useTeamMembers'

test('useTeamMembers fetches data', async () => {
  const { result } = renderHook(() => useTeamMembers())

  expect(result.current.loading).toBe(true)

  await waitFor(() => {
    expect(result.current.loading).toBe(false)
    expect(result.current.data).toHaveLength(2)
  })
})
```

### Testing Context

```typescript
import { render, screen } from '@testing-library/react'
import { AuthProvider } from '@/contexts/AuthContext'
import { ProtectedComponent } from '@/components/ProtectedComponent'

test('shows content when authenticated', () => {
  render(
    <AuthProvider value={{ user: mockUser, isAuthenticated: true }}>
      <ProtectedComponent />
    </AuthProvider>
  )

  expect(screen.getByText(/protected content/i)).toBeInTheDocument()
})
```

## Output Format

After testing, report:

1. **Tests Run**: X passed, Y failed
2. **Coverage**: X% of components/lines covered
3. **Failed Tests**: List with error messages
4. **Accessibility Issues**: WCAG violations found
5. **Performance**: Slow-rendering components
6. **Recommendations**: Suggested improvements

## Best Practices

1. **Test user behavior**, not implementation details
2. **Use semantic queries** (getByRole, getByLabel, getByText)
3. **Avoid testing IDs or classes** when possible
4. **Test accessibility** (keyboard navigation, screen readers)
5. **Mock external dependencies** (API calls, localStorage)
6. **Keep tests independent** - no shared state
7. **Use descriptive test names** - what you're testing and expected outcome
8. **Test error scenarios** - not just happy path
