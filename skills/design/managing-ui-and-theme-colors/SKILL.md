---
name: managing-design-system
description: Defines the core visual identity, color tokens, interaction patterns, and signature UI layouts for Tourly. Use when implementing or styling any frontend component to ensure brand consistency.
---

# Design System & UI Context

## Desktop UI:
![alt text](<Desktop UI.png>)
  - Note: Reference for Header height, hero, horizontal search bar alignment, and "Folder Style" tabs.

## Mobile UI:
![alt text](<Mobile UI.jpeg>)
   - Note: Reference for bottom navbar, horizontal scrolling service pills, and stacked input fields.

## When to use this skill
- When creating or modifying any UI component.
- To ensure visual consistency with the "Gilgit river/sky" Azure Blue brand.
- When implementing the signature "Search Box" or "Folder Style" tabs.

## 1. Core Color System
- **Primary Brand**: Vibrant Azure Blue (Gilgit river/sky inspired).
    - Use for: Discover buttons, active tabs, primary highlights.
    - Tailwind: `bg-primary`, `text-primary`.
- **Backgrounds**: 
    - Card/Widgets: `bg-white`.
    - Mobile Page: `bg-slate-50`.
- **Borders**: `border-slate-200` for outlines.
- **Typography**:
    - Headings: `text-slate-900` (Dark/Black).
    - Labels: `text-slate-500` (Medium Gray, Uppercase).
    - Values: `text-slate-500` or `text-slate-600` (Low opacity aesthetic).

## 2. Interaction & State Styles
- **Hover**: 20% opacity primary blue tint (`hover:bg-primary/20`).
- **Focus**: Remove all browser rings. Use container borders. (`outline-none ring-0 focus:ring-0`).
- **Active Tabs**:
    - Desktop: White background (`bg-white`) with dark text.
    - Inactive: Dark or transparent.
- **Mobile Services**: Active icon uses solid blue rounded background with white text.

## 3. UI Component Architecture

### A. Search Input "Box" Design
Each input (Location, Dates, Travelers) must be in its own rounded container.
- **Container**: `rounded-lg border border-slate-200 bg-white pt-2 pb-3 px-4`.
- **Top Label**: `text-[10px] font-bold uppercase text-slate-500 leading-none`.
- **Main Value**: `text-base font-semibold text-slate-500 mt-1.5`.
- **Invisible Input**: The inner `<input>` must have `appearance-none border-none bg-transparent p-0 w-full focus:ring-0`.

### B. Navigation & Layout
- **Desktop Header**: `h-16` (64px). Centered links: "Destinations", "Agencies", "Services".
- **Search Tabs**: "Folder Style"—Square joints, rounded far-left and far-right corners of the group.
- **Mobile Bottom Nav**: `h-14` (56px). Items: "Explore", "Wishlists", "Profile". `text-xs`.
- **Mobile Service Menu**: `overflow-x-auto` row of service pills (Stays, Transport, Guides, TripAI).

### C. Buttons
- **Discover Button**:
    - Solid Vibrant Blue.
    - Desktop: Horizontal, matches input box height.
    - Mobile: Full-width stacked below inputs.

## 4. Typography Rules
- **Family**: Inter, DM Sans, or similar modern Sans-serif.
- **Hero**: White text on images with a subtle dark overlay.
- **Labels**: Small, bold, uppercase (`text-xs` or `text-[10px]`).

## 5. Specific Feature Logic
- **Smart Date Selection**: Restart logic if selected < start. Popover stays open for correction.
- **Mobile Form Behavior**: Inputs update dynamically based on the active service tab.

## Instructions
- **Aesthetics First**: Every design choice must feel premium and "alive".
- **No Layout Shifts**: Use fixed height containers for inputs to maintain alignment across service switches.
