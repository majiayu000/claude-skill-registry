---
name: copywriter
description: Expert in writing compelling copy for web, marketing, and product
version: 1.0.0
tags: [copywriting, content, marketing, ux-writing, microcopy]
---

# Copywriter Skill

I help you write clear, compelling copy for your product, marketing, and user experience.

## What I Do

**UX Writing:**

- Button labels, form fields, error messages
- Empty states, onboarding flows
- Tooltips, help text
- Confirmation dialogs

**Marketing Copy:**

- Landing pages, hero sections
- Feature descriptions
- Call-to-action (CTA) buttons
- Email campaigns

**Product Content:**

- Product descriptions
- Feature announcements
- Release notes
- Documentation

## UX Writing Patterns

### Button Labels

```typescript
// ❌ Bad: Vague, passive
<Button>Submit</Button>
<Button>OK</Button>
<Button>Click Here</Button>

// ✅ Good: Specific, action-oriented
<Button>Create Account</Button>
<Button>Save Changes</Button>
<Button>Start Free Trial</Button>
```

**Guidelines:**

- Use verb + noun ("Save Changes" not "Save")
- Be specific ("Delete Post" not "Delete")
- Show outcome ("Start Free Trial" not "Submit")

---

### Error Messages

```typescript
// ❌ Bad: Technical, blaming user
"Invalid input"
"Error 422: Unprocessable Entity"
"You entered the wrong password"

// ✅ Good: Helpful, actionable
"Please enter a valid email address"
"We couldn't find an account with that email"
"Password must be at least 8 characters"

// Implementation
function PasswordInput() {
  const [error, setError] = useState('')

  const validate = (password: string) => {
    if (password.length < 8) {
      setError('Password must be at least 8 characters')
    } else if (!/[A-Z]/.test(password)) {
      setError('Password must include at least one uppercase letter')
    } else if (!/[0-9]/.test(password)) {
      setError('Password must include at least one number')
    } else {
      setError('')
    }
  }

  return (
    <div>
      <input type="password" onChange={(e) => validate(e.target.value)} />
      {error && <p className="text-red-600">{error}</p>}
    </div>
  )
}
```

**Error Message Formula:**

1. What happened
2. Why it happened (optional)
3. How to fix it

---

### Empty States

```typescript
// ❌ Bad: Just says it's empty
<EmptyState message="No results" />

// ✅ Good: Explains and guides user
function EmptySearchResults() {
  return (
    <div className="text-center py-12">
      <h3 className="text-lg font-semibold">No results found</h3>
      <p className="mt-2 text-gray-600">
        Try adjusting your search or filters to find what you're looking for
      </p>
      <Button onClick={clearFilters} className="mt-4">
        Clear Filters
      </Button>
    </div>
  )
}

function EmptyInbox() {
  return (
    <div className="text-center py-12">
      <h3 className="text-lg font-semibold">You're all caught up!</h3>
      <p className="mt-2 text-gray-600">
        No new messages. Enjoy your day! 🎉
      </p>
    </div>
  )
}
```

**Empty State Formula:**

- Headline (what's empty)
- Explanation (why it's empty)
- Action (what to do next)

---

### Form Labels

```typescript
// ❌ Bad: Unclear, jargon
<Label>Metadata</Label>
<Label>FTP Credentials</Label>

// ✅ Good: Clear, helpful
<Label>
  Email Address
  <span className="text-gray-500 text-sm ml-2">
    We'll never share your email
  </span>
</Label>

<Label>
  Password
  <span className="text-gray-500 text-sm ml-2">
    Must be at least 8 characters
  </span>
</Label>
```

**Label Guidelines:**

- Use clear, everyday language
- Add help text for complex fields
- Avoid technical jargon

---

### Loading States

```typescript
// ❌ Bad: Generic
<Loading message="Loading..." />

// ✅ Good: Specific, reassuring
function LoadingStates() {
  return (
    <>
      <Loading message="Creating your account..." />
      <Loading message="Processing payment..." />
      <Loading message="Uploading image (2/5)..." />
      <Loading message="This might take a minute..." />
    </>
  )
}
```

---

### Success Messages

```typescript
// ❌ Bad: Just confirms action
<Toast message="Saved" />

// ✅ Good: Confirms and suggests next step
function SuccessMessages() {
  return (
    <>
      <Toast
        message="Post published!"
        action={
          <Button onClick={viewPost}>View Post</Button>
        }
      />

      <Toast
        message="Payment successful. Receipt sent to your email."
      />

      <Toast
        message="Profile updated. Changes are now live."
      />
    </>
  )
}
```

---

## Landing Page Copy

### Hero Section

```typescript
// components/Hero.tsx

export function Hero() {
  return (
    <section className="text-center py-20">
      {/* Headline: Clear value proposition */}
      <h1 className="text-5xl font-bold">
        Deploy your app in seconds, not hours
      </h1>

      {/* Subheadline: Expand on headline */}
      <p className="mt-6 text-xl text-gray-600 max-w-2xl mx-auto">
        Skip the complex setup. Push your code and we'll handle the deployment,
        scaling, and monitoring automatically.
      </p>

      {/* CTA: Primary action */}
      <div className="mt-10 flex gap-4 justify-center">
        <Button size="lg">
          Start Free Trial
        </Button>
        <Button size="lg" variant="outline">
          Watch Demo (2 min)
        </Button>
      </div>

      {/* Social proof */}
      <p className="mt-8 text-sm text-gray-500">
        Trusted by 50,000+ developers at companies like Airbnb, Netflix, and Shopify
      </p>
    </section>
  )
}
```

**Hero Copy Formula:**

1. Headline: Main benefit (not what you do)
2. Subheadline: How it works or who it's for
3. CTA: Primary action
4. Social proof: Build credibility

**Examples:**

```markdown
❌ Bad:
"Cloud Deployment Platform"
"We provide deployment services"

✅ Good:
"Deploy with confidence"
"Ship faster with zero-config deploys"
"From code to production in 30 seconds"
```

---

### Feature Descriptions

```typescript
// components/Features.tsx

const features = [
  {
    title: 'Lightning-Fast Deploys',
    description: 'Push your code and see it live in under 30 seconds. No waiting, no config files.',
    icon: '⚡'
  },
  {
    title: 'Auto-Scaling',
    description: 'Handle any traffic spike without lifting a finger. We scale from zero to millions seamlessly.',
    icon: '📈'
  },
  {
    title: 'Zero Downtime',
    description: 'Deploy updates without taking your site offline. Your users won't even notice.',
    icon: '🛡️'
  }
]

export function Features() {
  return (
    <section className="py-20">
      <h2 className="text-3xl font-bold text-center">
        Everything you need to ship fast
      </h2>

      <div className="mt-12 grid md:grid-cols-3 gap-8">
        {features.map((feature) => (
          <div key={feature.title}>
            <div className="text-4xl mb-4">{feature.icon}</div>
            <h3 className="text-xl font-semibold">{feature.title}</h3>
            <p className="mt-2 text-gray-600">{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
```

**Feature Copy Guidelines:**

- Focus on benefits, not features
- Use active voice
- Be specific (numbers, timeframes)
- Keep it scannable

---

### Call-to-Action (CTA)

```typescript
// Different CTA styles

// ❌ Generic
<Button>Sign Up</Button>
<Button>Learn More</Button>

// ✅ Value-focused
<Button>Start Free Trial</Button>
<Button>Get Started Free</Button>
<Button>Try it Free for 14 Days</Button>

// ✅ Urgency
<Button>Claim Your Spot</Button>
<Button>Join 10,000 Developers</Button>

// ✅ Low commitment
<Button>Browse Templates</Button>
<Button>See How It Works</Button>
```

**CTA Copy Formula:**

- Start with a verb
- Highlight the benefit
- Remove friction ("Free", "No credit card", etc.)

---

## Email Copywriting

### Welcome Email

```typescript
// Email template (React Email)
import { Button, Html, Heading, Text } from '@react-email/components'

export function WelcomeEmail({ name }: { name: string }) {
  return (
    <Html>
      <Heading>Welcome to TechStart, {name}! 👋</Heading>

      <Text>
        Thanks for signing up! We're excited to help you deploy faster.
      </Text>

      <Text>
        Here's what to do next:
      </Text>

      <ul>
        <li>Connect your Git repository</li>
        <li>Deploy your first project (takes 2 minutes)</li>
        <li>Invite your team members</li>
      </ul>

      <Button href="https://app.techstart.com/deploy">
        Deploy Your First Project
      </Button>

      <Text>
        Need help? Reply to this email or check our{' '}
        <a href="https://docs.techstart.com">docs</a>.
      </Text>

      <Text>
        Happy deploying!<br />
        The TechStart Team
      </Text>
    </Html>
  )
}
```

### Transactional Email

```typescript
export function PaymentSuccessEmail({ orderNumber, total }: {
  orderNumber: string
  total: string
}) {
  return (
    <Html>
      <Heading>Payment Successful</Heading>

      <Text>
        We've received your payment of {total}.
      </Text>

      <Text>
        <strong>Order Number:</strong> {orderNumber}<br />
        <strong>Receipt:</strong> Sent to your email
      </Text>

      <Button href={`https://app.techstart.com/orders/${orderNumber}`}>
        View Order Details
      </Button>

      <Text>
        Questions? Contact support@techstart.com
      </Text>
    </Html>
  )
}
```

---

## Microcopy Examples

### Tooltips

```typescript
// ❌ Bad: Repeats label
<Tooltip content="Click to delete">
  <Button>Delete</Button>
</Tooltip>

// ✅ Good: Adds helpful context
<Tooltip content="This action cannot be undone">
  <Button>Delete</Button>
</Tooltip>

<Tooltip content="Visible to all team members">
  <Toggle>Public</Toggle>
</Tooltip>
```

### Confirmation Dialogs

```typescript
// ❌ Bad: Scary, unclear
<Dialog
  title="Warning"
  message="Are you sure?"
  confirmButton="Yes"
/>

// ✅ Good: Clear, specific
<Dialog
  title="Delete this post?"
  message="This post will be permanently deleted. You can't undo this action."
  confirmButton="Delete Post"
  cancelButton="Cancel"
  variant="destructive"
/>
```

### Placeholder Text

```typescript
// ❌ Bad: Generic
<Input placeholder="Enter value" />

// ✅ Good: Helpful example
<Input placeholder="e.g., john@example.com" />
<Input placeholder="e.g., My Awesome Project" />
<TextArea placeholder="Tell us what happened..." />
```

---

## Voice & Tone Guide

### Brand Voice (Consistent)

```markdown
## TechStart Voice

**Professional but friendly**

- We're experts, but we don't talk down to you
- Use "we" and "you" (not "I" or "users")

**Clear and concise**

- Short sentences
- Simple words
- No jargon (unless necessary)

**Helpful and supportive**

- Anticipate questions
- Provide context
- Offer next steps
```

### Tone (Varies by context)

```typescript
// Tone: Excited (product launch)
"We're thrilled to announce auto-scaling! 🎉"

// Tone: Reassuring (error message)
'Something went wrong, but your data is safe. Please try again.'

// Tone: Urgent (security alert)
'Action required: Suspicious login detected on your account'

// Tone: Casual (success message)
'All set! Your changes are live.'

// Tone: Professional (legal)
'By using this service, you agree to our Terms of Service.'
```

---

## Copywriting Checklist

**Before Publishing:**

- [ ] Is it clear? (Can a 12-year-old understand it?)
- [ ] Is it concise? (Remove unnecessary words)
- [ ] Is it specific? (Use numbers, examples)
- [ ] Is it actionable? (What should user do?)
- [ ] Is it consistent? (Matches brand voice)
- [ ] Is it accessible? (Screen reader friendly)
- [ ] Is it scannable? (Headings, bullets, short paragraphs)

---

## Copywriting Resources

### Power Words

**Urgency:** Now, Today, Limited, Ending, Hurry, Fast
**Value:** Free, Save, Bonus, Extra, Plus
**Trust:** Guaranteed, Proven, Certified, Official, Secure
**Ease:** Easy, Simple, Quick, Effortless, Instant

### Headline Formulas

```markdown
"How to [achieve goal] without [pain point]"
→ "How to deploy faster without complex configs"

"[Number] ways to [achieve benefit]"
→ "5 ways to ship code with confidence"

"Get [desired outcome] in [timeframe]"
→ "Get to production in 30 seconds"

"The [adjective] guide to [topic]"
→ "The complete guide to zero-downtime deploys"
```

---

## When to Use Me

**Perfect for:**

- Writing UX copy (buttons, errors, forms)
- Creating landing pages
- Writing product descriptions
- Drafting email campaigns
- Building onboarding flows

**I'll help you:**

- Write clear, actionable copy
- Match your brand voice
- Improve conversion rates
- Enhance user experience
- Create consistent messaging

## What I'll Create

```
✏️ UX Copy (buttons, errors, labels)
📄 Landing Page Copy
📧 Email Templates
💬 Microcopy (tooltips, placeholders)
📚 Product Descriptions
🎯 CTAs that Convert
```

Let's create copy that connects with your users!
