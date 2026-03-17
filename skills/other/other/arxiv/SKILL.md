---
name: arxiv
description: Search, download, and summarize academic papers from arXiv. Built for AI/ML researchers.
---

# arXiv Research Assistant

Search, fetch, and analyze academic papers from arXiv.org directly from your AI assistant.

## Description

This skill enables Claude to search arXiv for academic papers, fetch paper details, download PDFs, and help you stay updated with the latest research in any field.

**Perfect for:**
- Researchers staying current with literature
- Students doing literature reviews  
- Content creators finding authoritative sources
- Interview prep with cutting-edge knowledge
- Anyone building expertise in a technical field

## Usage

### Search Papers
```
"Search arXiv for LLM security attacks"
"Find recent papers on prompt injection"
"arXiv papers about transformer architecture from 2024"
```

### Get Paper Details
```
"Get arXiv paper 2401.12345"
"Summarize this arXiv paper: [URL]"
```

### Download Papers
```
"Download the PDF for arXiv 2401.12345"
```

### Track Reading List
```
"Add this paper to my reading list"
"Show my saved papers"
"Mark paper 2401.12345 as read"
```

## Examples

**Research Query:**
> "Find the top 5 papers on LLM jailbreaking from 2025"

**Response includes:**
- Paper titles with authors
- Publication dates
- Abstracts (summarized)
- Direct PDF links
- Citation counts (if available)

**Interview Prep:**
> "What are the latest papers on AI red teaming?"

**Content Creation:**
> "Find a paper I can break down for a LinkedIn post about prompt injection"

## Configuration

No API key required - arXiv API is free and open.

Optional MongoDB integration for paper tracking:
```yaml
# In your .env
MONGODB_URI=your_connection_string
MONGODB_DB_NAME=your_database
```

## Author

Created by [Ractor](https://github.com/Ractorrr)
