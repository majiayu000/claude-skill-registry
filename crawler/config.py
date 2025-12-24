"""
Crawler configuration
"""

# GitHub API settings
GITHUB_API_BASE = "https://api.github.com"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"

# Search queries for finding SKILL.md files
SEARCH_QUERIES = [
    "filename:SKILL.md",
    "filename:SKILL.md claude",
    "filename:SKILL.md skills",
    "path:.claude/skills SKILL.md",
    "path:skills SKILL.md",
]

# Rate limiting
REQUESTS_PER_MINUTE = 30  # GitHub API rate limit for authenticated requests
REQUEST_DELAY = 2.0  # Seconds between requests

# Quality filters
MIN_STARS = 0  # Minimum stars to include (0 = include all)
MIN_RECENT_DAYS = 365  # Include repos updated within this many days

# Categories mapping based on keywords
CATEGORY_KEYWORDS = {
    "development": ["code", "dev", "programming", "software", "build", "compile", "debug", "refactor"],
    "testing": ["test", "testing", "tdd", "unit", "integration", "e2e", "playwright", "cypress", "jest"],
    "data": ["data", "ml", "ai", "machine-learning", "analytics", "sql", "database", "visualization"],
    "design": ["design", "ui", "ux", "frontend", "css", "tailwind", "figma", "animation"],
    "documents": ["doc", "pdf", "docx", "xlsx", "pptx", "markdown", "documentation"],
    "productivity": ["productivity", "workflow", "automation", "task", "planning", "memory"],
    "devops": ["devops", "ci", "cd", "docker", "kubernetes", "deploy", "infrastructure"],
    "security": ["security", "audit", "vulnerability", "owasp", "pentest", "fuzzing"],
    "marketing": ["marketing", "seo", "content", "brand", "campaign", "social"],
    "product": ["product", "prd", "roadmap", "feature", "user-research", "metrics"],
}

# Output paths
OUTPUT_DIR = "sources"
CRAWLED_FILE = "crawled.json"
