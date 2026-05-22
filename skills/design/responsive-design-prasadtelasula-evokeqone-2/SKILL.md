---
name: responsive-design
description: Implement mobile-first responsive design with Tailwind CSS breakpoints for mobile, tablet, and desktop. Use when building responsive layouts or fixing layout issues.
allowed-tools: Read, Write, Edit, Glob
---

You implement responsive design for the QA Team Portal using Tailwind CSS mobile-first approach.

## Requirements from PROJECT_PLAN.md

- Responsive: Mobile, tablet, desktop support
- Mobile-first design approach
- Touch-friendly interface
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Responsive images and media
- Flexible layouts with CSS Grid and Flexbox

## Tailwind CSS Breakpoints

```
sm:  @media (min-width: 640px)   - Mobile landscape, small tablets
md:  @media (min-width: 768px)   - Tablets
lg:  @media (min-width: 1024px)  - Desktop
xl:  @media (min-width: 1280px)  - Large desktop
2xl: @media (min-width: 1536px)  - Extra large desktop
```

## Implementation

### 1. Mobile-First Layout Pattern

**Start with mobile styles, then add larger breakpoints:**

```typescript
// ❌ Wrong: Desktop-first approach
<div className="grid grid-cols-4 md:grid-cols-2 sm:grid-cols-1">

// ✅ Correct: Mobile-first approach
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
```

### 2. Responsive Navigation

**Location:** `frontend/src/components/Navigation.tsx`

```typescript
import { useState } from 'react'
import { Menu, X } from 'lucide-react'
import { Button } from '@/components/ui/button'

export const Navigation = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <img src="/logo.svg" alt="Evoke" className="h-8 w-8" />
            <span className="hidden sm:inline font-heading text-xl font-bold">
              QA Team Portal
            </span>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            <a href="#team" className="text-sm font-medium hover:text-primary transition-colors">
              Team
            </a>
            <a href="#updates" className="text-sm font-medium hover:text-primary transition-colors">
              Updates
            </a>
            <a href="#tools" className="text-sm font-medium hover:text-primary transition-colors">
              Tools
            </a>
            <a href="#resources" className="text-sm font-medium hover:text-primary transition-colors">
              Resources
            </a>
            <Button size="sm">Admin Portal</Button>
          </nav>

          {/* Mobile Menu Button */}
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </Button>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <nav className="md:hidden py-4 border-t border-border animate-slide-in">
            <div className="flex flex-col gap-4">
              <a
                href="#team"
                className="text-base font-medium hover:text-primary transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                Team
              </a>
              <a
                href="#updates"
                className="text-base font-medium hover:text-primary transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                Updates
              </a>
              <a
                href="#tools"
                className="text-base font-medium hover:text-primary transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                Tools
              </a>
              <a
                href="#resources"
                className="text-base font-medium hover:text-primary transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                Resources
              </a>
              <Button className="w-full">Admin Portal</Button>
            </div>
          </nav>
        )}
      </div>
    </header>
  )
}
```

### 3. Responsive Grid Layouts

**Team Members Grid:**

```typescript
// frontend/src/components/TeamGrid.tsx
export const TeamGrid = ({ members }: { members: TeamMember[] }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
      {members.map((member) => (
        <TeamCard key={member.id} member={member} />
      ))}
    </div>
  )
}
```

**Tools by Category:**

```typescript
// frontend/src/components/ToolsSection.tsx
export const ToolsSection = ({ tools }: { tools: Tool[] }) => {
  return (
    <div className="space-y-8">
      {Object.entries(toolsByCategory).map(([category, categoryTools]) => (
        <div key={category}>
          <h3 className="text-xl sm:text-2xl font-bold mb-4">{category}</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {categoryTools.map((tool) => (
              <ToolCard key={tool.id} tool={tool} />
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
```

### 4. Responsive Typography

```typescript
// frontend/src/components/Hero.tsx
export const Hero = () => {
  return (
    <section className="py-12 sm:py-16 md:py-20 lg:py-32">
      <div className="container mx-auto px-4">
        <div className="max-w-3xl mx-auto text-center">
          {/* Responsive heading sizes */}
          <h1 className="font-heading text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-balance mb-4 sm:mb-6">
            Welcome to Evoke QA Team
          </h1>

          {/* Responsive paragraph sizes */}
          <p className="text-base sm:text-lg md:text-xl text-muted-foreground text-balance mb-6 sm:mb-8">
            Building quality software through comprehensive testing and collaboration
          </p>

          {/* Responsive button sizes */}
          <Button size="default" className="w-full sm:w-auto">
            Get Started
          </Button>
        </div>
      </div>
    </section>
  )
}
```

### 5. Responsive Spacing

```typescript
// Use responsive padding, margin, gap
<div className="
  p-4 sm:p-6 lg:p-8           // Padding increases on larger screens
  mb-4 sm:mb-6 lg:mb-8        // Margin increases
  space-y-4 sm:space-y-6      // Gap between children increases
">
  <h2 className="text-2xl sm:text-3xl lg:text-4xl">Title</h2>
  <p className="text-sm sm:text-base lg:text-lg">Content</p>
</div>
```

### 6. Responsive Card Component

```typescript
// frontend/src/components/TeamCard.tsx
export const TeamCard = ({ member }: { member: TeamMember }) => {
  return (
    <Card className="group h-full flex flex-col">
      {/* Responsive image aspect ratio */}
      <div className="relative overflow-hidden rounded-t-lg aspect-square sm:aspect-[4/3] lg:aspect-square">
        <img
          src={member.photo_url}
          alt={member.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
      </div>

      <CardContent className="flex-1 p-4 sm:p-6">
        {/* Responsive text sizes */}
        <h3 className="font-heading text-lg sm:text-xl font-semibold mb-1">
          {member.name}
        </h3>
        <p className="text-sm sm:text-base text-primary-600 mb-2 sm:mb-3">
          {member.role}
        </p>

        {/* Hide bio on very small screens */}
        {member.bio && (
          <p className="hidden sm:block text-sm text-muted-foreground line-clamp-3">
            {member.bio}
          </p>
        )}
      </CardContent>
    </Card>
  )
}
```

### 7. Responsive Table

**Desktop: Full table, Mobile: Card layout:**

```typescript
// frontend/src/components/admin/TeamMembersTable.tsx
export const TeamMembersTable = ({ members }: { members: TeamMember[] }) => {
  return (
    <>
      {/* Desktop Table - hidden on mobile */}
      <div className="hidden md:block overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b">
              <th className="text-left p-4">Photo</th>
              <th className="text-left p-4">Name</th>
              <th className="text-left p-4">Role</th>
              <th className="text-left p-4">Email</th>
              <th className="text-right p-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            {members.map((member) => (
              <tr key={member.id} className="border-b">
                <td className="p-4">
                  <img src={member.photo_url} className="w-12 h-12 rounded-full" />
                </td>
                <td className="p-4">{member.name}</td>
                <td className="p-4">{member.role}</td>
                <td className="p-4">{member.email}</td>
                <td className="p-4 text-right">
                  <Button variant="ghost" size="sm">Edit</Button>
                  <Button variant="ghost" size="sm">Delete</Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile Card Layout - hidden on desktop */}
      <div className="md:hidden space-y-4">
        {members.map((member) => (
          <Card key={member.id}>
            <CardContent className="p-4">
              <div className="flex items-start gap-4">
                <img src={member.photo_url} className="w-16 h-16 rounded-full" />
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold truncate">{member.name}</h3>
                  <p className="text-sm text-muted-foreground">{member.role}</p>
                  <p className="text-sm text-muted-foreground truncate">{member.email}</p>
                </div>
              </div>
              <div className="flex gap-2 mt-4">
                <Button variant="outline" size="sm" className="flex-1">Edit</Button>
                <Button variant="outline" size="sm" className="flex-1">Delete</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </>
  )
}
```

### 8. Responsive Form Layout

```typescript
// frontend/src/components/admin/TeamMemberForm.tsx
export const TeamMemberForm = () => {
  return (
    <form className="space-y-6">
      {/* Single column on mobile, two columns on desktop */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
        <div className="space-y-2">
          <Label htmlFor="name">Name</Label>
          <Input id="name" />
        </div>

        <div className="space-y-2">
          <Label htmlFor="role">Role</Label>
          <Input id="role" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" />
        </div>

        <div className="space-y-2">
          <Label htmlFor="photo">Photo</Label>
          <Input id="photo" type="file" />
        </div>
      </div>

      {/* Full width */}
      <div className="space-y-2">
        <Label htmlFor="bio">Bio</Label>
        <Textarea id="bio" rows={4} />
      </div>

      {/* Responsive button layout */}
      <div className="flex flex-col sm:flex-row gap-3 sm:justify-end">
        <Button type="button" variant="outline" className="w-full sm:w-auto">
          Cancel
        </Button>
        <Button type="submit" className="w-full sm:w-auto">
          Save Changes
        </Button>
      </div>
    </form>
  )
}
```

### 9. Responsive Images

```typescript
// frontend/src/components/OptimizedImage.tsx
export const ResponsiveImage = ({ src, alt }: { src: string; alt: string }) => {
  return (
    <picture>
      {/* Mobile: 640w */}
      <source
        media="(max-width: 640px)"
        srcSet={`${src}?w=640 1x, ${src}?w=1280 2x`}
      />
      {/* Tablet: 1024w */}
      <source
        media="(max-width: 1024px)"
        srcSet={`${src}?w=1024 1x, ${src}?w=2048 2x`}
      />
      {/* Desktop: 1920w */}
      <source
        media="(min-width: 1025px)"
        srcSet={`${src}?w=1920 1x, ${src}?w=3840 2x`}
      />
      {/* Fallback */}
      <img
        src={src}
        alt={alt}
        loading="lazy"
        decoding="async"
        className="w-full h-auto"
      />
    </picture>
  )
}
```

### 10. Responsive Container

```typescript
// frontend/src/components/Container.tsx
export const Container = ({ children, className }: { children: React.ReactNode; className?: string }) => {
  return (
    <div className={cn(
      "mx-auto w-full",
      "px-4 sm:px-6 lg:px-8",          // Responsive horizontal padding
      "max-w-7xl",                      // Maximum width
      className
    )}>
      {children}
    </div>
  )
}
```

### 11. Touch-Friendly Targets

```typescript
// Ensure minimum 44x44px touch targets on mobile
<Button
  size="default"  // default is 40px height
  className="h-11 px-4 sm:h-10"  // 44px on mobile, 40px on desktop
>
  Click Me
</Button>

// Increase spacing between interactive elements
<div className="flex gap-3 sm:gap-2">
  <Button>Action 1</Button>
  <Button>Action 2</Button>
  <Button>Action 3</Button>
</div>
```

### 12. Responsive Sidebar Layout

```typescript
// frontend/src/layouts/AdminLayout.tsx
export const AdminLayout = ({ children }: { children: React.ReactNode }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="min-h-screen bg-background">
      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={cn(
        "fixed inset-y-0 left-0 z-50 w-64 bg-card border-r transform transition-transform",
        "lg:translate-x-0 lg:static",  // Always visible on desktop
        sidebarOpen ? "translate-x-0" : "-translate-x-full"  // Slide in/out on mobile
      )}>
        <nav className="p-4 space-y-2">
          <a href="/admin/dashboard" className="block px-4 py-2 rounded-lg hover:bg-accent">
            Dashboard
          </a>
          <a href="/admin/team-members" className="block px-4 py-2 rounded-lg hover:bg-accent">
            Team Members
          </a>
          <a href="/admin/tools" className="block px-4 py-2 rounded-lg hover:bg-accent">
            Tools
          </a>
        </nav>
      </aside>

      {/* Main Content */}
      <div className="lg:pl-64">
        {/* Header with mobile menu button */}
        <header className="sticky top-0 z-30 border-b bg-background px-4 sm:px-6 h-16 flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            className="lg:hidden"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="h-6 w-6" />
          </Button>
          <h1 className="text-xl font-bold">Admin Portal</h1>
        </header>

        {/* Page Content */}
        <main className="p-4 sm:p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  )
}
```

## Responsive Design Checklist

### Layout
- [ ] Mobile-first approach used (base styles for mobile, breakpoints for larger)
- [ ] Grid layouts adjust columns based on screen size
- [ ] Sidebar collapses on mobile with hamburger menu
- [ ] Containers use responsive padding (px-4 sm:px-6 lg:px-8)
- [ ] Max-width set for very large screens
- [ ] Flexbox direction changes on smaller screens (flex-col sm:flex-row)

### Typography
- [ ] Headings use responsive sizes (text-3xl sm:text-4xl lg:text-5xl)
- [ ] Body text readable on all devices (text-base sm:text-lg)
- [ ] Line height appropriate for small screens
- [ ] Text balance used for headings

### Navigation
- [ ] Desktop: Horizontal navigation bar
- [ ] Mobile: Hamburger menu with slide-out drawer
- [ ] Touch targets >= 44x44px on mobile
- [ ] Active state visible on all devices

### Images
- [ ] Responsive images with srcset
- [ ] Aspect ratios adjust for different screens
- [ ] Lazy loading enabled
- [ ] WebP format with fallback

### Forms
- [ ] Single column on mobile, multiple columns on desktop
- [ ] Labels above inputs on mobile
- [ ] Full-width buttons on mobile, auto-width on desktop
- [ ] Adequate spacing between form fields

### Tables
- [ ] Desktop: Full table
- [ ] Mobile: Card layout or horizontal scroll
- [ ] Important columns visible on small screens
- [ ] Sticky header on scroll (optional)

### Testing
- [ ] Tested on real devices (iOS, Android)
- [ ] Tested on different browsers (Chrome, Safari, Firefox)
- [ ] Tested all breakpoints (sm, md, lg, xl)
- [ ] Tested landscape and portrait orientations
- [ ] Touch interactions work smoothly
- [ ] No horizontal scrolling on any screen size

## Testing Responsive Design

**Chrome DevTools:**
```
1. Open DevTools (F12)
2. Click "Toggle device toolbar" (Ctrl+Shift+M)
3. Test different devices and screen sizes
4. Check both portrait and landscape
```

**Test Breakpoints:**
```typescript
// Add to development environment
const breakpoints = [
  { name: 'Mobile', width: 375, height: 667 },
  { name: 'Mobile L', width: 425, height: 667 },
  { name: 'Tablet', width: 768, height: 1024 },
  { name: 'Laptop', width: 1024, height: 768 },
  { name: 'Desktop', width: 1440, height: 900 },
]
```

**Playwright Responsive Tests:**
```python
# tests/e2e/test_responsive.py
def test_mobile_layout(page):
    page.set_viewport_size({'width': 375, 'height': 667})
    page.goto('http://localhost:5173')

    # Mobile menu should be visible
    assert page.locator('[data-testid="mobile-menu-button"]').is_visible()

    # Desktop menu should be hidden
    assert not page.locator('[data-testid="desktop-menu"]').is_visible()

def test_desktop_layout(page):
    page.set_viewport_size({'width': 1920, 'height': 1080})
    page.goto('http://localhost:5173')

    # Desktop menu should be visible
    assert page.locator('[data-testid="desktop-menu"]').is_visible()

    # Mobile menu button should be hidden
    assert not page.locator('[data-testid="mobile-menu-button"]').is_visible()
```

## Common Responsive Patterns

```typescript
// Hide/Show based on screen size
<div className="hidden md:block">Desktop only</div>
<div className="block md:hidden">Mobile only</div>

// Change layout direction
<div className="flex flex-col md:flex-row">...</div>

// Adjust gap/spacing
<div className="space-y-4 md:space-y-6 lg:space-y-8">...</div>
<div className="gap-3 md:gap-4 lg:gap-6">...</div>

// Full width on mobile, auto on desktop
<Button className="w-full md:w-auto">Click Me</Button>

// Responsive grid columns
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">...</div>

// Responsive font sizes
<h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl">Title</h1>

// Responsive padding
<div className="p-4 sm:p-6 md:p-8 lg:p-12">Content</div>
```

## Report

✅ Mobile-first approach implemented
✅ All breakpoints defined (sm, md, lg, xl)
✅ Responsive navigation with mobile menu
✅ Grid layouts adjust for different screens
✅ Typography scales responsively
✅ Forms optimized for mobile input
✅ Tables convert to cards on mobile
✅ Touch targets >= 44x44px
✅ Images responsive with srcset
✅ Tested on multiple devices and browsers
