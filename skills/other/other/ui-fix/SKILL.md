---
name: ui-fix
description: Generate implementation instructions or code patches for UI issues identified by ui-review
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, mcp__memory__*
context: full
agent: general-purpose
model: claude-sonnet-4-20250514
---

# ui-fix

Generate implementation instructions or code patches for UI issues. Works with output from `/ui-review` to create actionable fixes.

## When To Use

- After running `/ui-review` with issues identified
- When you know what UI fix is needed but not how to implement it
- To generate instructions for developers
- User mentions: "fix the UI", "implement the changes", "generate patches"

## Workflow

### 1. Gather Issue Context

Either:
- Read the UI review report (if `/ui-review` was run first)
- Ask user to describe the specific issue

Required information:
- **What's wrong:** The specific issue (e.g., "contrast ratio too low")
- **Where:** Component/file location
- **Design system:** Which system applies (Trustee/Saville)

### 2. Determine Fix Type

| Issue Type | Fix Approach |
|------------|--------------|
| **Colour/token** | Update CSS custom property or Tailwind class |
| **Spacing/sizing** | Update padding/margin/size values |
| **Typography** | Update font-family, weight, or size |
| **Structure** | Modify HTML/JSX structure |
| **Accessibility** | Add ARIA labels, semantic elements |
| **Animation** | Update transition/animation duration |

### 3. Generate Instructions

For **non-coders** (instruction mode):

```markdown
## Fix: [Issue Title]

### What Needs to Change
[Plain language explanation of the change]

### Step-by-Step Instructions

1. **Find the file**: [Path to file]
2. **Look for**: [What to search for - be specific]
3. **Change it to**: [What it should become]
4. **Why**: [Brief explanation of why this fixes the issue]

### Verification
After making this change:
- [ ] [Check 1]
- [ ] [Check 2]

### If You're Stuck
Tell Claude: "In [file], change [old] to [new] for [issue]"
```

For **developers** (code mode):

```markdown
## Fix: [Issue Title]

### Files to Modify
- `src/components/[Component].tsx`

### Code Changes

\`\`\`diff
- className="bg-[#0F0F0F]"
+ className="bg-[#121210]"
\`\`\`

### Related Files (May Need Updates)
- `tailwind.config.js` (if adding new tokens)
- `src/styles/globals.css` (if using CSS variables)

### Tests
- [ ] Visual regression test
- [ ] Accessibility audit passes
```

### 4. Design System Reference Cards

Quick reference for common fixes:

#### Trustee Edition Fixes

| Issue | Fix |
|-------|-----|
| Wrong primary colour | Change to `#1A4F7A` |
| Background too dark | Change to `#FFFFFF` (Paper White) |
| Wrong font | Use `font-family: 'Inter', -apple-system, sans-serif` |
| Status badge wrong | Use compliance palette (see TRUSTEE.md) |
| Touch target too small | Add `min-h-[44px] min-w-[44px]` |
| Missing focus ring | Add `focus:ring-[3px] focus:ring-[#1A4F7A] focus:ring-offset-2` |
| Missing print styles | Add `@media print { ... }` block |

#### Saville v5.0 Fixes

| Issue | Fix |
|-------|-----|
| Wrong warm carbon | Change `#0F0F0F` to `#121210` |
| Code bar too short | Change to `height: 6px` |
| Wrong code bar order | Green→Teal→Blue→Purple→Coral→Orange |
| Orange on small text | Only use `#F57C00` at 19pt+ |
| Animation too long | Cap at `300ms` |
| Border radius too big | Cap at `12px` (Saville) or `8px` (Trustee) |
| Missing matte (Core) | Add matte texture at 15% dark / 8% light |
| Has matte (Clarity) | Remove matte texture for data-dense views |

### 5. Batch Fix Generation

For multiple issues from a review report:

```markdown
# UI Fix Batch: [Product Name]
Generated: [Date]

## Fixes by Priority

### Critical (Must Fix Now)

#### Fix 1: [Title]
[Instructions or code]

#### Fix 2: [Title]
[Instructions or code]

### Warnings (Fix Soon)

#### Fix 3: [Title]
[Instructions or code]

---

## Implementation Order
1. [Fix 1] - Foundation change
2. [Fix 3] - Depends on Fix 1
3. [Fix 2] - Independent

## Estimated Effort
- Non-coder with instructions: ~[X] hours
- Developer with patches: ~[Y] hours
```

### 6. AI Transparency Fixes (Common)

For EU AI Act compliance issues:

```typescript
// Add AI-Generated badge to AI outputs
<div className="relative">
  <AIOutput content={response} />
  <span className="absolute top-2 right-2 text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">
    AI-Generated
  </span>
</div>

// Add verification footer
<footer className="text-xs text-gray-500 mt-4 border-t pt-2">
  Generated with Claude | Always verify AI suggestions
</footer>

// Add human approval step
const handleAISuggestion = (suggestion: string) => {
  setShowApprovalDialog(true);
  setPendingSuggestion(suggestion);
  // Never auto-apply
};
```

### 7. WCAG Quick Fixes

Common accessibility fixes:

```typescript
// Missing alt text
<img src={src} alt="" />  // ❌
<img src={src} alt="Compliance status chart for Q4 2025" />  // ✅

// Missing form labels
<input type="text" placeholder="Name" />  // ❌
<label>
  <span className="sr-only">Name</span>
  <input type="text" placeholder="Name" />
</label>  // ✅

// Missing focus visible
className="..."  // ❌
className="... focus-visible:ring-2 focus-visible:ring-offset-2"  // ✅

// Insufficient contrast
<p className="text-gray-400">...</p>  // ❌ (may fail 4.5:1)
<p className="text-gray-600">...</p>  // ✅ (usually passes)

// Touch target too small
<button className="p-1">...</button>  // ❌
<button className="p-3 min-h-[44px] min-w-[44px]">...</button>  // ✅
```

## Output Modes

Based on user preference:

| Mode | Trigger | Output |
|------|---------|--------|
| **Instructions** | Default, or "explain how to fix" | Plain language steps |
| **Code** | "generate code", "show me the patch" | Diff-style patches |
| **Both** | "full fix" | Instructions + Code |

## Integration

```
/ui-review → Identifies issues
/ui-fix    → Generates fixes (THIS SKILL)
```

## Model Preference

**sonnet** - Fix generation is procedural, not reasoning-heavy

---
*Part of 45Black UI Expert Devstack*
*For non-coders: This skill tells you exactly how to fix UI problems*
