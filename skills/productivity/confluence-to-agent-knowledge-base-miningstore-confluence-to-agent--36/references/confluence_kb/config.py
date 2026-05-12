"""
Configuration management for confluence-kb.

Supports multi-company setups via YAML config files.
Each company gets its own config with Confluence connection details,
space selections, and compilation preferences.
"""

from __future__ import annotations

import os
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


DEFAULT_CONFIG_NAME = "ckb-config.yaml"


@dataclass
class ConfluenceConfig:
    """Confluence connection settings."""
    url: str  # e.g. "https://miningstore.atlassian.net"
    email: str  # API token email
    api_token: str  # Confluence API token
    cloud_id: Optional[str] = None  # Auto-resolved if not set


@dataclass
class SpaceConfig:
    """Configuration for which spaces to ingest."""
    include: list[str] = field(default_factory=list)  # Space keys to include (empty = all)
    exclude: list[str] = field(default_factory=list)  # Space keys to exclude
    include_archived: bool = False  # Whether to include archived spaces
    include_personal: bool = False  # Whether to include personal spaces


@dataclass
class CompileConfig:
    """LLM compilation settings."""
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096
    # How to organize the compiled wiki
    categories: list[str] = field(default_factory=lambda: [
        "processes",
        "policies",
        "teams",
        "projects",
        "technical",
        "meetings",
        "onboarding",
        "general",
    ])
    # Minimum page content length to include (skip near-empty pages)
    min_content_length: int = 50
    # Whether to generate concept articles linking related content
    generate_concepts: bool = True
    # Whether to generate cross-references and backlinks
    generate_backlinks: bool = True


@dataclass
class KBConfig:
    """Top-level knowledge base configuration."""
    company_name: str
    company_description: str = ""
    confluence: ConfluenceConfig = field(default_factory=lambda: ConfluenceConfig(
        url="", email="", api_token=""
    ))
    spaces: SpaceConfig = field(default_factory=SpaceConfig)
    compile: CompileConfig = field(default_factory=CompileConfig)
    # Paths (relative to config file location)
    raw_dir: str = "raw"
    wiki_dir: str = "wiki"
    output_dir: str = "output"
    # Anthropic API key (can also be set via ANTHROPIC_API_KEY env var)
    anthropic_api_key: str = ""

    @property
    def effective_anthropic_key(self) -> str:
        return self.anthropic_api_key or os.environ.get("ANTHROPIC_API_KEY", "")


def load_config(config_path: Path) -> KBConfig:
    """Load configuration from a YAML file."""
    with open(config_path, "r") as f:
        raw = yaml.safe_load(f)

    if not raw:
        raise ValueError(f"Empty config file: {config_path}")

    confluence_raw = raw.get("confluence", {})
    # Support env var references in config
    confluence = ConfluenceConfig(
        url=_resolve_env(confluence_raw.get("url", "")),
        email=_resolve_env(confluence_raw.get("email", "")),
        api_token=_resolve_env(confluence_raw.get("api_token", "")),
        cloud_id=confluence_raw.get("cloud_id"),
    )

    spaces_raw = raw.get("spaces", {})
    spaces = SpaceConfig(
        include=spaces_raw.get("include", []),
        exclude=spaces_raw.get("exclude", []),
        include_archived=spaces_raw.get("include_archived", False),
        include_personal=spaces_raw.get("include_personal", False),
    )

    compile_raw = raw.get("compile", {})
    compile_cfg = CompileConfig(
        model=compile_raw.get("model", "claude-sonnet-4-20250514"),
        max_tokens=compile_raw.get("max_tokens", 4096),
        categories=compile_raw.get("categories", CompileConfig().categories),
        min_content_length=compile_raw.get("min_content_length", 50),
        generate_concepts=compile_raw.get("generate_concepts", True),
        generate_backlinks=compile_raw.get("generate_backlinks", True),
    )

    return KBConfig(
        company_name=raw.get("company_name", "Unknown Company"),
        company_description=raw.get("company_description", ""),
        confluence=confluence,
        spaces=spaces,
        compile=compile_cfg,
        raw_dir=raw.get("raw_dir", "raw"),
        wiki_dir=raw.get("wiki_dir", "wiki"),
        output_dir=raw.get("output_dir", "output"),
        anthropic_api_key=_resolve_env(raw.get("anthropic_api_key", "")),
    )


def save_config(config: KBConfig, config_path: Path) -> None:
    """Save configuration to a YAML file."""
    data = {
        "company_name": config.company_name,
        "company_description": config.company_description,
        "confluence": {
            "url": config.confluence.url,
            "email": config.confluence.email,
            "api_token": "${CONFLUENCE_API_TOKEN}",  # Never save raw tokens
            "cloud_id": config.confluence.cloud_id,
        },
        "spaces": {
            "include": config.spaces.include,
            "exclude": config.spaces.exclude,
            "include_archived": config.spaces.include_archived,
            "include_personal": config.spaces.include_personal,
        },
        "compile": {
            "model": config.compile.model,
            "max_tokens": config.compile.max_tokens,
            "categories": config.compile.categories,
            "min_content_length": config.compile.min_content_length,
            "generate_concepts": config.compile.generate_concepts,
            "generate_backlinks": config.compile.generate_backlinks,
        },
        "raw_dir": config.raw_dir,
        "wiki_dir": config.wiki_dir,
        "output_dir": config.output_dir,
        "anthropic_api_key": "${ANTHROPIC_API_KEY}",
    }

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def _resolve_env(value: str) -> str:
    """Resolve ${ENV_VAR} references in config values."""
    if not isinstance(value, str):
        return value
    if value.startswith("${") and value.endswith("}"):
        env_var = value[2:-1]
        return os.environ.get(env_var, "")
    return value
