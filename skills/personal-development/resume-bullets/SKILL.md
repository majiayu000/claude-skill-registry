---
name: resume-bullet-extraction
description: |
  TRIGGERS: "resume bullet", "portfolio update", "how should I describe this?", "job application",
  resume writing, portfolio, achievement bullets, quantified impact, career documentation.
  USE WHEN: Completing significant tasks, updating resume, building portfolio, job searching.
  PROVIDES: Action-verb bullets, quantified achievements, recruiter-friendly descriptions.
---

# Resume Bullet Extraction

> "Your resume isn't a job description. It's a highlight reel of impact."

## Purpose

Transform completed work into powerful resume bullet points that demonstrate value and technical competence.

---

## The Bullet Formula

```
[Strong Action Verb] + [What You Did] + [Technical Context] + [Impact/Result]
```

### Components

| Component | Purpose | Example |
|-----------|---------|---------|
| Action Verb | Shows initiative | Engineered, Architected, Optimized |
| What You Did | The accomplishment | JWT authentication system |
| Technical Context | Shows skill | using React, Node.js, Redis |
| Impact | Why it matters | reducing auth errors by 40% |

---

## Strong Action Verbs

### Building/Creating
- Engineered
- Architected
- Developed
- Implemented
- Built
- Designed

### Improving
- Optimized
- Enhanced
- Refactored
- Modernized
- Streamlined
- Accelerated

### Problem Solving
- Resolved
- Debugged
- Eliminated
- Reduced
- Prevented
- Mitigated

### Leading/Collaborating
- Led
- Spearheaded
- Collaborated
- Mentored
- Coordinated

---

## Impact Quantification

Always try to quantify. If you can't measure directly, estimate reasonably.

### Performance
- "reducing load time by 60%"
- "improving response time from 2s to 200ms"
- "handling 10,000+ concurrent users"

### Reliability
- "achieving 99.9% uptime"
- "eliminating production errors"
- "reducing bug reports by 50%"

### Business
- "increasing user retention by 25%"
- "supporting 50,000 monthly active users"
- "saving 10 hours/week of manual work"

### Scale
- "processing 1M+ transactions daily"
- "managing 500GB of user data"
- "serving 100+ API endpoints"

---

## Bullet Templates

### Feature Implementation
```
[Verb] [feature] using [technologies] that [impact]

Examples:
- Engineered JWT authentication with refresh token rotation using Node.js and Redis, eliminating session hijacking vulnerabilities
- Built real-time notification system using WebSockets and React, improving user engagement by 35%
```

### Performance Optimization
```
[Verb] [what] by [how], resulting in [metric]

Examples:
- Optimized database queries through index analysis and query restructuring, reducing API response time by 70%
- Accelerated page load performance by implementing code splitting and lazy loading, improving Core Web Vitals by 40%
```

### Bug Fix / Problem Solving
```
[Verb] [problem] by [solution], preventing [impact]

Examples:
- Resolved race condition in checkout flow by implementing optimistic locking, preventing duplicate charges
- Eliminated memory leak in React components through proper cleanup, reducing crash reports by 90%
```

### Architecture / Refactoring
```
[Verb] [system] from [old] to [new], enabling [benefit]

Examples:
- Migrated monolithic application to microservices architecture using Docker and Kubernetes, enabling independent team deployments
- Refactored authentication module from session-based to JWT, reducing server memory usage by 60%
```

---

## Quality Checklist

- [ ] Starts with strong action verb (not "Responsible for")
- [ ] Includes specific technologies
- [ ] Has quantifiable impact OR clear business value
- [ ] Is one concise sentence
- [ ] Avoids jargon recruiters won't understand
- [ ] Demonstrates ownership ("I" is implied)
- [ ] Would make sense to a technical interviewer

---

## Bad vs Good Examples

### Bad
```
❌ "Worked on the login system"
   - No action verb, no specifics, no impact

❌ "Responsible for user authentication"
   - Passive, no accomplishment shown

❌ "Helped with performance improvements"
   - Vague, no ownership, no metrics
```

### Good
```
✅ "Engineered JWT authentication with refresh token rotation, reducing session vulnerability surface and supporting 50,000+ daily active users"

✅ "Optimized PostgreSQL queries through index analysis, reducing average API response time from 800ms to 120ms"

✅ "Built responsive dashboard using React and D3.js, enabling real-time visualization of 1M+ daily events"
```

---

## Extraction Flow

### Step 1: Identify the Highlight
> "What's the most impressive aspect of what you just built?"

Options:
- Technical complexity solved
- Business problem addressed
- Performance improved
- Scale achieved
- Security enhanced

### Step 2: Draft the Bullet
Use the formula: Verb + What + Technical Context + Impact

### Step 3: Quantify
> "Can we add numbers? How much faster? How many users? What percentage improvement?"

### Step 4: Polish
- Remove weak words ("helped", "assisted", "worked on")
- Add specific technologies
- Ensure it stands alone (no context needed)

---

## Resume Section Placement

| Bullet Type | Resume Section |
|-------------|---------------|
| Feature/System built | Projects or Experience |
| Performance optimization | Experience (shows impact) |
| Architecture decision | Experience or Technical Skills |
| Learning/Growth | Skills or Side Projects |

---

## Socratic Bullet Questions

1. **Finding impact:** "If this feature didn't exist, what would break?"
2. **Quantifying:** "How many users does this affect? How much time does it save?"
3. **Technical depth:** "What would you tell a technical interviewer about how this works?"
4. **Differentiation:** "What makes your implementation better than a basic solution?"

---

## Save Location

Bullets are compiled in STAR story files:
```
ownyourcode/career/stories/[date]-[feature-name].md
```

The resume bullet appears at the end of each story for easy extraction.
