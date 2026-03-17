---
name: atomic-design-gluestack
description: |
  Enforces atomic design methodology (atoms, molecules, organisms, templates, pages) for React Native/Expo projects using Gluestack UI. This skill should be used when creating new components, validating existing component organization, reviewing component placement decisions, or planning component architecture. Use this skill to ensure components are properly categorized, placed in correct directories, and follow composition patterns appropriate to their atomic level.
---

# Atomic Design with Gluestack UI

## Overview

This skill enforces Brad Frost's atomic design methodology adapted for React Native/Expo projects using Gluestack UI v3 + NativeWind v4. It provides clear guidelines for component categorization, directory structure, composition patterns, and testing strategies for each atomic level.

## Core Principles

### The Atomic Hierarchy

Components are organized into five levels, from simplest to most complex:

| Level | Definition | State | Examples |
|-------|------------|-------|----------|
| **Atoms** | Foundational building blocks that cannot be broken down further while remaining functional | Stateless (purely presentational) | Button, Text, Icon, Input, Badge |
| **Molecules** | Simple groups of UI elements functioning together as a unit | Isolated state (form validation, toggles) | SearchField, FormField, AvatarWithName |
| **Organisms** | Complex components composed of molecules and atoms forming distinct interface sections | Feature state, coordinates children | Header, ProductCard, NavigationDrawer |
| **Templates** | Page-level layouts that place components into a structure (skeleton without real content) | Layout state only | MainLayout, AuthLayout, DashboardLayout |
| **Pages** | Specific instances of templates with real content and data | Connected to global state | HomeScreen, ProfileScreen, SettingsScreen |

### Design Tokens Foundation

Design tokens sit **below atoms** as the foundational layer. In this project, tokens are defined in:
- `components/ui/gluestack-ui-provider/config.ts` - Color tokens (primary, secondary, error, success, etc.)
- `tailwind.config.js` - Spacing, typography, and other design tokens via NativeWind

## Directory Structure

### Required Structure

```
components/
├── ui/                          # Gluestack UI library components (DO NOT MODIFY unless extending)
├── atoms/                       # Project-specific atoms
│   ├── AppIcon/
│   │   ├── index.tsx
│   │   ├── AppIcon.test.tsx
│   │   └── types.ts
│   └── index.ts                 # Barrel export for atoms
├── molecules/                   # Composite simple components
│   ├── SearchField/
│   │   ├── index.tsx
│   │   ├── SearchFieldView.tsx
│   │   ├── SearchField.test.tsx
│   │   └── types.ts
│   └── index.ts
├── organisms/                   # Complex feature components
│   ├── Header/
│   │   ├── index.tsx
│   │   ├── HeaderView.tsx
│   │   ├── Header.test.tsx
│   │   └── types.ts
│   └── index.ts
└── templates/                   # Page layouts
    ├── MainLayout/
    │   ├── index.tsx
    │   ├── MainLayoutView.tsx
    │   └── types.ts
    └── index.ts

features/
└── [feature-name]/
    ├── components/              # Feature-specific components (follow atomic naming)
    │   ├── atoms/
    │   ├── molecules/
    │   └── organisms/
    └── screens/                 # Pages (specific to this feature)

app/                             # Expo Router pages (connect templates with data)
```

### Gluestack UI Components Location

The 40+ Gluestack UI components in `components/ui/` serve as the **foundation atom library**. When building custom components:

1. **Use Gluestack components as atoms** - Import from `@/components/ui/`
2. **Extend when needed** - Create project-specific atoms in `components/atoms/`
3. **Never modify `components/ui/`** - Except for theme customization in `config.ts`

## Component Classification Rules

### Rule 1: Atoms (Building Blocks)

**Definition**: Smallest functional UI elements that cannot be broken down further.

**Characteristics**:
- Stateless and purely presentational
- Accept props for customization
- No business logic
- Highly reusable across the entire app

**Gluestack Atoms** (use directly from `@/components/ui/`):
- Box, Center, HStack, VStack, ScrollView
- Text, Heading
- Button, ButtonText, ButtonIcon
- Input, InputField, InputSlot
- Icon, Image, Avatar
- Badge, Divider, Spinner

**When to create custom atoms**:
- Project-specific iconography
- Branded text variants
- Wrapper components with default styling

```typescript
/**
 * AppLogo atom - Branded logo component
 * @description Displays the application logo with consistent sizing
 */
const AppLogo = memo(function AppLogo({ size = "md" }: AppLogoProps) {
  return (
    <Image
      source={logoSource}
      className={logoSizes[size]}
      alt="App Logo"
    />
  );
});
```

### Rule 2: Molecules (Simple Compositions)

**Definition**: Simple groups of atoms functioning together as a unit.

**Characteristics**:
- Combines 2-5 atoms
- Single responsibility (does one thing well)
- May have isolated UI state (toggle, validation)
- No external data fetching

**Examples**:
```typescript
/**
 * SearchField molecule - Search input with button
 * @description Combines Input and Button atoms for search functionality
 */
const SearchField = memo(function SearchField({
  onSearch,
  placeholder
}: SearchFieldProps) {
  const [value, setValue] = useState("");

  return (
    <HStack space="sm" className="items-center">
      <Input className="flex-1">
        <InputField
          value={value}
          onChangeText={setValue}
          placeholder={placeholder}
        />
      </Input>
      <Button onPress={() => onSearch(value)}>
        <ButtonIcon as={SearchIcon} />
      </Button>
    </HStack>
  );
});
```

**Molecule Checklist**:
- [ ] Uses only atoms (Gluestack or custom)
- [ ] Has a single, clear purpose
- [ ] State is UI-only (no business logic)
- [ ] Reusable in multiple contexts

### Rule 3: Organisms (Complex Sections)

**Definition**: Relatively complex components forming distinct interface sections.

**Characteristics**:
- Combines molecules and atoms
- May have feature-specific state
- Can coordinate child component behavior
- Represents a standalone section of UI

**Examples**:
```typescript
/**
 * ProductCard organism - Complete product display
 * @description Displays product information with actions
 */
const ProductCard = memo(function ProductCard({
  product,
  onAddToCart
}: ProductCardProps) {
  return (
    <Card variant="elevated" size="md">
      <ProductImage source={product.image} />      {/* Atom */}
      <VStack space="sm" className="p-4">
        <Heading size="md">{product.name}</Heading> {/* Atom */}
        <PriceDisplay price={product.price} />      {/* Molecule */}
        <RatingStars rating={product.rating} />     {/* Molecule */}
        <AddToCartButton onPress={onAddToCart} />   {/* Molecule */}
      </VStack>
    </Card>
  );
});
```

**Organism Checklist**:
- [ ] Forms a distinct interface section
- [ ] Combines molecules and/or atoms
- [ ] Has clear boundaries
- [ ] May receive data as props (but doesn't fetch)

### Rule 4: Templates (Page Layouts)

**Definition**: Page-level layouts that place components into a structure.

**Characteristics**:
- Defines layout skeleton with slots
- No real content (uses placeholder or children)
- Handles responsive behavior
- Manages layout-specific state only

**Example**:
```typescript
/**
 * MainLayout template - Primary app layout
 * @description Provides consistent header, content, and footer structure
 */
const MainLayout = memo(function MainLayout({
  children,
  showHeader = true,
  showFooter = true
}: MainLayoutProps) {
  return (
    <SafeAreaView className="flex-1 bg-background-0">
      {showHeader && <Header />}
      <ScrollView className="flex-1">
        {children}
      </ScrollView>
      {showFooter && <Footer />}
    </SafeAreaView>
  );
});
```

### Rule 5: Pages (Screens)

**Definition**: Specific instances of templates with real content and data.

**Characteristics**:
- Connects to global state (Apollo, Context)
- Handles data fetching
- Passes data to organisms/molecules
- Lives in `app/` (Expo Router) or `features/*/screens/`

**Example**:
```typescript
/**
 * HomeScreen page - Main home page
 * @description Renders home content with fetched data
 */
export default function HomeScreen() {
  const { data, loading } = useHomeDataQuery();

  return (
    <MainLayout>
      {loading ? (
        <LoadingSpinner />
      ) : (
        <VStack space="lg">
          <FeaturedProducts products={data.featured} />
          <RecentActivity items={data.activity} />
        </VStack>
      )}
    </MainLayout>
  );
}
```

## Validation Rules

### Enforcement Checklist

When creating or reviewing components, verify:

1. **Correct Directory Placement**
   - Atoms in `components/atoms/` or `features/*/components/atoms/`
   - Molecules in `components/molecules/` or `features/*/components/molecules/`
   - Organisms in `components/organisms/` or `features/*/components/organisms/`
   - Templates in `components/templates/`
   - Pages in `app/` or `features/*/screens/`

2. **State Appropriateness**
   - Atoms: No state
   - Molecules: UI state only (useState for toggles, form values)
   - Organisms: Feature state, may use custom hooks
   - Templates: Layout state only
   - Pages: Connected to global state, data fetching

3. **Import Direction** (dependencies flow upward only)
   ```
   Pages → Templates → Organisms → Molecules → Atoms → Design Tokens
   ```
   - Atoms MUST NOT import from molecules, organisms, templates, or pages
   - Molecules MUST NOT import from organisms, templates, or pages
   - Organisms MUST NOT import from templates or pages

4. **Composition Appropriateness**
   - Molecules combine 2-5 atoms
   - Organisms can be complex but should represent a single interface section
   - If an organism becomes too large, extract sub-organisms

### Common Mistakes to Avoid

| Mistake | Problem | Solution |
|---------|---------|----------|
| Atom with useState | Atoms should be stateless | Move state to parent molecule |
| Molecule fetching data | Data fetching belongs in pages | Accept data as props |
| Organism in atoms folder | Misclassification | Move to organisms folder |
| Template with business logic | Templates handle layout only | Move logic to page |
| Importing organism in atom | Wrong dependency direction | Restructure component hierarchy |

## Testing by Atomic Level

| Level | Test Type | Focus |
|-------|-----------|-------|
| Atoms | Unit + Snapshot | Props rendering, accessibility |
| Molecules | Unit + Interaction | Composition, isolated state |
| Organisms | Integration | Data flow, child coordination |
| Templates | Layout | Slot rendering, responsiveness |
| Pages | E2E | Full user flows |

## Quick Reference

### Decision Tree: Which Level?

```
Is it a single, indivisible UI element?
├─ YES → ATOM
└─ NO → Does it combine 2-5 atoms for a single purpose?
         ├─ YES → MOLECULE
         └─ NO → Does it form a distinct interface section?
                  ├─ YES → ORGANISM
                  └─ NO → Is it a layout skeleton?
                           ├─ YES → TEMPLATE
                           └─ NO → PAGE
```

### Gluestack Component Level Map

Reference `references/gluestack-mapping.md` for the complete mapping of all 40 Gluestack UI components to their atomic levels.

## Resources

### references/
- `atomic-levels.md` - Detailed definitions with comprehensive examples
- `gluestack-mapping.md` - Complete Gluestack UI component classification
- `folder-structure.md` - Detailed directory structure requirements

### scripts/
- `validate_atomic_structure.py` - Validates component placement and imports
