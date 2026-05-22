---
name: dcode:improve-copy
description: Improve UI copy using proven frameworks (JTBD, benefit-first, error patterns). Use when a designer wants to improve button text, error messages, empty states, or audit copy in a component. Supports interactive walkthrough mode for reviewing changes one-by-one, or batch mode for quick fixes.
---

# Improve Copy

Improve UI microcopy using proven UX writing frameworks.

**For designers who think:** "This button says 'Submit'... there has to be something better."

## Frameworks Reference

### JTBD (Jobs to Be Done)
Focus on the outcome the user is hiring the product to achieve.
- "Submit" → "Get my results"
- "Sign up" → "Start saving time"
- Formula: What does the user *get*, not what they *do*

### Benefit-First
Lead with value, then the action.
- "Enable notifications" → "Never miss updates — enable notifications"
- "Enter email" → "Get weekly tips — enter your email"
- Formula: "[Benefit] — [action]"

### Action-First
Start with the verb, be direct.
- "User settings page" → "Manage your account"
- "Password reset functionality" → "Reset your password"
- Formula: "[Verb] [object]"

### Error Messages
Structure: [What happened] [Why] [What to do]
- "Error" → "Couldn't save. Connection lost. Try again."
- "Invalid input" → "Email format looks wrong. Try name@example.com"

### Empty States
Structure: "No [items] yet. [Action] to [benefit]."
- "No results" → "No projects yet. Create one to get started."
- Variants: encouraging, minimal, benefit-focused

### Confirmation Dialogs
Structure: "[Consequence]. [Question]?"
- "Are you sure?" → "This will delete all your data. Continue?"
- Be specific about what happens

### Loading States
Tell users what's happening, or build anticipation.
- "Loading..." → "Finding your files..."
- "Please wait" → "Preparing your dashboard..."
- Formula: "[Action in progress]..." or "[Benefit coming]..."

### Voice Dimensions
Calibrate tone on these spectrums:

| Dimension | Range |
|-----------|-------|
| Formal ↔ Casual | "Please submit your request" ↔ "Send it over" |
| Serious ↔ Playful | "Error occurred" ↔ "Oops, something broke" |
| Respectful ↔ Irreverent | "We appreciate your patience" ↔ "Hang tight" |
| Matter-of-fact ↔ Enthusiastic | "File uploaded" ↔ "Your file is ready to go!" |

Match your product's personality. Banking apps stay serious; creative tools can be playful.

### Contextual Tone Shifting
Same voice, different tone based on situation:

| Context | Tone | Example |
|---------|------|---------|
| Onboarding | Warm, encouraging | "Welcome! Let's get you set up." |
| Success | Celebratory but brief | "Done! Your changes are live." |
| Error | Calm, helpful | "Couldn't save. Check your connection." |
| Destructive action | Serious, clear | "This will permanently delete your data." |
| Empty state | Encouraging | "Nothing here yet—let's fix that." |

### The 4 C's
Quality checklist for any copy:

| Principle | Question to ask |
|-----------|-----------------|
| **Clear** | Would a new user understand this? |
| **Concise** | Can I say this in fewer words? |
| **Conversational** | Does this sound like a helpful human? |
| **Consistent** | Am I using the same terms everywhere? |

## Modes

### Single Suggestion Mode
User provides copy, get suggestions:
```
Input: "Submit"
Output: Table of options across frameworks
```

### Audit Mode
Scan a file or current context for copy to improve:
```
/dcode:copy -audit [file]
```

### Interactive Walkthrough
Step through each item with choices. Default for < 10 items.

### Batch Mode
Show all suggestions in a table. Use `--batch` flag or type `a` during walkthrough.

## Instructions

### 1. Determine Mode

Check the input:
- If text in quotes → Single suggestion mode
- If `-audit` flag → Audit mode
- If `-list` → Show frameworks reference
- If no input and context available → Offer to audit current file

### 2. For Single Suggestions

Present improvements across relevant frameworks:

```
"Submit" improvements:

| Framework | Suggestion | Why |
|-----------|------------|-----|
| jtbd | Get my results | Focuses on outcome |
| action-first | Send request | Clear action |
| contextual | Save changes | Matches actual behavior |

Recommendation: [best option based on context]
```

If context is unclear, ask: "What does this button do?"

### 3. For Audit Mode

#### 3a. Context Detection
If no file specified:
- Check if user has been working on a file in this session
- Ask: "I see you're working on [file]. Audit that? (y/n/other)"
- If no context: "What should I audit? (paste path or describe screen)"

#### 3b. Scan for Copy
Find UI copy in the file:
- Button/link text
- Labels and headings
- Error messages
- Empty states
- Placeholder text
- Tooltips
- Confirmation dialogs

Categorize each item by type (button, error, empty, label, etc.)

#### 3c. Choose Walkthrough or Batch
- If ≤ 10 items and no `--batch` flag → Interactive walkthrough
- If > 10 items or `--batch` flag → Batch mode
- User can switch modes anytime

### 4. Interactive Walkthrough

For each copy item:

```
────────────────────────────────────────
[1/4] Line 23: Button
────────────────────────────────────────

Current:  "Submit"
Context:  Form submission button

Suggestions:
  1. "Get started" (jtbd)
  2. "Save changes" (action-first)
  3. "Continue" (minimal)
  4. Keep as-is
  5. Custom...

Choice (1-5, s=skip, a=all, r=apply-to-similar, q=quit):
```

#### Shortcut Keys
| Key | Action |
|-----|--------|
| `1-5` | Pick suggestion |
| `s` | Skip this item |
| `a` | Show all remaining as table (exit walkthrough) |
| `r` | Apply this choice to all remaining items of same type |
| `q` | Quit audit |
| `e` | Enter custom text |
| `?` | Show help |
| `↵` | Accept first suggestion |

#### Apply-to-Similar Pattern
When user picks a suggestion and types `r`:
```
Apply "jtbd" style to all remaining buttons? (y/n)
> y

✓ Applied to 3 buttons:
  - Line 45: "Submit" → "Complete purchase"
  - Line 67: "Send" → "Send message"
  - Line 89: "OK" → "Got it"

Moving to error messages...
```

### 5. Batch Mode

Show all items in a table:

```
Copy audit for CheckoutForm.tsx:

| Line | Type | Current | Suggestion |
|------|------|---------|------------|
| 23 | button | "Submit" | "Complete purchase" |
| 31 | error | "Invalid" | "Card number looks wrong" |
| 45 | empty | "No items" | "Your cart is empty" |
| 52 | button | "Cancel" | Keep as-is |

Apply all? (y/n/review-each)
```

### 6. Summary & Apply

After walkthrough or batch review:

```
────────────────────────────────────────
Audit complete
────────────────────────────────────────

Changes:
  ✓ Line 23: "Submit" → "Complete purchase"
  ✓ Line 31: "Invalid" → "Card number looks wrong"
  · Line 45: skipped
  ✓ Line 52: "Cancel" → kept as-is

Apply to file? (y/n/preview)
```

If `preview`:
- Show diff of changes
- Confirm before applying

If `y`:
- Apply changes to file
- Report success

### 7. Power User Flags

| Flag | Behavior |
|------|----------|
| `--batch` | Skip walkthrough, show table |
| `--dry-run` | Preview only, no prompts to apply |
| `--apply` | Auto-apply first suggestion (use with caution) |
| `--framework X` | Only suggest using framework X |

## Examples

**Improve a single piece of copy:**
```
/dcode:copy "Click here to learn more"
```

**List available frameworks:**
```
/dcode:copy -list
```

**Audit current file interactively:**
```
/dcode:copy -audit
```

**Audit specific file in batch mode:**
```
/dcode:copy -audit src/components/LoginForm.tsx --batch
```

**Get JTBD suggestions only:**
```
/dcode:copy "Submit" --framework jtbd
```
