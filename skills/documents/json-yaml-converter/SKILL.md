---
name: json-yaml-converter
description: 在JSON、YAML和TOML格式之间转换，验证和格式化配置文件。
metadata:
  short-description: 转换JSON/YAML/TOML格式
source:
  repository: https://github.com/yaml/pyyaml
  license: MIT
---

# JSON/YAML Converter Tool

## Description
Convert between JSON, YAML, and TOML formats with validation and formatting.

## Trigger
- `/convert-config` command
- User requests format conversion
- User needs to validate JSON/YAML

## Usage

```bash
# Convert JSON to YAML
python scripts/json_yaml_converter.py convert --input config.json --output config.yaml

# Convert YAML to JSON
python scripts/json_yaml_converter.py convert --input config.yaml --output config.json

# Validate file
python scripts/json_yaml_converter.py validate --input config.yaml

# Format/prettify
python scripts/json_yaml_converter.py format --input config.json --indent 2
```

## Tags
`json`, `yaml`, `toml`, `config`, `convert`

## Compatibility
- Codex: ✅
- Claude Code: ✅
