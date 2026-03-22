---
name: figma-design
description: "Design collaborative UI/UX projects in Figma with real-time teamwork. Use for: interface design, component systems, Auto Layout, prototyping, design systems, team collaboration, developer handoff, and responsive design."
---

# Figma Design

Master collaborative UI/UX design in Figma, the cloud-based platform for real-time teamwork, prototyping, and developer handoff.

## Overview

Figma is a cloud-based design tool that revolutionizes UI/UX workflows through real-time collaboration, comprehensive design features, and seamless developer handoff. It's accessible via browser or desktop app, enabling teams to work together from anywhere.

## Core Features

### Real-Time Collaboration

**Multiplayer Editing**:
- Multiple users edit simultaneously
- See cursors and selections in real-time
- Live updates as changes happen
- No file versioning conflicts
- Single source of truth

**Commenting**:
- Add comments directly on designs
- Tag team members
- Resolve conversations
- Centralized feedback
- Context-preserved discussions

**Sharing**:
- Share links to files
- View-only or edit access
- Password protection
- Public or private sharing
- Embed in presentations

### Components and Variants

**Components**:
- Reusable UI elements
- Master component and instances
- Update all instances globally
- Override properties locally
- Nested components

**Variants**:
- Multiple states in one component
- Properties for different types
- Example: Button (Primary, Secondary, Disabled)
- Reduces component clutter
- Easier to manage

**Component Properties**:
- Boolean (show/hide elements)
- Text (editable content)
- Instance swap (change nested components)
- Variant selection
- Simplifies component usage

### Auto Layout

**Purpose**:
- Responsive, flexible layouts
- Automatic resizing
- Consistent spacing
- Handles content changes
- Essential for design systems

**How It Works**:
- Convert frame to Auto Layout
- Set direction (horizontal/vertical)
- Define spacing between items
- Set padding
- Configure resizing behavior

**Use Cases**:
- Buttons that adapt to text length
- Lists that grow with items
- Cards with variable content
- Navigation bars
- Form fields

### Styles

**Text Styles**:
- Define typography
- Font, size, weight, line height
- Apply globally
- Update all instances
- Maintain consistency

**Color Styles**:
- Define color palette
- Apply to fills, strokes, effects
- Update globally
- Organize by category
- Support themes

**Effect Styles**:
- Shadows and blurs
- Reusable effects
- Consistent depth and elevation
- Update globally

**Grid Styles**:
- Layout grids
- Column grids
- Baseline grids
- Reusable across frames

## Design Workflow

### Setting Up Files

**File Structure**:
- Pages for organization
- Sections within pages
- Frames for artboards
- Groups and layers
- Clear naming conventions

**Organization Best Practices**:
- Separate pages: Explorations, Final Designs, Components, Archive
- Use frames for each screen
- Group related elements
- Name layers descriptively
- Use emoji for quick identification

### Designing Interfaces

**Frame Tool**:
- Create artboards
- Preset sizes (iPhone, Desktop, etc.)
- Custom dimensions
- Nested frames
- Clip content option

**Shape Tools**:
- Rectangle, ellipse, polygon, star, line
- Boolean operations (union, subtract, intersect)
- Vector editing
- Pen tool for custom shapes

**Text Tool**:
- Add text layers
- Apply text styles
- Auto width, height, or fixed
- OpenType features
- Variable fonts support

**Images**:
- Drag and drop
- Fill frames
- Crop and adjust
- Masks
- Image effects

### Building Components

**Creating Components**:
1. Design element
2. Select and create component (Ctrl/Cmd+Alt+K)
3. Name descriptively
4. Organize in component page
5. Publish to library

**Component Best Practices**:
- Atomic design principles
- Descriptive naming (Button/Primary/Large)
- Use Auto Layout
- Define variants
- Document usage

**Team Libraries**:
- Publish components
- Share across files
- Update propagates to all instances
- Version control
- Team-wide consistency

## Prototyping

### Creating Prototypes

**Connections**:
- Link frames with hotspots
- Define trigger (click, hover, etc.)
- Set destination frame
- Choose transition
- Configure animation

**Interactions**:
- On click
- On hover
- On press
- On drag
- While hovering
- Mouse enter/leave
- After delay

**Transitions**:
- Instant
- Dissolve
- Smart Animate
- Move in/out
- Push
- Slide in/out
- Custom easing

### Smart Animate

**Purpose**:
- Automatic animations between frames
- Matches layers by name
- Animates position, size, rotation, opacity
- Creates fluid transitions

**How to Use**:
1. Duplicate frame
2. Modify elements (move, resize, etc.)
3. Keep layer names identical
4. Set transition to Smart Animate
5. Preview animation

**Use Cases**:
- Button state changes
- Menu expansions
- Card flips
- Progress indicators
- Morphing shapes

### Interactive Components

**Purpose**:
- Components with built-in interactions
- Hover states
- Click states
- No need for multiple frames

**Creating**:
1. Create component with variants
2. Switch to Prototype tab
3. Connect variants with interactions
4. Define triggers and transitions
5. Use component in designs

**Benefits**:
- Reusable interactions
- Consistent behavior
- Easier maintenance
- Faster prototyping

## Design Systems

### Building Design Systems

**Foundation**:
- Color palette
- Typography scale
- Spacing system
- Grid system
- Iconography

**Components**:
- Atoms: Buttons, inputs, icons
- Molecules: Form fields, cards
- Organisms: Headers, footers, forms
- Templates: Page layouts

**Documentation**:
- Component descriptions
- Usage guidelines
- Do's and don'ts
- Code snippets
- Accessibility notes

### Managing Design Systems

**Team Libraries**:
- Publish design system file
- Enable as library
- Team members use components
- Updates notify all users
- Accept or ignore updates

**Versioning**:
- Figma tracks changes
- Version history
- Restore previous versions
- Branch for experiments
- Merge changes

## Developer Handoff

### Dev Mode

**Purpose**:
- Dedicated workspace for developers
- Inspect designs
- Copy code
- Export assets
- Specifications

**Features**:
- Measurements and spacing
- CSS, iOS, Android code
- Asset export
- Component properties
- Responsive behavior

**Workflow**:
1. Designer shares file
2. Developer opens in Dev Mode
3. Inspect elements
4. Copy code snippets
5. Export assets
6. Implement design

### Inspect Panel

**Information Provided**:
- Dimensions and position
- Colors (hex, RGB, HSL)
- Typography (font, size, weight)
- Effects (shadows, blurs)
- Spacing between elements
- Border radius, opacity

**Code Export**:
- CSS
- iOS (Swift)
- Android (XML)
- Copy to clipboard
- Implement in code

### Asset Export

**Export Settings**:
- Format (PNG, JPG, SVG, PDF)
- Scale (1x, 2x, 3x)
- Suffix naming
- Batch export
- Export presets

**Best Practices**:
- Use SVG for icons
- PNG for images with transparency
- JPG for photos
- Multiple scales for different devices
- Organize exports

## Collaboration Features

### Comments and Feedback

**Adding Comments**:
- Click to add comment
- Tag team members (@mention)
- Attach to specific elements
- Threaded conversations
- Resolve when addressed

**Review Process**:
- Share link for review
- Stakeholders add comments
- Designer addresses feedback
- Mark comments as resolved
- Iterate and update

### Permissions and Sharing

**Access Levels**:
- Can view: Read-only
- Can edit: Full editing
- Owner: Manage permissions
- Team/organization access

**Sharing Options**:
- Anyone with link
- Specific people
- Password protection
- Expiring links
- Embed in websites

## Plugins and Integrations

### Popular Plugins

**Content**:
- Unsplash: Free stock photos
- Content Reel: Realistic data
- Iconify: Icon libraries

**Productivity**:
- Autoflow: User flow diagrams
- Stark: Accessibility checker
- Remove BG: Background removal

**Design**:
- Blush: Illustrations
- Noise & Texture: Add grain
- Arc: Curved text

### Using Plugins

**Installation**:
- Plugins menu > Browse
- Search and install
- Run from Plugins menu
- Keyboard shortcuts

**Custom Plugins**:
- Figma API
- JavaScript/TypeScript
- Automate tasks
- Extend functionality

## Best Practices

### File Organization

**Naming Conventions**:
- Descriptive names
- Consistent format
- Version numbers
- Date stamps
- Project prefixes

**Layer Organization**:
- Group related elements
- Use frames for sections
- Lock background elements
- Hide unused layers
- Delete unused elements

### Performance Optimization

**Keep Files Fast**:
- Limit components per file
- Optimize images
- Simplify complex vectors
- Remove unused styles
- Archive old versions

**Component Management**:
- Separate component library
- Publish only finalized components
- Regular cleanup
- Document changes

### Design Consistency

**Use Styles and Components**:
- Define styles early
- Create components for repeated elements
- Use team libraries
- Update globally
- Maintain design system

**Grid and Layout**:
- Consistent grid system
- Align to grid
- Use Auto Layout
- Responsive design
- Test different sizes

## Conclusion

Figma transforms UI/UX design through real-time collaboration, powerful components, and seamless handoff. Master its features, build robust design systems, and leverage collaboration to create exceptional digital products efficiently.
