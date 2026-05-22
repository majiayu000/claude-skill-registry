---
name: ux-ui-exp
description: "UI/UX design intelligence with Bootstrap 5, Font Awesome, SweetAlert2. Use: /ux-ui-exp {command}"
license: MIT
compatibility: "OpenCode with Node.js 18+"
metadata:
  version: "1.0.0"
  author: "Mifuyuu"
---

# UXUI-Experience - Design Intelligence

Comprehensive design database with Bootstrap 5, Font Awesome, SweetAlert2 support.
57+ UI styles, 95 palettes, 56 font pairings, 183 icons, 25 alert patterns.

## Slash Command

Use `/ux-ui-exp` followed by sub-command:

### Generate Design System
```
/ux-ui-exp generate {description} for {project-name} using {stack}
/ux-ui-exp generate SaaS dashboard for MyApp using bootstrap5
/ux-ui-exp gen fintech platform for FinApp
```

---

## Instructions for AI

When user invokes this skill with `/ux-ui-exp`:

### Step 1: Parse Command

Detect command pattern:
- **generate/gen** → Use `ui_ux_generate_design_system`
- **search** → Use `ui_ux_search`
- **stack** → Use `ui_ux_get_stack_guidelines`
- **icons** → Use `ui_ux_get_icons`
- **colors** → Search domain 'color'
- **alerts** → Use `ui_ux_get_alerts`
- **fonts/typography** → Search domain 'typography'
- **bs5/bootstrap** → Stack 'bootstrap5'

### Step 2: Extract Parameters

From command text, extract:
- **Project name**: Look for "for {name}" pattern
- **Stack**: bootstrap5|react|nextjs|vue|svelte|shadcn|flutter|swiftui
- **Domain**: style|color|typography|icons|landing|alerts
- **Query**: Remaining text after command

### Step 3: Execute MCP Tool

Call appropriate MCP tool:

**For generate commands:**
```javascript
ui_ux_generate_design_system({
  query: extracted_description,
  projectName: extracted_project_name || "MyProject",
  stack: extracted_stack || "html-tailwind",
  format: "markdown"
})
```

**For search commands:**
```javascript
ui_ux_search({
  domain: extracted_domain,
  query: extracted_query,
  maxResults: 5
})
```

**For stack commands:**
```javascript
ui_ux_get_stack_guidelines({
  stack: extracted_stack,
  category: extracted_category || "",
  maxResults: 10
})
```

**For icons commands:**
```javascript
ui_ux_get_icons({
  query: extracted_query,
  library: "all",
  maxResults: 10
})
```

**For alerts commands:**
```javascript
ui_ux_get_alerts({
  type: extracted_type || "",
  maxResults: 5
})
```

### Step 4: Format Output

Present results in user-friendly format:
- **Markdown tables** for guidelines/icons
- **Code blocks** for examples
- **Checklists** for best practices
- **Highlighted key information**

---

## Available Stacks

- `bootstrap5` - Bootstrap 5 (NEW!)
- `html-tailwind` - HTML + Tailwind CSS
- `react` - React.js
- `nextjs` - Next.js
- `vue` - Vue.js
- `svelte` - Svelte
- `nuxtjs` - Nuxt.js
- `shadcn` - shadcn/ui
- `flutter` - Flutter
- `swiftui` - SwiftUI
- `react-native` - React Native

## Search Domains

- `style` - UI styles (glassmorphism, neumorphism, etc.)
- `color` - Color palettes by industry
- `typography` - Font pairings
- `icons` - Icons from Lucide + Font Awesome (183 total)
- `landing` - Landing page patterns
- `alerts` - SweetAlert2 alert patterns (25 types)

## Examples

```
/ux-ui-exp generate SaaS CRM dashboard for CRMPro using bootstrap5
→ Full design system with Bootstrap 5 guidelines

/ux-ui-exp search icons shopping cart
→ Shopping cart icons from both Lucide and Font Awesome

/ux-ui-exp stack bootstrap5 components
→ Bootstrap 5 component best practices

/ux-ui-exp alerts confirm delete
→ SweetAlert2 delete confirmation patterns

/ux-ui-exp colors healthcare
→ Color palettes for healthcare apps

/ux-ui-exp fonts luxury
→ Typography for luxury brands
```

## Notes

- **Bootstrap 5**: 40 guidelines covering layout, components, utilities, accessibility
- **Font Awesome**: 90 popular icons added (faHouse, faUser, faShoppingCart, etc.)
- **SweetAlert2**: 25 patterns (success, error, confirm, toast, input, etc.)
- All icons include import code and usage examples
- Design systems include anti-patterns and pre-delivery checklists
