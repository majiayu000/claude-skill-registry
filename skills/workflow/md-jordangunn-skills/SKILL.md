---
name: md
description: >
  Orchestrates markdown chunking workflows (split → index → summary)
metadata:
  author: Jordan Godau
  version: 0.1.0
  keywords:
    - markdown
    - split
    - index
    - summary
    - docs
    - progressive-disclosure
  skillset:
    name: md
    schema_version: 1
    skills:
      - md-split
    pipelines:
      default:
        - md-split
      allowed:
        - [md-split]
---
