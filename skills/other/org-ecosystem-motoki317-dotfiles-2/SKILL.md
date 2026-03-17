---
name: Org Ecosystem
description: This skill should be used when the user asks to "write org", "org-mode", "org file", ".org file", "org syntax", "org document", "org babel", "org export", "org agenda", "org capture", "GTD", "literate programming", "org publishing", or "org-mode workflow". Provides comprehensive Org-mode patterns and best practices.
---

# Org Ecosystem

Patterns for Org-mode document creation, GTD workflow, literate programming with Babel, and export/publishing.

## Syntax Fundamentals

### Headings and Properties
```org
* Top-level heading
** Second-level heading
*** Third-level heading

* Task
:PROPERTIES:
:CATEGORY: work
:EFFORT:   2h
:END:
```

### Timestamps
- `<2024-01-15 Mon>` - active (shows in agenda)
- `[2024-01-15 Mon]` - inactive
- `<2024-01-15 Mon +1w>` - repeating weekly
- `<2024-01-15 Mon .+1d>` - restart from completion

### Markup
- `*bold*` `/italic/` `_underline_` `=verbatim=` `~code~` `+strikethrough+`

### Links
- `[[https://orgmode.org][Org website]]` - external
- `[[file:./other.org][Local file]]` - file link
- `[[*Heading][Internal link]]` - heading link
- `[[id:unique-id][ID link]]` - stable cross-file reference

### Tables
```org
| Name  | Qty | Price | Total |
|-------+-----+-------+-------|
| Item1 |   2 |  10.0 |  20.0 |
#+TBLFM: $4=$2*$3
```

## GTD Workflow

### TODO States
```org
#+TODO: TODO(t) NEXT(n) WAITING(w@/!) | DONE(d!) CANCELLED(c@)
```
- `@` prompts for note, `!` records timestamp, `|` separates active/done

### Capture Templates
```elisp
(setq org-capture-templates
  '(("t" "Todo" entry (file+headline "~/org/inbox.org" "Tasks")
     "* TODO %?\n  %i\n  %a")
    ("n" "Note" entry (file "~/org/notes.org")
     "* %? :note:\n  %U\n  %i")))
```
- `%?` cursor, `%i` region, `%a` annotation, `%U` inactive timestamp

### Clocking
```org
:LOGBOOK:
CLOCK: [2024-01-15 Mon 10:00]--[2024-01-15 Mon 12:30] =>  2:30
:END:
```
- `C-c C-x C-i` clock in, `C-c C-x C-o` clock out

## Babel (Literate Programming)

### Code Blocks
```org
#+NAME: example-block
#+BEGIN_SRC python :results output :exports both
print("Hello from Python")
#+END_SRC
```

### Header Arguments
- `:results` - value, output, silent, table
- `:exports` - code, results, both, none
- `:var` - variable binding
- `:session` - persistent session
- `:tangle` - extract to file
- `:noweb` - reference expansion

### Tangling
```org
#+BEGIN_SRC python :tangle ./script.py :shebang "#!/usr/bin/env python3"
def main():
    print("Generated from org file")
#+END_SRC
```
- `C-c C-v t` to tangle

### Noweb References
```org
#+NAME: imports
#+BEGIN_SRC python :noweb-ref imports
import os
#+END_SRC

#+BEGIN_SRC python :tangle ./program.py :noweb yes
<<imports>>
#+END_SRC
```

## Export

### Document Header
```org
#+TITLE: Document Title
#+AUTHOR: Author Name
#+OPTIONS: toc:2 num:t author:t
```

### Export Backends
- HTML: `C-c C-e h h`
- PDF via LaTeX: `C-c C-e l p`
- Beamer slides: `C-c C-e l b`
- Markdown: `C-c C-e m m`

### Selective Export
```org
* Exported heading
* Not exported :noexport:

#+BEGIN_EXPORT html
<div class="custom">Raw HTML</div>
#+END_EXPORT
```

## Best Practices

**Critical:**
- One file per major project or area
- Keep inbox.org for captures, refile regularly
- Consistent TODO state workflow across files

**High:**
- Add SCHEDULED/DEADLINE to time-sensitive tasks
- Use tags for context (@home, @work) not categories
- Archive completed subtrees periodically

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Single giant file | Split by project/topic |
| Deep nesting (>4 levels) | Flatten or split files |
| Never refiling captures | Daily/weekly inbox processing |
| Hardcoded paths | Use relative paths or org-directory |
| Babel side effects | Use `:results silent`, document clearly |

## Constraints

**Must:**
- Use appropriate heading levels (don't skip)
- Close all drawers and blocks properly
- Use relative paths for portability

**Avoid:**
- Excessive nesting beyond 4-5 levels
- Side effects in babel without documentation
