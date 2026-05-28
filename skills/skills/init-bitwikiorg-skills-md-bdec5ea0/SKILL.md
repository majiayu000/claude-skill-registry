---
description: Imported skill __init__ from agentskills
name: __init__
signature: a3da705c4847ac19c016f67e3a6c56a94e160986a823d148c21dca4c9b312b4a
source: /a0/tmp/skills_research/agentskills/skills-ref/src/skills_ref/__init__.py
---

"""Reference library for Agent Skills."""

from .errors import ParseError, SkillError, ValidationError
from .models import SkillProperties
from .parser import find_skill_md, read_properties
from .prompt import to_prompt
from .validator import validate

__all__ = [
    "SkillError",
    "ParseError",
    "ValidationError",
    "SkillProperties",
    "find_skill_md",
    "validate",
    "read_properties",
    "to_prompt",
]

__version__ = "0.1.0"
