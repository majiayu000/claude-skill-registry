---
name: funurl
description: Parse, modify, encode, decode, and deduplicate URLs from the command line. Use when the user needs to extract URL components, manipulate URLs, encode/decode URL strings, or deduplicate URL lists for security testing or web automation.
---

# funURL - A Functional URL Swiss Army Knife

funURL is a CLI tool for parsing, validating, modifying, encoding/decoding, and deduplicating URLs.

## Installation

### .NET Tool

```bash
dotnet tool install --global funurl
```

### Binary Download

Download from [Releases](https://github.com/HappyHackingSpace/funURL/releases) for Linux, macOS, or Windows (x64 and ARM64).

## Commands

### URL Parsing

Extract specific components from a URL:

```bash
# Parse all URL components
funurl parse https://subdomain.example.com/path?query=value#fragment

# Extract specific components
funurl parse -c https://example.com          # protocol/scheme
funurl parse -s https://sub.example.com      # subdomain
funurl parse -t https://example.com          # top-level domain
funurl parse -n https://example.com          # hostname
funurl parse -p https://example.com/path     # path
funurl parse -q https://example.com/?k=v     # query parameters
funurl parse -f https://example.com/#section # fragment
```

### URL Modification

```bash
# Change protocol
funurl modify -c https http://example.com

# Update path
funurl modify -p /new/path https://example.com/old/path

# Change query string
funurl modify -q "key1=val1&key2=val2" https://example.com?old=param

# Update fragment
funurl modify -f "new-section" https://example.com#old-section
```

### URL Encoding

```bash
# Path-encode
funurl encode "hello world"

# Query component encoding
funurl encode -c "param=value with spaces"
```

### URL Decoding

```bash
# Path-decode
funurl decode "hello%20world"

# Query component decoding
funurl decode -c "param%3Dvalue%20with%20spaces"
```

### URL Deduplication

```bash
# Deduplicate from arguments
funurl dedupe https://google.com https://google.com/home?qs=value https://google.com/home?qs=secondValue

# Deduplicate from stdin
cat urls.txt | funurl dedupe
```

## Input Methods

1. Via command-line argument: `funurl parse https://example.com`
2. Via stdin (pipe): `echo "https://example.com" | funurl parse`
3. Via interactive input: `funurl parse` then type URL and press Enter

## References

- Repository: https://github.com/HappyHackingSpace/funURL
