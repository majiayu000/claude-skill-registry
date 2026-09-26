---
name: clone-website
description: Rebuild an existing web page 1:1 from measurement instead of by eye — into Figma, Penpot, or code. Captures the rendered page, the raw source and the computed styles, rebuilds section by section, then verifies the result visually, structurally and semantically. Use when reproducing a live page as editable layers or components, or when checking whether a rebuild actually matches the original.
metadata:
  priority: 8
  promptSignals:
    phrases:
      - "clone this website"
      - "clone a page"
      - "copy this page"
      - "recreate this site"
      - "rebuild this page"
      - "website to figma"
      - "html to figma"
      - "import site into figma"
      - "pixel perfect copy"
      - "reverse engineer landing page"
      - "1:1 copy"
      - "teardown"
retrieval:
  aliases:
    - clone website
    - website to figma
    - html to design layers
    - rebuild a landing page
    - page teardown
  intents:
    - reproduce a live page as editable design layers
    - rebuild a competitor landing page for a teardown
    - migrate a production page back into a design tool
    - verify that a rebuild matches the original page
  examples:
    - clone stripe.com/pricing into Figma
    - rebuild this landing page as React components
    - turn this URL into editable layers
    - check whether my rebuild matches the original page
---

# Clone a Website, Accurately

One-click cloners return a lookalike: it resembles the page, and nothing in the
process ever checked whether it matches it. This skill produces a different
artifact — values traceable to the source, and a diff that says what is still
wrong.

**The one rule: if the page states a value, read it. If it does not, and only
then, decide it.** A rebuild done that way is finished when the diff is empty,
which you can check, rather than when it looks about right, which nobody can.

Only the rebuild step cares whether the target is Figma, Penpot or a codebase.
Everything else is the same job.

## Decide before you capture

- **Two widths are the design target**, 390 mobile and 1440 desktop. Real
  devices open the same page at other ratios, so these are what you design to,
  not what you will see.
- A site that follows the light and dark preference renders **two different
  pages**. Capture both, or say which one you copied.
- The IP, locale, consent state and A/B branch reach the site before you do, so
  **what you capture is one visitor's view**, not the page. Check from a second
  location before trusting prices or copy.

## 1. Capture the rendered page

Drive a real browser and take four things at once: full-page screenshots at
both widths, the rendered DOM, the computed styles of each section, and the
asset URLs the page requested. On a client-rendered page this is the only
capture that contains anything at all.

Rendered state is the specification, not the file the server sent.

## 2. Take the raw source as well

Markup carries text verbatim and names every asset URL without a screenshot in
the loop.

```bash
wget -r -l 3 -k -p -E -nc https://example.com/page
```

Host-spanning is left out on purpose: CDN assets stay unfetched, their URLs are
in the markup, and they get downloaded directly at step 4. `wget` does not run
JavaScript, which is why it is the second capture and not the first.

## 3. Measure the design values

Read the tokens off the live page rather than off a picture — the type scale,
palette and spacing are already declared. Use [[extract-design]] for the
extraction; `--design-md` gives you a brief you can hand straight to the
rebuild step.

## 4. Take content and images from the capture

Parse headings, body copy, numbers, lists, links and the footer out of the DOM,
then download every referenced asset. Never retype a string and never infer a
value the source states. Nothing retyped means nothing drifts.

## 5. Build section by section

One section at a time — header, hero, feature rows, tables, media, testimonials,
FAQ, footer — in auto layout or real layout containers, never pinned
coordinates. Screenshot each section and compare it before moving on. A rebuild
judged only at the end gets judged once, badly.

## 6. Compare three things, not one

| Check | Question |
|---|---|
| Visual | Does it look the same at each width? |
| Structural | Is it built from sane containers rather than absolute positions? |
| Semantic | Are the words, links, numbers and variants the ones the source states? |

The third is the one people drop, and it is the one that matters most. A
perfect visual copy can carry wrong data, and it will pass every screenshot
comparison you run against it.

Token-level verification is free: extract the original, extract the rebuild,
compare the two token sets. The difference is your remaining work, stated as a
list instead of a feeling.

## 7. Fix what the capture could not see

Some errors are structural blindness, not degradation, and none of them look
like errors:

- A hero using the wrong image because the real one is a CSS background.
- Carousel or video items in the wrong order.
- Two cards whose values differ by variant, copied from each other.

Report what you could not resolve rather than guessing.

## 8. Fonts: stand in, then swap

Licensed foundry fonts usually cannot be loaded in an automated environment,
and a visual lookalike is the wrong answer because it moves every line break
you are about to verify. Build on a metric-compatible stand-in, then swap to
the real face at the end with one find and replace.

## 9. Fix by targeted prompt, not by rerunning

Every remaining error is local, so the instruction has to be local too: name
the section, name what is wrong, name the source value. Rerunning the whole
rebuild to fix one card costs the hour again and moves the errors somewhere
new.

Where the fix is a judgement call rather than a value, produce two or three
versions of that one section and ask which is right — and ask what made it
right. That sentence is what gets applied to the next section instead of a
guess.

## 10. Throw the scaffolding away

Import gone, staging assets gone. What is left is the two frames, named layers,
icons as vectors, not one absolutely positioned element. If the import is still
in the file, the file is still a draft.

## What this is for

Reproducing a page is research: teardowns, redesign baselines, migration
references, and regression checks against your own site. The last is the most
undervalued — the fastest way to learn whether production still matches its
design system is to extract it and compare.

Shipping someone else's layout, copy or brand as your own is a different act,
and the pipeline being fast does not make it a better idea. Respect robots.txt
and terms of service.

## Related

- [[extract-design]] — the measurement step, and the verification pass
- [[generate-ui-from-brand]] — when the goal is new UI in a brand, not a copy
- [[authentic-product-representation]] — keeping rebuilt content truthful
