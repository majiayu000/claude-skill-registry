/*============================================================================*/
/* WCAG-ACCESSIBILITY SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: wcag-accessibility
version: 1.0.0
description: |
  [assert|neutral] WCAG 2.1 AA/AAA accessibility compliance specialist for ARIA attributes, keyboard navigation, screen reader testing, color contrast validation, semantic HTML, and automated a11y testing with axe-core/ [ground:given] [conf:0.95] [state:confirmed]
category: Compliance
tags:
- general
author: system
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute wcag-accessibility workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic Compliance processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "wcag-accessibility",
  category: "Compliance",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Evidential",
  source: "Turkish",
  force: "How do you know?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["wcag-accessibility", "Compliance", "workflow"],
  context: "user needs wcag-accessibility capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# WCAG Accessibility Specialist

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Expert web accessibility implementation for WCAG 2.1 AA/AAA compliance and inclusive design.

## Purpose

Comprehensive accessibility expertise including ARIA attributes, keyboard navigation, screen reader compatibility, color contrast, semantic HTML, and automated testing. Ensures web applications are usable by people with disabilities and meet legal requirements.

## When to Use

- Implementing WCAG 2.1 AA or AAA compliance
- Fixing accessibility violations found in audits
- Building accessible components and forms
- Testing with screen readers (NVDA, JAWS, VoiceOver)
- Meeting ADA or Section 508 legal requirements
- Implementing keyboard-only navigation
- Optimizing for assistive technologies

## Prerequisites

**Required**: HTML/CSS, JavaScript basics, understanding of semantic HTML

**Agents**: `tester`, `reviewer`, `code-analyzer`, `coder`

## Core Workflows

### Workflow 1: Accessible Form Implementation

**Step 1: Semantic HTML with Labels**

```html
<!-- ✅ GOOD: Proper labels and structure -->
<form>
  <div class="form-group">
    <label for="email">Email Address *</label>
    <input
      type="email"
      id="email"
      name="email"
      required
      aria-required="true"
      aria-describedby="email-help email-error"
    />
    <small id="email-help">We'll never share your email.</small>
    <span id="email-error" role="alert" aria-live="polite"></span>
  </div>

  <fieldset>
    <legend>Choose your plan</legend>
    <div>
      <input type="radio" id="plan-free" name="plan" value="free" />
      <label for="plan-free">Free</label>
    </div>
    <div>
      <input type="radio" id="plan-pro" name="plan" value="pro" />
      <label for="plan-pro">Pro</label>
    </div>
  </fieldset>

  <button type="submit">Subscribe</button>
</form>

<!-- ❌ BAD: No labels, placeholder only -->
<form>
  <input type="email" placeholder="Email" />
  <input type="text" placeholder="Plan" />
  <button>Submit</button>
</form>
```

**Step 2: Client-Side Validation with Accessibility**

```javascript
const form = document.querySelector('form');
const emailInput = document.getElementById('email');
const emailError = document.getElementById('email-error');

emailInput.addEventListener('blur', () => {
  if (!emailInput.validity.valid) {
    emailError.textContent = 'Please enter a valid email address.';
    emailInput.setAttribute('aria-invalid', 'true');
  } else {
    emailError.textContent = '';
    emailInput.removeAttribute('aria-invalid');
  }
});
```

### Workflow 2: Keyboard Navigation

**Step 1: Focus Management**

```javascript
// Modal with focus trap
class AccessibleModal {
  constructor(modalElement) {
    this.modal = modalElement;
    this.focusableElements = this.modal.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    this.firstFocusable = this.focusableElements[0];
    this.lastFocusable = this.focusableElements[this.focusableElements.length - 1];
  }

  open() {
    this.previouslyFocused = document.activeElement;
    this.modal.setAttribute('aria-hidden', 'false');
    this.modal.addEventListener('keydown', this.trapFocus.bind(this));
    this.firstFocusable.focus();
  }

  close() {
    this.modal.setAttribute('aria-hidden', 'true');
    this.modal.removeEventListener('keydown', this.trapFocus);
    this.previouslyFocused.focus();
  }

  trapFocus(e) {
    if (e.key === 'Tab') {
      if (e.shiftKey) {
        if (document.activeElement === this.firstFocusable) {
          e.preventDefault();
          this.lastFocusable.focus();
        }
      } else {
        if (document.activeElement === this.lastFocusable) {
          e.preventDefault();
          this.firstFocusable.focus();
        }
      }
    }
    if (e.key === 'Escape') {
      this.close();
    }
  }
}
```

**Step 2: Skip Links**

```html
<body>
  <a href="#main-content" class="ski

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/Compliance/wcag-accessibility/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "wcag-accessibility-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>WCAG_ACCESSIBILITY_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
