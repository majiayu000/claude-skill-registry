---
name: translation
description: Translate text between languages with cultural adaptation, terminology consistency, and support for multiple document types including technical docs, marketing copy, and UI strings. Use when the user requests translation or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Translation

This skill enables an AI agent to translate text between languages while preserving meaning, tone, and context. It goes beyond word-for-word substitution by handling idiomatic expressions, cultural nuance, domain-specific terminology, and formality registers. The agent can translate technical documentation, marketing copy, UI strings, legal text, and general prose, adapting output to the conventions of the target locale.

## Workflow

1. **Analyze Source Context**
   Examine the source text to determine its domain (technical, marketing, legal, casual), register (formal, informal, neutral), and intended audience. Identify any idiomatic expressions, culturally specific references, or humor that will require adaptation rather than literal translation. Note the document format (plain text, Markdown, JSON, HTML) so structure is preserved in the output.

2. **Research Terminology**
   For specialized content, build or consult a terminology glossary to ensure consistency. Technical documents require exact translations of domain terms (e.g., "endpoint" stays "endpoint" in many languages or maps to an accepted equivalent). Marketing copy may need creative transcreation rather than direct translation. If the user provides a glossary or translation memory, integrate it before proceeding.

3. **Translate the Content**
   Produce the translation following the determined tone, formality level, and terminology. Preserve all formatting markers such as Markdown headings, code blocks, HTML tags, and JSON keys. For UI strings, keep placeholder tokens (e.g., `{username}`, `%d`) intact and in the correct grammatical position for the target language. Handle pluralization rules specific to the target language.

4. **Localize Cultural References**
   Adapt units of measurement, date formats, currency symbols, and culturally bound metaphors to the target locale. For example, convert miles to kilometers when translating for a European audience, or replace an American sports analogy with one that resonates in the target culture. For marketing content, ensure slogans and calls-to-action carry the same persuasive impact in the target language.

5. **Review for Accuracy and Fluency**
   Re-read the translated text to verify grammatical correctness, natural phrasing, and faithful representation of the source meaning. Check that no sentences were accidentally omitted or duplicated. Confirm terminology consistency across the entire document by cross-referencing the glossary established in step 2.

6. **Deliver with Annotations**
   Return the translated text in the same format as the source. Where translation choices were ambiguous, include brief translator notes explaining the reasoning. If the user requested multiple formality levels or regional variants, provide each variant clearly labeled.

## Usage

Provide the text to translate along with the target language. Optionally specify:

- **Source language** (if not auto-detectable)
- **Formality level** — formal, informal, or neutral
- **Domain** — technical, marketing, legal, medical, general
- **Glossary** — key terms and their required translations
- **Output format** — plain text, Markdown, JSON locale file, etc.

Example prompt: "Translate the following API error messages to Japanese (formal). Keep the JSON structure and all placeholder tokens intact."

## Examples

### Example 1: Translating a Technical Paragraph (English to German, Formal)

**Input:**

> The authentication module uses OAuth 2.0 with PKCE to secure API requests. When a user initiates a login, the client generates a code verifier and code challenge. The authorization server validates the challenge before issuing an access token. Tokens expire after 3600 seconds and must be refreshed using the refresh token endpoint.

**Output:**

> Das Authentifizierungsmodul verwendet OAuth 2.0 mit PKCE, um API-Anfragen abzusichern. Wenn ein Benutzer eine Anmeldung einleitet, erzeugt der Client einen Code-Verifier und eine Code-Challenge. Der Autorisierungsserver validiert die Challenge, bevor er ein Zugriffstoken ausstellt. Token laufen nach 3600 Sekunden ab und müssen über den Refresh-Token-Endpunkt erneuert werden.

**Translator note:** "Code Verifier," "Code Challenge," and "Refresh-Token-Endpunkt" are kept close to the English originals because these are established terms in the German-speaking developer community.

### Example 2: Localizing UI Strings (English to Spanish, JSON Locale File)

**Input:**

```json
{
  "greeting": "Hello, {username}!",
  "items_in_cart": "You have {count} item(s) in your cart.",
  "checkout_button": "Proceed to Checkout",
  "empty_cart": "Your cart is empty. Start shopping!",
  "order_confirmation": "Your order #{orderId} has been placed on {date}."
}
```

**Output:**

```json
{
  "greeting": "Hola, {username}!",
  "items_in_cart": "Tienes {count} artículo(s) en tu carrito.",
  "checkout_button": "Proceder al pago",
  "empty_cart": "Tu carrito está vacío. ¡Empieza a comprar!",
  "order_confirmation": "Tu pedido n.º {orderId} se ha realizado el {date}."
}
```

**Translator note:** Placeholder tokens `{username}`, `{count}`, `{orderId}`, and `{date}` are preserved exactly. The informal "tú" form is used; switch to "usted" for formal contexts.

## Best Practices

- **Preserve formatting and structure.** Never strip Markdown, HTML tags, or JSON keys during translation. The translated output must be drop-in compatible with the source format.
- **Maintain terminology consistency.** Use the same translated term for a given source term throughout the entire document. Build a glossary at the start and reference it continuously.
- **Respect formality registers.** Languages like Japanese, Korean, German, and Spanish have distinct formal and informal modes. Always confirm the desired register before translating.
- **Handle pluralization rules.** Many languages have complex plural forms (e.g., Arabic has six). When translating UI strings with count-dependent text, account for the target language's pluralization system.
- **Avoid literal translation of idioms.** Phrases like "hit the ground running" or "low-hanging fruit" should be replaced with equivalent expressions in the target language, not translated word-for-word.
- **Annotate ambiguous choices.** When a source term has multiple valid translations, include a brief note explaining the chosen translation and alternatives.

## Edge Cases

- **Untranslatable terms:** Some technical terms (e.g., "API," "OAuth," "webhook") have no standard translation in certain languages. Keep them in the original language and note this decision.
- **Right-to-left languages:** When translating to Arabic, Hebrew, or Persian, ensure that mixed-direction text (e.g., English brand names within Arabic sentences) is handled with proper bidirectional markers.
- **Character encoding:** CJK languages may cause string length issues in fixed-width UI fields. Flag any translations that significantly exceed the source string's character count.
- **Gender-neutral language:** Some target languages require grammatical gender. When the source is gender-neutral, ask the user for guidance or provide both gendered variants.
- **Empty or placeholder source text:** If the source contains only placeholders or empty strings, return them unchanged and note that no translation was needed.
