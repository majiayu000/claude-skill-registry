---
name: examples-patelmm79-dev-nexus
description: '> 📢 UPDATED: This guide now uses the modular architecture (v2.0).'
---

# Adding the Documentation Review Skill (Modular v2.0)

> **📢 UPDATED**: This guide now uses the **modular architecture** (v2.0).
> Adding a skill is now much simpler - create one skill module file!

This guide shows how to integrate the documentation review skill into dev-nexus using the modular architecture.

## Prerequisites

The `core/documentation_service.py` file has already been created. Now you just need to create a skill module that uses it.

## Step 1: Create the Skill Module (3 minutes)

Create `a2a/skills/documentation.py`:

```python
"""
Documentation Review Skills

Skills for analyzing documentation quality and standards compliance.
"""

import os
from typing import Dict, Any, List
import anthropic
from github import Github

from a2a.skills.base import BaseSkill


class ReviewDocumentationSkill(BaseSkill):
    """Analyze documentation for quality, consistency, and standards adherence"""

    def __init__(self, kb_manager):
        self.kb_manager = kb_manager

    @property
    def skill_id(self) -> str:
        return "review_documentation"

    @property
    def skill_name(self) -> str:
        return "Review Documentation"

    @property
    def skill_description(self) -> str:
        return "Analyze documentation for quality, consistency, and adherence to standards. Checks completeness, clarity, examples, structure, accuracy, and formatting."

    @property
    def tags(self) -> List[str]:
        return ["documentation", "quality", "standards", "review"]

    @property
    def requires_authentication(self) -> bool:
        return False

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "repository": {
                    "type": "string",
                    "description": "Repository name in format 'owner/repo'"
                },
                "doc_paths": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Specific documentation files to review. If empty, reviews common docs (README.md, CLAUDE.md, etc.)",
                    "default": []
                },
                "standards": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["completeness", "clarity", "examples", "structure", "accuracy", "formatting"]
                    },
                    "description": "Standards to check against",
                    "default": ["completeness", "clarity", "examples", "structure"]
                }
            },
            "required": ["repository"]
        }

    @property
    def examples(self) -> List[Dict[str, Any]]:
        return [
            {
                "input": {
                    "repository": "patelmm79/dev-nexus",
                    "doc_paths": ["README.md", "CLAUDE.md"],
                    "standards": ["completeness", "clarity", "examples"]
                },
                "description": "Review main documentation files for dev-nexus"
            },
            {
                "input": {
                    "repository": "patelmm79/my-project",
                    "standards": ["completeness", "clarity", "examples", "structure", "accuracy", "formatting"]
                },
                "description": "Comprehensive review of all documentation with all standards"
            }
        ]

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review documentation for quality and standards compliance

        Input:
            - repository: str - Repository name (format: "owner/repo")
            - doc_paths: List[str] - Documentation files to review (optional)
            - standards: List[str] - Standards to check (optional)

        Output:
            - reviews: List of review results for each document
            - overall_assessment: Summary of documentation quality
        """
        try:
            from core.documentation_service import DocumentationReviewer

            repository = input_data.get('repository')
            doc_paths = input_data.get('doc_paths', [])
            standards = input_data.get('standards', ['completeness', 'clarity', 'examples', 'structure'])

            if not repository:
                return {
                    "success": False,
                    "error": "Missing required parameter: 'repository'"
                }

            # Validate standards
            valid_standards = ["completeness", "clarity", "examples", "structure", "accuracy", "formatting"]
            invalid_standards = [s for s in standards if s not in valid_standards]
            if invalid_standards:
                return {
                    "success": False,
                    "error": f"Invalid standards: {', '.join(invalid_standards)}. Valid options: {', '.join(valid_standards)}"
                }

            # Initialize reviewer
            anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')
            if not anthropic_api_key:
                return {
                    "success": False,
                    "error": "ANTHROPIC_API_KEY not configured"
                }

            reviewer = DocumentationReviewer(
                anthropic_client=anthropic.Anthropic(api_key=anthropic_api_key),
                kb_manager=self.kb_manager
            )

            # Get GitHub client
            github_token = os.environ.get('GITHUB_TOKEN')
            if not github_token:
                return {
                    "success": False,
                    "error": "GITHUB_TOKEN not configured"
                }

            github_client = Github(github_token)

            # Get repository
            try:
                repo = github_client.get_repo(repository)
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to access repository '{repository}': {str(e)}"
                }

            # If no paths specified, review common docs
            if not doc_paths:
                doc_paths = []
                common_files = ['README.md', 'CLAUDE.md', 'CONTRIBUTING.md', 'docs/README.md', 'docs/API.md']

                for filename in common_files:
                    try:
                        repo.get_contents(filename)
                        doc_paths.append(filename)
                    except:
                        pass  # File doesn't exist

                if not doc_paths:
                    return {
                        "success": False,
                        "error": "No documentation files found. Specify doc_paths explicitly."
                    }

            # Review each document
            reviews = []
            for doc_path in doc_paths:
                try:
                    # Fetch document content
                    file_content = repo.get_contents(doc_path)
                    content = file_content.decoded_content.decode('utf-8')

                    # Review document
                    review = reviewer.review_documentation(
                        repository=repository,
                        doc_content=content,
                        doc_path=doc_path,
                        standards=standards
                    )
                    reviews.append(review)

                except Exception as e:
                    reviews.append({
                        "doc_path": doc_path,
                        "error": f"Failed to review: {str(e)}",
                        "overall_score": 0.0
                    })

            # Calculate overall assessment
            successful_reviews = [r for r in reviews if 'overall_score' in r and 'error' not in r]

            if not successful_reviews:
                return {
                    "success": False,
                    "error": "All document reviews failed",
                    "reviews": reviews
                }

            total_score = sum(r['overall_score'] for r in successful_reviews)
            avg_score = total_score / len(successful_reviews)

            # Determine rating
            if avg_score >= 0.8:
                rating = "Excellent"
                rating_emoji = "✅"
            elif avg_score >= 0.6:
                rating = "Good"
                rating_emoji = "👍"
            elif avg_score >= 0.4:
                rating = "Fair"
                rating_emoji = "⚠️"
            else:
                rating = "Needs Improvement"
                rating_emoji = "❌"

            # Collect all recommendations
            all_recommendations = []
            for review in successful_reviews:
                if 'recommendations' in review:
                    all_recommendations.extend(review['recommendations'])

            return {
                "success": True,
                "repository": repository,
                "reviews": reviews,
                "overall_assessment": {
                    "average_score": round(avg_score, 2),
                    "rating": rating,
                    "rating_emoji": rating_emoji,
                    "documents_reviewed": len(successful_reviews),
                    "documents_failed": len(reviews) - len(successful_reviews),
                    "standards_checked": standards
                },
                "top_recommendations": all_recommendations[:10]  # Top 10 across all docs
            }

        except Exception as e:
            import traceback
            return {
                "success": False,
                "error": f"Failed to review documentation: {str(e)}",
                "traceback": traceback.format_exc()
            }
```

## Step 2: Register the Skill (1 minute)

Edit `a2a/server.py` and add these lines after the other skill imports (around line 33):

```python
from a2a.skills.documentation import ReviewDocumentationSkill
```

Then after the other skill registrations (around line 72):

```python
# Register documentation review skill
doc_review_skill = ReviewDocumentationSkill(kb_manager)
registry.register(doc_review_skill)
```

## Step 3: Test It! (1 minute)

**That's it!** The skill is now registered and available. No routing changes needed!

```bash
# Start server
python a2a/server.py
# Should show: "Skills registered: 8"

# Verify skill appears in AgentCard
curl http://localhost:8080/.well-known/agent.json | jq '.skills[] | select(.id == "review_documentation")'

# Test the skill
curl -X POST http://localhost:8080/a2a/execute \
  -H "Content-Type: application/json" \
  -d '{
    "skill_id": "review_documentation",
    "input": {
      "repository": "patelmm79/dev-nexus",
      "doc_paths": ["README.md", "CLAUDE.md"],
      "standards": ["completeness", "clarity", "examples", "structure"]
    }
  }' | jq
```

## Example Output

```json
{
  "success": true,
  "repository": "patelmm79/dev-nexus",
  "reviews": [
    {
      "repository": "patelmm79/dev-nexus",
      "doc_path": "CLAUDE.md",
      "reviewed_at": "2025-01-10T15:30:00",
      "standards_checked": ["completeness", "clarity", "examples", "structure"],
      "checks": {
        "completeness": {
          "score": 1.0,
          "found_sections": ["overview", "commands", "examples"],
          "missing_sections": [],
          "message": "Found 3/3 required sections"
        },
        "clarity": {
          "score": 0.85,
          "issues": ["Found 3 sentences over 40 words"],
          "message": "Clarity score: 0.85 - 1 issues found"
        }
      },
      "overall_score": 0.95,
      "recommendations": [
        "[Clarity] Break down longer sentences for better readability",
        "[Examples] Add troubleshooting section with common issues"
      ]
    }
  ],
  "overall_assessment": {
    "average_score": 0.95,
    "rating": "Excellent",
    "rating_emoji": "✅",
    "documents_reviewed": 1,
    "documents_failed": 0
  }
}
```

## Advanced: Standalone CLI Script

Create `scripts/review_docs.py`:

```python
#!/usr/bin/env python3
"""Standalone script to review documentation"""

import os
import sys
import anthropic
from github import Github

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.documentation_service import DocumentationReviewer
from core.knowledge_base import KnowledgeBaseManager

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Review repository documentation')
    parser.add_argument('repository', help='Repository in format owner/repo')
    parser.add_argument('--files', nargs='+', help='Specific files to review')
    parser.add_argument('--all-standards', action='store_true', help='Check all standards')
    args = parser.parse_args()

    # Initialize services
    anthropic_client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
    github_client = Github(os.environ['GITHUB_TOKEN'])
    kb_manager = KnowledgeBaseManager(github_client, os.environ.get('KNOWLEDGE_BASE_REPO', 'patelmm79/dev-nexus'))

    reviewer = DocumentationReviewer(anthropic_client, kb_manager)

    # Review documents
    standards = ['completeness', 'clarity', 'examples', 'structure', 'accuracy', 'formatting'] if args.all_standards else ['completeness', 'clarity', 'examples', 'structure']

    print(f"📚 Reviewing {args.repository}...")
    # ... implementation ...

if __name__ == '__main__':
    main()
```

## Key Differences from Old Approach

### Old Way (Monolithic)
1. Edit `server.py` - Add 30-60 lines to hardcoded AgentCard
2. Edit `executor.py` - Add routing elif case
3. Edit `executor.py` - Add 80+ line handler method
4. Total: Edit 2 files, ~130 lines

### New Way (Modular)
1. Create `a2a/skills/documentation.py` - All code in one place
2. Import and register in `server.py` - 2 lines
3. Total: Create 1 file, add 2 lines

**Result**: 4x simpler, self-contained, independently testable!

## Benefits of Modular Approach

1. **One File**: All skill code in `a2a/skills/documentation.py`
2. **Self-Contained**: Metadata + implementation together
3. **Auto-Discovery**: Registry handles routing automatically
4. **No Duplication**: AgentCard generated from skill properties
5. **Easy Testing**: Import and test skill directly
6. **No Conflicts**: Your skill file won't conflict with others

---

**The modular architecture makes adding skills dramatically simpler!** 🚀
