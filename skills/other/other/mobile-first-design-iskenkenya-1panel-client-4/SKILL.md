---
name: mobile-first-design
description: Design for mobile devices first, then scale up to larger screens. Create responsive interfaces that work seamlessly across all device sizes.
---

# Mobile-First Design

## Overview

Mobile-first design prioritizes small screens as the starting point, ensuring core functionality works on all devices while leveraging larger screens for enhanced experience.

## When to Use

- Web application design
- Responsive website creation
- Feature prioritization
- Performance optimization
- Progressive enhancement
- Cross-device experience design

## Instructions

### 1. **Mobile-First Principles**

```yaml
Mobile-First Approach:

Step 1: Design for Mobile (320px - 480px)
  - Constrained space forces priorities
  - Focus on essential content and actions
  - Single column layout
  - Touch-friendly interactive elements

Step 2: Enhance for Tablet (768px - 1024px)
  - Add secondary content
  - Multi-column layouts possible
  - Optimize spacing and readability
  - Take advantage of hover states

Step 3: Optimize for Desktop (1200px+)
  - Full-featured experience
  - Advanced layouts
  - Rich interactions
  - Multiple columns and sidebars

---

## Responsive Breakpoints:

Mobile: 320px - 480px
  - iPhone SE, older phones
  - Strict space constraints
  - Touch-only interaction

Tablet: 481px - 768px
  - iPad mini, tablets
  - More space available
  - Touch + keyboard/mouse

Large Tablet/Small Desktop: 769px - 1024px
  - iPad Pro, small laptops
  - Transitional breakpoint
  - Both touch and pointer

Desktop: 1025px - 1440px
  - Standard laptops
  - Full feature set
  - Hover states enabled

Large Desktop: 1441px+
  - Ultrawide monitors
  - Consider max-width container
  - Avoid stretching too wide

---

## Mobile Design Patterns:

Navigation:
  Mobile: Hamburger menu, bottom tabs
  Tablet: Side drawer
  Desktop: Horizontal menu bar

Forms:
  Mobile: Single column, large touch targets (48px)
  Tablet: 2 columns if space allows
  Desktop: Multi-column, side-by-side labels

Content Layout:
  Mobile: Full width, single column
  Tablet: 1-2 columns
  Desktop: Multi-column, sidebar

Images:
  Mobile: Full width
  Tablet: Full or constrained width
  Desktop: Constrained width, may use columns
```

### 2. **Responsive Design Implementation**

```python
# Implement responsive CSS and layouts

class ResponsiveDesign:
    def create_responsive_grid(self, mobile_cols=1):
        """CSS Grid responsive structure"""
        return {
            'mobile': {
                'columns': 1,
                'gap': '16px',
                'breakpoint': 'max-width: 480px'
            },
            'tablet': {
                'columns': 2,
                'gap': '24px',
                'breakpoint': '481px - 768px'
            },
            'desktop': {
                'columns': 3,
                'gap': '32px',
                'breakpoint': 'min-width: 769px'
            }
        }

    def responsive_typography(self):
        """Fluid font sizes"""
        return {
            'h1': {
                'mobile': '24px',
                'tablet': '32px',
                'desktop': '48px',
                'line_height': {
                    'mobile': '1.2',
                    'desktop': '1.3'
                }
            },
            'body': {
                'mobile': '14px',
                'tablet': '16px',
                'desktop': '16px',
                'line_height': '1.6'
            }
        }

    def responsive_spacing(self):
        """Adaptive padding and margins"""
        return {
            'container_padding': {
                'mobile': '16px',
                'tablet': '24px',
                'desktop': '32px'
            },
            'section_margin': {
                'mobile': '24px',
                'desktop': '48px'
            },
            'touch_target_size': '44px minimum (Apple)'
        }

    def touch_friendly_design(self):
        """Mobile interaction optimization"""
        return {
            'button_size': '44px x 44px minimum',
            'touch_target_spacing': '8px minimum between',
            'form_input_height': '44px + 16px padding',
            'scrolling_area': 'Full width swipe friendly',
            'modal_height': 'Max 85vh, scrollable',
            'keyboard_awareness': 'Account for software keyboard'
        }
```

### 3. **Mobile Performance**

```yaml
Mobile Performance Optimization:

Image Optimization:
  - Responsive images (srcset, picture element)
  - WebP format with fallback
  - Lazy loading for below-fold
  - Compress ruthlessly
  - Serve appropriately sized images

Metric Goals:
  - Mobile: <3 second First Contentful Paint
  - Mobile: <4 second Largest Contentful Paint
  - Mobile: < 100 Cumulative Layout Shift

Bundle Size:
  - Mobile: <100KB JavaScript (gzipped)
  - Mobile: <50KB CSS (gzipped)
  - Critical CSS inline

Network:
  - Minimize requests (combine files)
  - Enable gzip compression
  - Use CDN for assets
  - Cache aggressively

---

Testing Devices:

Physical Devices:
  - iPhone SE (320px baseline)
  - iPhone 13 Pro (390px)
  - Samsung S21 (360px)
  - iPad (768px)

Emulation:
  - Chrome DevTools device mode
  - Responsive design mode
  - Test orientation changes

Real Device Testing:
  - Test on actual devices
  - Check touch interactions
  - Verify performance
  - Test with slow network
```

### 4. **Progressive Enhancement**

```yaml
Progressive Enhancement Strategy:

Layer 1: Core Content (HTML)
  - Semantic HTML
  - Works without CSS or JavaScript
  - Text content readable
  - Forms functional

Layer 2: Enhanced (CSS)
  - Visual design
  - Layout and spacing
  - Colors and typography
  - Responsive design

Layer 3: Interactive (JavaScript)
  - Progressive loading
  - Form enhancements
  - Smooth interactions
  - Offline functionality
  - Push notifications

Fallback Approach:
  - Input: range slider → Text input fallback
  - Video: HTML5 video → Link to download
  - Map: Interactive map → Static image link
  - Single-page app → Server-side rendering

---

Testing Strategy:

1. Disable JavaScript
   - Core content still accessible
   - Forms still submit
   - Links work

2. Slow 3G Network
   - Page loads
   - Critical content visible
   - Non-critical lazy loads

3. No Styles (CSS disabled)
   - Content readable
   - Text size appropriate
   - Contrast sufficient
```

## Best Practices

### ✅ DO
- Design for smallest screen first
- Test on real mobile devices
- Use responsive images
- Optimize for mobile performance
- Make touch targets 44x44px minimum
- Stack content vertically on mobile
- Use hamburger menu on mobile
- Hide non-essential content on mobile
- Test with slow networks
- Progressive enhancement approach

### ❌ DON'T
- Assume all mobile users have fast networks
- Use desktop-only patterns on mobile
- Ignore touch interaction needs
- Make buttons too small
- Forget about landscape orientation
- Over-complicate mobile layout
- Ignore mobile performance
- Assume no keyboard (iPad users)
- Skip mobile user testing
- Forget about notches and safe areas

## Mobile-First Design Tips

- Use max-width containers (max 1200px typical)
- Test on oldest iPhone SE (320px) for baseline
- Implement touch-friendly spacing (48px minimum)
- Use flexible layouts over fixed widths
- Test with slow 3G network simulation
