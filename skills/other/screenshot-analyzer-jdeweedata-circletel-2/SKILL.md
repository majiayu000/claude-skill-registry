---
name: screenshot-analyzer
description: Analyze screenshots with accurate coordinate mapping for UI debugging and Playwright testing. Use when debugging UI issues from screenshots, creating precise click targets, or implementing visual test automation.
---

# Screenshot Analyzer

Skill for analyzing screenshots with accurate coordinate mapping.

## When to Use

This skill activates when you:
- Debug UI issues from screenshots
- Need precise element coordinates
- Create Playwright test click targets
- Analyze responsive design issues
- Map visual elements to code
- Verify UI implementations

**Keywords**: screenshot, coordinates, click, position, pixel, UI debug, element location, Playwright, visual testing

## How It Works

Claude Code v2.0.64 preserves original image dimensions when resizing screenshots:

1. **Original dimensions stored** - Even if image is compressed for display
2. **Accurate coordinate mapping** - Click targets are precise to original
3. **Consistent measurements** - Pixel values match actual screen

## Quick Reference

### Coordinate System
```
(0,0) ─────────────────────────► X (width)
  │
  │
  │
  │
  ▼
  Y (height)

Coordinates: (x, y)
- x = horizontal distance from LEFT edge
- y = vertical distance from TOP edge
```

### Common Screen Sizes
| Device | Width | Height |
|--------|-------|--------|
| iPhone SE | 375 | 667 |
| iPhone 14 | 390 | 844 |
| iPhone 14 Pro Max | 430 | 932 |
| iPad | 768 | 1024 |
| iPad Pro | 1024 | 1366 |
| Laptop | 1366 | 768 |
| Desktop HD | 1920 | 1080 |
| Desktop 4K | 3840 | 2160 |

## Usage Patterns

### Pattern 1: UI Bug Debugging

```
You: [Paste screenshot of bug]
"The submit button isn't working. What's happening?"

Claude: "Based on the screenshot (1920x1080):

        The submit button is at (960, 750) but there's a
        transparent overlay div covering it at z-index: 1000
        from coordinates (0, 600) to (1920, 900).

        Fix: Remove or reposition the overlay
        File: components/checkout/CheckoutForm.tsx:145"
```

### Pattern 2: Playwright Test Creation

```
You: [Paste screenshot of login form]
"Create a Playwright test for this login"

Claude: "Screenshot dimensions: 1440x900

        Element positions:
        - Email field: (720, 280)
        - Password field: (720, 360)
        - Submit button: (720, 450)
        - Forgot password link: (720, 500)

        ```typescript
        test('user can login', async ({ page }) => {
          await page.goto('/login')

          // Using data-testid (preferred)
          await page.fill('[data-testid="email"]', 'user@example.com')
          await page.fill('[data-testid="password"]', 'password123')
          await page.click('[data-testid="submit"]')

          // Or using coordinates (fallback)
          // await page.click({ x: 720, y: 450 })

          await expect(page).toHaveURL('/dashboard')
        })
        ```"
```

### Pattern 3: Responsive Design Analysis

```
You: [Paste mobile screenshot]
"The navigation looks off on mobile"

Claude: "Screenshot: 375x667 (iPhone SE)

        Issues detected:
        1. Menu icon at (355, 30) - only 20px from edge
           Recommended: (335, 30) for better touch target

        2. Logo at (20, 25) - too large for viewport
           Currently: 80px wide
           Recommended: 60px max on mobile

        3. Search icon overlapping menu
           Search: (310, 30)
           Menu: (340, 30)
           Gap: only 30px, need 44px for touch targets

        Fix in: components/layout/Header.tsx
        ```tsx
        <nav className='flex items-center gap-4 md:gap-2'>
        ```"
```

### Pattern 4: Element Overlap Detection

```
You: [Paste screenshot with layout issue]
"Something is blocking the checkout button"

Claude: "Screenshot: 1280x720

        Checkout button: (640, 580)

        Overlapping elements detected:
        1. Cookie banner: (0, 650) to (1280, 720)
           - Partially covers button area

        2. Live chat widget: (1180, 500) to (1280, 600)
           - Clear of button

        The cookie banner's top edge (y=650) is only 70px below
        the button center (y=580). On smaller viewports, this
        will overlap.

        Fix: Add bottom padding to main content
        ```css
        .checkout-container {
          padding-bottom: 100px; /* Space for cookie banner */
        }
        ```"
```

## CircleTel UI Debugging

### Customer Dashboard Issues

```
You: [Screenshot of dashboard]
"The billing card is cut off"

Claude: "Screenshot: 1366x768

        Billing card boundaries:
        - Start: (50, 400)
        - End: (450, 700) - extends 68px below viewport!

        Container height: 768px
        Card bottom: 700px + 68px padding = 768px (edge)

        Fix in: app/dashboard/page.tsx
        Add scrollable container or reduce card height"
```

### Admin Portal Tables

```
You: [Screenshot of admin orders table]
"Export button disappears on laptop screens"

Claude: "Screenshot: 1366x768

        Table container: (0, 100) to (1366, 768)
        Export button: (1400, 120) - OUTSIDE viewport!

        The button is positioned at x=1400 but viewport
        width is only 1366px.

        Fix options:
        1. Make button sticky inside table header
        2. Add horizontal scroll
        3. Move button above table

        File: components/admin/orders/OrdersTable.tsx:45"
```

### Payment Form Alignment

```
You: [Screenshot of checkout]
"Card fields look misaligned"

Claude: "Screenshot: 1920x1080

        Field positions (left edge):
        - Card number: x=400
        - Expiry: x=420 (20px offset!)
        - CVV: x=400
        - Name: x=400

        The expiry field has extra padding-left.

        Fix: components/checkout/CardFields.tsx:78
        ```tsx
        // Change
        <input className='pl-5' ... />
        // To
        <input className='pl-4' ... />
        ```"
```

## Playwright Test Generation

### Form Testing
```
You: [Screenshot of registration form]
"Generate Playwright test for this form"

Claude: "Screenshot: 1440x900

        Form fields:
        - First name: (500, 200)
        - Last name: (900, 200)
        - Email: (700, 280)
        - Phone: (700, 360)
        - Address: (700, 440)
        - Submit: (700, 540)

        ```typescript
        test('complete registration', async ({ page }) => {
          await page.goto('/register')

          await page.fill('[name="firstName"]', 'John')
          await page.fill('[name="lastName"]', 'Doe')
          await page.fill('[name="email"]', 'john@example.com')
          await page.fill('[name="phone"]', '+27821234567')
          await page.fill('[name="address"]', '123 Main St')

          await page.click('button[type="submit"]')

          await expect(page.locator('.success-message')).toBeVisible()
        })
        ```"
```

### Mobile Navigation Testing
```
You: [Mobile screenshot of menu]
"Generate mobile menu test"

Claude: "Screenshot: 375x812 (iPhone)

        Menu elements:
        - Hamburger: (335, 50)
        - Close (when open): (335, 50)
        - Menu items (when open):
          - Dashboard: (187, 150)
          - Services: (187, 210)
          - Billing: (187, 270)
          - Support: (187, 330)

        ```typescript
        test('mobile navigation', async ({ page }) => {
          await page.setViewportSize({ width: 375, height: 812 })
          await page.goto('/dashboard')

          // Open menu
          await page.click('[data-testid="mobile-menu-toggle"]')
          await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible()

          // Navigate to billing
          await page.click('text=Billing')
          await expect(page).toHaveURL('/dashboard/billing')
        })
        ```"
```

### Multi-Step Wizard
```
You: [Screenshot of checkout wizard]
"Generate test for full checkout flow"

Claude: "Screenshot: 1440x900

        Step 1 - Coverage:
        - Address input: (720, 300)
        - Check button: (720, 400)

        Step 2 - Package:
        - Basic package: (400, 350)
        - Premium package: (720, 350)
        - Enterprise: (1040, 350)
        - Continue: (720, 550)

        Step 3 - Payment:
        - Card number: (720, 300)
        - Pay button: (720, 500)

        ```typescript
        test('complete checkout', async ({ page }) => {
          // Step 1: Coverage
          await page.goto('/order')
          await page.fill('[data-testid="address"]', '123 Main St')
          await page.click('[data-testid="check-coverage"]')
          await page.waitForSelector('[data-testid="coverage-result"]')

          // Step 2: Package selection
          await page.click('[data-testid="package-premium"]')
          await page.click('[data-testid="continue"]')

          // Step 3: Payment
          await page.fill('[data-testid="card-number"]', '4111111111111111')
          await page.fill('[data-testid="card-expiry"]', '12/25')
          await page.fill('[data-testid="card-cvv"]', '123')
          await page.click('[data-testid="pay-now"]')

          await expect(page).toHaveURL('/order/success')
        })
        ```"
```

## Best Practices

### Screenshot Quality
1. **Use full resolution** - Don't crop unless necessary
2. **Include context** - Show surrounding elements
3. **Capture actual state** - Screenshot the actual bug

### Coordinate Usage
1. **Prefer selectors** - data-testid > text > coordinates
2. **Coordinates as fallback** - When no good selector exists
3. **Document why** - Comment coordinate usage

### Large Screenshots
- Claude handles 4K+ images accurately
- Original dimensions always preserved
- No loss of coordinate precision

### Responsive Testing
- Always note viewport dimensions
- Test multiple breakpoints
- Consider touch target sizes (44x44px minimum)

## Integration with Other Skills

### With Bug Fixing
```
1. Paste screenshot of bug
2. Get coordinates and analysis
3. Use bug-fixing skill for solution
```

### With Mobile Testing
```
1. Capture mobile screenshots
2. Analyze coordinates
3. Generate Playwright mobile tests
```

## Troubleshooting

### Coordinates seem off
- Verify screenshot wasn't cropped
- Check if browser zoom was 100%
- Confirm viewport size in screenshot

### Can't identify element
- Use higher resolution screenshot
- Ensure element is visible (not behind overlay)
- Check if element is in iframe

### Playwright test fails
- Verify selectors exist
- Add appropriate waits
- Check if page is responsive (coordinates shift)

---

**Version**: 1.0.0
**Last Updated**: 2025-12-10
**For**: Claude Code v2.0.64+
