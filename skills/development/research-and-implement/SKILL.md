---
name: research-and-implement
description: Researches implementation approaches using browser automation via /chrome, then implements the best solution. Use when building new features, solving unfamiliar problems, or need to find best practices before implementing. Combines learning with doing.
---

# Research and Implement

Combines research with implementation - uses browser automation to find best practices, then builds the solution based on what's learned.

## When I Activate

I activate when:
- Building a feature you haven't built before
- Integrating a new library or API
- User says "research how to..." or "find the best way to..."
- Need to understand best practices before implementing
- Unclear what approach to take
- Want to see how others solve similar problems

## Philosophy

**Learn first, build second:**
- Research saves debugging time
- Following best practices prevents common mistakes
- Understanding patterns helps you learn
- Adapting examples is faster than starting from scratch

**Use real sources:**
- Official documentation (most reliable)
- Popular examples and tutorials
- Stack Overflow for specific problems
- GitHub repos for implementation patterns

---

## Research and Implement Workflow

### Phase 1: Define What to Research

**Clarify the goal:**
```
1. What exactly are we trying to build?
2. What technology/library are we using?
3. What's the specific challenge or uncertainty?
4. What decisions do we need to make?
```

**Example:**
```
Goal: Add Stripe payments to checkout page
Technology: Stripe API with React
Challenge: Don't know best practices for client-side integration
Decisions: Which Stripe integration approach to use
```

---

### Phase 2: Research Using /chrome

**Step 1: Connect and Navigate**
```
1. Connect to Chrome: /chrome
2. Navigate to primary source (usually official docs)
3. Read relevant sections
4. Extract key information
```

**Step 2: Find Examples**
```
1. Navigate to example repositories or tutorials
2. Read implementation code
3. Identify patterns and best practices
4. Note any gotchas or warnings
```

**Step 3: Check for Common Issues**
```
1. Search Stack Overflow for related problems
2. Read about common mistakes
3. Find solutions to edge cases
4. Note testing approaches
```

**Step 4: Compare Approaches**
```
If multiple ways exist:
1. List the options
2. Research pros/cons of each
3. Recommend the best fit for this project
4. Explain the reasoning
```

---

### Phase 3: Document Findings

**Research Summary Format:**
```
## Research Summary

**Goal:** [What we're trying to build]

**Sources Reviewed:**
- [Official docs link]
- [Tutorial/example link]
- [Stack Overflow discussions]

**Key Findings:**
1. [Important discovery 1]
2. [Important discovery 2]
3. [Important discovery 3]

**Recommended Approach:**
[Which approach to use and why]

**Implementation Pattern:**
[Code pattern to follow based on research]

**Common Gotchas to Avoid:**
- [Pitfall 1]
- [Pitfall 2]

**Testing Strategy:**
[How to verify it works]
```

---

### Phase 4: Implement Based on Research

**Implementation Steps:**
```
1. Start with the pattern found in research
2. Adapt it to the project's structure
3. Follow best practices discovered
4. Add error handling based on common issues found
5. Include comments explaining key parts
6. Implement testing based on research
```

**Code Organization:**
```
1. Structure code like the examples (if good pattern)
2. Use naming conventions from docs
3. Follow API usage patterns exactly
4. Include necessary configuration
```

---

### Phase 5: Verify with Test-and-Verify Skill

After implementation:
```
1. Test the implementation thoroughly
2. Verify it matches documentation expectations
3. Check for issues mentioned in research
4. Confirm it works end-to-end
```

---

## Research Strategies by Task Type

### New Library Integration

**Research Checklist:**
```
1. Official "Getting Started" documentation
2. Installation requirements
3. Basic setup/configuration
4. Simple "Hello World" example
5. Common patterns for our use case
6. Best practices and recommendations
7. Common errors and solutions
```

**Browser Workflow:**
```
/chrome navigate to [library docs]
Read: Installation section
Read: Quick Start guide
Read: Best Practices
Navigate to examples repository
Find example similar to our use case
Extract relevant code patterns
```

**Example: Research React Query**
```
1. Navigate to tanstack.com/query/latest/docs/react/overview
2. Read core concepts
3. Find: Basic usage pattern
4. Navigate to examples
5. Extract: Query setup, error handling, loading states
6. Note: Recommended patterns for mutations
7. Implement based on findings
```

---

### API Integration

**Research Checklist:**
```
1. API documentation (endpoints, auth, data formats)
2. Authentication method (API key, OAuth, etc.)
3. Request/response examples
4. Rate limits and constraints
5. Error codes and handling
6. Example implementations
7. Testing approach (sandbox, test keys)
```

**Browser Workflow:**
```
/chrome navigate to [API docs]
Read: Authentication section
Read: Endpoint documentation
Find: Example requests/responses
Navigate to code examples
Extract: Client setup, error handling
Check: Common issues on Stack Overflow
```

**Example: Research Stripe API**
```
1. Navigate to stripe.com/docs
2. Read: Payment Intents API
3. Find: Client-side integration pattern
4. Check: Security best practices
5. Extract: Example code for checkout
6. Note: Testing with test mode keys
7. Implement Stripe Elements based on official example
```

---

### Solving Specific Problems

**Research Checklist:**
```
1. Understand the exact problem
2. Search for similar problems
3. Read multiple solutions
4. Identify most reliable/recent answers
5. Check if solution applies to our stack
6. Look for caveats or limitations
```

**Browser Workflow:**
```
/chrome navigate to Stack Overflow or Google
Search: [specific error or problem]
Read top 3-5 results
Identify common solution pattern
Check dates (prefer recent)
Verify applies to our tech stack
Extract solution approach
```

**Example: Research "React form validation"**
```
1. Search: "react form validation best practices 2025"
2. Read articles from top results
3. Compare approaches:
   - Built-in HTML5 validation
   - React Hook Form library
   - Custom validation logic
4. Check bundle sizes and complexity
5. Recommend: React Hook Form for complex forms
6. Implement based on official examples
```

---

### Design Pattern Research

**Research Checklist:**
```
1. Find pattern definition and use cases
2. See example implementations
3. Understand pros and cons
4. Check if it fits our problem
5. Find adaptation examples in our tech stack
```

**Browser Workflow:**
```
/chrome navigate to [pattern documentation]
Read: Pattern description
Find: When to use vs when not to use
Navigate to examples in our framework
Extract: Implementation pattern
Check: Real-world usage examples
```

**Example: Research "Custom React Hooks Pattern"**
```
1. Navigate to react.dev/learn/reusing-logic-with-custom-hooks
2. Read when to create custom hooks
3. See examples of common hooks
4. Navigate to real projects using pattern
5. Extract structure and naming conventions
6. Implement custom hook following patterns found
```

---

## Source Quality Evaluation

### Trusted Sources (Use First)

**Official Documentation:**
- Most accurate and up-to-date
- Shows intended usage
- Includes best practices

**Official Examples:**
- GitHub repos by library maintainers
- Code sandbox examples
- Starter templates

### Good Sources (Use Second)

**Popular Tutorials:**
- Recent blog posts from recognized developers
- Video tutorials from established channels
- Courses from reputable platforms

**Stack Overflow:**
- High-voted answers
- Answers marked as accepted
- Recent answers (within 1-2 years)

### Questionable Sources (Verify Before Using)

**Random Blogs:**
- May be outdated
- May show anti-patterns
- Verify against official docs

**Old Stack Overflow:**
- Answers from 5+ years ago
- May reference deprecated APIs
- Check if still applicable

---

## Research Notes Template

While researching, keep notes:

```
## Research Notes: [Feature Name]

### Official Docs Findings
- Key API: [endpoint or method]
- Auth required: [type]
- Rate limits: [if applicable]
- Data format: [JSON structure]

### Example Code Found
[Paste or summarize relevant code snippet]
Source: [URL]

### Best Practices
1. [Practice 1]
2. [Practice 2]
3. [Practice 3]

### Common Errors to Avoid
- [Error 1]: [How to avoid]
- [Error 2]: [How to avoid]

### Testing Approach
- [How to test this feature]
- [What to verify]

### Dependencies Needed
- [Package 1]: [version]
- [Package 2]: [version]

### Configuration Required
[Any setup or config needed]

### Implementation Plan
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

---

## Adaptation Guidelines

When adapting researched code:

### Do:
- Follow the core pattern
- Adapt variable names to match your project
- Adjust data structures to fit your needs
- Add error handling for your specific use case
- Include comments explaining adaptations

### Don't:
- Copy code you don't understand
- Skip error handling from examples
- Ignore warnings in documentation
- Mix multiple conflicting patterns
- Over-complicate beyond what docs show

---

## Research to Implementation Example

### Example: Add user authentication

**Phase 1: Research**
```
/chrome navigate to firebase.google.com/docs/auth

Findings:
- Multiple auth methods available (email, Google, etc.)
- Client SDK provides signInWithEmailAndPassword()
- Need to initialize Firebase first
- Best practice: Use auth state listener
- Handle errors with try/catch
- Store user in React context or state management

Example code found:
```javascript
const auth = getAuth();
signInWithEmailAndPassword(auth, email, password)
  .then((userCredential) => {
    const user = userCredential.user;
  })
  .catch((error) => {
    console.error(error.code, error.message);
  });
```

Common errors to avoid:
- Not handling auth state persistence
- Exposing API keys in client code (use environment variables)
- Not validating email format before sending
```

**Phase 2: Implement**
```javascript
// Adapted implementation based on research

import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';

export async function loginUser(email, password) {
  // Validate email format first (best practice from research)
  if (!email.includes('@')) {
    throw new Error('Invalid email format');
  }

  try {
    const auth = getAuth();

    // Using pattern from Firebase docs
    const userCredential = await signInWithEmailAndPassword(
      auth,
      email,
      password
    );

    // Return user data (following example structure)
    return userCredential.user;

  } catch (error) {
    // Error handling based on common errors found in research
    if (error.code === 'auth/wrong-password') {
      throw new Error('Incorrect password');
    } else if (error.code === 'auth/user-not-found') {
      throw new Error('No account found with this email');
    } else {
      throw new Error('Login failed. Please try again.');
    }
  }
}
```

**Phase 3: Test**
```
Use test-and-verify skill to:
1. Test with valid credentials
2. Test with invalid credentials
3. Test error messages display
4. Verify user state persists
5. Check console for errors
```

---

## Browser Automation Commands for Research

### Navigate to Documentation
```
/chrome navigate to [docs URL]
```

### Read Specific Sections
```
/chrome read page filtering for [keyword]
```

### Find Code Examples
```
/chrome find code blocks
/chrome read code examples
```

### Search for Issues
```
/chrome navigate to stackoverflow.com
/chrome search for [query]
/chrome read top answers
```

### Compare Multiple Sources
```
1. /chrome navigate to source 1
2. Take notes
3. /chrome navigate to source 2
4. Compare findings
5. /chrome navigate to source 3
6. Synthesize best approach
```

---

## Common Research Scenarios

### Scenario 1: "How do I add feature X?"

**Research Steps:**
```
1. Define feature clearly
2. Navigate to relevant library/framework docs
3. Find the section covering this feature
4. Read implementation guide
5. Find example code
6. Adapt to project
7. Implement with test-and-verify
```

---

### Scenario 2: "What's the best library for Y?"

**Research Steps:**
```
1. List candidate libraries
2. For each library:
   - Navigate to docs
   - Check bundle size
   - Read installation complexity
   - Review API simplicity
   - Check last update date
   - Read community feedback
3. Compare findings
4. Recommend best fit
5. Implement winner
```

---

### Scenario 3: "This error keeps happening"

**Research Steps:**
```
1. Copy exact error message
2. Search on Stack Overflow
3. Read top 3 answers
4. Find solution matching your stack
5. Understand why error happens
6. Implement fix
7. Verify error resolved
```

---

## Integration with Other Skills

**After research-and-implement:**
→ Use test-and-verify to confirm implementation works

**During implementation:**
→ Use code-explainer to understand complex patterns found

**If research reveals uncertainty:**
→ Use prompt-helper to structure better research queries

**If implementation fails:**
→ Use debug-buddy to troubleshoot

---

## Research Quality Checklist

Before implementing:

- [ ] Reviewed official documentation
- [ ] Found at least one working example
- [ ] Understood the core pattern
- [ ] Identified common errors to avoid
- [ ] Know how to test the implementation
- [ ] Checked for recent updates or deprecations
- [ ] Verified compatibility with project stack
- [ ] Have confidence in chosen approach

---

## Cost-Conscious Research

- Start with official docs (most reliable, saves re-research)
- Read targeted sections, not entire docs
- Use search/filtering to find specific info
- Stop when you have enough to implement confidently
- Don't over-research edge cases before building basic version
- Capture key info in notes to avoid re-researching

---

## Success Metrics

Research is successful when:
- ✅ Found clear implementation pattern
- ✅ Understand why approach is recommended
- ✅ Know common pitfalls to avoid
- ✅ Have confidence to implement
- ✅ Can test the implementation
- ✅ Learned reusable patterns/concepts

---

## Example Workflows

### Full Workflow: Add dark mode toggle

```
1. RESEARCH PHASE
   /chrome navigate to React docs on context
   Find: Context pattern for theme management
   Extract: Provider pattern

   /chrome navigate to CSS-in-JS library docs
   Find: Theme switching examples
   Extract: Light/dark theme objects

   /chrome search Stack Overflow for "React dark mode best practices"
   Find: localStorage persistence pattern
   Extract: Save preference across sessions

2. IMPLEMENTATION PHASE
   Create ThemeContext based on React docs pattern
   Create light/dark theme objects
   Add ThemeProvider to app
   Create toggle component
   Add localStorage persistence
   Style components with theme

3. VERIFICATION PHASE
   Use test-and-verify skill:
   - Toggle switches themes ✓
   - Preference persists on reload ✓
   - All components adapt to theme ✓
   - No console errors ✓

Result: ✅ Dark mode working based on researched best practices
```

---

## When Research Reveals Complexity

If research shows task is more complex than expected:

```
## Research Findings: [Task] is Complex

**What I discovered:**
[Explanation of complexity]

**Options:**
1. [Simpler approach with tradeoffs]
2. [Full approach with more work]
3. [Alternative solution]

**Recommendation:**
[Suggested path forward]

**Would you like me to:**
- Proceed with simplified version?
- Build full implementation?
- Explore alternatives?
```

This keeps you informed and in control of decisions.
