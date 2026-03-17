---
name: style-audit
description: Audits code against CI/CD style rules, quality guidelines, and best practices, then rewrites code to meet standards without breaking functionality. Use this skill after functionality validation to ensure code is not just correct but also maintainable, readable, and production-ready. The skill applies linting rules, enforces naming conventions, improves code organization, and refactors for clarity while preserving all behavioral correctness verified by functionality audits.
---

# Style Audit

This skill transforms functionally correct code into production-grade code through systematic style improvement. While functionality audits verify that code works, style audits ensure that code is maintainable, readable, secure, performant, and aligned with team standards. The skill applies CI/CD quality guidelines to identify style violations, then rewrites code to eliminate issues while preserving functionality.

## When to Use This Skill

Use the style-audit skill after functionality validation confirms code works correctly, before code reviews to catch style issues proactively, when preparing code for team collaboration or handoff, or when inheriting code that works but violates team standards. The skill is essential for maintaining codebases at scale where consistency and maintainability matter more than individual cleverness.

## The Importance of Code Style

Code style is not superficial formatting but fundamental to software maintainability, team effectiveness, and long-term project success.

**Readability and Comprehension**: Code is read far more often than it is written. Every team member who touches the code, every code reviewer who evaluates it, and every future maintainer who debugs it must understand what the code does. Clear, consistent style dramatically reduces the cognitive load of reading code. Developers spend less time deciphering intent and more time implementing improvements or fixes.

Poor style creates confusion that wastes time and introduces bugs. When variable names are cryptic, when formatting is inconsistent, when complex logic lacks decomposition, developers make mistakes because they misunderstand what the code does. Clear style prevents these comprehension failures.

**Maintainability and Evolution**: Software evolves through its lifetime with bug fixes, feature additions, and refactoring. Maintainable code makes evolution straightforward while unmaintainable code turns small changes into large projects. Style choices like proper decomposition into functions, clear separation of concerns, and consistent patterns enable evolution by making it obvious where to add new behavior without breaking existing functionality.

Technical debt accumulates when code is hard to maintain. Style audits prevent technical debt by ensuring code starts in a maintainable state rather than requiring expensive future cleanup.

**Bug Prevention Through Clarity**: Many bugs stem from confusion or misunderstanding. When code structure is clear, when edge cases are explicitly handled, when error conditions are managed properly, bugs become less likely because developers can see what the code does and identify problems visually. Style that promotes clarity also promotes correctness.

Defensive programming practices encoded in style guidelines like input validation, null checking, and explicit error handling prevent entire classes of bugs. Style audits that enforce these practices systematically reduce bug rates.

**Team Collaboration**: Consistent style across a codebase allows team members to move fluidly between different parts of the system. When every file follows the same conventions, developers do not need to mentally shift gears when working in different areas. The cognitive overhead of context switching decreases, and the team becomes more effective overall.

Style consistency also facilitates code review by establishing shared expectations. Reviewers can focus on logic and correctness rather than debating formatting choices. Teams that invest in style consistency experience faster, more effective code reviews.

## Style Audit Methodology

The style audit follows a systematic process to identify style issues and improve code quality.

### Phase 1: Automated Linting

Begin by running automated linting tools appropriate to the programming language. For Python, use pylint, flake8, and mypy for type checking. For JavaScript, use ESLint and Prettier. For other languages, use their standard linters. Automated tools catch common style violations efficiently and consistently.

Collect all linting errors and warnings with their locations, descriptions, and severity levels. Categorize issues by type such as formatting violations, naming convention violations, unused code, missing documentation, potential bugs caught by static analysis, and complexity warnings. This categorization helps prioritize remediation efforts.

Configure linters to match team standards rather than using default configurations. Custom configurations encode team preferences and project requirements, ensuring linting results align with actual quality goals rather than generic recommendations.

### Phase 2: Manual Style Review

Supplement automated linting with manual review for issues that tools cannot detect. Examine code for proper decomposition where functions are appropriately sized and single-purpose, effective naming where identifiers clearly communicate purpose, logical organization where related functionality is grouped coherently, appropriate abstraction where common patterns are extracted, and reasonable complexity where intricate logic includes explanatory comments.

Manual review catches issues that require human judgment such as whether a function is doing too much, whether abstractions make sense, or whether the code will be understandable to future maintainers. Tools flag syntactic issues while humans evaluate semantic quality.

### Phase 3: Security and Performance Review

Review code for security vulnerabilities including input validation to prevent injection attacks, proper authentication and authorization, secure handling of sensitive data, protection against common attack vectors, and safe use of cryptography. Security issues are style issues because secure coding should be the standard style.

Evaluate performance characteristics including algorithmic efficiency to avoid unnecessarily slow operations, memory usage to prevent leaks or bloat, resource cleanup to properly close files and connections, lazy loading where appropriate, and caching strategies for expensive operations. Performance problems often stem from stylistic choices about how to structure code.

### Phase 4: Documentation Review

Assess code documentation including module and file-level documentation explaining purpose, function and method documentation describing parameters and behavior, inline comments explaining non-obvious logic, README files and usage guides for public interfaces, and API documentation for libraries or services. Undocumented code is poorly styled code because it places unnecessary burden on future readers.

Documentation should explain why decisions were made, not just what the code does. The code itself shows what it does. Documentation adds value by explaining intent, rationale, and context that is not apparent from code alone.

### Phase 5: Consistency Analysis

Check for consistency across the codebase including naming convention adherence, formatting style uniformity, error handling patterns, code organization structures, and dependency management approaches. Inconsistency increases cognitive load because developers must constantly adapt to different patterns rather than relying on established conventions.

Identify instances where newer code follows better practices than older code. These inconsistencies suggest opportunities for broad refactoring that would improve overall codebase quality beyond the immediate files under audit.

## Code Rewriting Workflow

After identifying style issues, systematically rewrite code to address them while preserving functionality.

### Step 1: Prioritize Issues by Impact

Not all style issues have equal importance. Prioritize fixes based on impact to functionality where security vulnerabilities demand immediate fixing, readability where confusing code causes comprehension failures, maintainability where poor structure impedes evolution, and performance where inefficiencies cause user-facing problems. Address high-impact issues before lower-impact cosmetic changes.

For large codebases with many issues, fixing everything at once may be impractical. Prioritization ensures effort focuses where it provides the most value. Create a phased plan if comprehensive rewriting would disrupt ongoing development work.

### Step 2: Validate Functionality Before Changes

Before rewriting any code, ensure comprehensive test coverage exists for that code. If functionality-audit has already run, use those test cases. If not, create basic tests that validate current behavior. These tests serve as regression checks ensuring rewriting does not break functionality.

Functionality must be preserved during style improvements. Tests provide the safety net that makes aggressive style improvements feasible. Without tests, developers become conservative about changes, leaving style issues unfixed because the risk of breaking things seems too high.

### Step 3: Apply Automated Fixes

Start with fixes that can be applied automatically by formatting tools like Black for Python or Prettier for JavaScript, import organization tools, and linting autofix features. Automated fixes are fast, reliable, and require minimal review because they follow established patterns consistently.

Run automated tools across the entire codebase at once to fix widespread formatting inconsistencies. This eliminates noise in future code reviews where reviewers would otherwise be distracted by formatting issues rather than focusing on logic.

### Step 4: Refactor for Clarity

Apply manual refactoring to improve code clarity through extracting complex logic into well-named functions, decomposing large functions into smaller single-purpose ones, introducing explanatory variables for complex expressions, reorganizing code to follow logical flow, and simplifying control flow to eliminate unnecessary nesting. Each refactoring should have a clear purpose and make the code measurably more understandable.

Refactoring for clarity is the most valuable manual improvement because it directly addresses comprehension barriers. Focus on code that you found confusing during review. If you struggled to understand it, future maintainers will too.

### Step 5: Improve Error Handling

Strengthen error handling by adding input validation at function boundaries, replacing generic exceptions with specific types, including meaningful error messages that aid debugging, implementing proper resource cleanup using context managers or finally blocks, and adding logging for error conditions. Robust error handling is a style issue because it should be standard practice, not an optional enhancement.

Many codebases handle only happy paths while neglecting error conditions. Style audits systematically identify missing error handling and add appropriate checks and recovery logic.

### Step 6: Enhance Documentation

Add or improve documentation at all levels including module docstrings explaining purpose and usage, function docstrings with parameter descriptions and return value specifications, inline comments for complex logic or non-obvious decisions, type hints to document expected types, and README updates to reflect current state. Documentation improvements pay dividends in reduced confusion and faster onboarding.

Write documentation for someone who has never seen the code before. Avoid inside jokes or assumptions about prior knowledge. Clear documentation serves the future team, which may include people not currently involved in the project.

### Step 7: Verify Functionality After Changes

After each significant rewriting step, run the test suite to verify functionality is preserved. If tests fail, investigate immediately to determine if the rewriting broke something or if the test was incorrectly specified. Fix issues immediately before proceeding to further changes. Incremental verification catches problems early when the cause is obvious rather than after multiple changes make root cause unclear.

Regression testing after style improvements is crucial because even "safe" refactoring can introduce subtle bugs. The verification step ensures style improvements genuinely improve code without sacrificing correctness.

### Step 8: Commit Changes Atomically

Commit style improvements in small, focused commits that each address one type of issue. For example, separate commits for automated formatting, renaming for clarity, error handling improvements, and documentation additions. Atomic commits make code review easier and allow reversion of specific changes if needed without losing all improvements.

Write clear commit messages explaining what was improved and why. Good commit messages help future developers understand the evolution of the codebase and the reasoning behind style improvements.

## Style Guidelines from Best Practices

Apply these evidence-based style guidelines during code rewriting.

### Function and Method Design

Functions should be small and focused on a single responsibility. A good heuristic is that functions should be understandable at a glance without scrolling. If a function exceeds about 50 lines, consider whether it is doing too much and should be decomposed. Single-responsibility functions are easier to test, reuse, and reason about.

Name functions clearly using verbs that describe what they do. Avoid generic names like "process" or "handle" in favor of specific names like "validateUserInput" or "calculateTaxAmount". Clear names reduce the need for comments because the function name itself documents its purpose.

Limit function parameters to a reasonable number. Functions with more than about four parameters become difficult to call correctly and often indicate poor abstraction. Consider grouping related parameters into objects or configuration structures.

### Variable Naming and Scope

Use descriptive variable names that communicate purpose and type. Avoid single-letter names except for loop counters in small scopes. For example, "userEmail" is clearer than "e" and "totalAmount" is clearer than "t". Clarity in naming prevents bugs that stem from confusion about what variables represent.

Keep variable scope as narrow as possible. Declare variables close to where they are used rather than at the start of functions. Narrow scope reduces cognitive load because readers do not need to track variables across large code sections.

Use constants for magic numbers and strings. Replace literal values like "42" or "pending" with named constants that explain what they represent. This makes code self-documenting and facilitates changes since constant values are defined in one place.

### Code Organization and Structure

Organize code logically with related functionality grouped together. Public interfaces should appear before private implementation details. Higher-level abstractions should appear before lower-level details. This top-down organization matches how developers read code when trying to understand it.

Separate concerns into distinct modules or classes. Business logic should be separate from UI code, which should be separate from data access code. Clear separation of concerns makes code modular and testable because each component has clear responsibilities and minimal coupling to others.

Avoid deep nesting of control structures. Code with many levels of indentation is hard to read and often indicates complex logic that should be decomposed. Use early returns and guard clauses to flatten control flow.

### Error Handling and Logging

Handle errors explicitly rather than allowing them to propagate silently. Catch specific exception types rather than generic exceptions. Include meaningful error messages that help diagnose problems. Log errors with sufficient context to support debugging but without exposing sensitive information.

Validate inputs at boundaries where external data enters the system. Do not trust user input, API responses, or file contents. Explicit validation prevents entire classes of bugs and security vulnerabilities.

Clean up resources properly using context managers in Python, try-finally blocks in JavaScript, or equivalent constructs in other languages. Resource leaks from forgotten cleanup cause production issues that are difficult to diagnose.

### Performance and Efficiency

Avoid premature optimization but also avoid obvious inefficiencies. Do not perform expensive operations in loops if they can be hoisted out. Do not allocate large data structures unnecessarily. Use appropriate data structures for the problem at hand.

Profile code to identify actual performance bottlenecks rather than optimizing based on intuition. Measure before optimizing and measure after to verify improvements. Performance work without measurement often wastes time on parts of code that do not meaningfully affect overall speed.

Consider algorithmic complexity when choosing approaches. An O(n²) algorithm might work fine for small datasets but becomes problematic at scale. Choose algorithms appropriate to expected data sizes.

## Integration with CI/CD Pipeline

Style audits integrate with continuous integration and deployment pipelines to enforce quality standards automatically.

### Pre-commit Hooks

Configure pre-commit hooks that run linting and formatting tools before code is committed. This prevents style violations from entering version control and provides immediate feedback to developers. Pre-commit hooks are the first line of defense in maintaining code quality.

Pre-commit checks should be fast enough to not significantly slow down the development workflow. Focus on quick automated checks rather than comprehensive analysis that belongs in CI pipeline.

### Continuous Integration Checks

Configure CI systems to run comprehensive style audits on every pull request including all linting tools with strict settings, type checking if applicable, complexity analysis, and security scanning. CI checks provide systematic quality gates that code must pass before merging.

Fail CI builds for high-severity style violations including security vulnerabilities, broken functionality indicated by failed tests, and critical linting errors. Make lower-severity issues warnings that create visibility without blocking merges.

### Automated Code Review

Integrate automated code review tools that comment on pull requests with style suggestions, security concerns, or best practice violations. Automated review supplements human review by catching mechanical issues so humans can focus on logic and design.

Configure automated review to align with team standards and avoid noisy or pedantic feedback. Tools should provide value without overwhelming developers with minor complaints.

### Quality Metrics Tracking

Track code quality metrics over time including linting error counts, test coverage percentages, code complexity scores, and technical debt estimates. Visualize trends to show whether quality is improving or degrading. Metrics create visibility into code health and motivate continued investment in quality.

Set team goals for quality metrics and celebrate improvements. Metrics work best when they inform positive cultural change rather than becoming punitive measures used to judge individual developers.

## Output Report Structure

The style audit produces a comprehensive report documenting current quality and improvements made.

### Executive Summary

Begin with a high-level summary stating how many style issues were found by category, what percentage were fixed automatically versus manually, overall code quality assessment, and critical issues requiring attention. The summary gives stakeholders quick insight without detailed technical content.

### Detailed Findings

Document each identified style issue including location in the codebase, specific violation description, severity level, recommendation for fixing, and whether it was automatically or manually fixed. Detailed findings support review of changes and provide learning opportunities for the team.

Group findings by category such as formatting, naming, complexity, error handling, and documentation. Categorical organization reveals patterns in code quality issues.

### Refactoring Summary

For each significant refactoring performed, document what was changed and why, how functionality was preserved, what tests verify the refactoring, and what improvements resulted. Refactoring documentation helps reviewers understand changes and provides examples of good practices for the team.

### Remaining Issues

List issues that were identified but not fixed including explanation of why fixing was deferred, estimated effort to fix, and prioritization relative to other work. Not all issues can be fixed immediately but they should be tracked rather than forgotten.

### Quality Metrics

Include quantitative metrics showing code quality before and after the style audit including lines of code, complexity scores, linting error counts, test coverage percentages, and documentation coverage. Metrics provide objective evidence of improvement.

## Integration with Claude Code Workflow

The style-audit skill integrates with Claude Code as the final step in a comprehensive quality pipeline.

### Invocation Context

Claude Code invokes style-audit after functionality validation confirms code works by providing paths to code files to audit, team style guidelines or linting configurations, information about the target environment or framework, and whether to apply automated fixes or just report issues.

### Execution and Reporting

The skill runs linting tools, performs manual style review, identifies security and performance issues, and produces a comprehensive report. For issues that can be safely fixed automatically, the skill applies fixes and reruns tests to verify functionality is preserved.

The skill may ask about team preferences when multiple valid style choices exist. It escalates decisions rather than imposing arbitrary standards that may not match team culture.

### Integration with Other Audit Skills

Style audit is the final step after theater-detection-audit ensures all mock code is completed and functionality-audit verifies everything works. Together, these three audits transform raw code into production-ready software that is genuine, functional, and maintainable. The skills form a complete quality pipeline where each addresses a distinct dimension of code quality.

## Working with the Style Audit Skill

To use this skill effectively, provide code to audit, team style guidelines or linting configurations, information about target production environment, and priorities for which issues are most important. The more context about team standards and project requirements, the more targeted and valuable the style improvements.

The skill will systematically audit code, identify style issues, rewrite code to address problems, and verify functionality is preserved. It produces code that is not just correct but exemplifies professional software engineering standards. When combined with theater-detection-audit and functionality-audit, it ensures code meets the highest standards of quality before deployment.

