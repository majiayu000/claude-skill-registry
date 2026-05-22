---
name: atomic-design-fundamentals
description: Use when applying Atomic Design methodology to organize UI components into quarks, atoms, molecules, organisms, templates, and pages. Core principles and hierarchy.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Atomic Design Fundamentals

Master Brad Frost's Atomic Design methodology (extended with quarks) for building scalable, maintainable component-based user interfaces. This skill covers the core hierarchy, principles, and organization strategies for modern design systems.

## Overview

Atomic Design is a methodology for creating design systems inspired by chemistry. Just as atoms combine to form molecules, which combine to form organisms, UI components follow a similar hierarchical structure. We extend this with **quarks** - the sub-atomic level of design tokens:

0. **Quarks** - Design tokens (colors, spacing, typography scales, shadows)
1. **Atoms** - Basic building blocks (buttons, inputs, labels)
2. **Molecules** - Groups of atoms functioning together (search form, card)
3. **Organisms** - Complex UI sections (header, footer, sidebar)
4. **Templates** - Page-level layouts without real content
5. **Pages** - Templates with real representative content

## The Six Stages

### 0. Quarks

The sub-atomic building blocks - design tokens and primitive values that atoms consume. Quarks are not UI components themselves; they are the raw values that define your design language.

**Examples:**

- Color tokens (primary-500, neutral-100)
- Spacing scales (4px, 8px, 16px)
- Typography tokens (font sizes, weights, line heights)
- Border radii
- Shadow definitions
- Animation durations and easing functions
- Breakpoints

**Characteristics:**

- Pure values, not visual components
- Cannot import from any other level
- Define the design language
- Enable theming and consistency
- Single source of truth for design decisions

### 1. Atoms

The smallest functional UI units of your interface. Atoms consume quarks for styling but cannot be broken down further without losing meaning.

**Examples:**

- Buttons
- Input fields
- Labels
- Icons
- Typography elements (headings, paragraphs)
- Color swatches
- Avatars

**Characteristics:**

- Self-contained and independent
- No business logic
- Highly reusable
- Accept styling props
- Framework-agnostic when possible

### 2. Molecules

Combinations of atoms working together as a unit. Molecules have a single responsibility but are composed of multiple atoms.

**Examples:**

- Search form (input + button)
- Form field (label + input + error message)
- Media object (avatar + text)
- Card header (icon + title + action button)
- Navigation link (icon + text)

**Characteristics:**

- Composed of atoms only
- Single purpose or function
- Reusable across contexts
- May have minimal internal state

### 3. Organisms

Complex, standalone sections of an interface. Organisms represent distinct sections that could exist independently.

**Examples:**

- Header (logo + navigation + user menu)
- Footer (links + social icons + copyright)
- Product card (image + title + price + add to cart)
- Comment section (avatar + content + actions)
- Sidebar navigation

**Characteristics:**

- Composed of molecules and atoms
- Represent distinct UI sections
- May contain business logic
- Context-specific but reusable

### 4. Templates

Page-level layouts that define content structure without actual content. Templates show the skeletal structure of a page.

**Examples:**

- Blog post template (header + content area + sidebar + footer)
- Dashboard layout (navigation + main content + widgets)
- Product page layout (gallery + details + related products)
- Landing page structure

**Characteristics:**

- Composed of organisms
- Define page structure
- Use placeholder content
- Establish content hierarchy

### 5. Pages

Specific instances of templates with real, representative content. Pages are what users actually see and interact with.

**Examples:**

- Homepage with actual hero content
- Product detail with real product data
- User profile with actual user information
- Blog post with real article content

**Characteristics:**

- Templates filled with real content
- Represent actual user experience
- Used for testing and validation
- May reveal design issues

## Directory Structure

### Standard Structure

```text
src/
  quarks/                    # Design tokens
    index.ts
    colors.ts
    spacing.ts
    typography.ts
    shadows.ts
    borders.ts
  components/
    atoms/
      Button/
        Button.tsx
        Button.test.tsx
        Button.stories.tsx
        index.ts
      Input/
      Label/
      Icon/
    molecules/
      SearchForm/
      FormField/
      Card/
    organisms/
      Header/
      Footer/
      ProductCard/
    templates/
      MainLayout/
      DashboardLayout/
    pages/
      HomePage/
      ProductPage/
```

### Alternative Flat Structure

```text
src/
  quarks/
    colors.ts
    spacing.ts
    typography.ts
  components/
    atoms/
      Button.tsx
      Input.tsx
      Label.tsx
    molecules/
      SearchForm.tsx
      FormField.tsx
    organisms/
      Header.tsx
      Footer.tsx
    templates/
      MainLayout.tsx
    pages/
      HomePage.tsx
```

### Feature-Based Hybrid

```text
src/
  quarks/                    # Shared design tokens
    index.ts
    colors.ts
    spacing.ts
  features/
    products/
      components/
        atoms/
        molecules/
        organisms/
      templates/
      pages/
    checkout/
      components/
        atoms/
        molecules/
        organisms/
  shared/
    components/
      atoms/
      molecules/
```

## Component Naming Conventions

### File Naming

```text
# PascalCase for component files
Button.tsx
SearchForm.tsx
ProductCard.tsx

# Index files for clean imports
index.ts

# Test files
Button.test.tsx
Button.spec.tsx

# Story files (Storybook)
Button.stories.tsx
```

### Component Naming

```typescript
// Atoms - simple, descriptive names
Button
Input
Label
Avatar
Icon

// Molecules - action or composition-based names
SearchForm
FormField
MediaObject
NavItem

// Organisms - section or feature-based names
Header
Footer
ProductCard
CommentSection
UserProfile

// Templates - layout-focused names
MainLayout
DashboardLayout
AuthLayout

// Pages - page-specific names
HomePage
ProductDetailPage
CheckoutPage
```

## Import Patterns

### Barrel Exports

```typescript
// src/components/atoms/index.ts
export { Button } from './Button';
export { Input } from './Input';
export { Label } from './Label';
export { Icon } from './Icon';

// src/components/molecules/index.ts
export { SearchForm } from './SearchForm';
export { FormField } from './FormField';

// src/components/index.ts
export * from './atoms';
export * from './molecules';
export * from './organisms';
```

### Usage

```typescript
// Clean imports from barrel files
import { Button, Input, Label } from '@/components/atoms';
import { SearchForm, FormField } from '@/components/molecules';
import { Header, Footer } from '@/components/organisms';

// Or from unified barrel
import { Button, SearchForm, Header } from '@/components';
```

## Composition Rules

### Strict Hierarchy

```text
Quarks     -> Used by: Atoms, Molecules, Organisms, Templates, Pages
Atoms      -> Used by: Molecules, Organisms, Templates, Pages
Molecules  -> Used by: Organisms, Templates, Pages
Organisms  -> Used by: Templates, Pages
Templates  -> Used by: Pages
Pages      -> Not used by other components
```

### Valid Compositions

```typescript
// Atom using quarks for styling
import { colors, spacing } from '@/quarks';

const Button = styled.button`
  background: ${colors.primary[500]};  {/* Quark */}
  padding: ${spacing.md};              {/* Quark */}
`;

// Molecule using atoms only
const SearchForm = () => (
  <form>
    <Input placeholder="Search..." />  {/* Atom */}
    <Button>Search</Button>            {/* Atom */}
  </form>
);

// Organism using molecules and atoms
const Header = () => (
  <header>
    <Logo />                           {/* Atom */}
    <Navigation />                     {/* Molecule */}
    <SearchForm />                     {/* Molecule */}
    <UserMenu />                       {/* Molecule */}
  </header>
);

// Template using organisms
const MainLayout = ({ children }) => (
  <div>
    <Header />                         {/* Organism */}
    <main>{children}</main>
    <Footer />                         {/* Organism */}
  </div>
);
```

### Invalid Compositions (Anti-patterns)

```typescript
// BAD: Atom importing from molecule
// atoms/Button.tsx
import { FormField } from '../molecules'; // WRONG!

// BAD: Molecule importing from organism
// molecules/SearchForm.tsx
import { Header } from '../organisms'; // WRONG!

// BAD: Skipping levels without justification
// organisms/Header.tsx
import { MainLayout } from '../templates'; // WRONG!
```

## Design Tokens Integration

### Token Structure

```typescript
// design-tokens/colors.ts
export const colors = {
  primary: {
    50: '#e3f2fd',
    100: '#bbdefb',
    500: '#2196f3',
    900: '#0d47a1',
  },
  neutral: {
    0: '#ffffff',
    100: '#f5f5f5',
    900: '#212121',
  },
};

// design-tokens/spacing.ts
export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
};

// design-tokens/typography.ts
export const typography = {
  fontFamily: {
    sans: 'Inter, system-ui, sans-serif',
    mono: 'Fira Code, monospace',
  },
  fontSize: {
    xs: '12px',
    sm: '14px',
    base: '16px',
    lg: '18px',
    xl: '24px',
  },
};
```

### Using Tokens in Atoms

```typescript
import { colors, spacing, typography } from '@/design-tokens';

const Button = styled.button`
  background-color: ${colors.primary[500]};
  padding: ${spacing.sm} ${spacing.md};
  font-family: ${typography.fontFamily.sans};
  font-size: ${typography.fontSize.base};
`;
```

## Best Practices

### 1. Start with Atoms

Build your design system from the ground up:

```typescript
// 1. Define core atoms first
const Button = ({ variant, size, children }) => { ... };
const Input = ({ type, placeholder }) => { ... };
const Label = ({ htmlFor, children }) => { ... };

// 2. Compose into molecules
const FormField = ({ label, ...inputProps }) => (
  <div>
    <Label>{label}</Label>
    <Input {...inputProps} />
  </div>
);

// 3. Build organisms from molecules
const LoginForm = () => (
  <form>
    <FormField label="Email" type="email" />
    <FormField label="Password" type="password" />
    <Button>Login</Button>
  </form>
);
```

### 2. Props Flow Downward

```typescript
// Atoms receive primitive props
interface ButtonProps {
  variant: 'primary' | 'secondary';
  size: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

// Molecules receive atoms' props via spread
interface SearchFormProps {
  onSubmit: (query: string) => void;
  inputProps?: Partial<InputProps>;
  buttonProps?: Partial<ButtonProps>;
}

// Organisms receive domain-specific props
interface HeaderProps {
  user?: User;
  onLogout: () => void;
  navigation: NavItem[];
}
```

### 3. Avoid Business Logic in Atoms

```typescript
// BAD: Atom with business logic
const PriceButton = ({ productId }) => {
  const price = useProductPrice(productId); // WRONG!
  return <Button>${price}</Button>;
};

// GOOD: Atom receives processed data
const PriceButton = ({ price, onClick }) => (
  <Button onClick={onClick}>${price}</Button>
);

// Business logic lives in organisms or higher
const ProductCard = ({ productId }) => {
  const { price } = useProduct(productId);
  return <PriceButton price={price} onClick={handleBuy} />;
};
```

### 4. Document Component Purpose

```typescript
/**
 * Button - Atomic component for user actions
 *
 * @level Atom
 * @example
 * <Button variant="primary" size="md">Click me</Button>
 */
export const Button: React.FC<ButtonProps> = ({ ... }) => { ... };

/**
 * SearchForm - Search input with submit button
 *
 * @level Molecule
 * @composition Input, Button
 * @example
 * <SearchForm onSubmit={(query) => search(query)} />
 */
export const SearchForm: React.FC<SearchFormProps> = ({ ... }) => { ... };
```

## Common Pitfalls

### 1. Over-Atomization

```typescript
// BAD: Too granular - unnecessary atoms
const ButtonText = ({ children }) => <span>{children}</span>;
const ButtonContainer = ({ children }) => <div>{children}</div>;

// GOOD: Appropriate granularity
const Button = ({ children }) => (
  <button className="btn">{children}</button>
);
```

### 2. Under-Atomization

```typescript
// BAD: Too much in one component
const MegaForm = () => (
  <form>
    <div><label>Name</label><input /></div>
    <div><label>Email</label><input /></div>
    <div><label>Message</label><textarea /></div>
    <button>Submit</button>
  </form>
);

// GOOD: Properly decomposed
const ContactForm = () => (
  <form>
    <FormField label="Name" type="text" />
    <FormField label="Email" type="email" />
    <TextAreaField label="Message" />
    <Button type="submit">Submit</Button>
  </form>
);
```

### 3. Circular Dependencies

```typescript
// BAD: Atoms importing from molecules
// atoms/Icon.tsx
import { IconButton } from '../molecules'; // Creates circular dep!

// GOOD: Keep imports flowing downward
// molecules/IconButton.tsx
import { Icon } from '../atoms';
import { Button } from '../atoms';
```

### 4. Inconsistent Naming

```typescript
// BAD: Inconsistent naming patterns
atoms/btn.tsx
atoms/InputField.tsx
atoms/text-label.tsx

// GOOD: Consistent PascalCase
atoms/Button.tsx
atoms/Input.tsx
atoms/Label.tsx
```

## When to Use This Skill

- Setting up a new design system
- Organizing an existing component library
- Onboarding team members to atomic design
- Auditing component structure
- Planning component architecture
- Creating documentation for design systems
- Refactoring monolithic components

## Related Skills

- `atomic-design-quarks` - Design tokens and primitive values
- `atomic-design-atoms` - Creating atomic-level components
- `atomic-design-molecules` - Composing atoms into molecules
- `atomic-design-organisms` - Building complex organisms
- `atomic-design-templates` - Page layouts without content
- `atomic-design-integration` - Framework-specific implementation

## Resources

### Documentation

- Brad Frost's Atomic Design: <https://atomicdesign.bradfrost.com/>
- Pattern Lab: <https://patternlab.io/>

### Books

- "Atomic Design" by Brad Frost
- "Design Systems" by Alla Kholmatova

### Tools

- Storybook: <https://storybook.js.org/>
- Pattern Lab: <https://patternlab.io/>
- Fractal: <https://fractal.build/>
