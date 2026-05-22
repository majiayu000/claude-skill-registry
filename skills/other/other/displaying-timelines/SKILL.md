---
name: displaying-timelines
description: Displays chronological events and activity through timelines, activity feeds, Gantt charts, and calendar interfaces. Use when showing historical events, project schedules, social feeds, notifications, audit logs, or time-based data. Provides implementation patterns for vertical/horizontal timelines, interactive visualizations, real-time updates, and responsive designs with accessibility (WCAG/ARIA).
---

# Displaying Timelines & Activity Components

## Purpose

This skill enables systematic creation of timeline and activity components, from simple vertical timelines to complex interactive Gantt charts. It provides clear decision frameworks based on use case and data characteristics, ensuring optimal performance, real-time updates, and accessible implementations.

## When to Use

Activate this skill when:
- Creating activity feeds (social, notifications, audit logs)
- Displaying timelines (vertical, horizontal, interactive)
- Building Gantt charts or project schedules
- Implementing calendar interfaces (month, week, day views)
- Showing chronological events or historical data
- Handling real-time activity updates
- Requiring timestamp formatting (relative, absolute)
- Ensuring timeline accessibility or responsive behavior

## Quick Decision Framework

Select component type based on use case:

```
Social Activity        → Activity Feed (infinite scroll, reactions)
System Events          → Audit Log (searchable, exportable, precise timestamps)
User Notifications     → Notification Feed (read/unread, grouped by date)
Historical Events      → Vertical Timeline (milestones, alternating sides)
Project Planning       → Gantt Chart (dependencies, drag-to-reschedule)
Scheduling             → Calendar Interface (month/week/day views)
Interactive Roadmap    → Horizontal Timeline (zoom, pan, filter)
```

For detailed selection criteria, reference `references/component-selection.md`.

## Core Implementation Patterns

### Activity Feeds

**Social Feed Pattern:**
- User avatar + name + action description
- Relative timestamps ("2 hours ago")
- Reactions and comments
- Infinite scroll with pagination
- Real-time updates via WebSocket
- Reference `references/activity-feeds.md`

**Notification Feed Pattern:**
- Grouped by date sections
- Read/unread states with indicators
- Mark all as read functionality
- Filter by notification type
- Action buttons (view, dismiss)
- Reference `references/notification-feeds.md`

**Audit Log Pattern:**
- System events with precise timestamps
- User action tracking
- Searchable with advanced filters
- Exportable (CSV, JSON)
- Security-focused display
- Reference `references/audit-logs.md`

Example: `examples/social-activity-feed.tsx`

### Timeline Visualizations

**Vertical Timeline:**
- Events stacked chronologically
- Connecting line with marker dots
- Date markers and event cards
- Optional alternating sides
- Best for: Historical events, project milestones
- Reference `references/vertical-timelines.md`

**Horizontal Timeline:**
- Events along horizontal axis
- Scroll or zoom to navigate
- Density varies by zoom level
- Best for: Project timelines, roadmaps
- Reference `references/horizontal-timelines.md`

**Interactive Timeline:**
- Click events for detail view
- Filter by category/type
- Zoom in/out controls
- Pan and scroll navigation
- Best for: Data exploration, rich interactivity
- Reference `references/interactive-timelines.md`

Example: `examples/milestone-timeline.tsx`

### Gantt Charts

**Project Planning Features:**
- Tasks as horizontal bars
- Dependencies with arrows
- Critical path highlighting
- Drag to reschedule
- Progress indicators
- Milestone markers (diamonds)
- Resource allocation
- Today marker line
- Zoom levels (day/week/month/year)

To generate Gantt chart data:
```bash
python scripts/generate_gantt_data.py --tasks 50 --dependencies auto
```

Reference `references/gantt-patterns.md` for implementation details.

Example: `examples/project-gantt.tsx`

### Calendar Interfaces

**Month View:**
- Traditional calendar grid
- Events in date cells
- Click to create/edit
- Color-coded categories
- Multi-calendar overlay

**Week View:**
- Time slots (hourly)
- Events as draggable blocks
- Resize to change duration
- Multiple calendars overlay

**Day/Agenda View:**
- Detailed daily schedule
- List format with time duration
- Location and attendees
- Scrollable timeline

Reference `references/calendar-patterns.md` for all views.

Example: `examples/calendar-scheduler.tsx`

## Timestamp Formatting

Essential timestamp patterns:

**Relative (Recent Events):**
- "Just now" (<1 min)
- "5 minutes ago"
- "3 hours ago"
- "Yesterday at 3:42 PM"

**Absolute (Older Events):**
- "Jan 15, 2025"
- "January 15, 2025 at 3:42 PM"
- ISO 8601 for APIs

**Implementation Considerations:**
- Timezone handling (display user's local time)
- Locale-aware formatting
- Hover for precise timestamp
- Auto-update relative times

To format timestamps consistently:
```bash
node scripts/format_timestamps.js --locale en-US --timezone auto
```

Reference `references/timestamp-formatting.md` for complete patterns.

## Real-Time Updates

**Live Activity Feed:**
- WebSocket or SSE for new events
- Smooth insertion animation
- "X new items" notification banner
- Click to load new items
- Optimistic updates for user actions

**Implementation Pattern:**
1. Show user action immediately
2. Update timestamp to "Just now"
3. Send to server in background
4. Rollback if error occurs

Reference `references/real-time-updates.md` for WebSocket patterns.

Example: `examples/realtime-activity.tsx`

## Performance Optimization

Critical performance thresholds:

```
<100 events       → Client-side rendering, no virtualization
100-1,000 events  → Virtual scrolling recommended
1,000+ events     → Virtual scrolling + server pagination
Real-time         → Debounce updates, batch insertions
```

**Optimization Strategies:**
- Memoize timeline item components
- Lazy load event details
- Virtual scrolling for long timelines
- Debounce real-time updates (batch every 500ms)
- Optimize timestamp calculations

To benchmark performance:
```bash
node scripts/benchmark_timeline.js --events 10000
```

Reference `references/performance-optimization.md` for details.

## Accessibility Requirements

Essential WCAG compliance:

**Semantic HTML:**
- Use `<ol>` or `<ul>` for timelines
- Proper heading hierarchy
- Semantic time elements

**ARIA Patterns:**
- `role="feed"` for activity feeds
- `role="article"` for timeline items
- `aria-label` for timestamps
- `aria-busy` during loading

**Keyboard Navigation:**
- Tab through interactive items
- Arrow keys for timeline navigation
- Enter/Space to expand items
- Skip to latest/oldest controls

**Screen Reader Support:**
- Announce new items in feeds
- Descriptive timestamp labels
- Progress updates for Gantt charts

To validate accessibility:
```bash
node scripts/validate_timeline_accessibility.js
```

Reference `references/accessibility-patterns.md` for complete requirements.

## Responsive Design

Three proven strategies:

**1. Stack Vertically (Mobile)**
- Convert horizontal to vertical
- Maintain chronological order
- Adjust spacing and font sizes

**2. Simplify Display**
- Show essential info only
- Expand for details
- Reduce visual complexity

**3. Horizontal Scroll**
- Keep layout intact
- Enable touch scrolling
- Add scroll indicators

Reference `references/responsive-strategies.md` for implementations.

Example: `examples/responsive-timeline.tsx`

## Library Recommendations

### Timeline: react-chrono (Flexible)

Best for timeline visualizations with rich content:
- Horizontal, vertical, alternating layouts
- Image and video support
- Custom item rendering
- TypeScript support
- Responsive out of the box

```bash
npm install react-chrono
```

See `examples/react-chrono-timeline.tsx` for setup.

**Alternative: react-vertical-timeline-component**
- Simple, clean vertical timelines
- Lightweight (~10KB)
- Icon support
- Good for basic timelines

### Gantt Charts: SVAR React Gantt

Best for project management:
- Modern, dependency-free
- Drag-and-drop tasks
- Dependencies and milestones
- Customizable appearance
- TypeScript ready

```bash
npm install @svar/gantt
```

**Enterprise Alternative: Bryntum Gantt**
- Feature-complete solution
- Commercial license required
- Handles complex projects
- Advanced resource management

### Calendar: react-big-calendar

Best for scheduling interfaces:
- Month, week, day, agenda views
- Drag-and-drop events
- Customizable styling
- Large community support

```bash
npm install react-big-calendar
```

**Alternative: FullCalendar**
- Premium features available
- Excellent documentation
- Multiple framework support

For detailed comparison, reference `references/library-comparison.md`.

## Design Token Integration

Timelines use the design-tokens skill for consistent theming:

**Timeline-Specific Tokens:**
- `--timeline-line-color` - Connecting line color
- `--timeline-dot-color` - Event marker color
- `--timeline-dot-active-color` - Current/active event
- `--event-card-bg` - Event card background
- `--timestamp-color` - Timestamp text

**Standard Token Categories:**
- Color tokens for backgrounds and states
- Spacing tokens for gaps and padding
- Typography tokens for text hierarchy
- Shadow tokens for card elevation
- Motion tokens for animations

Supports light, dark, high-contrast, and custom themes.
Reference the design-tokens skill for theme switching.

## Working Examples

Start with the example matching the requirements:

```
social-activity-feed.tsx       # Social feed with reactions
notification-center.tsx        # Notification system with filters
audit-log-viewer.tsx           # System audit log
milestone-timeline.tsx         # Vertical timeline with milestones
project-gantt.tsx              # Gantt chart with dependencies
calendar-scheduler.tsx         # Full calendar with all views
realtime-activity.tsx          # Live updates via WebSocket
responsive-timeline.tsx        # Mobile-optimized timeline
```

## Testing Tools

Generate mock timeline data:
```bash
python scripts/generate_timeline_data.py --events 500 --realtime
```

Test real-time updates:
```bash
node scripts/simulate_realtime.js --rate 5/sec --duration 60s
```

Validate accessibility:
```bash
node scripts/validate_timeline_accessibility.js
```

Benchmark performance:
```bash
node scripts/benchmark_timeline.js --events 10000 --virtual
```

## Next Steps

1. Identify the timeline use case (activity, events, schedule)
2. Select the appropriate component type
3. Choose a library or build custom with tokens
4. Start with the matching example file
5. Implement core functionality
6. Add real-time updates if needed
7. Test performance with large datasets
8. Validate accessibility compliance
9. Apply responsive strategy for mobile
