# 👁️ Preview Mode Skill

---
name: preview-mode
description: Preview changes before deploying, visual diff comparison, and safe testing environments
---

## 🎯 Purpose

Enable safe preview of changes before committing or deploying, reducing risk of breaking production.

## 📋 When to Use

- Before deploying to production
- Testing UI changes
- Reviewing code changes
- Demonstrating features to stakeholders

## 🔧 Preview Methods

### 1. Local Development Server
```bash
# Vite
npm run dev

# Next.js
npm run dev

# Create React App
npm start

# Static files
npx serve .
```

### 2. Browser Preview
```javascript
// Use browser_subagent to:
// 1. Navigate to localhost
// 2. Take screenshots
// 3. Record interactions
```

### 3. Build Preview
```bash
# Build and preview production bundle
npm run build
npm run preview  # Vite
npx serve out    # Next.js static
```

## 📸 Screenshot Comparison

### Before/After Workflow
```
1. Take BEFORE screenshot
2. Make changes
3. Take AFTER screenshot
4. Compare side-by-side
5. Document differences
```

### Visual Diff Tools
```bash
# Using browser automation
browser_subagent → capture screenshot
compare_images → detect differences
```

## 🎬 Recording Previews

### Browser Recording
```javascript
// Recording name convention
recording_name: "{feature}_preview"

// Example
"login_flow_preview"
"dashboard_changes_preview"
"mobile_responsive_preview"
```

## 🌐 Preview Environments

| Environment | Purpose | Access |
|-------------|---------|--------|
| **localhost** | Development | Developer only |
| **staging** | Pre-production | Team |
| **preview-branch** | Feature preview | Reviewer |
| **production** | Live | Public |

## 📝 Preview Checklist

### Before Preview
- [ ] All tests passing
- [ ] No console errors
- [ ] Build completes successfully
- [ ] Dependencies up to date

### During Preview
- [ ] Check all pages/routes
- [ ] Test responsive layouts
- [ ] Verify interactive elements
- [ ] Check dark mode (if applicable)
- [ ] Test error states

### After Preview
- [ ] Document issues found
- [ ] Take screenshots for record
- [ ] Get stakeholder approval
- [ ] Proceed to next stage

## 🔄 Preview Workflow

```
Code Changes
     │
     ▼
┌─────────────┐
│ Local Test  │ ─── npm run dev
└─────────────┘
     │
     ▼
┌─────────────┐
│ Build       │ ─── npm run build
└─────────────┘
     │
     ▼
┌─────────────┐
│ Preview     │ ─── npm run preview
└─────────────┘
     │
     ▼
┌─────────────┐
│ Screenshot  │ ─── browser_subagent
└─────────────┘
     │
     ▼
   Deploy ✅
```

## 🔗 Related Skills

- `browser-automation` - Automated previews
- `testing` - Run tests before preview
- `deployment` - Deploy after preview approval
