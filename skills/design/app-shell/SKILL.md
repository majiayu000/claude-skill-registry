---
name: app-shell
description: The persistent shell around an application — the top bar, the app launcher, the tenant and environment cue, and in heavy tools a status bar. In an estate of several applications the shell belongs to the estate rather than to any one app, and it is what carries a user between tools. Use when designing a top bar, an app switcher, a tenant selector, an environment cue, a status bar, or navigation between separate tools behind one login. For the locale, currency and unit controls the shell carries, see global-toolbar-controls.
metadata:
  priority: 5
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "design-system/**"
    - "ui/**"
  promptSignals:
    phrases:
      - "app shell"
      - "top bar"
      - "app launcher"
      - "app switcher"
      - "tenant"
      - "status bar"
      - "environment banner"
retrieval:
  aliases:
    - app shell
    - top bar
    - app launcher
    - app switcher
    - tenant selector
    - status bar
    - environment cue
  intents:
    - add an app launcher to the top bar
    - let users move between our internal tools
    - add a tenant or customer selector
    - add a status bar to a heavy tool
    - make staging impossible to confuse with production
  examples:
    - how do users get from the shop to the intranet portal
    - where does the customer selector belong
    - what goes in the top bar across all our apps
---
# The App Shell

The shell is the part of the screen that does not change when the user navigates: the bar across the top, whatever sits in it, and in heavy tools a strip along the bottom. Everything between them belongs to the application. The shell is small, and it carries more weight than its size suggests — it is the only thing a user sees on every screen of every tool.

## The Shell Belongs to the Estate, Not to the App

One company rarely has one application. It has a public site, a shop, a customer portal, an internal admin tool, and something older that nobody wants to touch but that people depend on. The user crosses between them during a working day, and each crossing is where the sense of one company either holds or breaks.

**The rule: the top bar is estate-level furniture. The app owns everything below it.** An app that restyles the shared bar to fit its own look has taken something that was not its to change — the bar's job is to be the one fixed point.

But *fixed* is not the same as *full*. What the shell contains may shrink to whatever of its jobs are still unanswered here; what remains is identical — same position, same behaviour, same wording. Quantity flexes, treatment does not.

This also settles a hierarchy question that otherwise gets argued per team. Anything *above* the application in scope lives in the shell; anything *within* the application lives in the app's own navigation.

| Lives in the shell (above the app) | Lives in the app's own nav (within it) |
|---|---|
| Tenant / customer / organisation | Sections, modules, pages |
| Region or market | Filters and views |
| Language and locale | Entity-level actions |
| Identity, role, sign-out | Feature settings |
| App launcher | Search within this tool |

If a control changes what the *whole estate* shows you, it is a shell control. If it changes what *this tool* shows you, it is not.

## How Small the Shell May Get

A sub-application entered only from its parent has one estate-level job left — the way back — so the shell may collapse to a single line: one label, one icon, on the same background as the content, no bar and no chrome. Everything else the shell would carry was already answered upstream, and repeating it is noise.

The condition is the entry path, and it is the whole rule:

- **Entry is always through the parent** — a return affordance is enough.
- **Entry can be direct or lateral** — a deep link from chat, a bookmark, an email button, another tool — then a return affordance points at nothing, because browser history is not hierarchy. Carry a home affordance instead. It can still be one icon.

**Name it by destination, not by action.** `← Dashboard` stays true when history and hierarchy disagree; `← Back` does not. Back is a history concept, up is a hierarchy concept, and a shell that conflates them lies exactly when the user is most lost.

## The App Launcher

When a user has access to more than three tools, the shell needs a launcher: one icon in the top bar that opens the full set. It is what replaces the bookmark folder and the link someone pasted in chat two years ago.

- **Show everything the user can reach, and nothing they cannot** — a launcher listing tools that return a 403 teaches users to distrust it
- **Name tools the way people name them out loud**, not by internal project codename
- **Mark what opens in a new context** — a 2006 system that will not share the shell's look should say so, quietly, rather than surprising the user
- **Order by the user's use, then alphabetically** — not by the org chart of who built what

## Tenant, Environment, and the Colour Trap

In a multi-tenant or multi-customer tool, the user must always know whose data is on screen. Two related controls, one important difference.

**Environment is worth a colour.** Production, staging, and a local build should be impossible to confuse, because the cost of the confusion is a real change to real data. A coloured strip or a tinted bar is the right tool, and this is one of the few places where deliberately breaking the calm of the shell is correct.

**Tenant is not.** Tinting the whole UI per customer is a tempting idea that makes every customer a different-looking product, breaks the brand, and quietly wrecks contrast the moment a customer's colour is not one you chose. Show the tenant as a **label** in the shell — name, and an avatar or initials if you have one — not as a theme. If a tenant genuinely needs its own visual identity, that is a white-label decision made once at the product level, not a per-session tint ([[brand-visual-language]]).

Whoever is selected, the shell states it plainly and permanently, and destructive actions repeat it in the confirmation ([[ui-context-and-scope]]).

## The Status Bar

Heavy tools — dispatch boards, data managers, editors people sit in for six hours ([[operational-expert-tool-ui]]) — benefit from a strip along the bottom that carries ambient state. It answers questions the user would otherwise have to go looking for:

connection and sync state · environment · active filters and how many records they match · selection count · last saved · the one keyboard hint that matters here

It is ambient, so it stays quiet: the same small, muted type as the rest of the shell, no animation, no colour except when something is genuinely wrong. A status bar that flashes is a notification in the wrong place ([[notifications-and-recovery]]).

Consumer products almost never need one. If the user is not in the tool long enough to build a habit of glancing down, the strip is just a stolen row of screen.

## Review Checklist

- [ ] Is the shell in the same position, with the same behaviour and wording, across every application in the estate?
- [ ] Where it is reduced, is the reduction justified by the entry path rather than by one app's taste?
- [ ] Does a return affordance name its destination rather than saying "back"?
- [ ] Does every control sit at the right level: estate-scope in the shell, app-scope in the app's own nav?
- [ ] Does the launcher list exactly the tools this user can actually open?
- [ ] Is the current tenant stated as a label rather than applied as a theme?
- [ ] Is the environment (production / staging) unmistakable?
- [ ] In a heavy tool, does the status bar carry ambient state — and stay quiet?
