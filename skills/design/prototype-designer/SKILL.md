---
name: Prototype Designer
description: Create interactive prototypes, design user flows, implement prototype testing strategies, and manage handoff to development. Validate ideas before building.
version: 1.0.0
tags: [prototyping, user-flows, interaction-design, testing]
---

# Prototype Designer

Validate ideas through interactive prototypes before writing code.

## Core Principle

**Test before you build.**

Prototypes let you:

- Validate assumptions
- Test with real users
- Iterate faster than code
- Communicate ideas clearly
- Reduce development waste

---

## Phase 1: Choosing Prototyping Tools

### Tool Comparison

| Tool         | Best For                          | Learning Curve | Fidelity  |
| ------------ | --------------------------------- | -------------- | --------- |
| **Figma**    | Full designs, collaboration       | Medium         | High      |
| **Framer**   | Code-based, advanced interactions | High           | Very High |
| **ProtoPie** | Complex interactions, sensors     | Medium         | Very High |
| **Adobe XD** | Adobe ecosystem users             | Low            | High      |
| **InVision** | Design handoff, simple clicks     | Low            | Medium    |
| **Axure**    | Complex logic, documentation      | High           | High      |

### Quick Start Recommendations

**Beginner:** Start with Figma

- Built-in to design tool
- No separate app needed
- Intuitive interactions
- Free for individuals

**Advanced:** Graduate to Framer or ProtoPie

- More complex interactions
- Variable support
- Conditional logic
- Sensor integration (mobile)

---

## Phase 2: User Flow Design

### What is a User Flow?

A user flow shows the path users take through your app to complete a task.

**Example: User Registration Flow**

```
Start
  ↓
Landing Page
  ↓
Click "Sign Up"
  ↓
Email Entry → Validation
  ↓ [Valid]
Password Entry → Validation
  ↓ [Valid]
Success Screen
  ↓
Onboarding Flow
```

### Creating User Flows in Figma

**1. Create Flow Frames:**

```
Frames needed:
├── 01-landing
├── 02-signup-form
├── 03-email-verification
├── 04-success
└── 05-onboarding-step-1
```

**2. Add Interactions:**

```
Click "Sign Up" button → Navigate to 02-signup-form
Click "Submit" → Navigate to 03-email-verification
Click "Continue" → Navigate to 04-success
```

**3. Add Overlays:**

```
Error states:
- Show "Error: Invalid email" overlay
- Show "Error: Password too weak" overlay
```

### User Flow Template

```typescript
// user-flows.ts

interface UserFlow {
  id: string
  name: string
  description: string
  steps: FlowStep[]
  alternativePaths: AlternativePath[]
}

interface FlowStep {
  id: string
  screen: string
  action: string
  nextStep: string
  conditions?: string[]
}

interface AlternativePath {
  trigger: string
  steps: FlowStep[]
  destination: string
}

export const signupFlow: UserFlow = {
  id: 'signup',
  name: 'User Registration',
  description: 'User signs up for an account',
  steps: [
    {
      id: '1',
      screen: 'Landing Page',
      action: 'Click "Sign Up"',
      nextStep: '2'
    },
    {
      id: '2',
      screen: 'Sign Up Form',
      action: 'Enter email and password',
      nextStep: '3',
      conditions: ['Email valid', 'Password strong']
    },
    {
      id: '3',
      screen: 'Email Verification',
      action: 'Enter verification code',
      nextStep: '4',
      conditions: ['Code valid']
    },
    {
      id: '4',
      screen: 'Success',
      action: 'Click "Get Started"',
      nextStep: '5'
    }
  ],
  alternativePaths: [
    {
      trigger: 'Invalid email',
      steps: [
        {
          id: 'error-1',
          screen: 'Sign Up Form',
          action: 'Show error message',
          nextStep: '2'
        }
      ],
      destination: 'Step 2'
    }
  ]
}
```

---

## Phase 3: Interactive Prototyping

### Figma Prototyping Basics

**1. Basic Click Navigation:**

```
Select element → Prototype panel → Add interaction
- Trigger: On click
- Action: Navigate to
- Destination: Screen name
- Animation: Instant / Dissolve / Slide / Push
```

**2. Hover States:**

```
Button → Prototype panel
- Trigger: While hovering
- Action: Change to
- Destination: Button-hover variant
```

**3. Scroll Behavior:**

```
Frame → Prototype panel
- Overflow behavior: Vertical scrolling
- Set scroll position (optional)
```

**4. Smart Animate:**

```
Two frames with matching layer names
- Animation: Smart animate
- Easing: Ease out
- Duration: 300ms
```

### Advanced Interactions

**Conditional Logic (Variables):**

```typescript
// Figma Variables (Beta)
Variables:
  - isLoggedIn: Boolean
  - userType: String
  - itemCount: Number

Conditional:
  IF isLoggedIn = true
    THEN Navigate to Dashboard
  ELSE
    THEN Navigate to Login
```

**Multi-Step Forms:**

```
Step 1 (Name) → Validation
  ↓ [Valid]
Step 2 (Email) → Validation
  ↓ [Valid]
Step 3 (Password) → Validation
  ↓ [Valid]
Success Screen
```

**State Management:**

```
Component: Button
States:
  - Default
  - Hover
  - Pressed
  - Disabled
  - Loading

Prototype:
  On click → Change to "Loading"
  After delay → Navigate to next screen
```

---

## Phase 4: Framer Prototyping

### When to Use Framer

Use Framer for:

- Complex animations
- Code-driven interactions
- Real data integration
- Advanced logic
- Production-ready components

### Framer Code Component Example

```tsx
// components/Counter.tsx

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 16
      }}
    >
      <h1 style={{ fontSize: 48 }}>{count}</h1>
      <div style={{ display: 'flex', gap: 8 }}>
        <button
          onClick={() => setCount(count - 1)}
          style={{
            padding: '12px 24px',
            fontSize: 16,
            borderRadius: 8,
            border: 'none',
            cursor: 'pointer',
            background: '#0066cc',
            color: 'white'
          }}
        >
          -
        </button>
        <button
          onClick={() => setCount(count + 1)}
          style={{
            padding: '12px 24px',
            fontSize: 16,
            borderRadius: 8,
            border: 'none',
            cursor: 'pointer',
            background: '#0066cc',
            color: 'white'
          }}
        >
          +
        </button>
      </div>
    </div>
  )
}
```

### Framer Motion Animations

```tsx
// components/AnimatedCard.tsx

import { motion } from 'framer-motion'

export function AnimatedCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      style={{
        width: 300,
        height: 200,
        background: 'white',
        borderRadius: 16,
        padding: 24,
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        cursor: 'pointer'
      }}
    >
      <h2>Card Title</h2>
      <p>Hover or click me!</p>
    </motion.div>
  )
}
```

---

## Phase 5: Prototype Testing

### Usability Testing Plan

**1. Define Goals:**

- What do you want to learn?
- What tasks should users complete?
- What metrics will you measure?

**2. Recruit Participants:**

- 5-8 participants (enough to find major issues)
- Match your target audience
- Diverse backgrounds

**3. Create Test Script:**

```markdown
# Prototype Usability Test Script

## Introduction (2 min)

"Thank you for helping us test this prototype. There are no wrong answers - we're testing the design, not you. Please think aloud as you complete tasks."

## Tasks (20 min)

### Task 1: Sign Up

"Imagine you want to create an account. Show me how you would do that."

Success criteria:

- [ ] Found sign up button
- [ ] Entered email
- [ ] Entered password
- [ ] Completed verification
- [ ] Reached dashboard

### Task 2: Find Settings

"You want to change your notification preferences. Show me how you would do that."

Success criteria:

- [ ] Navigated to settings
- [ ] Found notifications section
- [ ] Changed setting
- [ ] Saved changes

## Questions (5 min)

1. What was the easiest part?
2. What was the hardest part?
3. What would you change?
4. Would you use this? Why/why not?
```

**4. Conduct Tests:**

- Record sessions (with permission)
- Take notes
- Don't help unless stuck
- Ask follow-up questions

**5. Analyze Results:**

```typescript
// test-results.ts

interface TestResult {
  participant: string
  task: string
  completed: boolean
  timeSeconds: number
  errors: string[]
  feedback: string
}

const results: TestResult[] = [
  {
    participant: 'User 1',
    task: 'Sign up',
    completed: true,
    timeSeconds: 45,
    errors: ['Missed verification step'],
    feedback: 'Form was clear but verification was confusing'
  }
  // ...
]

// Calculate metrics
function analyzeResults(results: TestResult[]) {
  const completionRate = results.filter(r => r.completed).length / results.length
  const avgTime = results.reduce((sum, r) => sum + r.timeSeconds, 0) / results.length
  const commonErrors = findCommonErrors(results)

  return {
    completionRate: `${(completionRate * 100).toFixed(0)}%`,
    avgTime: `${avgTime.toFixed(0)}s`,
    commonErrors
  }
}
```

### Remote Testing Tools

**Unmoderated:**

- **UserTesting.com** - Recruit + test
- **Maze** - Analytics for prototypes
- **Lookback** - Session recording

**Moderated:**

- **Zoom** - Screen sharing
- **Google Meet** - Built-in recording
- **Loom** - Async feedback

---

## Phase 6: Developer Handoff

### Prepare Prototype for Handoff

**1. Documentation:**

```markdown
# Prototype Documentation

## User Flows

- [Sign Up Flow](figma-link)
- [Purchase Flow](figma-link)

## Interactions

- Button hover: Scale 1.05, 200ms ease-out
- Page transition: Slide right, 300ms ease-in-out
- Error shake: Translate X ±10px, 3 times, 100ms

## States

- Default
- Hover
- Active
- Disabled
- Loading
- Error

## Animations

- Fade in: opacity 0→1, 300ms
- Slide up: translateY 20px→0, 400ms ease-out

## Breakpoints

- Mobile: 375px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px+
```

**2. Annotate Prototype:**

In Figma:

- Add notes explaining complex interactions
- Document edge cases
- Show error states
- Clarify timing

**3. Export Specifications:**

```typescript
// specs/interactions.ts

export const interactions = {
  button: {
    hover: {
      scale: 1.05,
      duration: 200,
      easing: 'ease-out'
    },
    click: {
      scale: 0.95,
      duration: 100,
      easing: 'ease-in'
    }
  },
  page: {
    transition: {
      type: 'slide',
      direction: 'right',
      duration: 300,
      easing: 'ease-in-out'
    }
  },
  modal: {
    open: {
      backdrop: { opacity: 0.5 },
      content: { scale: 0.9, opacity: 0 },
      to: { scale: 1, opacity: 1 },
      duration: 200
    },
    close: {
      backdrop: { opacity: 0 },
      content: { scale: 0.9, opacity: 0 },
      duration: 200
    }
  }
}
```

**4. Create Implementation Guide:**

```markdown
# Implementation Guide

## Tech Stack Recommendations

### Animations

- **Framer Motion** - React animations
- **GSAP** - Advanced animations
- **CSS Transitions** - Simple effects

### State Management

- **useState** - Local component state
- **Zustand** - Global state
- **React Query** - Server state

### Forms

- **React Hook Form** - Form validation
- **Zod** - Schema validation

## Code Examples

### Button with Hover Effect

\`\`\`tsx
import { motion } from 'framer-motion'

export function Button({ children, onClick }) {
return (
<motion.button
whileHover={{ scale: 1.05 }}
whileTap={{ scale: 0.95 }}
transition={{ duration: 0.2 }}
onClick={onClick}
style={{
        padding: '12px 24px',
        borderRadius: 8,
        border: 'none',
        background: '#0066cc',
        color: 'white',
        fontSize: 16,
        fontWeight: 600,
        cursor: 'pointer'
      }} >
{children}
</motion.button>
)
}
\`\`\`
```

---

## Best Practices

### 1. Start Low-Fidelity

Begin with sketches/wireframes before high-fidelity prototypes.

**Progression:**

1. Paper sketches (1-2 hours)
2. Wireframes (half day)
3. High-fidelity design (1-2 days)
4. Interactive prototype (1 day)
5. User testing (2-3 days)
6. Iteration (1-2 days)

### 2. Focus on Critical Paths

Prototype the most important user flows first:

- Sign up / Login
- Core feature usage
- Purchase / Checkout
- Onboarding

Skip:

- Settings pages
- Admin panels
- Edge cases (initially)

### 3. Use Real Content

Avoid "Lorem ipsum" - use realistic:

- Text lengths
- Image dimensions
- Data variations
- Error messages

### 4. Test Early, Test Often

- Test wireframes before designing
- Test prototypes before building
- Test with 5 users, iterate, test again

### 5. Maintain Prototype

Keep prototype updated as:

- Designs change
- Feedback comes in
- Features are added
- Bugs are found

---

## Common Patterns

### Pattern 1: Loading States

```tsx
// Loading state progression
1. Button: "Submit" (clickable)
2. Button: "Loading..." (disabled, spinner)
3. Button: "Success!" (green, checkmark)
4. After 2s: Back to "Submit"
```

### Pattern 2: Form Validation

```tsx
// Real-time validation
1. User types in field
2. On blur: Validate
3. Show error if invalid
4. Disable submit until all valid
5. Show success after submit
```

### Pattern 3: Modal Flows

```tsx
// Modal interaction
1. Click trigger → Open modal (backdrop + animation)
2. User interacts with modal content
3. Click outside / X button → Close modal
4. Prevent scroll on body when open
```

---

## Tools & Resources

**Prototyping:**

- [Figma](https://www.figma.com/) - All-in-one design
- [Framer](https://www.framer.com/) - Code-based prototyping
- [ProtoPie](https://www.protopie.io/) - Advanced interactions

**Testing:**

- [Maze](https://maze.co/) - Prototype testing
- [UserTesting](https://www.usertesting.com/) - User research
- [Hotjar](https://www.hotjar.com/) - Heatmaps & recordings

**Animation:**

- [Lottie](https://lottiefiles.com/) - Animation library
- [Principle](https://principleformac.com/) - Animation tool
- [Jitter](https://jitter.video/) - Motion design

**Related Skills:**

- `ux-designer` - User experience design
- `frontend-builder` - Implementing prototypes
- `user-researcher` - Testing & validation

---

**Prototype fast, validate early, build right.** 🚀
