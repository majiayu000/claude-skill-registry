---
name: categorizing-bsky-accounts
description: Analyze and categorize Bluesky accounts by topic using keyword extraction. Use when users mention Bluesky account analysis, following/follower lists, topic discovery, account curation, or network analysis.
metadata:
  version: 0.2.1
---

# Categorizing Bluesky Accounts

Fetch Bluesky account data and extract keywords for Claude to categorize by topic. The script compresses account context (bio + posts) into bio + keywords, then Claude performs intelligent categorization.

## Prerequisites

**Requires:** extracting-keywords skill (provides YAKE venv + domain stopwords)

The analyzer delegates keyword extraction to the extracting-keywords skill, which provides:
- Optimized YAKE installation with minimal dependencies
- Domain-specific stopwords: English (574), AI/ML (1357), Life Sciences (1293)
- Support for 34 languages

## Core Workflow

When users request Bluesky account analysis:

1. **Ensure keyword extraction is set up** - Invoke the extracting-keywords skill using the Skill tool to ensure YAKE venv exists (skip if already invoked in this session)

2. **Determine input mode** based on user's request:
   - Following list → use `--following handle`
   - Followers → use `--followers handle`
   - List of handles → use `--handles "h1,h2,h3"`
   - File provided → use `--file accounts.txt`

3. **Configure parameters:**
   - `--accounts N` - Number to analyze (default: 100, max: 100)
   - `--posts N` - Posts per account (default: 20, max: 100)
   - `--stopwords [en|ai|ls]` - Choose domain-specific stopwords:
     - `en`: English (general purpose)
     - `ai`: AI/ML domain (recommended for tech accounts)
     - `ls`: Life Sciences (for biomedical/research accounts)
   - `--exclude "pattern1,pattern2"` - Skip spam/bot accounts

4. **Run script** - Outputs simple text format to stdout:
   ```
   @handle1.bsky.social (Display Name)
   Bio text here
   Keywords: keyword1, keyword2, keyword3

   @handle2.bsky.social (Another Name)
   Bio text here
   Keywords: keyword4, keyword5, keyword6
   ```

5. **Categorize accounts** - Claude analyzes bio + keywords to categorize by topic

## Quick Start

**Analyze following list with AI/ML stopwords:**
```bash
python scripts/bluesky_analyzer.py --following austegard.com --stopwords ai
```

**Analyze followers:**
```bash
python scripts/bluesky_analyzer.py --followers austegard.com
```

**Analyze specific handles:**
```bash
python scripts/bluesky_analyzer.py --handles "user1.bsky.social,user2.bsky.social,user3.bsky.social"
```

**From file:**
```bash
python scripts/bluesky_analyzer.py --file accounts.txt --stopwords ai
```

**Filter out bot accounts:**
```bash
python scripts/bluesky_analyzer.py --following handle --exclude "bot,spam,promo" --stopwords ai
```

## Parameters

### Input Modes (choose one)

**--handles "h1,h2,h3"**
Comma-separated list of Bluesky handles

**--following HANDLE**
Analyze accounts followed by HANDLE

**--followers HANDLE**
Analyze accounts following HANDLE

**--file PATH**
Read handles from file (one per line)

### Analysis Options

**--accounts N**
Number of accounts to analyze (1-100, default: 100)

**--posts N**
Posts to fetch per account (1-100, default: 20)

**--stopwords [en|ai|ls]**
Stopwords to use for keyword extraction (default: en)
- `en`: English stopwords (574 terms) - general purpose
- `ai`: AI/ML domain stopwords (1357 terms) - tech-focused accounts
- `ls`: Life Sciences stopwords (1293 terms) - biomedical/research accounts

**--exclude "word1,word2"**
Skip accounts with these keywords in bio/posts

## Output Format

The script outputs simple text format for Claude to process:

```
@alice.bsky.social (Alice Smith)
AI researcher working on LLM alignment and safety
Keywords: alignment, safety research, interpretability, llm evaluation

@bob.bsky.social (Bob Johnson)
Full-stack developer building web applications
Keywords: react, typescript, node.js, api design, postgresql

@carol.bsky.social (Carol Williams)
Biotech researcher studying CRISPR applications
Keywords: crispr, gene editing, therapeutics, clinical trials
```

Claude then categorizes accounts based on bio + keywords without hardcoded rules.

## Common Workflows

### Audit Your Following List

```bash
python scripts/bluesky_analyzer.py --following your-handle.bsky.social --stopwords ai
```

Claude will categorize accounts by topic and identify patterns in who you follow.

### Find Experts in a Topic

```bash
python scripts/bluesky_analyzer.py --following alice.bsky.social --stopwords ai
```

Ask Claude: "Which of these accounts are ML researchers?" or "Who focuses on climate tech?"

### Analyze a Curated List

```bash
cat > accounts.txt << 'EOF'
expert1.bsky.social
expert2.bsky.social
expert3.bsky.social
EOF

python scripts/bluesky_analyzer.py --file accounts.txt --stopwords ls
```

### Filter Out Bot Accounts

```bash
python scripts/bluesky_analyzer.py --following handle --exclude "bot,spam,promo,follow back" --stopwords ai
```

## Technical Details

### Keyword Extraction

Delegates to **extracting-keywords skill** using YAKE venv:
- **Stopwords options** (--stopwords):
  - `en`: English (574 terms) - general purpose
  - `ai`: AI/ML domain (1357 terms) - filters technical noise, ML boilerplate
  - `ls`: Life Sciences (1293 terms) - filters research methodology, clinical terms
- N-grams: 1-3 words
- Deduplication: 0.9 threshold
- Top keywords: 10 per account
- Performance: ~5% overhead with domain stopwords vs English

### API Rate Limits

Bluesky API limits:
- 3000 requests per 5 minutes
- 5000 requests per hour

The analyzer respects these limits with built-in delays.

### Categorization Algorithm

**Script's role:**
1. Fetch account data (bio + posts)
2. Extract keywords to compress context
3. Output bio + keywords in simple format

**Claude's role:**
1. Read bio + keywords for each account
2. Intelligently categorize by topic (no hardcoded rules)
3. Group accounts, identify patterns, answer user questions

This agentic pattern is more flexible than hardcoded keyword matching.

## Troubleshooting

**"No accounts to analyze"**
- Verify handle format (include domain: handle.bsky.social)
- Check if account exists and has public following/followers

**"Insufficient content for keyword extraction"**
- Account has few posts (<5)
- Posts are very short
- Try increasing `--posts` parameter

**Rate limit errors**
- Reduce `--accounts` parameter
- Add delays between batches
- Check Bluesky API status

**Import errors**
- Verify extracting-keywords skill is available
- Check YAKE venv exists: `/home/claude/yake-venv/bin/python -c "import yake"`
- Verify Python 3.8+: `python3 --version`

## Integration with Other Skills

**Built-in integration:**
- **extracting-keywords**: Automatically delegates keyword extraction to this skill's optimized YAKE venv with domain-specific stopwords

## Example Sessions

**User:** "Can you analyze the accounts I follow on Bluesky and tell me what topics they focus on?"

**Claude:**
```bash
python scripts/bluesky_analyzer.py --following user-handle.bsky.social --stopwords ai
```

Based on the output, I can see you follow:
- **AI/ML researchers** (15 accounts): Focus on LLM safety, alignment, interpretability
- **Software engineers** (20 accounts): Web development, React, TypeScript, DevOps
- **Writers** (8 accounts): Tech journalism, newsletters, long-form content
- **Scientists** (7 accounts): Climate science, biotech, physics

**User:** "Find ML researchers in @alice's network"

**Claude:**
```bash
python scripts/bluesky_analyzer.py --following alice.bsky.social --stopwords ai
```

I found 23 ML researchers in Alice's network:
- 8 working on LLM alignment and safety
- 6 focused on model evaluation and benchmarks
- 5 in ML infrastructure and MLOps
- 4 in computer vision and multimodal models

**User:** "Here's a list of 30 accounts, categorize them"

**Claude:**
```bash
python scripts/bluesky_analyzer.py --file accounts.txt --stopwords ai
```

Categorized into:
- Climate Tech (8 accounts)
- Biotech (6 accounts)
- Fintech (5 accounts)
- AI/ML (7 accounts)
- Other (4 accounts)
