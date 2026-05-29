---
name: mediawiki-wikitext
description: MediaWiki Wikitext markup language for Wikipedia and wiki-based sites. Use when creating or editing wiki articles, generating wikitext content, working with wiki tables/templates/references, or converting content to wikitext format. Triggers on requests mentioning Wikipedia, MediaWiki, wikitext, wiki markup, or wiki article creation.
---

# MediaWiki Wikitext

Generate and edit content using MediaWiki's wikitext markup language.

## Quick Reference

### Text Formatting
```wikitext
''italic''  '''bold'''  '''''bold italic'''''
<code>inline code</code>  <sub>subscript</sub>  <sup>superscript</sup>
<s>strikethrough</s>  <u>underline</u>
```

### Headings (line start only, avoid level 1)
```wikitext
== Level 2 ==
=== Level 3 ===
==== Level 4 ====
```

### Lists
```wikitext
* Bullet item        # Numbered item       ; Term
** Nested            ## Nested             : Definition
```

### Links
```wikitext
[[Page Name]]                      Internal link
[[Page Name|Display Text]]         With display text
[[Page Name#Section]]              Section link
[https://url Display Text]         External link
[[File:image.jpg|thumb|Caption]]   Image
[[Category:Name]]                  Category (place at end)
```

### Table
```wikitext
{| class="wikitable"
|+ Caption
|-
! Header 1 !! Header 2
|-
| Cell 1 || Cell 2
|}
```

### Templates & Variables
```wikitext
{{TemplateName}}                   Basic call
{{TemplateName|arg1|name=value}}   With arguments
{{{parameter|default}}}            Parameter (in template)
{{PAGENAME}}  {{CURRENTYEAR}}      Magic words
```

### References
```wikitext
Text<ref>Citation here</ref>
<ref name="id">Citation</ref>      Named reference
<ref name="id" />                  Reuse reference
{{Reflist}}                        Display footnotes
```

### Special Tags
```wikitext
<nowiki>[[escaped]]</nowiki>       Disable markup
<pre>preformatted block</pre>      Preformatted (no markup)
<syntaxhighlight lang="python">    Code highlighting
code here
</syntaxhighlight>
<math>x^2 + y^2 = z^2</math>       LaTeX math
<!-- comment -->                   Comment (hidden)
----                               Horizontal rule
#REDIRECT [[Target Page]]          Redirect (first line only)
```

### Magic Words
```wikitext
__NOTOC__           Hide table of contents
__TOC__             Position TOC here
__NOEDITSECTION__   Hide section edit links
```

## Common Patterns

### Article Structure
```wikitext
{{Infobox Type
| name = Example
| image = Example.jpg
}}

'''Article Title''' is a brief introduction.

== Section ==
Content with citation<ref>Source</ref>.

=== Subsection ===
More content.

== See also ==
* [[Related Article]]

== References ==
{{Reflist}}

== External links ==
* [https://example.com Official site]

{{DEFAULTSORT:Sort Key}}
[[Category:Category Name]]
```

### Template Definition
```wikitext
<noinclude>{{Documentation}}</noinclude><includeonly>
{| class="wikitable"
! {{{title|Default Title}}}
|-
| {{{content|No content provided}}}
{{#if:{{{footer|}}}|
{{!}}-
{{!}} {{{footer}}}
}}
|}
</includeonly>
```

## Key Syntax Rules

1. **Headings**: Use `==` to `======`; don't use `=` (reserved for page title)
2. **Line-start markup**: Lists (`*#;:`), headings, tables (`{|`) must start at line beginning
3. **Closing tags**: Close heading equals on same line; no text after closing `==`
4. **Blank lines**: Create paragraph breaks; single newlines are ignored
5. **Pipes in templates**: Use `{{!}}` for literal `|` inside templates
6. **Escaping**: Use `<nowiki>` to escape markup; `&amp;` for `&`, `&lt;` for `<`

## Resources

For detailed syntax, see:
- **references/syntax.md**: Complete markup reference with all options
- **references/templates.md**: Template and parser function details
- **assets/snippets.yaml**: Editor snippets for common patterns
