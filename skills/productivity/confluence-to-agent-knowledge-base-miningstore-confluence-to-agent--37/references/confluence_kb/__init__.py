"""
confluence-kb: Turn Confluence spaces into LLM-powered company knowledge bases.

Inspired by Karpathy's LLM knowledge base approach:
  raw data → LLM-compiled wiki → queryable knowledge base

Usage:
  ckb init                    # Initialize a new knowledge base config
  ckb ingest                  # Pull Confluence pages into raw/
  ckb compile                 # LLM compiles raw/ into wiki/
  ckb query "your question"   # Ask questions against the wiki
  ckb search "search terms"   # Full-text search the wiki
  ckb lint                    # Health check the wiki
  ckb status                  # Show sync status
"""

__version__ = "0.1.0"
