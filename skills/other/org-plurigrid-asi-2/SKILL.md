---
name: org
description: Org-mode manual (25K lines info).
metadata:
  trit: 0
---

# org

Org-mode manual (25K lines info).

## Structure

```org
* Heading 1
** Heading 2
*** TODO Task [#A]
    DEADLINE: <2025-12-25>
    :PROPERTIES:
    :CUSTOM_ID: task-1
    :END:
```

## Markup

```org
*bold* /italic/ _underline_ =verbatim= ~code~
[[https://example.com][Link]]
#+BEGIN_SRC python
print("hello")
#+END_SRC
```

## Keys

```
TAB       Cycle visibility
C-c C-t   Toggle TODO
C-c C-s   Schedule
C-c C-d   Deadline
C-c C-c   Execute/toggle
C-c '     Edit src block
```

## Export

```elisp
(org-export-dispatch)  ; C-c C-e
```
