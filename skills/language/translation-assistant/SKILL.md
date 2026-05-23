---
name: Translation Assistant
slug: translation-assistant
description: Handle multilingual translation tasks with quality and cultural sensitivity
category: ai-ml
complexity: intermediate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "translate text"
  - "translation"
  - "multilingual"
  - "language translation"
  - "localization"
tags:
  - translation
  - multilingual
  - NLP
  - localization
  - language
---

# Translation Assistant

The Translation Assistant skill guides you through implementing multilingual translation systems that bridge language barriers accurately and culturally appropriately. From simple phrase translation to full document localization, this skill covers the spectrum of translation needs.

Modern translation has been transformed by neural machine translation and large language models, but effective translation still requires understanding context, domain, and cultural nuances. This skill helps you choose the right tools, handle translation quality, and build systems that work across languages.

Whether you're translating user interfaces, customer communications, technical documentation, or creative content, this skill ensures your translations are accurate, natural, and culturally appropriate.

## Core Workflows

### Workflow 1: Choose Translation Approach
1. **Assess** requirements:
   - Language pairs needed
   - Domain specificity
   - Quality requirements
   - Volume and speed needs
   - Budget constraints
2. **Compare** options:
   | Approach | Quality | Speed | Cost | Best For |
   |----------|---------|-------|------|----------|
   | Google Translate API | Good | Fast | $ | General, high volume |
   | DeepL | Very good | Fast | $$ | European languages, quality |
   | OpenAI/Anthropic | Excellent | Medium | $$$ | Nuanced, context-heavy |
   | Custom NMT | Domain-specific | Fast | Setup cost | Specialized domains |
   | Human + MT | Best | Slow | $$$$ | Critical content |
3. **Select** based on tradeoffs
4. **Plan** quality assurance process

### Workflow 2: Implement Translation Pipeline
1. **Set up** translation service:
   ```python
   from google.cloud import translate_v2 as translate

   class TranslationPipeline:
       def __init__(self, provider="google"):
           if provider == "google":
               self.client = translate.Client()
           elif provider == "deepl":
               self.client = deepl.Translator(auth_key)
           elif provider == "llm":
               self.client = LLMTranslator()

       def translate(self, text, source_lang, target_lang):
           # Preprocess
           prepared = self.preprocess(text, source_lang)

           # Translate
           if self.provider == "google":
               result = self.client.translate(
                   prepared,
                   source_language=source_lang,
                   target_language=target_lang
               )
               translated = result["translatedText"]
           elif self.provider == "llm":
               translated = self.llm_translate(prepared, source_lang, target_lang)

           # Postprocess
           final = self.postprocess(translated, target_lang)

           return final
   ```
2. **Handle** special content:
   - Preserve placeholders and variables
   - Handle HTML/markup
   - Maintain formatting
3. **Validate** translation quality
4. **Add** caching for repeated content

### Workflow 3: Build Localization System
1. **Extract** translatable content:
   ```python
   def extract_strings(source_files):
       """Extract strings needing translation."""
       strings = []
       for file in source_files:
           # Find translatable strings
           content = read_file(file)
           matches = find_translatable(content)

           for match in matches:
               strings.append({
                   "key": generate_key(match),
                   "source": match.text,
                   "context": match.surrounding_context,
                   "file": file,
                   "line": match.line
               })

       return strings
   ```
2. **Translate** with context:
   ```python
   def translate_with_context(strings, target_lang):
       results = []
       for s in strings:
           translation = translate(
               text=s["source"],
               context=s["context"],
               target_lang=target_lang
           )
           results.append({
               **s,
               "translation": translation,
               "target_lang": target_lang
           })
       return results
   ```
3. **Store** in translation management:
   - Translation memory for consistency
   - Glossary for terminology
   - Version control for changes
4. **Deploy** localized content

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Translate text | "Translate [text] to [language]" |
| Choose service | "Best translation for [use case]" |
| Handle domain terms | "Translation glossary for [domain]" |
| Quality check | "Check translation quality" |
| Localize app | "Localize UI for [languages]" |
| Batch translate | "Translate [N] documents" |

## Best Practices

- **Provide Context**: Translation quality depends on context
  - Include surrounding text
  - Specify domain/subject matter
  - Note tone and register (formal/informal)

- **Maintain Terminology Consistency**: Key terms should translate consistently
  - Build domain glossaries
  - Use translation memory
  - Review terminology with stakeholders

- **Preserve Formatting and Variables**: Technical content has special needs
  - Protect placeholders ({name}, %s, etc.)
  - Maintain HTML/markdown structure
  - Handle number and date formats

- **Handle Untranslatable Content**: Some things shouldn't be translated
  - Brand names and trademarks
  - Technical identifiers and codes
  - Legal disclaimers (sometimes)

- **Quality Assurance is Essential**: Machine translation makes mistakes
  - Back-translation for verification
  - Native speaker review
  - Automated quality checks

- **Consider Cultural Adaptation**: Translation != localization
  - Date and number formats
  - Currency and units
  - Cultural references and idioms
  - Right-to-left languages

## Advanced Techniques

### LLM-Based Contextual Translation
Use language models for nuanced translation:
```python
def llm_translate(text, source_lang, target_lang, context=None, style=None):
    prompt = f"""Translate the following text from {source_lang} to {target_lang}.

{"Context: " + context if context else ""}
{"Style: " + style if style else ""}

Important guidelines:
- Maintain the meaning and tone of the original
- Use natural, fluent {target_lang}
- Preserve any formatting, placeholders, or special characters
- If there are cultural references, adapt them appropriately

Source text:
{text}

Translation:"""

    return llm.complete(prompt)

# Example with context
result = llm_translate(
    text="The app crashed when I clicked submit.",
    source_lang="English",
    target_lang="Japanese",
    context="This is a bug report from a user",
    style="Formal technical support"
)
```

### Translation Memory System
Reuse previous translations for consistency:
```python
class TranslationMemory:
    def __init__(self):
        self.memory = {}  # source -> {lang: translation}
        self.fuzzy_index = FuzzyMatcher()

    def add(self, source, target_lang, translation):
        if source not in self.memory:
            self.memory[source] = {}
        self.memory[source][target_lang] = translation
        self.fuzzy_index.add(source)

    def lookup(self, source, target_lang, fuzzy_threshold=0.8):
        # Exact match
        if source in self.memory and target_lang in self.memory[source]:
            return {
                "match_type": "exact",
                "translation": self.memory[source][target_lang],
                "confidence": 1.0
            }

        # Fuzzy match
        matches = self.fuzzy_index.search(source, threshold=fuzzy_threshold)
        if matches:
            best = matches[0]
            if target_lang in self.memory[best.text]:
                return {
                    "match_type": "fuzzy",
                    "original_source": best.text,
                    "translation": self.memory[best.text][target_lang],
                    "confidence": best.score
                }

        return None

    def translate_with_memory(self, text, target_lang):
        # Check memory first
        cached = self.lookup(text, target_lang)
        if cached and cached["confidence"] > 0.95:
            return cached["translation"]

        # Translate fresh
        translation = translate_api(text, target_lang)

        # Store in memory
        self.add(text, target_lang, translation)

        return translation
```

### Domain Glossary Management
Ensure consistent terminology:
```python
class TranslationGlossary:
    def __init__(self, domain):
        self.domain = domain
        self.terms = {}  # source_term -> {lang: translated_term}

    def add_term(self, source, translations):
        self.terms[source.lower()] = translations

    def apply_to_translation(self, source_text, target_lang, translation):
        """
        Ensure glossary terms are used correctly in translation.
        """
        corrections = []
        source_lower = source_text.lower()

        for term, translations in self.terms.items():
            if term in source_lower and target_lang in translations:
                expected = translations[target_lang]
                if expected.lower() not in translation.lower():
                    corrections.append({
                        "source_term": term,
                        "expected": expected,
                        "found": False
                    })

        if corrections:
            # Re-translate with glossary enforcement
            return self.translate_with_glossary(source_text, target_lang)

        return translation

    def translate_with_glossary(self, text, target_lang):
        glossary_context = "\n".join([
            f"'{term}' should be translated as '{trans[target_lang]}'"
            for term, trans in self.terms.items()
            if target_lang in trans
        ])

        prompt = f"""Translate to {target_lang}, using these required terms:
{glossary_context}

Text: {text}"""

        return llm.complete(prompt)
```

### Quality Estimation
Automatically assess translation quality:
```python
def estimate_translation_quality(source, translation, source_lang, target_lang):
    """
    Estimate translation quality without reference translation.
    """
    checks = []

    # Check 1: Back-translation similarity
    back_translated = translate(translation, target_lang, source_lang)
    back_similarity = compute_similarity(source, back_translated)
    checks.append({
        "check": "back_translation",
        "score": back_similarity,
        "details": {"back_translated": back_translated}
    })

    # Check 2: Length ratio (translations should be similar length)
    length_ratio = len(translation) / max(len(source), 1)
    expected_ratio = get_expected_length_ratio(source_lang, target_lang)
    length_score = 1 - abs(length_ratio - expected_ratio) / expected_ratio
    checks.append({
        "check": "length_ratio",
        "score": max(0, length_score),
        "details": {"ratio": length_ratio, "expected": expected_ratio}
    })

    # Check 3: LLM quality assessment
    quality_prompt = f"""Rate this translation from 1-10 for accuracy and fluency.

Source ({source_lang}): {source}
Translation ({target_lang}): {translation}

Provide scores and brief explanation."""

    llm_assessment = llm.complete(quality_prompt)
    checks.append({
        "check": "llm_assessment",
        "score": parse_score(llm_assessment) / 10,
        "details": {"assessment": llm_assessment}
    })

    # Combined score
    overall = sum(c["score"] for c in checks) / len(checks)

    return {
        "overall_score": overall,
        "checks": checks,
        "recommendation": "accept" if overall > 0.8 else "review"
    }
```

### Batch Translation with Consistency
Translate large volumes while maintaining consistency:
```python
async def batch_translate_consistent(texts, target_lang, batch_size=50):
    """
    Translate many texts while maintaining terminology consistency.
    """
    # Step 1: Extract unique terms for glossary
    all_text = " ".join(texts)
    key_terms = extract_key_terms(all_text)

    # Step 2: Translate key terms first for consistency
    term_translations = {}
    for term in key_terms:
        translation = await translate_with_verification(term, target_lang)
        term_translations[term] = translation

    # Step 3: Batch translate with glossary context
    results = []
    for batch in chunk(texts, batch_size):
        batch_results = await asyncio.gather(*[
            translate_with_glossary(text, target_lang, term_translations)
            for text in batch
        ])
        results.extend(batch_results)

    return results
```

## Common Pitfalls to Avoid

- Translating without context, leading to wrong word choices
- Inconsistent terminology across a project
- Not handling placeholders and variables correctly
- Ignoring cultural differences (dates, currencies, idioms)
- Trusting machine translation without quality checks
- Not maintaining translation memory for consistency
- Forgetting about text expansion (translations are often longer)
- Ignoring right-to-left language considerations
