---
name: frontend-verification
description: Verify and test Angular 18 frontend changes using Chrome DevTools MCP.
  Automatically check console errors, network requests, and visual rendering after
  implementing tasks or when fixing UI bugs. Use w
---

---
name: Frontend Verification & Testing
description: Verify and test Angular 18 frontend changes using Chrome DevTools MCP. Automatically check console errors, network requests, and visual rendering after implementing tasks or when fixing UI bugs. Use when creating components, debugging visual issues, validating API integration, or ensuring UI requirements are met. File types: .ts, .html, .css, .scss
allowed-tools: Read, Bash, mcp__chrome-devtools__*
---

# Frontend Verification & Testing

Verify Angular 18 frontend using Chrome DevTools MCP - check console, network, and visual rendering.

## Project Context

**Photo Map MVP** - Angular 18 SPA with geolocation photo management.

**Stack:**
- Angular 18.2.0+ (standalone components)
- Dev Server: http://localhost:4200
- Backend API: http://localhost:8080 (Spring Boot 3)
- Build: Angular CLI + esbuild

**Constraints:**
- Both frontend and backend must be running
- JWT authentication for protected routes
- All API calls include `Authorization: Bearer <token>`

---

## When to Use This Skill

**Automatic Triggers:**

1. **After implementing task logic** - po ukończeniu implementacji feature
   - Example: Po dodaniu Gallery Component → verify photos load
   - Example: Po implementacji Login → check form + API call

2. **When uncertain about code behavior** - gdy wątpliwości czy działa
   - Example: Complex RxJS pipeline → verify console
   - Example: Leaflet map init → check visual rendering

3. **When fixing UI bugs (iterative)** - przy naprawie błędów (sprawdź → napraw → sprawdź)
   - Example: Layout issue → screenshot → fix CSS → verify
   - Example: API 401 → check network → fix auth → verify

4. **On explicit request** - na żądanie użytkownika
   - Example: "zweryfikuj frontend", "sprawdź czy login działa"

**DO NOT use for:**
- ❌ Simple code reading (use Read tool)
- ❌ Unit test execution (use Bash with `ng test`)
- ❌ Backend-only changes (use spring-boot-backend skill)

---

## Server Management

**Check if servers running:**
```bash
# Check PID files
[ -f scripts/.pid/backend.pid ] && kill -0 $(cat scripts/.pid/backend.pid)
[ -f scripts/.pid/frontend.pid ] && kill -0 $(cat scripts/.pid/frontend.pid)

# Health checks
curl http://localhost:8080/actuator/health  # Backend
curl -I http://localhost:4200               # Frontend
```

**Start servers:**
```bash
./scripts/start-dev.sh          # Backend + Frontend
./scripts/start-dev.sh --with-db # Include PostgreSQL
```

**When to restart:**
- ✅ Code changes (Java/TypeScript modified)
- ✅ Servers not responding (PID dead, ports free)
- ✅ Health checks failing

**Rebuild & Restart:**
```bash
./scripts/stop-dev.sh
cd backend && ./mvnw clean package  # If backend changes
cd frontend && npm run build         # If frontend changes
./scripts/start-dev.sh
```

→ Full docs: `references/server-management.md`

---

## Verification Workflow

### 5-Step Process

```
Step 0: Verify Servers Running
   ↓
Step 1: Navigate & Capture State
   ↓
Step 2: Check Console Errors
   ↓
Step 3: Check Network Requests
   ↓
Step 4: Visual Verification
   ↓
Step 5: Report Results
```

### Detailed Steps

**Step 0: Verify Servers Running**
```bash
# Check if servers running (PID + health)
[ -f scripts/.pid/backend.pid ] && kill -0 $(cat scripts/.pid/backend.pid)
[ -f scripts/.pid/frontend.pid ] && kill -0 $(cat scripts/.pid/frontend.pid)

# If NOT running OR code changes → restart
./scripts/stop-dev.sh
./scripts/start-dev.sh
```

**Step 1: Navigate & Capture State**
- `list_pages()` → check open pages
- `navigate_page(url: "http://localhost:4200/path")` → go to route
- `take_snapshot()` → accessibility tree (structural check)
- `take_screenshot()` → visual representation

**Step 2: Check Console Errors**
- `list_console_messages(types: ["error", "warn"])` → filter errors
- `get_console_message(msgid: N)` → detailed stack trace

**Step 3: Check Network Requests**
- `list_network_requests(resourceTypes: ["xhr", "fetch"])` → API calls
- `get_network_request(reqid: N)` → headers, payload, response

**Step 4: Visual Verification**
- `take_screenshot(fullPage: true)` → full page visual
- `resize_page(width, height)` → test responsive (375, 768, 1920)
- `hover(uid)`, `click(uid)` → test interactions

**Step 5: Report Results**
- ✅ **PASS:** "All verifications passed. No console errors, API calls 200 OK, UI renders correctly."
- ❌ **FAIL:** "Issues found: Console error at component.ts:42, Network POST /api/login → 401, Visual: missing padding"

---

## Key MCP Tools

**Navigation:**
- `list_pages()` - list open tabs
- `navigate_page(url, timeout)` - go to URL
- `wait_for(text, timeout)` - wait for text to appear

**State Capture:**
- `take_snapshot(verbose)` - accessibility tree (fast, text)
- `take_screenshot(uid, fullPage, format)` - visual capture (PNG/JPEG/WebP)
- `evaluate_script(function, args)` - execute JS in page

**Console & Network:**
- `list_console_messages(types, pageIdx, pageSize)` - get console logs
- `get_console_message(msgid)` - detailed error info
- `list_network_requests(resourceTypes, pageIdx)` - list HTTP requests
- `get_network_request(reqid)` - detailed request/response

**Interaction:**
- `click(uid, dblClick)` - click element by UID
- `fill(uid, value)` - fill input/textarea
- `fill_form(elements)` - fill multiple fields
- `hover(uid)` - hover over element

**Emulation:**
- `resize_page(width, height)` - change viewport (mobile: 375x667, tablet: 768x1024, desktop: 1920x1080)
- `emulate_network(throttlingOption)` - simulate network (Offline, Slow 3G, Fast 3G, etc.)
- `performance_start_trace(reload, autoStop)` - measure Core Web Vitals

→ Full docs: `references/mcp-tools-reference.md`

---

## Quick Start

### Example 1: Verify Console After Component Implementation
```typescript
navigate_page(url: "http://localhost:4200/gallery")
list_console_messages(types: ["error", "warn"])
// ✅ No errors → Component works
// ❌ Errors found → get_console_message(msgid) → Fix
```

### Example 2: Verify Network After API Integration
```typescript
navigate_page(url: "http://localhost:4200/login")
fill_form([{ uid: "input-email", value: "test@example.com" }, { uid: "input-password", value: "test123456" }])
click(uid: "btn-login")
wait_for(text: "Photo Gallery", timeout: 5000)
list_network_requests(resourceTypes: ["fetch"])
get_network_request(reqid: 1)
// → POST /api/auth/login → 200 OK → JWT token ✅
```

### Example 3: Verify Visual Layout
```typescript
navigate_page(url: "http://localhost:4200/gallery")
take_screenshot(fullPage: true)
resize_page(width: 375, height: 667)  // Mobile
take_screenshot()
// → Check: Single column layout on mobile ✅
```

→ Detailed scenarios: `examples/*.md`
→ Detailed patterns: `references/verification-patterns.md`

---

## Best Practices

1. **Always check console first** - even if UI looks correct
   ```typescript
   list_console_messages(types: ["error", "warn"])
   ```

2. **Check network for API calls** - verify status codes, headers, payloads
   ```typescript
   list_network_requests(resourceTypes: ["xhr", "fetch"])
   ```

3. **Test responsive layouts** - mobile (375), tablet (768), desktop (1920)
   ```typescript
   resize_page(width: 375, height: 667)
   ```

4. **Use snapshots for structure, screenshots for visual**
   - Snapshot (fast, text) → "Are elements present?"
   - Screenshot (slow, image) → "Does it look right?"

5. **Iterative verification for bug fixes**
   - Verify bug → Fix code → Re-verify → Repeat until ✅

6. **Report actionable issues**
   - ❌ BAD: "Login doesn't work"
   - ✅ GOOD: "Login failed: POST /api/auth/login → 401. Request missing Authorization header. Check AuthInterceptor."

7. **Restart servers when code changes**
   ```bash
   ./scripts/stop-dev.sh && ./scripts/start-dev.sh
   ```

---

## Related Skills

- **angular-frontend** - for implementing Angular components
- **spring-boot-backend** - for backend API development
- **code-review** - for code quality checks

---

## Key Reminders

**Proactive Verification:**
- ✅ Use after implementing tasks
- ✅ Verify BEFORE marking complete
- ✅ Catch issues early

**Comprehensive Checks:**
- ✅ Console errors (ALWAYS)
- ✅ Network requests (for API features)
- ✅ Visual rendering (for UI features)
- ✅ Responsive layout (mobile, tablet, desktop)

**Server Management:**
- ✅ Check servers before starting (PID/health)
- ✅ Restart when code changes
- ✅ Use project scripts (`./scripts/start-dev.sh`)
