---
name: browser-app-creator
description: Creates complete single-file HTML/CSS/JS web apps with localStorage persistence, ADHD-optimized UI (60px+ buttons), dark mode, and offline functionality. Use when user says "create app", "build tool", "make dashboard", or requests any browser-based interface.
priority: HIGH
conflicts_with: [rapid-prototyper]
use_when:
  - User wants a COMPLETE, POLISHED web application
  - User wants ADHD optimization (60px+ buttons, auto-save, dark mode)
  - User wants something that WORKS OFFLINE
  - User wants a DOWNLOADABLE single HTML file
  - User says "app", "tool", "dashboard", "tracker"
avoid_when:
  - User wants QUICK PROTOTYPE only
  - User says "simple", "basic", "test idea"
---

# Browser App Creator

## Purpose

Creates production-ready single-file web applications that work offline with zero setup. Perfect for quick tools, dashboards, trackers, and prototypes.

**For ADHD users**: Large buttons (60px+), auto-save everything, visual feedback, zero configuration.
**For SDAM users**: All data persists in localStorage with timestamps.
**For all users**: Download and use immediately - no server, no build step, no dependencies.

## Activation Triggers

- User says: "create app", "build tool", "make dashboard", "create tracker"
- Requests for: habit tracker, todo list, timer, calculator, form, visualization
- Any request for a browser-based interface or tool

## Core Workflow

### 1. Understand Requirements

Ask clarifying questions only if absolutely necessary:

```javascript
{
  app_type: "dashboard|tracker|form|tool|visualization",
  primary_function: "What does the app do?",
  data_to_track: ["What data needs to be stored?"],
  key_actions: ["What can users do?"],
  visual_requirements: "Any specific layout needs?"
}
```

### 2. Generate Single-File App

**Template structure**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{App Name}</title>
  <style>
    /* ADHD-Optimized Styles */
  </style>
</head>
<body>
  <!-- App UI -->
  <script>
    // App Logic + localStorage
  </script>
</body>
</html>
```

### 3. ADHD Optimization Requirements

**Required UI elements**:
- ✅ **Buttons**: Minimum 60px height, high contrast
- ✅ **Dark mode**: Default theme (can toggle)
- ✅ **Auto-save**: Every action saves to localStorage
- ✅ **Visual feedback**: Success/error messages
- ✅ **Mobile responsive**: Works on all screen sizes
- ✅ **Large touch targets**: 44px minimum for mobile

**CSS Requirements**:
```css
/* ADHD-Optimized Base Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #1a1a1a;
  color: #e0e0e0;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

button {
  min-height: 60px;
  padding: 15px 30px;
  font-size: 18px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #4a9eff;
  color: white;
}

button:hover {
  background: #357abd;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 158, 255, 0.4);
}

button:active {
  transform: translateY(0);
}

input, textarea, select {
  min-height: 50px;
  padding: 12px 15px;
  font-size: 16px;
  border: 2px solid #333;
  border-radius: 6px;
  background: #2a2a2a;
  color: #e0e0e0;
  width: 100%;
}

input:focus, textarea:focus, select:focus {
  outline: none;
  border-color: #4a9eff;
  box-shadow: 0 0 0 3px rgba(74, 158, 255, 0.2);
}
```

### 4. localStorage Pattern

**Always include**:
```javascript
// localStorage Manager
const Storage = {
  key: 'app-name-data',

  save(data) {
    try {
      localStorage.setItem(this.key, JSON.stringify({
        ...data,
        lastUpdated: new Date().toISOString()
      }));
      this.showFeedback('✅ Saved!');
    } catch (error) {
      this.showFeedback('❌ Save failed', true);
      console.error('Save error:', error);
    }
  },

  load() {
    try {
      const data = localStorage.getItem(this.key);
      return data ? JSON.parse(data) : this.getDefaults();
    } catch (error) {
      console.error('Load error:', error);
      return this.getDefaults();
    }
  },

  getDefaults() {
    return {
      items: [],
      settings: {},
      created: new Date().toISOString()
    };
  },

  showFeedback(message, isError = false) {
    const feedback = document.createElement('div');
    feedback.textContent = message;
    feedback.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 15px 25px;
      background: ${isError ? '#ff4444' : '#44ff88'};
      color: #000;
      border-radius: 8px;
      font-weight: 600;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      z-index: 1000;
      animation: slideIn 0.3s ease;
    `;
    document.body.appendChild(feedback);
    setTimeout(() => feedback.remove(), 2000);
  }
};

// Auto-save on any change
function autoSave(data) {
  Storage.save(data);
}

// Load on page load
let appData = Storage.load();
```

### 5. App Templates

See [templates.md](templates.md) for complete examples of:
- **Dashboard**: Metrics, charts, status indicators
- **Tracker**: Habits, tasks, progress
- **Form**: Data entry, validation, submission
- **Tool**: Calculators, converters, utilities
- **Visualization**: Charts, graphs, timelines

### 6. Deliver the App

**Format**:
```
✅ **{App Name}** complete!

**Features**:
- {Feature 1}
- {Feature 2}
- {Feature 3}

**Usage**:
1. Save the file as `{app-name}.html`
2. Open in any browser
3. Works offline
4. Data auto-saves to your browser

**Customization**:
- Colors: Edit the CSS variables at the top
- Features: Modify the JavaScript section
- Layout: Adjust the HTML structure
```

Then provide the complete HTML file.

## Common App Types

### Dashboard
**Purpose**: Display metrics, status, and key information
**Elements**: Cards, charts, progress bars, status indicators
**Data**: Real-time or static metrics
**Example**: Project status dashboard, analytics viewer

### Tracker
**Purpose**: Record and monitor recurring items
**Elements**: Add/remove items, checkboxes, timestamps
**Data**: List of items with status and dates
**Example**: Habit tracker, task list, mood journal

### Form/Input
**Purpose**: Collect and validate user input
**Elements**: Input fields, validation, submit button
**Data**: Form submissions with timestamps
**Example**: Survey, calculator, data entry tool

### Visualization
**Purpose**: Display data visually
**Elements**: Charts, graphs, timelines
**Data**: Visual representation of datasets
**Example**: Chart builder, timeline viewer, graph tool

### Interactive Tool
**Purpose**: Perform specific tasks or calculations
**Elements**: Controls, real-time updates, results
**Data**: Temporary or persistent tool state
**Example**: Timer, converter, game, simulator

## Advanced Features

### Dark/Light Mode Toggle
```javascript
function toggleTheme() {
  const currentTheme = document.body.dataset.theme || 'dark';
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.body.dataset.theme = newTheme;
  localStorage.setItem('theme-preference', newTheme);
}

// Load saved theme
document.body.dataset.theme = localStorage.getItem('theme-preference') || 'dark';
```

### Export Data
```javascript
function exportData() {
  const data = Storage.load();
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `app-data-${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
}
```

### Import Data
```javascript
function importData() {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'application/json';
  input.onchange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const data = JSON.parse(event.target.result);
        Storage.save(data);
        location.reload();
      } catch (error) {
        alert('Invalid file format');
      }
    };
    reader.readAsText(file);
  };
  input.click();
}
```

### Browser Notifications
```javascript
async function notifyUser(title, body) {
  if ('Notification' in window && Notification.permission === 'granted') {
    new Notification(title, { body });
  } else if (Notification.permission !== 'denied') {
    const permission = await Notification.requestPermission();
    if (permission === 'granted') {
      new Notification(title, { body });
    }
  }
}
```

## Styling Guidelines

See [styling.md](styling.md) for:
- Complete CSS framework
- Color schemes
- Responsive breakpoints
- Animation patterns
- Accessibility guidelines

## Integration with Other Skills

### Rapid Prototyper
If app needs backend:
```
browser-app-creator → Creates frontend
rapid-prototyper → Creates backend API
Result: Full-stack app
```

### Context Manager
Save app decisions:
```
remember: Created habit tracker with localStorage
Type: PROCEDURE
Tags: browser-app, localStorage, tracking
```

### Error Debugger
If app has bugs:
```
Automatically invokes error-debugger for:
- JavaScript errors
- localStorage issues
- Browser compatibility
```

## Quality Checklist

Before delivering, verify:
- ✅ Single file (HTML + CSS + JS)
- ✅ Works offline (no external dependencies)
- ✅ Buttons ≥60px height
- ✅ Dark mode default
- ✅ localStorage auto-save
- ✅ Visual feedback on actions
- ✅ Mobile responsive
- ✅ No console errors
- ✅ Data persists on reload

## Example Output

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Habit Tracker</title>
  <style>
    /* Complete styles here */
  </style>
</head>
<body>
  <h1>Habit Tracker</h1>
  <div id="app">
    <!-- App UI here -->
  </div>
  <script>
    // Complete logic here
  </script>
</body>
</html>
```

## Success Criteria

✅ App works immediately after opening
✅ Data persists across browser sessions
✅ ADHD-optimized (large buttons, auto-save)
✅ No setup or installation required
✅ Mobile-friendly
✅ Professional appearance
✅ Intuitive to use
✅ Handles errors gracefully

## Additional Resources

- **[App Templates](templates.md)** - Complete working examples
- **[Styling Guide](styling.md)** - CSS patterns and color schemes

## Quick Reference

### Trigger Phrases
- "create app"
- "build tool"
- "make dashboard"
- "create tracker"
- "build calculator"
- "make timer"

### File Location
All created apps should be saved to:
- Linux/macOS: `~/.claude-artifacts/`
- Windows: `%USERPROFILE%\.claude-artifacts\`

### Common Patterns
| App Type | Key Feature | localStorage Structure |
|----------|-------------|----------------------|
| Tracker | List + checkboxes | `{ items: [...], dates: {...} }` |
| Dashboard | Cards + metrics | `{ metrics: {...}, updated: "" }` |
| Form | Input + validation | `{ submissions: [...] }` |
| Tool | Controls + results | `{ settings: {...}, history: [...] }` |
