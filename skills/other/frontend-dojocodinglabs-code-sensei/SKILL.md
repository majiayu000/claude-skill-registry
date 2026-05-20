---
name: frontend
description: >
  React, components, state management, and modern frontend concepts. Activated when Claude
  works with .jsx/.tsx files or React-related code. Most vibecoded apps use React.
---

# Frontend Development — CodeSensei Teaching Module

## React
- **Analogy:** React lets you build a webpage out of LEGO bricks. Each brick (component) is a self-contained piece that knows how to display itself. You snap them together to build the full page.
- **Key insight:** Instead of one giant HTML file, React breaks the page into small, reusable pieces. A "Navbar" component, a "Card" component, a "Button" component — each one independent.

## Components
- **Analogy:** A component is like a custom sticker. You design it once (define the component), then stick it anywhere on the page as many times as you want.
- **Teaching flow:**
  1. A component is a function that returns HTML-like code (JSX)
  2. Components can receive data through "props" (like settings or configuration)
  3. Components can have their own memory through "state"
- **Quiz:** "If we have a 'UserCard' component, how many times can we use it on a page?"

## Props
- **Analogy:** Props are like the settings on a TV remote. The TV (component) is always the same, but you can change the channel, volume, and brightness (props) to customize what you see.
- `<UserCard name="Juan" role="CEO" />` — the component receives name and role as props
- **Key insight:** Props flow DOWN. A parent component passes data to its children, not the other way around.

## State (useState)
- **Analogy:** State is the component's personal notebook. It remembers things that can change — like whether a menu is open, what the user typed, or how many items are in a cart.
- **Key insight:** When state changes, React automatically re-draws that part of the page. You don't have to manually update the HTML — just change the state and React handles the rest.
- **Quiz:** "If a counter starts at 0 and the user clicks '+' three times, what should the state be?"

## useEffect
- **Analogy:** A "when this happens, do that" instruction. Like setting an alarm — when the component first appears, go fetch the latest data from the server.
- **Key insight:** Effects run AFTER the component displays. They're for side effects — things that happen outside the component itself, like loading data or starting a timer.

## JSX
- **Key insight:** JSX looks like HTML but it's actually JavaScript in disguise. That's why you can put `{variables}` inside it — it's mixing code with layout.
- **Common confusion:** `className` instead of `class`, `onClick` instead of `onclick` — small differences from regular HTML.

## File Structure Patterns
```
src/
├── components/     ← Reusable LEGO bricks
│   ├── Navbar.jsx
│   └── Card.jsx
├── pages/          ← Full pages built from components
│   ├── Home.jsx
│   └── About.jsx
├── App.jsx         ← The main container that holds everything
└── index.jsx       ← The starting point (plugs React into the HTML)
```
