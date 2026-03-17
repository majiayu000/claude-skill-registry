---
name: ux-review
description: UX review of storefront pages for layout, navigation, and accessibility
user-invocable: true
---

You are helping the team conduct a UX review of Jocko Fuel storefront pages.

Follow these steps:

### Step 1: Identify Pages to Review

Ask the user which pages or flows to review. Common targets:
- Homepage layout and hero section
- Product listing pages (collections)
- Product detail page (PDP)
- Cart and checkout flow
- Navigation and site search
- Mobile experience

If the user says "full review," prioritize: homepage, top PDP, collection page, cart.

### Step 2: Evaluate Layout and Navigation

Delegate to the `ux-reviewer` agent to assess:
- **Visual hierarchy**: Is the most important content prominent?
- **Navigation**: Can users find what they need in 3 clicks or fewer?
- **Content flow**: Does the page guide users toward conversion?
- **White space**: Is content properly spaced or cluttered?
- **Above the fold**: What loads first and does it communicate value?

### Step 3: Check Accessibility

Delegate to the `ux-reviewer` agent to check WCAG 2.1 compliance:
- **Color contrast**: Text meets minimum contrast ratios (4.5:1 for normal text)
- **Alt text**: All images have descriptive alt text
- **Keyboard navigation**: All interactive elements are keyboard-accessible
- **Screen reader**: Semantic HTML and ARIA labels are properly used
- **Touch targets**: Buttons and links are at least 44x44px on mobile
- **Focus indicators**: Visible focus states for keyboard users

### Step 4: Compare to Best Practices

Delegate to the `ux-reviewer` agent to compare against e-commerce UX standards:
- **Trust signals**: Reviews, security badges, return policy visibility
- **CTA clarity**: Primary actions are obvious and compelling
- **Product info**: Sufficient detail for purchase decisions
- **Social proof**: Customer reviews and ratings are accessible
- **Error handling**: Form validation is helpful and non-disruptive

### Step 5: Provide Recommendations

Compile findings into a report with:
- **Overall UX score** (1-10 scale with rationale)
- **Critical issues**: Must-fix items that hurt conversion or accessibility
- **Improvements**: Nice-to-have changes for better experience
- **Strengths**: What's working well (keep doing this)
- **Mobile-specific notes**: Issues unique to mobile experience

For each recommendation, include:
- What to change
- Why it matters
- Example of the ideal state (reference another site if helpful)

### Error Handling

- If pages require login, ask the user for access or screenshots
- If the storefront is under active development, note which issues may already be addressed
- If the review scope is too large, suggest splitting into focused reviews (e.g., "navigation audit" or "PDP review")
