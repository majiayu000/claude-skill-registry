"""
SKILL.md file parser
Extracts metadata and content from SKILL.md files
"""

import re
import yaml
from typing import Optional
from .config import CATEGORY_KEYWORDS


class SkillParser:
    """Parse SKILL.md files and extract metadata"""

    @staticmethod
    def parse_frontmatter(content: str) -> dict:
        """Extract YAML frontmatter from SKILL.md"""
        frontmatter = {}

        # Match YAML frontmatter between ---
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1)) or {}
            except yaml.YAMLError:
                pass

        return frontmatter

    @staticmethod
    def extract_title(content: str) -> Optional[str]:
        """Extract title from first # heading"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return None

    @staticmethod
    def extract_description(content: str) -> Optional[str]:
        """Extract description from content"""
        # Remove frontmatter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

        # Try to find first paragraph after title
        lines = content.strip().split('\n')
        description_lines = []

        found_title = False
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                found_title = True
                continue
            if found_title and line and not line.startswith('#'):
                description_lines.append(line)
                if len(' '.join(description_lines)) > 100:
                    break
            elif found_title and not line and description_lines:
                break

        if description_lines:
            desc = ' '.join(description_lines)
            # Truncate to 200 chars
            if len(desc) > 200:
                desc = desc[:197] + '...'
            return desc

        return None

    @staticmethod
    def extract_tags(content: str, name: str) -> list:
        """Extract tags from content"""
        tags = set()

        # Add tags from name
        name_parts = re.split(r'[-_]', name.lower())
        tags.update(name_parts)

        # Find common keywords in content
        content_lower = content.lower()
        common_tags = [
            'react', 'vue', 'svelte', 'angular', 'nextjs', 'typescript', 'javascript',
            'python', 'rust', 'go', 'java', 'kotlin', 'swift', 'ruby', 'php',
            'docker', 'kubernetes', 'aws', 'gcp', 'azure', 'terraform',
            'postgresql', 'mongodb', 'redis', 'mysql', 'sqlite',
            'git', 'github', 'gitlab', 'ci', 'cd', 'devops',
            'testing', 'tdd', 'jest', 'pytest', 'playwright', 'cypress',
            'api', 'rest', 'graphql', 'grpc', 'websocket',
            'mcp', 'claude', 'ai', 'llm', 'agent', 'automation',
        ]

        for tag in common_tags:
            if tag in content_lower:
                tags.add(tag)

        return list(tags)[:10]  # Limit to 10 tags

    @staticmethod
    def detect_category(name: str, description: str, tags: list) -> str:
        """Detect category based on name, description, and tags"""
        text = f"{name} {description} {' '.join(tags)}".lower()

        # Score each category
        scores = {}
        for category, keywords in CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[category] = score

        if scores:
            return max(scores, key=scores.get)

        return "development"  # Default category

    def parse(self, content: str, repo: str, path: str) -> dict:
        """Parse SKILL.md and return skill metadata"""
        frontmatter = self.parse_frontmatter(content)

        # Extract skill name from path or frontmatter
        name = frontmatter.get('name') or frontmatter.get('title')
        if not name:
            # Get from path: skills/my-skill/SKILL.md -> my-skill
            parts = path.rstrip('/').split('/')
            if 'SKILL.md' in parts:
                parts.remove('SKILL.md')
            name = parts[-1] if parts else 'unknown'

        # Clean name
        name = name.lower().replace(' ', '-')

        # Extract description
        description = frontmatter.get('description') or self.extract_description(content)
        if not description:
            description = f"Skill from {repo}"

        # Extract tags
        tags = frontmatter.get('tags', [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',')]
        tags = tags or self.extract_tags(content, name)

        # Detect category
        category = frontmatter.get('category') or self.detect_category(name, description, tags)

        # Build skill path (remove SKILL.md from path)
        skill_path = path.replace('/SKILL.md', '').replace('SKILL.md', '').strip('/')

        return {
            'name': name,
            'repo': repo,
            'path': skill_path,
            'description': description,
            'category': category,
            'tags': tags,
            'stars': 0,  # Will be filled by crawler
        }
