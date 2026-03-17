---
name: kb-fediverse-long-form-text
description: >
  Background knowledge about how long-form text works on the Fediverse and
  in ActivityPub, based on FEP-b2b8. Covers the Article type and when to use
  it instead of Note, the full set of Article properties (name, summary,
  content, preview, url, image, attributedTo, sensitive, etc.), the allowed
  HTML subset for content, the preview mechanism for microblogging client
  fallback, summary generation guidance (~500 chars), the sensitive flag
  with dcterms:subject display hierarchy, RSS 2.0 property parallels, and
  implementation differences across Mastodon, WordPress, Ghost, WriteFreely,
  NodeBB, Bonfire, and Threads. Load when the user asks about implementing
  long-form text, blog posts, or articles in ActivityPub; how Article
  differs from Note; how to structure an Article object; how to make
  articles display correctly on Mastodon; what the preview property is for;
  how to generate summaries; or what FEP-b2b8 specifies.
user-invocable: false
---

# Fediverse Long-form Text (FEP-b2b8) — Complete Reference

## Overview

Long-form text — blog posts, magazine articles, forum posts — is represented
in ActivityPub using the `Article` type, defined in the Activity Streams 2.0
vocabulary. FEP-b2b8 (authored by Evan Prodromou, received 2024-11-07, status
DRAFT) collects and extends guidance for publishers and consumers of
multi-paragraph text objects.

The core problem FEP-b2b8 addresses: the fediverse grew around microblogging
where `Note` dominates. Mastodon and similar clients either display `Article`
objects as just a title + link or strip their HTML, providing a degraded
experience. Many publishers worked around this by sending `Note` instead,
causing overly-long posts in microblog feeds. FEP-b2b8 defines how to
structure `Article` objects properly and introduces the `preview` property as
a fallback for microblogging clients.

---

## 1. Article vs. Note — When to Use Which

The Activity Vocabulary defines:
- **`Note`** — a short written work, typically less than a single paragraph
- **`Article`** — any kind of multi-paragraph written work

Publishers SHOULD use `Article` for multi-paragraph content. The common
workaround of stuffing long content into a `Note` causes problems for
consumers that expect Notes to be short. FEP-b2b8 explicitly discourages it:

> Publishers should avoid this workaround, and instead give consumers the
> full information they need to display the content correctly in their own
> interfaces.

The IndieWeb community uses a pragmatic heuristic: articles have titles
(a `name` property), notes don't. The post-type-discovery algorithm checks
whether `name` exists and is not simply a prefix of `content`.

---

## 2. The Article Object — Properties

### `id`

A unique HTTPS URL that resolves to the object. Equivalent to RSS 2.0 `guid`.

### `name`

The title. Should be plain text (no HTML entities like `&amp;`), 75–150
characters. Equivalent to RSS 2.0 `title`.

```json
"name": "Long-form text with included content"
```

### `url`

Location of the full HTML representation. Can be:
- A single string URL
- A `Link` object with `mediaType: "text/html"` and `href`
- An array of strings/Link objects for multiple representations

At least one entry should have `mediaType` of `text/html` and protocol
`https`. Equivalent to RSS 2.0 `link`.

```json
"url": "https://example.com/2024/11/07/long-form-text.html"
```

Or as a Link:

```json
"url": {
  "type": "Link",
  "mediaType": "text/html",
  "href": "https://example.com/2024/11/07/long-form-text.html"
}
```

### `summary`

A brief description, teaser, abstract, or "lede." Guidelines:
- Maximum about **500 characters**
- A few sentences or a short paragraph
- Can include HTML markup
- MUST NOT include embedded media (images, video, audio)
- MUST NOT include navigation elements or affordances (favourite, like,
  bookmark buttons)
- MUST NOT include "Read more..." links

Equivalent to RSS 2.0 `description`.

**Summary generation hierarchy** (recommended by Evan Prodromou):
1. Manual user-defined summary (preferred)
2. Use full text if it is ~500 chars and a single paragraph
3. Use first paragraph if it meets the rough guidelines
4. Truncate with ellipsis (`…`) as fallback

**Implementation note (NodeBB):** NodeBB allows a "magic string" (HTML
comment) that power users can place in their content to manually select
where the summary should end. The limit and marker are configurable per
instance. After consulting with Matt Baer (WriteFreely), this approach was
adopted alongside ellipsis on truncation.

**Interop quirk (GoToSocial):** GoToSocial treats `summary` as a content
warning, not as a teaser/abstract. This means Articles with a `summary`
may display with a content warning gate on GoToSocial, which is not the
publisher's intent.

### `attributedTo`

The author(s). Can be:

**A string** (just the actor id):
```json
"attributedTo": "https://example.com/evan"
```

**An object** with full author info:
```json
"attributedTo": {
  "type": "Person",
  "id": "https://example.com/evan",
  "name": "Evan Prodromou",
  "summary": "<p>Founder of Social Web Foundation</p>",
  "url": "https://example.com/evan",
  "icon": {
    "type": "Image",
    "mediaType": "image/png",
    "url": "https://example.com/evan.png"
  }
}
```

**A Link** (for authors without an AS2 representation):
```json
"attributedTo": {
  "type": "Link",
  "href": "https://example.com/evan",
  "name": "Evan Prodromou"
}
```

**An array** for multiple authors (strings, objects, or Links mixed).

### `published`

Publication date as `YYYY-MM-DDTHH:MM:SSZ`. Equivalent to RSS 2.0 `pubDate`.

### `updated`

Date of last update, same format. If absent, consumers can assume the object
has not been modified since `published`.

### `image`

A notable or representative image. Can be an `id` string or `Image` object.
Multiple values are allowed (array), ordered by importance (most important
first). Consumers use as many or as few as needed.

### `content`

The full text of the article in HTML. The HTML MUST be a sanitized subset —
no CSS, no JavaScript. Allowed elements:

| Element | Allowed Attributes |
|---|---|
| `<p>` | — |
| `<span>` | class |
| `<h2>` through `<h6>` | — |
| `<br>` | — |
| `<a>` | href, rel, class |
| `<del>` | — |
| `<pre>` | — |
| `<code>` | — |
| `<em>` | — |
| `<strong>` | — |
| `<b>` | — |
| `<i>` | — |
| `<u>` | — |
| `<ul>` | — |
| `<ol>` | start, reversed |
| `<li>` | value |
| `<blockquote>` | — |
| `<img>` | src, alt, title, width, height, class |
| `<video>` | src, controls, loop, poster, width, height, class |
| `<audio>` | src, controls, loop, class |
| `<source>` | src, type |
| `<ruby>` | — |
| `<rt>` | — |
| `<rp>` | — |

Notable omissions: `<h1>` (the title goes in `name`), `<table>`, `<div>`,
`<figure>`, `<figcaption>`, `<details>`, `<summary>`.

The content MUST NOT include navigation links (home page, category pages),
affordance buttons (favourite, like, bookmark), or "Read more" links. Any
embedded media (`<img>`, `<video>`, `<audio>`) in `content` SHOULD also be
listed in `attachment` for pre-fetching.

### `source`

If the text was originally created in a different format (e.g., Markdown),
the original source for editing:

```json
"source": {
  "mediaType": "text/markdown",
  "content": "# My Article\n\nFirst paragraph..."
}
```

### `replies`

A URL resolving to a collection of reply objects. Replies are usually `Note`
objects but can be `Article` or `Question`. Equivalent to RSS 2.0 `comments`.

### `inReplyTo`

If the article is a reply to another ActivityPub object, a string URL or
JSON object. If it is commentary on a web resource (not an AP object), a
`Link` object with `href` pointing to that resource.

### `attachment`

Additional media for pre-fetching without parsing `content`:

```json
"attachment": [
  {
    "type": "Image",
    "id": "https://example.com/image1.jpg",
    "mediaType": "image/jpeg"
  }
]
```

### `tag`

Two important tag types:
- **Hashtag**: `{ "type": "Hashtag", "name": "example", "href": "https://..." }`
- **Mention**: `{ "type": "Mention", "href": "https://..." }`

### `context`

Link to a larger collection — an article series, newspaper column, blog
category, magazine section. Can be an array. (For topic tagging, `tag` with
Hashtag may be more appropriate.)

### `generator`

Information about the publishing software. Usually an `Application` or
`Service` object with `id` and `name`.

### `to`, `cc`, `bcc`, `bto`, `audience`

Addressing properties. Determine delivery targets in ActivityPub and provide
access control. Publishers and consumers MUST NOT disclose Article properties
to anyone except addressees and creator(s).

### `sensitive`

Marks content as potentially sensitive (nudity, violence, spoilers, etc.).
When set, consumers should obscure the article until the user opts in.

To help users decide whether to read, display these properties (in order):

1. **`dcterms:subject`** — Dublin Core subject string(s). Most informative
   and least likely to leak sensitive content.
2. **`tag`** — Hashtag names. Less human-readable than subject.
3. **`name`** — Title. Authors may leak sensitive material here.
4. **`summary`** — Last resort. A well-written summary likely includes
   significant excerpts of the sensitive content.

Using `dcterms:subject` requires extending the context:

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://purl.archive.org/miscellany",
    {"dcterms": "http://purl.org/dc/terms/"}
  ],
  "type": "Article",
  "sensitive": true,
  "dcterms:subject": ["Citizen Kane"]
}
```

---

## 3. The `preview` Property — Microblogging Fallback

The `preview` property is a key innovation in FEP-b2b8 for bridging the
Article/microblogging gap. It provides a `Note` that gives a well-formatted
preview of the article:

```json
{
  "type": "Article",
  "id": "https://example.com/article.jsonld",
  "name": "Long-form text with preview",
  "url": "https://example.com/article.html",
  "attributedTo": "https://example.com/evan",
  "summary": "<p>This is the summary.</p>",
  "content": "<p>Full article content here...</p>",
  "published": "2024-11-07T12:00:00Z",
  "image": {
    "type": "Link",
    "href": "https://example.com/image.jpg",
    "mediaType": "image/jpeg"
  },
  "preview": {
    "type": "Note",
    "attributedTo": "https://example.com/evan",
    "content": "<p><strong>Long-form text with preview</strong></p><p>This is the summary.</p>",
    "published": "2024-11-07T12:00:00Z",
    "attachment": {
      "type": "Link",
      "href": "https://example.com/image.jpg",
      "mediaType": "image/jpeg"
    }
  }
}
```

Rules for `preview`:
- Type SHOULD be `Note`
- Content should combine the `name` (as bold text) and `summary`
- MUST NOT include a link to the HTML representation
- MUST NOT include navigation or affordance elements
- Metadata from the Article (`attributedTo`, `published`, `updated`, `tag`)
  can be repeated; consumers fall back to the Article's properties if absent
- The Article's `image` may be included as `attachment` in the preview
- The preview MAY have its own `id`
- The consumer (not the preview) is responsible for displaying a link to the
  full article content

**Community debate:** trwnh raised concerns that `preview` "muddies the
waters" by treating separate objects as unified. The mechanism remains in the
FEP but its long-term acceptance is not certain.

---

## 4. Complete Example — Minimal Article

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Article",
  "id": "https://example.com/2024/11/07/my-post.jsonld",
  "name": "My Blog Post Title",
  "url": "https://example.com/2024/11/07/my-post.html",
  "attributedTo": "https://example.com/users/alice",
  "summary": "<p>A brief teaser about the post content.</p>",
  "content": "<p>First paragraph of the full article.</p><p>Second paragraph with more detail.</p>",
  "published": "2024-11-07T12:00:00Z"
}
```

---

## 5. Complete Example — Article with External Content Only

An Article can omit `content` and link to external HTML instead:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Article",
  "id": "https://example.com/2024/11/07/external.jsonld",
  "name": "My External Article",
  "url": "https://example.com/2024/11/07/external.html",
  "attributedTo": "https://example.com/users/alice",
  "summary": "<p>A brief description of the article available at the URL.</p>",
  "published": "2024-11-07T12:00:00Z"
}
```

---

## 6. RSS 2.0 Property Mapping

FEP-b2b8 explicitly draws parallels to RSS 2.0 for publishers familiar with
syndication:

| Article Property | RSS 2.0 Equivalent |
|---|---|
| `id` | `guid` |
| `name` | `title` |
| `url` | `link` |
| `summary` | `description` |
| `attributedTo` | `author` |
| `published` | `pubDate` |
| `replies` | `comments` |

---

## 7. How Consumers Should Display Articles

FEP-b2b8 includes UI guidance for stream-oriented interfaces:

### Standard display (with image)
Show: author avatar + name, `name` as headline, `image` as hero/thumbnail,
`summary` as teaser text, `published` date, link to `url` for full reading.

### Without image
Same as above, minus the image. The `summary` gets more visual prominence.

### Without title
If `name` is absent, show the `summary` or beginning of `content` directly,
similar to how a Note would appear but with a link to the full content.

### Sensitive content
If `sensitive` is true, obscure the article behind a content warning. Show
`dcterms:subject` or `tag` names or `name` to help the user decide whether
to proceed.

### With preview
If the consumer does not natively support `Article`, display the `preview`
Note instead. The consumer is responsible for adding a link to the full
article.

### Fallback for consumers that only display short text
Show `name`, `summary`, and a link to `url` so users can read the full
content in a browser.

---

## 8. Interoperability Matrix

### Publishing platforms (send Article type)

| Platform | Sends Article | Uses summary | Uses preview | Notes |
|---|---|---|---|---|
| WordPress (AP plugin) | Yes | Yes | — | Historically sent Note as workaround; now sends Article |
| Ghost | Yes | Yes | — | Active SWF participant; Ghost 6 has full AP integration |
| WriteFreely / Write.as | Yes | Yes | — | PR for FEP-b2b8 support discussed May 2025 |
| Plume | Yes | Yes | — | Early Article adopter |
| NodeBB | Yes | Yes | — | Switches between Note/Article by length; magic string for summary breaks |
| Bonfire | Yes | Yes | — | Adopted FEP-b2b8 as technical foundation |

### Consuming platforms (display Article type)

| Platform | Article display | Notes |
|---|---|---|
| Mastodon | Title + link only | First-class types are Note and Question only; Article gets degraded display |
| Threads | Full display | Announced support for long-form Ghost content (2025) |
| Pleroma/Akkoma | Inline display | Supports rich text in both Note and Article |
| GoToSocial | Inline display | Treats `summary` as content warning (not teaser) |
| Bonfire | Full display | Dedicated "Articles" feed, in-app reading |

---

## 9. The Note vs. Article History

Understanding why FEP-b2b8 exists requires knowing the history:

**2017:** Mastodon treated Note and Article identically, stripping most HTML
from both. When this was raised, Mastodon changed Article to display only as
a title + link. This created a fundamental disincentive to use Article.

**2019–2023 (SocialHub discussions):** Years of debate over what distinguishes
Note from Article. Proposals included:
- Length-based (short vs. multi-paragraph)
- Formality-based (informal message vs. publication)
- Title-based (articles have `name`, notes don't — IndieWeb approach)
- Formatting-based (notes have minimal markup, articles have rich layout)

No spec-level resolution was reached.

**2024:** The Social Web Foundation identified long-form text as a priority.
Evan Prodromou convened implementer workshops with WordPress, WriteFreely,
Ghost, and others. FEP-b2b8 was submitted November 7, 2024.

**2025:** Threads announced Article support. Bonfire adopted FEP-b2b8.
WriteFreely worked on implementation. Community debates continued around
the `preview` mechanism and whether types should be semantic or length-based.

---

## 10. Known Issues and Pitfalls

- **Mastodon's degraded display** is the #1 practical problem. Articles
  appear as just a title and link in Mastodon's UI, losing boosts, replies,
  and in-app engagement. This is why many publishers historically sent Note.
- **GoToSocial summary-as-CW**: GoToSocial interprets `summary` as a content
  warning, not a teaser. Articles with summaries will display behind a CW
  gate, which is not what the publisher intended.
- **NodeBB engagement drop**: When NodeBB switched from Note to Article for
  longer posts, engagement dropped because the truncated summary was less
  compelling than the full Note.
- **No `<h1>` in content**: The allowed HTML subset starts at `<h2>`. The
  article title belongs in `name`, not in the HTML content.
- **No `<table>` in content**: Tables are not in the allowed element set.
  Content with tabular data must use alternative markup or be simplified.
- **preview debate**: trwnh and others question whether `preview` is the
  right mechanism, arguing it creates ambiguity about which object properties
  are authoritative.
- **summary length is guidance, not a hard limit**: "about 500 characters"
  is a recommendation. NodeBB made it configurable per instance. Some
  implementations may use longer summaries.

---

## 11. Scope Limitations

FEP-b2b8 explicitly does NOT cover:
- Book-length or longer text
- Specific media types beyond text with embedded media
- Client-to-server (C2S) article creation workflows
- Full-text search or discovery mechanisms
