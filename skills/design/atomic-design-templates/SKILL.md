---
name: atomic-design-templates
description: Use when creating page layouts without real content. Templates define the skeletal structure of pages using organisms, molecules, and atoms.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Atomic Design: Templates

Master the creation of templates - page-level layouts that define content structure without actual content. Templates establish the skeletal structure that pages will use.

## What Are Templates?

Templates are the page-level objects that place components into a layout and articulate the design's underlying content structure. They are:

- **Composed of organisms**: Arrange organisms into page layouts
- **Content-agnostic**: Use placeholder content, not real data
- **Structural**: Define where content types will appear
- **Reusable**: Same template can be used by multiple pages
- **Responsive**: Handle all viewport sizes

## Common Template Types

### Marketing Templates

- Landing page layouts
- Homepage layouts
- Product showcase layouts
- About/Company layouts

### Application Templates

- Dashboard layouts
- Settings page layouts
- Profile page layouts
- List/Detail page layouts

### Content Templates

- Blog post layouts
- Article layouts
- Documentation layouts
- Help center layouts

### E-commerce Templates

- Product listing layouts
- Product detail layouts
- Checkout layouts
- Order confirmation layouts

## MainLayout Template Example

### Complete Implementation

```typescript
// templates/MainLayout/MainLayout.tsx
import React from 'react';
import { Header, type HeaderProps } from '@/components/organisms/Header';
import { Footer, type FooterProps } from '@/components/organisms/Footer';
import styles from './MainLayout.module.css';

export interface MainLayoutProps {
  /** Header configuration */
  headerProps: HeaderProps;
  /** Footer configuration */
  footerProps: FooterProps;
  /** Main content */
  children: React.ReactNode;
  /** Show breadcrumbs */
  showBreadcrumbs?: boolean;
  /** Breadcrumb component */
  breadcrumbs?: React.ReactNode;
  /** Maximum content width */
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  /** Page background color */
  background?: 'white' | 'gray' | 'primary';
}

export const MainLayout: React.FC<MainLayoutProps> = ({
  headerProps,
  footerProps,
  children,
  showBreadcrumbs = false,
  breadcrumbs,
  maxWidth = 'lg',
  background = 'white',
}) => {
  return (
    <div className={`${styles.layout} ${styles[`bg-${background}`]}`}>
      <Header {...headerProps} />

      <main className={styles.main}>
        {showBreadcrumbs && breadcrumbs && (
          <div className={styles.breadcrumbs}>{breadcrumbs}</div>
        )}

        <div className={`${styles.content} ${styles[`max-${maxWidth}`]}`}>
          {children}
        </div>
      </main>

      <Footer {...footerProps} />
    </div>
  );
};

MainLayout.displayName = 'MainLayout';
```

```css
/* templates/MainLayout/MainLayout.module.css */
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.breadcrumbs {
  padding: 16px 24px;
  background-color: var(--color-neutral-50);
  border-bottom: 1px solid var(--color-neutral-200);
}

.content {
  flex: 1;
  margin: 0 auto;
  padding: 24px;
  width: 100%;
}

/* Max Width Variants */
.max-sm {
  max-width: 640px;
}

.max-md {
  max-width: 768px;
}

.max-lg {
  max-width: 1024px;
}

.max-xl {
  max-width: 1280px;
}

.max-full {
  max-width: 100%;
}

/* Background Variants */
.bg-white {
  background-color: var(--color-white);
}

.bg-gray {
  background-color: var(--color-neutral-50);
}

.bg-primary {
  background-color: var(--color-primary-50);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .content {
    padding: 16px;
  }
}
```

## DashboardLayout Template Example

```typescript
// templates/DashboardLayout/DashboardLayout.tsx
import React, { useState } from 'react';
import { Header } from '@/components/organisms/Header';
import { Sidebar, type SidebarProps } from '@/components/organisms/Sidebar';
import styles from './DashboardLayout.module.css';

export interface DashboardLayoutProps {
  /** Header props */
  headerProps: {
    logo: React.ReactNode;
    user?: { name: string; email: string; avatar?: string };
    onLogout?: () => void;
  };
  /** Sidebar props */
  sidebarProps: SidebarProps;
  /** Main content */
  children: React.ReactNode;
  /** Page title */
  pageTitle?: string;
  /** Page description */
  pageDescription?: string;
  /** Page actions (buttons, etc.) */
  pageActions?: React.ReactNode;
  /** Sidebar initially collapsed */
  sidebarCollapsed?: boolean;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  headerProps,
  sidebarProps,
  children,
  pageTitle,
  pageDescription,
  pageActions,
  sidebarCollapsed = false,
}) => {
  const [isCollapsed, setIsCollapsed] = useState(sidebarCollapsed);

  return (
    <div className={styles.layout}>
      {/* Top Header */}
      <Header
        logo={headerProps.logo}
        navigation={[]}
        user={headerProps.user}
        onLogout={headerProps.onLogout}
        showSearch={false}
      />

      <div className={styles.body}>
        {/* Sidebar */}
        <Sidebar
          {...sidebarProps}
          isCollapsed={isCollapsed}
          onToggleCollapse={() => setIsCollapsed(!isCollapsed)}
        />

        {/* Main Content Area */}
        <main className={styles.main}>
          {/* Page Header */}
          {(pageTitle || pageActions) && (
            <header className={styles.pageHeader}>
              <div className={styles.titleSection}>
                {pageTitle && <h1 className={styles.pageTitle}>{pageTitle}</h1>}
                {pageDescription && (
                  <p className={styles.pageDescription}>{pageDescription}</p>
                )}
              </div>
              {pageActions && (
                <div className={styles.pageActions}>{pageActions}</div>
              )}
            </header>
          )}

          {/* Page Content */}
          <div className={styles.content}>{children}</div>
        </main>
      </div>
    </div>
  );
};

DashboardLayout.displayName = 'DashboardLayout';
```

```css
/* templates/DashboardLayout/DashboardLayout.module.css */
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.body {
  display: flex;
  flex: 1;
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  background-color: var(--color-neutral-50);
}

.pageHeader {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
  padding: 24px;
  background-color: var(--color-white);
  border-bottom: 1px solid var(--color-neutral-200);
}

.titleSection {
  flex: 1;
}

.pageTitle {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: var(--color-neutral-900);
}

.pageDescription {
  margin: 4px 0 0;
  font-size: 14px;
  color: var(--color-neutral-500);
}

.pageActions {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

.content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .pageHeader {
    flex-direction: column;
    align-items: stretch;
  }

  .pageActions {
    margin-top: 16px;
  }

  .content {
    padding: 16px;
  }
}
```

## AuthLayout Template Example

```typescript
// templates/AuthLayout/AuthLayout.tsx
import React from 'react';
import styles from './AuthLayout.module.css';

export interface AuthLayoutProps {
  /** Logo element */
  logo: React.ReactNode;
  /** Page title */
  title: string;
  /** Page subtitle */
  subtitle?: string;
  /** Form content */
  children: React.ReactNode;
  /** Footer content (links, etc.) */
  footer?: React.ReactNode;
  /** Background image URL */
  backgroundImage?: string;
  /** Show decorative side panel */
  showSidePanel?: boolean;
  /** Side panel content */
  sidePanelContent?: React.ReactNode;
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({
  logo,
  title,
  subtitle,
  children,
  footer,
  backgroundImage,
  showSidePanel = false,
  sidePanelContent,
}) => {
  return (
    <div className={styles.layout}>
      {/* Side Panel (optional) */}
      {showSidePanel && (
        <div
          className={styles.sidePanel}
          style={
            backgroundImage
              ? { backgroundImage: `url(${backgroundImage})` }
              : undefined
          }
        >
          <div className={styles.sidePanelContent}>{sidePanelContent}</div>
        </div>
      )}

      {/* Main Content */}
      <div className={styles.main}>
        <div className={styles.container}>
          {/* Logo */}
          <div className={styles.logo}>{logo}</div>

          {/* Header */}
          <header className={styles.header}>
            <h1 className={styles.title}>{title}</h1>
            {subtitle && <p className={styles.subtitle}>{subtitle}</p>}
          </header>

          {/* Form Content */}
          <div className={styles.content}>{children}</div>

          {/* Footer */}
          {footer && <footer className={styles.footer}>{footer}</footer>}
        </div>
      </div>
    </div>
  );
};

AuthLayout.displayName = 'AuthLayout';
```

```css
/* templates/AuthLayout/AuthLayout.module.css */
.layout {
  display: flex;
  min-height: 100vh;
}

.sidePanel {
  display: none;
  width: 50%;
  background-color: var(--color-primary-600);
  background-size: cover;
  background-position: center;
  position: relative;
}

@media (min-width: 1024px) {
  .sidePanel {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

.sidePanelContent {
  padding: 48px;
  color: var(--color-white);
  text-align: center;
}

.main {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background-color: var(--color-neutral-50);
}

.container {
  width: 100%;
  max-width: 400px;
}

.logo {
  text-align: center;
  margin-bottom: 32px;
}

.header {
  text-align: center;
  margin-bottom: 32px;
}

.title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: var(--color-neutral-900);
}

.subtitle {
  margin: 8px 0 0;
  font-size: 16px;
  color: var(--color-neutral-500);
}

.content {
  background-color: var(--color-white);
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.footer {
  margin-top: 24px;
  text-align: center;
  font-size: 14px;
  color: var(--color-neutral-500);
}

.footer a {
  color: var(--color-primary-500);
  text-decoration: none;
}

.footer a:hover {
  text-decoration: underline;
}
```

## ProductListingLayout Template Example

```typescript
// templates/ProductListingLayout/ProductListingLayout.tsx
import React from 'react';
import { MainLayout, type MainLayoutProps } from '../MainLayout';
import styles from './ProductListingLayout.module.css';

export interface ProductListingLayoutProps {
  /** Main layout props */
  layoutProps: Omit<MainLayoutProps, 'children'>;
  /** Category title */
  categoryTitle: string;
  /** Category description */
  categoryDescription?: string;
  /** Product count */
  productCount: number;
  /** Filter sidebar content */
  filters: React.ReactNode;
  /** Sort/view controls */
  controls: React.ReactNode;
  /** Product grid content */
  products: React.ReactNode;
  /** Pagination content */
  pagination?: React.ReactNode;
  /** Show filters on mobile */
  mobileFiltersOpen?: boolean;
  /** Toggle mobile filters */
  onToggleMobileFilters?: () => void;
}

export const ProductListingLayout: React.FC<ProductListingLayoutProps> = ({
  layoutProps,
  categoryTitle,
  categoryDescription,
  productCount,
  filters,
  controls,
  products,
  pagination,
  mobileFiltersOpen = false,
  onToggleMobileFilters,
}) => {
  return (
    <MainLayout {...layoutProps} maxWidth="xl">
      {/* Category Header */}
      <header className={styles.header}>
        <div className={styles.titleSection}>
          <h1 className={styles.title}>{categoryTitle}</h1>
          {categoryDescription && (
            <p className={styles.description}>{categoryDescription}</p>
          )}
          <span className={styles.count}>{productCount} products</span>
        </div>
      </header>

      <div className={styles.body}>
        {/* Desktop Filters */}
        <aside className={styles.sidebar}>
          <div className={styles.sidebarContent}>{filters}</div>
        </aside>

        {/* Mobile Filters Overlay */}
        {mobileFiltersOpen && (
          <div className={styles.mobileFilters}>
            <div className={styles.mobileFiltersHeader}>
              <h2>Filters</h2>
              <button onClick={onToggleMobileFilters}>Close</button>
            </div>
            <div className={styles.mobileFiltersContent}>{filters}</div>
          </div>
        )}

        {/* Main Content */}
        <div className={styles.main}>
          {/* Controls Bar */}
          <div className={styles.controls}>
            <button
              className={styles.mobileFilterButton}
              onClick={onToggleMobileFilters}
            >
              Filters
            </button>
            {controls}
          </div>

          {/* Product Grid */}
          <div className={styles.products}>{products}</div>

          {/* Pagination */}
          {pagination && (
            <div className={styles.pagination}>{pagination}</div>
          )}
        </div>
      </div>
    </MainLayout>
  );
};

ProductListingLayout.displayName = 'ProductListingLayout';
```

## BlogPostLayout Template Example

```typescript
// templates/BlogPostLayout/BlogPostLayout.tsx
import React from 'react';
import { MainLayout, type MainLayoutProps } from '../MainLayout';
import { Avatar } from '@/components/atoms/Avatar';
import { Text } from '@/components/atoms/Typography';
import styles from './BlogPostLayout.module.css';

export interface Author {
  name: string;
  avatar?: string;
  bio?: string;
}

export interface BlogPostLayoutProps {
  /** Main layout props */
  layoutProps: Omit<MainLayoutProps, 'children'>;
  /** Post title */
  title: string;
  /** Post subtitle */
  subtitle?: string;
  /** Featured image */
  featuredImage?: string;
  /** Author information */
  author: Author;
  /** Publication date */
  publishedAt: string;
  /** Reading time */
  readingTime?: string;
  /** Post categories/tags */
  tags?: React.ReactNode;
  /** Main article content */
  children: React.ReactNode;
  /** Table of contents */
  tableOfContents?: React.ReactNode;
  /** Author bio card */
  showAuthorBio?: boolean;
  /** Related posts */
  relatedPosts?: React.ReactNode;
  /** Comments section */
  comments?: React.ReactNode;
  /** Social share buttons */
  shareButtons?: React.ReactNode;
}

export const BlogPostLayout: React.FC<BlogPostLayoutProps> = ({
  layoutProps,
  title,
  subtitle,
  featuredImage,
  author,
  publishedAt,
  readingTime,
  tags,
  children,
  tableOfContents,
  showAuthorBio = true,
  relatedPosts,
  comments,
  shareButtons,
}) => {
  const formattedDate = new Date(publishedAt).toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  });

  return (
    <MainLayout {...layoutProps} maxWidth="md">
      <article className={styles.article}>
        {/* Article Header */}
        <header className={styles.header}>
          {tags && <div className={styles.tags}>{tags}</div>}

          <h1 className={styles.title}>{title}</h1>

          {subtitle && <p className={styles.subtitle}>{subtitle}</p>}

          {/* Author & Meta */}
          <div className={styles.meta}>
            <div className={styles.author}>
              <Avatar
                src={author.avatar}
                alt={author.name}
                initials={author.name.slice(0, 2).toUpperCase()}
                size="md"
              />
              <div className={styles.authorInfo}>
                <Text weight="semibold">{author.name}</Text>
                <Text size="sm" color="muted">
                  {formattedDate}
                  {readingTime && ` · ${readingTime}`}
                </Text>
              </div>
            </div>

            {shareButtons && (
              <div className={styles.share}>{shareButtons}</div>
            )}
          </div>
        </header>

        {/* Featured Image */}
        {featuredImage && (
          <figure className={styles.featuredImage}>
            <img src={featuredImage} alt={title} />
          </figure>
        )}

        {/* Content with Optional TOC */}
        <div className={styles.contentWrapper}>
          {/* Table of Contents (Desktop) */}
          {tableOfContents && (
            <aside className={styles.toc}>
              <div className={styles.tocContent}>{tableOfContents}</div>
            </aside>
          )}

          {/* Main Content */}
          <div className={styles.content}>{children}</div>
        </div>

        {/* Author Bio */}
        {showAuthorBio && (
          <footer className={styles.authorBio}>
            <Avatar
              src={author.avatar}
              alt={author.name}
              initials={author.name.slice(0, 2).toUpperCase()}
              size="lg"
            />
            <div>
              <Text weight="semibold" size="lg">
                {author.name}
              </Text>
              {author.bio && <Text color="muted">{author.bio}</Text>}
            </div>
          </footer>
        )}

        {/* Share (Bottom) */}
        {shareButtons && (
          <div className={styles.bottomShare}>{shareButtons}</div>
        )}
      </article>

      {/* Related Posts */}
      {relatedPosts && (
        <section className={styles.relatedPosts}>
          <h2>Related Posts</h2>
          {relatedPosts}
        </section>
      )}

      {/* Comments */}
      {comments && (
        <section className={styles.comments}>{comments}</section>
      )}
    </MainLayout>
  );
};

BlogPostLayout.displayName = 'BlogPostLayout';
```

## TwoColumnLayout Template Example

```typescript
// templates/TwoColumnLayout/TwoColumnLayout.tsx
import React from 'react';
import styles from './TwoColumnLayout.module.css';

export interface TwoColumnLayoutProps {
  /** Left column (usually main content) */
  main: React.ReactNode;
  /** Right column (usually sidebar) */
  sidebar: React.ReactNode;
  /** Sidebar position */
  sidebarPosition?: 'left' | 'right';
  /** Sidebar width */
  sidebarWidth?: 'narrow' | 'medium' | 'wide';
  /** Sticky sidebar */
  stickySidebar?: boolean;
  /** Reverse on mobile (show sidebar first) */
  reverseMobile?: boolean;
  /** Gap between columns */
  gap?: 'sm' | 'md' | 'lg';
}

export const TwoColumnLayout: React.FC<TwoColumnLayoutProps> = ({
  main,
  sidebar,
  sidebarPosition = 'right',
  sidebarWidth = 'medium',
  stickySidebar = false,
  reverseMobile = false,
  gap = 'md',
}) => {
  const layoutClass = [
    styles.layout,
    styles[`sidebar-${sidebarPosition}`],
    styles[`width-${sidebarWidth}`],
    styles[`gap-${gap}`],
    reverseMobile && styles.reverseMobile,
  ]
    .filter(Boolean)
    .join(' ');

  const sidebarClass = [
    styles.sidebar,
    stickySidebar && styles.sticky,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div className={layoutClass}>
      <main className={styles.main}>{main}</main>
      <aside className={sidebarClass}>{sidebar}</aside>
    </div>
  );
};

TwoColumnLayout.displayName = 'TwoColumnLayout';
```

## Best Practices

### 1. Use Placeholder Content

```typescript
// GOOD: Template with placeholder content slots
const ProductDetailLayout = ({
  productGallery,    // Placeholder for gallery component
  productInfo,       // Placeholder for product details
  productTabs,       // Placeholder for tabs
  relatedProducts,   // Placeholder for recommendations
}) => (
  <div>
    <section>{productGallery}</section>
    <section>{productInfo}</section>
    <section>{productTabs}</section>
    <section>{relatedProducts}</section>
  </div>
);

// BAD: Template with hardcoded content
const ProductDetailLayout = ({ product }) => (
  <div>
    <ProductGallery images={product.images} />      {/* Too specific */}
    <h1>{product.name}</h1>                          {/* Real content */}
    <p>{product.description}</p>
  </div>
);
```

### 2. Define Clear Content Areas

```typescript
// GOOD: Clear, named content slots
interface PageTemplateProps {
  header: React.ReactNode;
  hero?: React.ReactNode;
  main: React.ReactNode;
  sidebar?: React.ReactNode;
  footer: React.ReactNode;
}

// BAD: Generic children only
interface PageTemplateProps {
  children: React.ReactNode;
}
```

### 3. Handle Responsive Layouts

```typescript
// GOOD: Responsive considerations built-in
const DashboardLayout = ({ sidebar, main }) => (
  <div className={styles.layout}>
    <aside className={styles.sidebar}>{sidebar}</aside>
    <main className={styles.main}>{main}</main>
  </div>
);

// CSS handles responsive behavior
// .sidebar { @media (max-width: 768px) { display: none; } }
```

### 4. Keep Templates Thin

```typescript
// GOOD: Template just arranges organisms
const MainLayout = ({ header, main, footer }) => (
  <div className={styles.layout}>
    <div className={styles.header}>{header}</div>
    <div className={styles.main}>{main}</div>
    <div className={styles.footer}>{footer}</div>
  </div>
);

// BAD: Template with business logic
const MainLayout = ({ userId }) => {
  const user = useUser(userId);          // Fetching data
  const isAdmin = user?.role === 'admin'; // Business logic

  return (
    <div>
      <Header user={user} showAdmin={isAdmin} />
      {/* ... */}
    </div>
  );
};
```

## Anti-Patterns to Avoid

### 1. Templates with Real Content

```typescript
// BAD: Hardcoded real content
const HomepageLayout = () => (
  <div>
    <h1>Welcome to Our Store</h1>           {/* Real content! */}
    <p>Shop our latest collection...</p>    {/* Real content! */}
  </div>
);

// GOOD: Content passed as props/children
const HomepageLayout = ({ heroTitle, heroDescription }) => (
  <div>
    <h1>{heroTitle}</h1>
    <p>{heroDescription}</p>
  </div>
);
```

### 2. Over-Nested Templates

```typescript
// BAD: Templates containing templates
const AppLayout = () => (
  <BaseLayout>
    <AuthLayout>
      <DashboardLayout>
        {/* Too much nesting */}
      </DashboardLayout>
    </AuthLayout>
  </BaseLayout>
);

// GOOD: Choose appropriate template directly
const AppPage = () => (
  <DashboardLayout>
    {/* Content */}
  </DashboardLayout>
);
```

### 3. Templates with Too Many Props

```typescript
// BAD: Too many configuration options
interface LayoutProps {
  showHeader: boolean;
  showFooter: boolean;
  showSidebar: boolean;
  sidebarPosition: 'left' | 'right';
  headerVariant: 'default' | 'minimal' | 'transparent';
  footerVariant: 'default' | 'minimal';
  maxWidth: 'sm' | 'md' | 'lg' | 'xl';
  // ... 20 more props
}

// GOOD: Create separate templates
const FullPageLayout = ({ ... }) => { ... };
const MinimalLayout = ({ ... }) => { ... };
const SidebarLayout = ({ ... }) => { ... };
```

## Template Composition Patterns

### Nested Layouts

```typescript
// Base layout for all pages
const BaseLayout = ({ children }) => (
  <div className="base">
    <SkipLink />
    {children}
  </div>
);

// Marketing layout extending base
const MarketingLayout = ({ children }) => (
  <BaseLayout>
    <MarketingHeader />
    <main>{children}</main>
    <MarketingFooter />
  </BaseLayout>
);

// App layout extending base
const AppLayout = ({ children }) => (
  <BaseLayout>
    <AppHeader />
    <main>{children}</main>
  </BaseLayout>
);
```

### Slot-Based Layouts

```typescript
interface SlotLayoutProps {
  slots: {
    header?: React.ReactNode;
    sidebar?: React.ReactNode;
    main: React.ReactNode;
    footer?: React.ReactNode;
  };
}

const SlotLayout: React.FC<SlotLayoutProps> = ({ slots }) => (
  <div className={styles.layout}>
    {slots.header && <header>{slots.header}</header>}
    <div className={styles.body}>
      {slots.sidebar && <aside>{slots.sidebar}</aside>}
      <main>{slots.main}</main>
    </div>
    {slots.footer && <footer>{slots.footer}</footer>}
  </div>
);
```

## When to Use This Skill

- Creating page structure patterns
- Building reusable layout components
- Establishing consistent page architectures
- Setting up responsive frameworks
- Defining content slot patterns

## Related Skills

- `atomic-design-fundamentals` - Core methodology overview
- `atomic-design-organisms` - Building complex organisms
- `atomic-design-integration` - Framework-specific patterns
