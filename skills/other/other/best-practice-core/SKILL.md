---
name: best-practice-core
description: "[Dev] Extracts and organizes best practices for a given topic into a minimal tree structure (max depth 3, max 5 children per node). Use during task planning when writing subtasks in Docs/{name}_Task.md - output is added under each subtask as a concise reference guide. Pure reasoning task with strict formatting rules: keywords/noun phrases only, no prose. (project)"
user_invocable: true
---

# Best Practice Core

> Extracts core best practices for a topic and formats them as a minimal, keyword-focused tree.

## Purpose

Extract essential best practices for implementation tasks and format them as ultra-concise tree structures for quick reference during development.

## When to Use

**Invocation Timing:**
- During task planning phase (before implementation)
- When writing subtasks in `Docs/{name}_Task.md` documents
- BEFORE Worker agents start implementation

**Output Location:**
- Written directly under each subtask in Task document
- Acts as quick reference for developers/agents

## Output Rules (STRICT ENFORCEMENT)

### Format Constraints

| Rule | Constraint |
|------|------------|
| Max depth | 3 levels |
| Max children per node | 5 items |
| Leaf node max length | 12 words OR 60 characters |
| Node format | Noun phrases/keywords ONLY |
| Duplicates | Merge into single item |
| Tree format | Markdown tree ONLY (no mixing) |

### Zero Tolerance Items

❌ **FORBIDDEN:**
- Intro paragraphs, conclusions, or commentary
- Full sentences in leaf nodes
- Explanatory text outside the tree
- Mixed tree formats (ASCII + Markdown)
- Depth > 3 or children > 5
- Duplicate items

✅ **REQUIRED:**
- ONLY output the tree structure
- Use noun phrases: "Error boundary setup", "State validation logic"
- Keep leaf nodes concise: max 12 words
- Merge similar concepts
- Single tree format (Markdown bullets)

## Example Output

**Topic: Implementing User Authentication**

```markdown
- User Authentication
  - Security
    - Password hashing (bcrypt/argon2)
    - JWT token management
    - HTTPS-only cookies
  - Validation
    - Input sanitization
    - Email format check
    - Rate limiting
  - Error Handling
    - Failed login attempts tracking
    - Account lockout mechanism
    - Clear error messages (no data leaks)
```

## Workflow

**When invoked with a topic:**

1. **Identify Core Areas**: Extract 2-5 main categories for the topic
2. **Extract Best Practices**: For each category, list 2-5 key practices
3. **Format as Keywords**: Convert to noun phrases (no full sentences)
4. **Verify Constraints**: Check depth ≤ 3, children ≤ 5, length ≤ 12 words
5. **Merge Duplicates**: Combine similar/overlapping items
6. **Output Tree ONLY**: No intro, no conclusion, just the tree

## Integration with Task Documents

### ⛔ CRITICAL: Task Document Format Protection

**Best Practice는 서브태스크 아래에 위치하되, Kanban 파서가 태스크로 인식하지 않는 형식을 사용해야 합니다.**

❌ **FORBIDDEN - 하이픈 리스트 사용:**
```markdown
  - [ ] Design login UI layout
    <!-- Best Practice Tree -->
    - Login UI           ← 파서가 태스크로 오인식!
      - Layout
```

✅ **REQUIRED - 4-space 들여쓰기 + 코드블록 또는 인용블록 사용:**
```markdown
## Worker1

- [ ] Implement user authentication #auth !high Deadline(2025:01:15)
  - [ ] Design login UI layout
    ```
    [Best Practice]
    · Layout: Mobile-first responsive, Focus management, Password toggle
    · Validation: Real-time feedback, Clear error states
    · Security: No password in URL, Auto-logout on idle
    ```
  - [ ] Create API integration
    ```
    [Best Practice]
    · Request: Token refresh logic, Retry with backoff
    · Error: Network failure degradation, 401/403 redirect
    · Security: Secure token storage, XSS/CSRF protection
    ```
```

### Format Rules

| Rule | Constraint |
|------|------------|
| **위치** | 서브태스크 바로 아래 (4-space 들여쓰기) |
| **형식** | 코드블록(```) 또는 인용블록(>) 사용 |
| **시작 문자** | 절대 `- ` 또는 `- [ ]`로 시작 금지 |
| **구분자** | 중점(·) 또는 화살표(→) 사용 |
| **길이** | 카테고리당 1줄, 총 3~5줄 이내 |

### Alternative Format (인용블록)

```markdown
  - [ ] Design login UI layout
    > **BP** · Layout: Mobile-first · Validation: Real-time feedback · Security: No password in URL
```

## Usage Notes

- **Concise over Complete**: Focus on critical practices, not exhaustive lists
- **Actionable Keywords**: Use phrases developers can immediately act on
- **Context-Aware**: Tailor to the specific subtask context (UI vs API vs DB)
- **No Duplication**: If practice applies to multiple subtasks, mention once in parent

## Common Topics

| Topic Type | Core Areas to Cover |
|------------|---------------------|
| UI Components | Layout, Accessibility, State, Events, Performance |
| API Integration | Request/Response, Error Handling, Caching, Security |
| Database Operations | Schema Design, Query Optimization, Transactions, Validation |
| State Management | Data Flow, Mutations, Side Effects, Persistence |
| Testing | Coverage, Edge Cases, Mocking, Performance |

---

**Remember: Output ONLY the tree. No explanations.**
