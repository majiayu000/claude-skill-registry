---
name: markdown-output
description: >-
  Enforce Markdown output formatting policy whenever the user asks for full
  Markdown source code, raw Markdown, or copyable Markdown documents. Use
  whenever the user says "output markdown", "give me the markdown source",
  "markdown 源码", "raw markdown", or similar requests for Markdown content
  that is meant to be copied as-is rather than rendered.
---

# Markdown Output Policy

This skill defines mandatory formatting rules for generating full Markdown
source code. These rules have **higher priority** than any stylistic
formatting preferences.

## Fencing Rules

1. **Always** wrap the entire Markdown document in triple tildes (`~~~`).
2. **Never** use triple backticks (`` ``` ``) as the outermost fence.
3. Triple backticks (`` ``` ``) are allowed **only inside** the document for
   code examples.
4. **Avoid** nested triple backticks. If a code block inside the document
   itself needs to show triple backticks, use an increased-count fence
   (e.g. `~~~~`) or indent-based code blocks instead.
5. The output must be copyable in its entirety without rendering breaks.

## Link Formatting Rules

6. In Markdown links, insert **one space** between the URL and the closing
   parenthesis:
   - Correct: `[text](https://example.com )`
   - Wrong:  `[text](https://example.com)`
7. After a bare URL (not inside a link), always insert **one space** before
   any following character, including punctuation:
   - Correct: `https://example.com ，下一段文字`
   - Wrong:  `https://example.com，下一段文字`

## Examples

### Fencing — correct

~~~
~~~
# My Document

Some text and a code block:

```js
console.log("hello");
```
~~~
~~~

### Fencing — wrong (uses triple backticks as outer fence)

Do **not** produce output like this:

~~~
```
# My Document
…
```
~~~

### Link — correct

~~~
See [GitHub](https://github.com ) for details.
~~~

### Link — wrong

~~~
See [GitHub](https://github.com) for details.
~~~
