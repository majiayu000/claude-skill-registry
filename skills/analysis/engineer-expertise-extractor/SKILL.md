---
name: engineer-expertise-extractor
description: Research and extract an engineer's coding style, patterns, and best practices from their GitHub contributions. Creates structured knowledge base for replicating their expertise.
---

# Engineer Expertise Extractor

Extract and document an engineer's coding expertise by analyzing their GitHub contributions, creating a structured knowledge base that captures their coding style, patterns, best practices, and architectural decisions.

## What This Skill Does

Researches an engineer's work to create a "digital mentor" by:
- **Analyzing Pull Requests** - Extract code patterns, review style, decisions
- **Extracting Coding Style** - Document their preferences and conventions
- **Identifying Patterns** - Common solutions and approaches they use
- **Capturing Best Practices** - Their quality standards and guidelines
- **Organizing Examples** - Real code samples from their work
- **Documenting Decisions** - Architectural choices and reasoning

## Why This Matters

**Knowledge Preservation:**
- Capture expert knowledge before they leave
- Document tribal knowledge
- Create mentorship materials
- Onboard new engineers faster

**Consistency:**
- Align team coding standards
- Replicate expert approaches
- Maintain code quality
- Scale expertise across team

**Learning:**
- Learn from senior engineers
- Understand decision-making
- See real-world patterns
- Improve code quality

## How It Works

### 1. Research Phase
Using GitHub CLI (`gh`), the skill:
- Fetches engineer's pull requests
- Analyzes code changes
- Reviews their comments and feedback
- Extracts patterns and conventions
- Identifies their expertise areas

### 2. Analysis Phase
Categorizes findings into:
- **Coding Style** - Formatting, naming, structure
- **Patterns** - Common solutions and approaches
- **Best Practices** - Quality guidelines
- **Architecture** - Design decisions
- **Testing** - Testing approaches
- **Code Review** - Feedback patterns
- **Documentation** - Doc style and practices

### 3. Organization Phase
Creates structured folders:
```
engineer_profiles/
└── [engineer_name]/
    ├── README.md (overview)
    ├── coding_style/
    │   ├── languages/
    │   ├── naming_conventions.md
    │   ├── code_structure.md
    │   └── formatting_preferences.md
    ├── patterns/
    │   ├── common_solutions.md
    │   ├── design_patterns.md
    │   └── code_examples/
    ├── best_practices/
    │   ├── code_quality.md
    │   ├── testing_approach.md
    │   ├── performance.md
    │   └── security.md
    ├── architecture/
    │   ├── design_decisions.md
    │   ├── tech_choices.md
    │   └── trade_offs.md
    ├── code_review/
    │   ├── feedback_style.md
    │   ├── common_suggestions.md
    │   └── review_examples.md
    └── examples/
        ├── by_language/
        ├── by_pattern/
        └── notable_prs/
```

## Output Structure

### Engineer Profile README

**Contains:**
- Engineer overview
- Areas of expertise
- Languages and technologies
- Key contributions
- Coding philosophy
- How to use this profile

### Coding Style Documentation

**Captures:**
- Naming conventions (variables, functions, classes)
- Code structure preferences
- File organization
- Comment style
- Formatting preferences
- Language-specific idioms

**Example:**
```markdown
# Coding Style: [Engineer Name]

## Naming Conventions

### Variables
- Use descriptive names: `userAuthentication` not `ua`
- Boolean variables: `isActive`, `hasPermission`, `canEdit`
- Collections: plural names `users`, `items`, `transactions`

### Functions
- Verb-first: `getUserById`, `validateInput`, `calculateTotal`
- Pure functions preferred
- Single responsibility

### Classes
- PascalCase: `UserService`, `PaymentProcessor`
- Interface prefix: `IUserRepository`
- Concrete implementations: `MongoUserRepository`

## Code Structure

### File Organization
- One class per file
- Related functions grouped together
- Tests alongside implementation
- Clear separation of concerns

### Function Length
- Max 20-30 lines preferred
- Extract helper functions
- Single level of abstraction
```

### Patterns Documentation

**Captures:**
- Recurring solutions
- Design patterns used
- Architectural patterns
- Problem-solving approaches

**Example:**
```markdown
# Common Patterns: [Engineer Name]

## Dependency Injection

Used consistently across services:

\`\`\`typescript
// Pattern: Constructor injection
class UserService {
  constructor(
    private readonly userRepo: IUserRepository,
    private readonly logger: ILogger
  ) {}
}
\`\`\`

**Why:** Testability, loose coupling, clear dependencies

## Error Handling

Consistent error handling approach:

\`\`\`typescript
// Pattern: Custom error types + global handler
class ValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

// Usage
if (!isValid(input)) {
  throw new ValidationError('Invalid input format');
}
\`\`\`

**Why:** Type-safe errors, centralized handling, clear debugging
```

### Best Practices Documentation

**Captures:**
- Quality standards
- Testing approaches
- Performance guidelines
- Security practices
- Documentation standards

**Example:**
```markdown
# Best Practices: [Engineer Name]

## Testing

### Unit Test Structure
- AAA pattern (Arrange, Act, Assert)
- One assertion per test preferred
- Test names describe behavior
- Mock external dependencies

\`\`\`typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      // Arrange
      const userData = { email: 'test@example.com', name: 'Test' };
      const mockRepo = createMockRepository();

      // Act
      const result = await userService.createUser(userData);

      // Assert
      expect(result.id).toBeDefined();
      expect(result.email).toBe(userData.email);
    });
  });
});
\`\`\`

### Test Coverage
- Aim for 80%+ coverage
- 100% coverage for critical paths
- Integration tests for APIs
- E2E tests for user flows

## Code Review Standards

### What to Check
- [ ] Tests included and passing
- [ ] No console.logs remaining
- [ ] Error handling present
- [ ] Comments explain "why" not "what"
- [ ] No hardcoded values
- [ ] Security considerations addressed
```

### Architecture Documentation

**Captures:**
- Design decisions
- Technology choices
- Trade-offs made
- System design approaches

**Example:**
```markdown
# Architectural Decisions: [Engineer Name]

## Decision: Microservices vs Monolith

**Context:** Scaling user service
**Decision:** Start monolith, extract services when needed
**Reasoning:**
- Team size: 5 engineers
- Product stage: MVP
- Premature optimization risk
- Easier debugging and deployment

**Trade-offs:**
- Monolith pros: Simpler, faster development
- Monolith cons: Harder to scale later
- Decision: Optimize for current needs, refactor when hitting limits

## Decision: REST vs GraphQL

**Context:** API design for mobile app
**Decision:** REST with versioning
**Reasoning:**
- Team familiar with REST
- Simple use cases
- Caching easier
- Over-fetching not a problem yet

**When to reconsider:** If frontend needs complex queries
```

### Code Review Documentation

**Captures:**
- Feedback patterns
- Review approach
- Common suggestions
- Communication style

**Example:**
```markdown
# Code Review Style: [Engineer Name]

## Review Approach

### Priority Order
1. Security vulnerabilities
2. Logic errors
3. Test coverage
4. Code structure
5. Naming and style

### Feedback Style
- Specific and constructive
- Explains "why" behind suggestions
- Provides examples
- Asks questions to understand reasoning

### Common Suggestions

**Security:**
- "Consider input validation here"
- "This query is vulnerable to SQL injection"
- "Should we rate-limit this endpoint?"

**Performance:**
- "This N+1 query could be optimized with a join"
- "Consider caching this expensive operation"
- "Memoize this pure function"

**Testing:**
- "Can we add a test for the error case?"
- "What happens if the API returns null?"
- "Let's test the boundary conditions"

**Code Quality:**
- "Can we extract this into a helper function?"
- "This function is doing too many things"
- "Consider a more descriptive variable name"
```

## Using This Skill

### Extract Engineer Profile

```bash
./scripts/extract_engineer.sh [github-username]
```

**Interactive workflow:**
1. Enter GitHub username
2. Select repository scope (all/specific org)
3. Choose analysis depth (last N PRs)
4. Specify focus areas (languages, topics)
5. Extract and organize findings

**Output:** Structured profile in `engineer_profiles/[username]/`

### Analyze Specific Repository

```bash
./scripts/analyze_repo.sh [repo-url] [engineer-username]
```

Focuses analysis on specific repository contributions.

### Update Existing Profile

```bash
./scripts/update_profile.sh [engineer-username]
```

Adds new PRs and updates existing profile.

## Research Sources

### GitHub CLI Queries

**Pull Requests:**
```bash
gh pr list --author [username] --limit 100 --state all
gh pr view [pr-number] --json title,body,files,reviews,comments
```

**Code Changes:**
```bash
gh pr diff [pr-number]
gh api repos/{owner}/{repo}/pulls/{pr}/files
```

**Reviews:**
```bash
gh pr view [pr-number] --comments
gh api repos/{owner}/{repo}/pulls/{pr}/reviews
```

**Commits:**
```bash
gh api search/commits --author [username]
```

### Analysis Techniques

**Pattern Recognition:**
- Identify recurring code structures
- Extract common solutions
- Detect naming patterns
- Find architectural choices

**Style Extraction:**
- Analyze formatting consistency
- Extract naming conventions
- Identify comment patterns
- Detect structural preferences

**Best Practice Identification:**
- Look for testing patterns
- Find error handling approaches
- Identify security practices
- Extract performance optimizations

## Use Cases

### 1. Onboarding New Engineers

**Problem:** New engineer needs to learn team standards
**Solution:** Provide senior engineer's profile as reference

**Benefits:**
- Real examples from codebase
- Understand team conventions
- See decision-making process
- Learn best practices

### 2. Code Review Training

**Problem:** Teaching good code review skills
**Solution:** Study experienced reviewer's feedback patterns

**Benefits:**
- Learn what to look for
- Understand feedback style
- See common issues
- Improve review quality

### 3. Knowledge Transfer

**Problem:** Senior engineer leaving, knowledge lost
**Solution:** Extract their expertise before departure

**Benefits:**
- Preserve tribal knowledge
- Document decisions
- Maintain code quality
- Reduce bus factor

### 4. Establishing Team Standards

**Problem:** Inconsistent coding styles across team
**Solution:** Extract patterns from best engineers, create standards

**Benefits:**
- Evidence-based standards
- Real-world examples
- Buy-in from team
- Consistent codebase

### 5. AI Agent Training

**Problem:** Agent needs to code like specific engineer
**Solution:** Provide extracted profile to agent

**Benefits:**
- Match expert's style
- Follow their patterns
- Apply their best practices
- Maintain consistency

## Profile Usage by Agents

When an agent has access to an engineer profile, it can:

**Code Generation:**
- Follow extracted naming conventions
- Use identified patterns
- Apply documented best practices
- Match architectural style

**Code Review:**
- Provide feedback in engineer's style
- Check for common issues they'd catch
- Apply their quality standards
- Match their priorities

**Problem Solving:**
- Use their common solutions
- Follow their architectural approach
- Apply their design patterns
- Consider their trade-offs

**Example Agent Prompt:**
```
"Using the profile at engineer_profiles/senior_dev/, write a user service
following their coding style, patterns, and best practices. Pay special
attention to their error handling approach and testing standards."
```

## Best Practices

### Research Ethics

**DO:**
- ✅ Get permission before extracting
- ✅ Focus on public contributions
- ✅ Respect privacy
- ✅ Use for learning and improvement

**DON'T:**
- ❌ Extract without permission
- ❌ Share profiles externally
- ❌ Include sensitive information
- ❌ Use for performance reviews

### Profile Maintenance

**Regular Updates:**
- Refresh every quarter
- Add new significant PRs
- Update with latest patterns
- Archive outdated practices

**Quality Control:**
- Verify extracted patterns
- Review examples for relevance
- Update documentation
- Remove deprecated practices

### Effective Usage

**For Learning:**
- Study patterns with context
- Understand reasoning behind choices
- Practice applying techniques
- Ask questions when unclear

**For Replication:**
- Start with style guide
- Reference patterns for similar problems
- Adapt to current context
- Don't blindly copy

## Limitations

**What This Extracts:**
- ✅ Coding style and conventions
- ✅ Common patterns and approaches
- ✅ Best practices and guidelines
- ✅ Architectural decisions
- ✅ Review feedback patterns

**What This Doesn't Capture:**
- ❌ Real-time problem-solving process
- ❌ Verbal communication style
- ❌ Meeting discussions
- ❌ Design phase thinking
- ❌ Interpersonal mentoring

## Future Enhancements

**Potential additions:**
- Slack message analysis (communication style)
- Design doc extraction (design thinking)
- Meeting notes analysis (decision process)
- Video analysis (pair programming sessions)
- Code metrics tracking (evolution over time)

## Example Output

```
engineer_profiles/
└── senior_dev/
    ├── README.md
    │   # Senior Dev - Staff Engineer
    │   Expertise: TypeScript, Node.js, System Design
    │   Focus: API design, performance optimization
    │
    ├── coding_style/
    │   ├── typescript_style.md
    │   ├── naming_conventions.md
    │   └── code_structure.md
    │
    ├── patterns/
    │   ├── dependency_injection.md
    │   ├── error_handling.md
    │   └── examples/
    │       ├── service_pattern.ts
    │       └── repository_pattern.ts
    │
    ├── best_practices/
    │   ├── testing_strategy.md
    │   ├── code_quality.md
    │   └── performance.md
    │
    ├── architecture/
    │   ├── api_design.md
    │   ├── database_design.md
    │   └── scaling_approach.md
    │
    ├── code_review/
    │   ├── feedback_examples.md
    │   └── review_checklist.md
    │
    └── examples/
        └── notable_prs/
            ├── pr_1234_auth_refactor.md
            └── pr_5678_performance_fix.md
```

## Summary

This skill transforms an engineer's GitHub contributions into a structured, reusable knowledge base. It captures their expertise in a format that:

- **Humans can learn from** - Clear documentation with examples
- **Agents can replicate** - Structured patterns and guidelines
- **Teams can adopt** - Evidence-based best practices
- **Organizations can preserve** - Knowledge that survives turnover

**The goal:** Make expertise scalable, learnable, and replicable.

---

**"The best way to learn is from those who have already mastered it."**
