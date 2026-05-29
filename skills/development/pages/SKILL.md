---
name: app-pages
description: Pattern for application pages
---

# Instructions

## Page Name and Component Location

Pages are the different top level views (aka panels) that we display in the application. Their names are defined in file `src/store/types.ts` in the following line of code.

```
export type AppView = 'browser' | 'search-results' | 'settings';
```

The 'browser' one is the main default application `src/App.tsx`, but any pages other than the main (browser) page should follow a pattern similar to what you find in `src/components/SearchResultsView.tsx`

## Tab Navigation

Each page has a corresponding tab button in the tab panel at the top of the screen (Browse, Search, Settings). When the user clicks a tab button, we update the `currentView` in the global `AppState`, and that causes the page to display at next render.

## React Global State Management

Example: `setCurrentView('search-results');`
