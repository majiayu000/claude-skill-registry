---
name: foundry-nextgen-frontend
description: Build elegant frontend UIs following Microsoft Foundry's NextGen Design System using Vite + React + pnpm + Framer Motion. Use when creating dashboards, agent builders, data grids, entity management interfaces, or any application matching Foundry's refined dark-themed aesthetic.
---

# Microsoft Foundry NextGen Frontend Skill

Build elegant, production-ready interfaces following Microsoft Foundry's NextGen Design System - a refined **neutral dark-themed** design language with **minimal purple accents** and **subtle animations**.

## ⚠️ CRITICAL: Color Usage Rules

**Purple (#8251EE / #A37EF5) is ONLY for:**
- Primary action buttons (filled background)
- Active tab indicators (2px underline)
- Row selection indicators (left border bar)
- Active sidebar navigation icons
- Links and interactive text
- Progress indicators and sliders

**Everything else uses NEUTRAL DARK GREYS:**
- Backgrounds: Near-black (#0A0A0A, #0D0D0D)
- Cards/Surfaces: Dark grey (#141414, #1C1C1C) with **NO visible borders** or very subtle ones
- Text: White (#FFFFFF), grey (#A1A1A1), muted (#6B6B6B)
- Borders: **Mostly invisible** or very subtle (#1F1F1F)

## Preferred Stack

```bash
pnpm create vite@latest my-foundry-app --template react-ts
cd my-foundry-app
pnpm install
pnpm add framer-motion lucide-react
```

**Required packages:**
- `framer-motion` - for subtle, elegant animations
- `lucide-react` - for icons

## ⚠️ CRITICAL: Spacing & Padding Rules

**Consistent spacing is non-negotiable. Use the spacing scale:**

```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
}
```

**Standard padding patterns:**
| Element | Padding |
|---------|---------|
| Page content | 32px (--space-8) |
| Card | 20px (--space-5) |
| Card header | 16px 20px |
| Button | 8px 16px |
| Input | 10px 12px |
| Table cell | 12px 16px |
| Modal body | 24px |
| Badge/Tag | 4px 10px |

**Grid gaps:**
| Layout | Gap |
|--------|-----|
| Card grid | 16px (--space-4) |
| Form fields | 20px (--space-5) |
| Button group | 12px (--space-3) |
| Tag group | 8px (--space-2) |

## Core Design Tokens

```css
:root {
  /* BACKGROUNDS - Neutral Darks */
  --bg-page: #0A0A0A;
  --bg-sidebar: #0D0D0D;
  --bg-card: #141414;
  --bg-surface: #1C1C1C;
  --bg-elevated: #242424;
  --bg-hover: rgba(255, 255, 255, 0.05);
  --bg-active: rgba(255, 255, 255, 0.08);

  /* TEXT */
  --text-primary: #FFFFFF;
  --text-secondary: #A1A1A1;
  --text-muted: #6B6B6B;
  --text-disabled: #4A4A4A;
  --text-link: #A37EF5;

  /* BRAND - Use Sparingly! */
  --brand-primary: #8251EE;
  --brand-hover: #9366F5;
  --brand-light: #A37EF5;

  /* BORDERS - Keep Subtle! */
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.08);
  --border-strong: rgba(255, 255, 255, 0.12);

  /* STATUS */
  --success: #10B981;
  --success-bg: rgba(16, 185, 129, 0.12);
  --warning: #F59E0B;
  --warning-bg: rgba(245, 158, 11, 0.12);
  --error: #EF4444;
  --error-bg: rgba(239, 68, 68, 0.12);
  --info: #3B82F6;
  --info-bg: rgba(59, 130, 246, 0.12);

  /* RADIUS */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
}
```

## ⚠️ CRITICAL: Animation with Framer Motion

**Always add subtle animations. Never skip animations.**

```jsx
import { motion } from 'framer-motion';

// Page/container fade in
const pageVariants = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1,
    transition: { duration: 0.3, ease: 'easeOut' }
  }
};

// Stagger children (for lists, grids)
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
      delayChildren: 0.1
    }
  }
};

// Individual item animation
const itemVariants = {
  hidden: { opacity: 0, y: 8 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.3, ease: 'easeOut' }
  }
};

// Hover scale for cards/buttons
const hoverScale = {
  whileHover: { scale: 1.01 },
  whileTap: { scale: 0.99 },
  transition: { duration: 0.15 }
};
```

**Standard animation patterns:**

```jsx
// Page wrapper - always animate page entry
<motion.div
  initial="hidden"
  animate="visible"
  variants={pageVariants}
  className="page"
>
  {children}
</motion.div>

// Card grid with stagger
<motion.div
  variants={containerVariants}
  initial="hidden"
  animate="visible"
  className="card-grid"
>
  {items.map(item => (
    <motion.div key={item.id} variants={itemVariants}>
      <Card {...item} />
    </motion.div>
  ))}
</motion.div>

// Interactive card with hover
<motion.div
  className="card"
  whileHover={{ scale: 1.01, backgroundColor: 'rgba(255,255,255,0.02)' }}
  whileTap={{ scale: 0.99 }}
  transition={{ duration: 0.15 }}
>
  {content}
</motion.div>

// Button with press feedback
<motion.button
  className="btn btn-primary"
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  transition={{ duration: 0.1 }}
>
  Create
</motion.button>

// Modal with backdrop
<motion.div
  className="modal-overlay"
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  exit={{ opacity: 0 }}
>
  <motion.div
    className="modal"
    initial={{ opacity: 0, scale: 0.95, y: 10 }}
    animate={{ opacity: 1, scale: 1, y: 0 }}
    exit={{ opacity: 0, scale: 0.95, y: 10 }}
    transition={{ duration: 0.2, ease: 'easeOut' }}
  >
    {content}
  </motion.div>
</motion.div>
```

## Card Component (Correct Implementation)

**Cards should have NO visible borders or very subtle ones.**

```jsx
import { motion } from 'framer-motion';

function Card({ title, description, status, tags, meta }) {
  return (
    <motion.div 
      className="card"
      whileHover={{ 
        scale: 1.01,
        backgroundColor: 'rgba(255, 255, 255, 0.02)'
      }}
      transition={{ duration: 0.15 }}
    >
      <div className="card-header">
        <h3 className="card-title">{title}</h3>
        {status && <StatusBadge status={status} />}
      </div>
      
      <p className="card-description">{description}</p>
      
      {tags && (
        <div className="card-tags">
          {tags.map(tag => (
            <span key={tag} className="tag">{tag}</span>
          ))}
        </div>
      )}
      
      {meta && (
        <div className="card-meta">
          {meta}
        </div>
      )}
    </motion.div>
  );
}
```

```css
.card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--space-5);  /* 20px */
  /* NO border or very subtle */
  border: 1px solid transparent;
  /* Use subtle shadow instead of border */
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.card:hover {
  /* Subtle border on hover only */
  border-color: var(--border-subtle);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-3);  /* 12px */
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.card-description {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0 0 var(--space-4);  /* 16px bottom */
  line-height: 1.5;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);  /* 8px */
  margin-bottom: var(--space-4);
}

.card-meta {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  font-size: 12px;
  color: var(--text-muted);
  padding-top: var(--space-3);
  border-top: 1px solid var(--border-subtle);
}
```

## Tags & Badges

```css
/* Service/integration tags - subtle, not colorful */
.tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  border-radius: var(--radius-sm);
  background: var(--bg-surface);
  color: var(--text-secondary);
}

/* Status badges */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  border-radius: var(--radius-sm);
}

.badge-success {
  background: var(--success-bg);
  color: var(--success);
}

.badge-info {
  background: var(--info-bg);
  color: var(--info);
}

.badge-warning {
  background: var(--warning-bg);
  color: var(--warning);
}
```

## Card Grid Layout

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-4);  /* 16px - consistent gap */
  padding: var(--space-8);  /* 32px page padding */
}

/* For fixed 4-column layout */
.card-grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
}

/* For 3-column layout */
.card-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}
```

## Page Layout with Sidebar

```jsx
function AppLayout({ children }) {
  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <TopBar />
        <motion.div 
          className="page-content"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
        >
          {children}
        </motion.div>
      </main>
    </div>
  );
}
```

```css
.app-layout {
  display: flex;
  min-height: 100vh;
  background: var(--bg-page);
}

.sidebar {
  width: 56px;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border-subtle);
  flex-shrink: 0;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.topbar {
  height: 48px;
  background: var(--bg-sidebar);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  padding: 0 var(--space-6);
}

.page-content {
  flex: 1;
  padding: var(--space-8);  /* 32px consistent padding */
  overflow-y: auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);  /* 24px before content */
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}
```

## Buttons

```jsx
<motion.button
  className="btn btn-primary"
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
>
  Create
</motion.button>

<motion.button
  className="btn btn-secondary"
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
>
  Cancel
</motion.button>
```

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background 0.15s ease;
}

.btn-primary {
  background: var(--brand-primary);
  color: white;
  border: none;
}

.btn-primary:hover {
  background: var(--brand-hover);
}

.btn-secondary {
  background: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-strong);
}

.btn-secondary:hover {
  background: var(--bg-hover);
}
```

## Critical Don'ts ❌

- **Don't use visible card borders** - cards blend into background
- **Don't use inconsistent padding** - follow the spacing scale
- **Don't forget animations** - every list, modal, page needs motion
- **Don't use purple for cards/backgrounds** - neutral greys only
- **Don't skip hover states** - everything interactive needs feedback
- **Don't use hard-coded pixel values** - use CSS variables

## Critical Do's ✅

- Use Framer Motion for all animations
- Use consistent spacing scale (4, 8, 12, 16, 20, 24, 32px)
- Use 32px padding for page content areas
- Use 16px gap for card grids
- Use transparent or very subtle borders
- Add hover animations to interactive elements
- Stagger list/grid item animations

## File References

- **Design Tokens**: See `references/design-tokens.md`
- **Components**: See `references/components.md`
- **Patterns**: See `references/patterns.md`
