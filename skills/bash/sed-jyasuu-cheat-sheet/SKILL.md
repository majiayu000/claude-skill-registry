---
name: sed
description: Stream editor for text substitution, line operations, and file transformations.
---

# sed — Stream Editor

**Basic Substitution**

```bash
# Replace all occurrences of "day" with "night"
sed 's/day/night/g' file.txt

# Replace first occurrence per line
sed 's/day/night/' file.txt

# Preview substitution without changes
sed 's/Name=Xfce Session/Name=Xfce_Session/' FILE

# Edit file in-place
sed -i 's/day/night/g' file.txt

# Edit with backup
sed -i.bak 's/day/night/g' file.txt
```

**Special Characters & Delimiters**

```bash
# Escape slashes in paths
sed -i 's/\/path\/to\/somewhere\//\/path\/to\/anotherplace\//' FILE

# Use pipe as delimiter to avoid escaping slashes
sed -i 's|/path/to/somewhere/|/path/to/anotherplace/|' FILE

# Replace tabs with 4 spaces
sed -i 's/\t/    /g' FILE
```

**Line Operations**

```bash
# Print 2nd line
sed -n '2p' FILE

# Print lines from 2 to 9
sed -n '2,9p' FILE

# Print last line
sed -n '$p' FILE

# Print line 5 and quit
sed -n '5{p;q}' FILE

# Print and quit at 3rd line
sed -n 'p;3q'

# Print lines starting from pattern until line 17
sed -n '/any/,17p' FILE

# Print between two patterns
sed -n '/strstart/,/strend/p' FILE
```

**Line Endings**

```bash
# Convert CRLF to LF (Windows to Linux)
sed -i 's/\r$//g' FILE

# Convert LF to CRLF (Linux to Windows)
sed -i 's/$/\r/' FILE

# Remove carriage return (original example)
sed -i 's/\r//g' FILE
```

**Whitespace & Formatting**

```bash
# Remove trailing spaces
sed -i -E "s/\s+$//g" FILE

# Remove leading spaces
sed -i -r 's/^\s+//g' FILE

# Remove empty lines
sed -i -E "/^\s*$/d" FILE

# Remove both leading and trailing spaces
sed -i -E 's/^\s+|\s+$//g' FILE
```

**Advanced Transformations**

```bash
# Rearrange date format YYYY-MM-DD to DD-MM-YYYY
echo '2024-01-22' | sed -E "s/([0-9]{4})-([0-9]{2})-([0-9]{2})/\3-\2-\1/"

# Anonymize MAC addresses
ifconfig | sed -E "/ether s/([0-9a-f]{2}:{0,1}){6}/00:00:00:00:00:00/g"

# Delete specific lines
sed -i '/pattern_to_match/d' file.txt

# Insert line before matching
sed -i '/pattern/i\New line text' file.txt

# Append line after matching
sed -i '/pattern/a\New line text' file.txt
```

**Multiple Commands**

```bash
# Multiple substitutions
sed -i -e 's/foo/bar/g' -e 's/baz/qux/g' file.txt

# Use semicolon for multiple commands
sed -i 's/a/b/; s/c/d/' file.txt

# Read commands from file
sed -i -f script.sed file.txt
```

**In-Place Examples**

```bash
# Delete lines 1-5
sed -i '1,5d' file.txt

# Delete lines containing "pattern"
sed -i '/pattern/d' file.txt

# Delete blank lines
sed -i '/^$/d' file.txt

# Replace in all .txt files
find . -name "*.txt" -exec sed -i 's/old/new/g' {} \;
```