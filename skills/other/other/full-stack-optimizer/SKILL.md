---
name: full-stack-optimizer
description: Multi-agent orchestration for comprehensive frontend + backend improvements. Use when user requests "improve the app", "optimize functionality", "make it perfect", or "enhance the system". Deploys specialized agents for parallel analysis and implementation.
version: 1.0.0
allowed-tools: [Task, Bash, Read, Write, Edit, Glob, Grep]
---

# Full-Stack Optimizer Skill

**Multi-agent orchestration for comprehensive application improvement**

## When to Use
- User says: "improve the app", "optimize functionality", "make it perfect"
- User requests: "analyze frontend and backend", "enhance the system"
- User wants: "bring it to perfection", "comprehensive improvements"
- After major feature completion: proactive optimization pass

## Agent Deployment Strategy

This skill deploys **5 specialized agents in parallel** for comprehensive analysis:

### Agent 1: Frontend Performance Analyzer
**Focus**: UI/UX, performance, accessibility, user experience
**Tasks**:
- Analyze all HTML/JS files in `/public`
- Check for unused CSS, duplicate code
- Validate accessibility (ARIA, semantic HTML)
- Test responsive design patterns
- Identify performance bottlenecks (large files, unoptimized assets)
- Check for console errors, deprecated APIs
- Validate client-side error handling

**Output**: `/.claude/reports/frontend-analysis.md`

### Agent 2: Backend API Optimizer
**Focus**: API efficiency, error handling, database queries
**Tasks**:
- Review all controllers (`/src/controllers`)
- Analyze all services (`/src/services`)
- Check for N+1 queries, missing indexes
- Validate error handling patterns
- Review API response times (check for slow endpoints)
- Identify duplicate code, refactoring opportunities
- Check for proper async/await usage
- Validate input sanitization

**Output**: `/.claude/reports/backend-analysis.md`

### Agent 3: Security & Validation Auditor
**Focus**: Security vulnerabilities, input validation, auth
**Tasks**:
- Scan for SQL injection vulnerabilities
- Check XSS prevention (input sanitization)
- Validate CORS configuration
- Review authentication/authorization flows
- Check for exposed secrets (hardcoded keys, passwords)
- Validate rate limiting implementation
- Review middleware security (helmet, express-validator)
- Check for CSRF protection

**Output**: `/.claude/reports/security-audit.md`

### Agent 4: Database & Performance Expert
**Focus**: Database optimization, caching, query performance
**Tasks**:
- Review database schema (`/src/models`)
- Analyze query patterns in services
- Check for missing indexes
- Validate connection pooling configuration
- Review Redis caching strategy
- Identify slow queries (check logs)
- Check for proper transaction usage
- Validate data normalization

**Output**: `/.claude/reports/database-optimization.md`

### Agent 5: Code Quality & Architecture Reviewer
**Focus**: Code organization, TypeScript usage, patterns
**Tasks**:
- Run ESLint and review violations
- Check TypeScript strict mode compliance
- Identify usage of `any` types (anti-pattern)
- Review file organization and module boundaries
- Check for proper error handling patterns
- Validate consistent naming conventions
- Review documentation completeness
- Check for circular dependencies

**Output**: `/.claude/reports/code-quality.md`

## Execution Flow

### Phase 1: Parallel Analysis (5 agents)
```bash
# Deploy all 5 agents in parallel (single message, multiple Task calls)
Task(subagent_type="general-purpose", description="Frontend analysis", ...)
Task(subagent_type="general-purpose", description="Backend optimization", ...)
Task(subagent_type="general-purpose", description="Security audit", ...)
Task(subagent_type="general-purpose", description="Database optimization", ...)
Task(subagent_type="general-purpose", description="Code quality review", ...)
```

**Estimated Time**: 5-10 minutes (parallel execution)

### Phase 2: Synthesis & Prioritization
After all agents complete:
1. Read all 5 reports from `/.claude/reports/`
2. Synthesize findings into unified improvement plan
3. Prioritize by:
   - **P0 (Critical)**: Security vulnerabilities, broken functionality
   - **P1 (High)**: Performance issues, poor UX, API errors
   - **P2 (Medium)**: Code quality, refactoring opportunities
   - **P3 (Low)**: Documentation, minor improvements

**Output**: `/.claude/reports/UNIFIED_IMPROVEMENT_PLAN.md`

### Phase 3: Implementation Agents (Prioritized)
Deploy implementation agents based on priority:

**Round 1: P0 Critical Fixes** (Deploy immediately)
- Security patches
- Broken functionality fixes
- Data integrity issues

**Round 2: P1 High-Impact Improvements** (Deploy after P0 complete)
- Performance optimizations
- API improvements
- UX enhancements

**Round 3: P2 Code Quality** (Deploy after P1 complete)
- Refactoring
- Type safety improvements
- Code organization

**Round 4: P3 Polish** (Optional, user approval)
- Documentation updates
- Minor UI tweaks
- Additional testing

### Phase 4: Validation & Testing
After each implementation round:
1. Run test suite: `npm test`
2. Run linter: `npm run lint`
3. Run type checker: `npm run typecheck` (if available)
4. Run build: `npm run build`
5. Test critical paths manually
6. Run deployment validator: `npm run test:render-ready`

## Detailed Agent Prompts

### Agent 1 Prompt: Frontend Performance Analyzer
```markdown
## Task
Analyze all frontend code in /public directory for performance, UX, and accessibility improvements.

## Steps
1. Use Glob to find all HTML files: `public/**/*.html`
2. Use Glob to find all JS files: `public/**/*.js`
3. Use Glob to find all CSS files: `public/**/*.css`
4. For each file:
   - Read file contents
   - Check for performance issues:
     * Large inline scripts (>1000 lines)
     * Duplicate code across files
     * Unoptimized images/assets
     * Missing compression/minification
   - Check for UX issues:
     * Poor error messages
     * Confusing navigation
     * Inconsistent styling
     * Missing loading states
   - Check for accessibility:
     * Missing ARIA labels
     * Poor semantic HTML
     * Missing alt text
     * Keyboard navigation issues
5. Test for console errors:
   - grep for `console.error`, `console.warn`
   - Check for deprecated APIs
6. Analyze bundle size (estimate):
   - Sum total file sizes
   - Identify largest files
   - Suggest code splitting opportunities

## Output Format
Create /.claude/reports/frontend-analysis.md with:
- Executive Summary (3-5 bullets)
- Performance Issues (with file paths and line numbers)
- UX Issues (with screenshots or descriptions)
- Accessibility Issues (with WCAG guidelines)
- Quick Wins (easy improvements with high impact)
- Long-term Recommendations

## Success Criteria
- All HTML/JS/CSS files analyzed
- Issues categorized by severity (P0-P3)
- Specific line numbers and file paths provided
- Actionable recommendations (not vague suggestions)
```

### Agent 2 Prompt: Backend API Optimizer
```markdown
## Task
Analyze backend API code for efficiency, error handling, and optimization opportunities.

## Steps
1. Use Glob to find all controllers: `src/controllers/**/*.ts`
2. Use Glob to find all services: `src/services/**/*.ts`
3. For each file:
   - Read file contents
   - Check for performance issues:
     * N+1 query patterns
     * Missing pagination
     * Inefficient loops
     * Blocking operations
   - Check for error handling:
     * Unhandled promise rejections
     * Missing try/catch blocks
     * Poor error messages
     * Inconsistent error formats
   - Check for code quality:
     * Duplicate logic
     * Long functions (>50 lines)
     * High complexity (nested ifs)
     * Usage of `any` types
4. Analyze API response times:
   - grep for slow operations (database queries, external calls)
   - Identify endpoints without caching
5. Check for proper async patterns:
   - grep for callback hell
   - Check for proper async/await usage

## Output Format
Create /.claude/reports/backend-analysis.md with:
- Executive Summary
- Performance Bottlenecks (with endpoints and response times)
- Error Handling Issues (with file paths)
- Refactoring Opportunities (with code samples)
- Caching Recommendations
- Quick Wins

## Success Criteria
- All controllers and services analyzed
- Specific performance metrics provided
- Code samples for issues
- Prioritized recommendations
```

### Agent 3 Prompt: Security & Validation Auditor
```markdown
## Task
Audit entire codebase for security vulnerabilities and input validation issues.

## Steps
1. Scan for common vulnerabilities:
   - SQL injection: grep for raw SQL queries without parameterization
   - XSS: grep for `innerHTML`, `dangerouslySetInnerHTML`
   - CSRF: check for CSRF tokens in forms
   - Exposed secrets: grep for `password`, `api_key`, `secret`
2. Review authentication:
   - Check JWT implementation
   - Validate session management
   - Check for proper password hashing
3. Review authorization:
   - Check RBAC implementation
   - Validate role checks on sensitive endpoints
4. Check input validation:
   - grep for `express-validator` usage
   - Check for missing validation on POST/PUT endpoints
5. Review middleware:
   - Check helmet configuration
   - Validate CORS settings
   - Check rate limiting

## Output Format
Create /.claude/reports/security-audit.md with:
- Executive Summary (risk level: Low/Medium/High/Critical)
- Critical Vulnerabilities (P0 - fix immediately)
- High-Risk Issues (P1 - fix soon)
- Medium-Risk Issues (P2 - fix in next sprint)
- Compliance Checklist (OWASP Top 10)
- Remediation Steps (specific code changes)

## Success Criteria
- All security risks identified and categorized
- OWASP Top 10 checklist completed
- Specific remediation code provided
- Risk levels assigned
```

### Agent 4 Prompt: Database & Performance Expert
```markdown
## Task
Optimize database schema, queries, and caching strategy.

## Steps
1. Review database schema:
   - Read all model files in /src/models
   - Check for missing indexes
   - Validate foreign key relationships
   - Check for proper normalization
2. Analyze query patterns:
   - grep for `db.query`, `pool.query`
   - Identify N+1 queries
   - Check for SELECT *
   - Look for missing WHERE clauses
3. Review caching:
   - Check Redis usage in services
   - Identify cacheable endpoints
   - Validate cache invalidation logic
4. Check connection pooling:
   - Review pool configuration
   - Check for connection leaks
5. Analyze transaction usage:
   - grep for BEGIN/COMMIT/ROLLBACK
   - Check for proper error handling in transactions

## Output Format
Create /.claude/reports/database-optimization.md with:
- Executive Summary
- Schema Issues (missing indexes, normalization problems)
- Query Optimization (slow queries with alternatives)
- Caching Strategy (what to cache, TTLs)
- Connection Pool Tuning
- Transaction Improvements
- Quick Wins

## Success Criteria
- All models and queries analyzed
- Specific index recommendations
- Query rewrites provided
- Caching strategy documented
```

### Agent 5 Prompt: Code Quality & Architecture Reviewer
```markdown
## Task
Review code organization, TypeScript usage, and architectural patterns.

## Steps
1. Run linter:
   - Execute: npm run lint
   - Capture output and categorize violations
2. Check TypeScript compliance:
   - grep for `any` types (anti-pattern)
   - Check for `@ts-ignore` comments
   - Validate strict mode compliance
3. Review file organization:
   - Check module boundaries
   - Identify circular dependencies
   - Validate separation of concerns
4. Check naming conventions:
   - Validate camelCase, PascalCase usage
   - Check for consistent file naming
5. Review error handling:
   - Check for custom error classes
   - Validate error propagation
6. Check documentation:
   - grep for JSDoc comments
   - Identify undocumented functions

## Output Format
Create /.claude/reports/code-quality.md with:
- Executive Summary
- TypeScript Issues (any usage, strict mode violations)
- Linting Violations (categorized by rule)
- Architectural Issues (module boundaries, circular deps)
- Documentation Gaps
- Refactoring Opportunities
- Quick Wins

## Success Criteria
- Lint report analyzed
- All `any` usages catalogued
- Architectural issues documented
- Specific refactoring steps provided
```

## Implementation Template

When this skill is invoked, use this template:

```markdown
🚀 **Full-Stack Optimization Initiated**

I'm deploying 5 specialized agents in parallel to comprehensively analyze and improve the application:

1. 🎨 **Frontend Performance Analyzer** - UI/UX, accessibility, performance
2. ⚙️ **Backend API Optimizer** - API efficiency, error handling, queries
3. 🔒 **Security & Validation Auditor** - Vulnerabilities, input validation
4. 🗄️ **Database & Performance Expert** - Schema, queries, caching
5. 📐 **Code Quality & Architecture Reviewer** - TypeScript, patterns, organization

**Estimated Time**: 5-10 minutes for analysis phase

I'll keep you updated as each agent completes their analysis...
```

### After All Agents Complete

```markdown
✅ **All 5 agents have completed their analysis!**

## Summary of Findings

**Frontend**: [X issues found - Y critical, Z high-priority]
**Backend**: [X issues found - Y critical, Z high-priority]
**Security**: [Risk Level: Low/Medium/High/Critical]
**Database**: [X optimization opportunities]
**Code Quality**: [X violations, Y refactoring opportunities]

## Unified Improvement Plan

I've synthesized all findings into a prioritized plan:

### 🔴 P0 - Critical (Fix Immediately)
[List critical issues from all agents]

### 🟠 P1 - High Priority (Fix This Sprint)
[List high-priority issues]

### 🟡 P2 - Medium Priority (Next Sprint)
[List medium-priority issues]

### 🟢 P3 - Low Priority (Nice to Have)
[List low-priority improvements]

## Next Steps

Would you like me to:
1. **Start implementing P0 critical fixes** (recommended)
2. **Review the full reports** (/.claude/reports/) before proceeding
3. **Deploy implementation agents for specific priorities**
4. **Focus on a specific area** (frontend, backend, security, database, or code quality)

I can deploy implementation agents in parallel to fix multiple issues simultaneously.
```

## Validation Checklist

After each implementation round, verify:
- [ ] All tests pass: `npm test`
- [ ] No lint errors: `npm run lint`
- [ ] Build succeeds: `npm run build`
- [ ] Type checking passes: `npm run typecheck` (if available)
- [ ] Deployment ready: `npm run test:render-ready`
- [ ] Manual smoke test of critical paths
- [ ] No new console errors in browser
- [ ] API health check passes: `curl http://localhost:3000/api/health`

## Success Metrics

Track improvement over time:
- **Performance**: Measure API response times before/after
- **Code Quality**: Lint errors reduced, `any` types eliminated
- **Security**: Vulnerabilities patched, security score improved
- **User Experience**: Faster page loads, fewer errors
- **Maintainability**: Clearer code organization, better documentation

## Iteration & Refinement

After first optimization pass:
1. Record metrics in `/.claude/reports/METRICS_BASELINE.md`
2. Schedule monthly optimization passes
3. Track progress over time
4. Refine agent prompts based on effectiveness
5. Add new agents for emerging needs (e.g., SEO, analytics)

## Commands for Manual Invocation

```bash
# Generate all reports (run agents manually)
npm run optimize:analyze

# Implement specific priority
npm run optimize:implement P0  # Critical fixes
npm run optimize:implement P1  # High priority
npm run optimize:implement P2  # Medium priority

# Full optimization cycle
npm run optimize:full  # Analyze → Synthesize → Implement → Validate

# View reports
npm run optimize:reports
```

## Integration with Existing Skills

This skill works with:
- **deployment-validator**: Auto-runs before final deployment
- **validation**: Self-correcting loop if tests fail
- **scout**: Finds external examples for complex improvements

## Continuous Improvement

This skill improves with use:
1. Track which recommendations had highest impact
2. Refine agent prompts for better analysis
3. Add new agents for uncovered areas
4. Update prioritization logic based on results
5. Document lessons learned in `/.claude/learning/optimization-lessons.md`

---

**Note**: This skill represents a significant time investment (1-2 hours for full cycle). Use for:
- Major releases
- Post-launch optimization
- Monthly health checks
- Before important demos
- After significant feature additions

For smaller improvements, use individual agents directly.
