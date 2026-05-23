---
name: writer
description: Iterative writing loop. Gemini 3 Pro writes, Claude Agent SDK reviews autonomously. Use for blog posts, docs, technical content needing quality iteration.
---

# Writer Skill

Iterative writing loop that combines Gemini 3 Pro's writing capabilities with Claude's review.

## Flow

1. User provides topic/context
2. Gemini 3 Pro writes draft
3. Claude Agent SDK reviews autonomously
4. If not approved, Gemini rewrites with feedback
5. Loop until approved (max 15 iterations)
6. DeepL improves grammar/style (if API key set)
7. Claude merges DeepL suggestions (preserves code, markdown, technical terms)

## Usage

```bash
shelve run --project Personal -- npx tsx ~/.claude/skills/writer/scripts/write-loop.ts "Write a blog post about Vue 3 composition API"
```

With context file:
```bash
shelve run --project Personal -- npx tsx ~/.claude/skills/writer/scripts/write-loop.ts "Write docs for this component" --context ./Component.vue
```

## Environment Variables

Use `shelve` skill to manage env vars in project "Personal":

- `GOOGLE_AI_KEY_1` - Primary Google AI API key
- `GOOGLE_AI_KEY_2` - Secondary key (quota rotation)
- `GOOGLE_AI_KEY_3` - Tertiary key (quota rotation)
- `DEEPL_API_KEY` - DeepL API key (for grammar step, optional)

## Options

### Templates

- `post` - Technical blog post (default)
- `doc` - Documentation
- `github-issue` - GitHub issue

```bash
shelve run --project Personal -- npx tsx ~/.claude/skills/writer/scripts/write-loop.ts --template doc "Vue composable docs"
```

### Model

- `--model pro` - Gemini 3 Pro (default, faster)
- `--model pro-think` - Gemini 3 Pro with thinking mode (slower, better quality)

```bash
shelve run --project Personal -- npx tsx ~/.claude/skills/writer/scripts/write-loop.ts --model pro-think "Complex technical post"
```

### Resume

If interrupted, resume from last state:

```bash
shelve run --project Personal -- npx tsx ~/.claude/skills/writer/scripts/write-loop.ts --resume
```

State saved to `.writer-state.json` after each iteration.

### Grammar Options

- `--no-grammar` - Skip DeepL grammar step
- `--style, -s` - Writing style: academic|business|casual|simple
- `--tone, -o` - Tone: confident|diplomatic|enthusiastic|friendly
- `--lang, -l` - Target language (default: en-US)
- `--max-iterations, -m` - Max iterations (default: 15)

Default styles per template:
- `post`: business + friendly
- `doc`: simple + confident
- `github-issue`: business + diplomatic

```bash
# Custom style/tone
shelve run --project Personal -- npx tsx ~/.claude/skills/writer/scripts/write-loop.ts --style casual --tone enthusiastic "Fun intro to TypeScript"

# Skip grammar step
shelve run --project Personal -- npx tsx ~/.claude/skills/writer/scripts/write-loop.ts --no-grammar "Quick draft"
```
