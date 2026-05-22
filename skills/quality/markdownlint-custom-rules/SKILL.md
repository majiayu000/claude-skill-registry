---
name: markdownlint-custom-rules
description: Create custom linting rules for markdownlint including rule structure, parser integration, error reporting, and automatic fixing.
allowed-tools: [Bash, Read]
---

# Markdownlint Custom Rules

Master creating custom markdownlint rules including rule structure, markdown-it and micromark parser integration, error reporting with fixInfo, and asynchronous rule development.

## Overview

Markdownlint allows you to create custom rules tailored to your project's specific documentation requirements. Custom rules can enforce project-specific conventions, validate content patterns, and ensure consistency beyond what built-in rules provide.

## Rule Object Structure

### Basic Rule Definition

Every custom rule must be a JavaScript object with specific properties:

```javascript
module.exports = {
  names: ["rule-name", "RULE001"],
  description: "Description of what this rule checks",
  tags: ["custom", "style"],
  parser: "markdownit",
  function: function(params, onError) {
    // Rule implementation
  }
};
```

### Required Properties

```javascript
{
  names: Array<String>,        // Rule identifiers (required)
  description: String,         // What the rule checks (required)
  tags: Array<String>,         // Categorization tags (required)
  parser: String,              // "markdownit", "micromark", or "none" (required)
  function: Function          // Rule logic (required)
}
```

### Optional Properties

```javascript
{
  information: URL,           // Link to rule documentation
  asynchronous: Boolean      // If true, function returns Promise
}
```

## Parser Selection

### markdown-it Parser

Best for token-based parsing with rich metadata:

```javascript
module.exports = {
  names: ["any-blockquote-markdown-it"],
  description: "Rule that reports an error for any blockquote",
  information: new URL("https://example.com/rules/any-blockquote"),
  tags: ["test"],
  parser: "markdownit",
  function: (params, onError) => {
    const blockquotes = params.parsers.markdownit.tokens
      .filter((token) => token.type === "blockquote_open");

    for (const blockquote of blockquotes) {
      const [startIndex, endIndex] = blockquote.map;
      const lines = endIndex - startIndex;

      onError({
        lineNumber: blockquote.lineNumber,
        detail: `Blockquote spans ${lines} line(s).`,
        context: blockquote.line
      });
    }
  }
};
```

### micromark Parser

Best for detailed token analysis and precise positioning:

```javascript
module.exports = {
  names: ["any-blockquote-micromark"],
  description: "Rule that reports an error for any blockquote",
  information: new URL("https://example.com/rules/any-blockquote"),
  tags: ["test"],
  parser: "micromark",
  function: (params, onError) => {
    const blockquotes = params.parsers.micromark.tokens
      .filter((token) => token.type === "blockQuote");

    for (const blockquote of blockquotes) {
      const lines = blockquote.endLine - blockquote.startLine + 1;

      onError({
        lineNumber: blockquote.startLine,
        detail: `Blockquote spans ${lines} line(s).`,
        context: params.lines[blockquote.startLine - 1]
      });
    }
  }
};
```

### No Parser

For simple line-based rules:

```javascript
module.exports = {
  names: ["no-todo-comments"],
  description: "Disallow TODO comments in markdown",
  tags: ["custom"],
  parser: "none",
  function: (params, onError) => {
    params.lines.forEach((line, index) => {
      if (line.includes("TODO:") || line.includes("FIXME:")) {
        onError({
          lineNumber: index + 1,
          detail: "TODO/FIXME comments should be resolved",
          context: line.trim()
        });
      }
    });
  }
};
```

## Function Parameters

### params Object

The `params` object contains all information about the markdown content:

```javascript
function rule(params, onError) {
  // params.name - Input file/string name
  // params.lines - Array of lines (string[])
  // params.frontMatterLines - Lines of front matter
  // params.config - Rule's configuration from .markdownlint.json
  // params.version - markdownlint library version
  // params.parsers - Parser outputs
}
```

### Accessing Lines

```javascript
function: (params, onError) => {
  params.lines.forEach((line, index) => {
    const lineNumber = index + 1;  // Lines are 1-based

    if (someCondition(line)) {
      onError({
        lineNumber,
        detail: "Issue description",
        context: line.trim()
      });
    }
  });
}
```

### Using Configuration

```javascript
// In .markdownlint.json
{
  "custom-rule": {
    "max_length": 50,
    "pattern": "^[A-Z]"
  }
}

// In rule
function: (params, onError) => {
  const config = params.config || {};
  const maxLength = config.max_length || 40;
  const pattern = config.pattern ? new RegExp(config.pattern) : null;

  // Use configuration values
}
```

### Working with Front Matter

```javascript
function: (params, onError) => {
  const frontMatterLines = params.frontMatterLines;

  if (frontMatterLines.length > 0) {
    // Process YAML front matter
    const frontMatter = frontMatterLines.join('\n');
    // Validate front matter
  }
}
```

## Error Reporting with onError

### Basic Error Reporting

```javascript
onError({
  lineNumber: 5,                          // Required: 1-based line number
  detail: "Line exceeds maximum length",  // Optional: Additional info
  context: "This is the problematic..."   // Optional: Relevant text
});
```

### Error with Range

Highlight specific portion of the line:

```javascript
onError({
  lineNumber: 10,
  detail: "Invalid heading format",
  context: "### Heading",
  range: [1, 3]  // Column 1, length 3 (highlights "###")
});
```

### Error with Fix Information

Enable automatic fixing:

```javascript
onError({
  lineNumber: 15,
  detail: "Extra whitespace",
  context: "  text  ",
  fixInfo: {
    editColumn: 1,
    deleteCount: 2,
    insertText: ""
  }
});
```

## Automatic Fixing with fixInfo

### Delete Characters

```javascript
// Remove 5 characters starting at column 10
fixInfo: {
  lineNumber: 5,
  editColumn: 10,
  deleteCount: 5
}
```

### Insert Text

```javascript
// Insert text at column 1
fixInfo: {
  lineNumber: 3,
  editColumn: 1,
  insertText: "# "
}
```

### Replace Text

```javascript
// Replace 3 characters with new text
fixInfo: {
  lineNumber: 7,
  editColumn: 5,
  deleteCount: 3,
  insertText: "new"
}
```

### Delete Entire Line

```javascript
// Delete the entire line
fixInfo: {
  lineNumber: 10,
  deleteCount: -1
}
```

### Insert New Line

```javascript
// Insert a blank line
fixInfo: {
  lineNumber: 8,
  insertText: "\n"
}
```

### Multi-Line Fix

Report multiple fixes for the same violation:

```javascript
function: (params, onError) => {
  // Fix requires changes on multiple lines
  onError({
    lineNumber: 5,
    detail: "Inconsistent list markers",
    fixInfo: {
      lineNumber: 5,
      editColumn: 1,
      deleteCount: 1,
      insertText: "-"
    }
  });

  onError({
    lineNumber: 6,
    detail: "Inconsistent list markers",
    fixInfo: {
      lineNumber: 6,
      editColumn: 1,
      deleteCount: 1,
      insertText: "-"
    }
  });
}
```

## Complete Rule Examples

### Enforce Heading Capitalization

```javascript
module.exports = {
  names: ["heading-capitalization", "HC001"],
  description: "Headings must start with a capital letter",
  tags: ["headings", "custom"],
  parser: "markdownit",
  function: (params, onError) => {
    const headings = params.parsers.markdownit.tokens
      .filter(token => token.type === "heading_open");

    for (const heading of headings) {
      const headingLine = params.lines[heading.lineNumber - 1];
      const match = headingLine.match(/^#+\s+(.+)$/);

      if (match) {
        const text = match[1];
        const firstChar = text.charAt(0);

        if (firstChar !== firstChar.toUpperCase()) {
          const hashCount = headingLine.indexOf(' ');

          onError({
            lineNumber: heading.lineNumber,
            detail: "Heading must start with capital letter",
            context: headingLine,
            range: [hashCount + 2, 1],
            fixInfo: {
              editColumn: hashCount + 2,
              deleteCount: 1,
              insertText: firstChar.toUpperCase()
            }
          });
        }
      }
    }
  }
};
```

### Require Blank Line Before Headings

```javascript
module.exports = {
  names: ["blank-line-before-heading", "BLH001"],
  description: "Require blank line before headings (except first line)",
  tags: ["headings", "custom", "whitespace"],
  parser: "markdownit",
  function: (params, onError) => {
    const headings = params.parsers.markdownit.tokens
      .filter(token => token.type === "heading_open");

    for (const heading of headings) {
      const lineNumber = heading.lineNumber;

      // Skip if first line or after front matter
      if (lineNumber <= params.frontMatterLines.length + 1) {
        continue;
      }

      const previousLine = params.lines[lineNumber - 2];

      if (previousLine.trim() !== "") {
        onError({
          lineNumber: lineNumber - 1,
          detail: "Expected blank line before heading",
          context: previousLine,
          fixInfo: {
            lineNumber: lineNumber - 1,
            editColumn: previousLine.length + 1,
            insertText: "\n"
          }
        });
      }
    }
  }
};
```

### Validate Code Block Language

```javascript
module.exports = {
  names: ["code-block-language", "CBL001"],
  description: "Code blocks must specify a language",
  tags: ["code", "custom"],
  parser: "markdownit",
  function: (params, onError) => {
    const config = params.config || {};
    const allowedLanguages = config.allowed_languages || [];

    const fences = params.parsers.markdownit.tokens
      .filter(token => token.type === "fence");

    for (const fence of fences) {
      const language = fence.info.trim();

      if (!language) {
        onError({
          lineNumber: fence.lineNumber,
          detail: "Code block must specify a language",
          context: fence.line
        });
      } else if (allowedLanguages.length > 0 && !allowedLanguages.includes(language)) {
        onError({
          lineNumber: fence.lineNumber,
          detail: `Language '${language}' not in allowed list: ${allowedLanguages.join(', ')}`,
          context: fence.line
        });
      }
    }
  }
};
```

### Detect Broken Relative Links

```javascript
const fs = require('fs');
const path = require('path');

module.exports = {
  names: ["no-broken-links", "NBL001"],
  description: "Detect broken relative links",
  tags: ["links", "custom"],
  parser: "markdownit",
  asynchronous: true,
  function: async (params, onError) => {
    const links = params.parsers.markdownit.tokens
      .filter(token => token.type === "link_open");

    for (const link of links) {
      const hrefToken = link.attrs.find(attr => attr[0] === "href");

      if (hrefToken) {
        const href = hrefToken[1];

        // Only check relative links
        if (!href.startsWith('http://') && !href.startsWith('https://')) {
          const filePath = path.join(path.dirname(params.name), href);

          try {
            await fs.promises.access(filePath);
          } catch (err) {
            onError({
              lineNumber: link.lineNumber,
              detail: `Broken link: ${href}`,
              context: link.line
            });
          }
        }
      }
    }
  }
};
```

### Enforce Consistent List Markers

```javascript
module.exports = {
  names: ["consistent-list-markers", "CLM001"],
  description: "Lists must use consistent markers within the same level",
  tags: ["lists", "custom"],
  parser: "micromark",
  function: (params, onError) => {
    const lists = params.parsers.micromark.tokens
      .filter(token => token.type === "listUnordered");

    for (const list of lists) {
      const items = params.parsers.micromark.tokens.filter(
        token => token.type === "listItemMarker" &&
                 token.startLine >= list.startLine &&
                 token.endLine <= list.endLine
      );

      if (items.length > 0) {
        const firstMarker = params.lines[items[0].startLine - 1]
          .charAt(items[0].startColumn - 1);

        for (const item of items.slice(1)) {
          const marker = params.lines[item.startLine - 1]
            .charAt(item.startColumn - 1);

          if (marker !== firstMarker) {
            onError({
              lineNumber: item.startLine,
              detail: `Inconsistent list marker: expected '${firstMarker}', found '${marker}'`,
              context: params.lines[item.startLine - 1],
              range: [item.startColumn, 1],
              fixInfo: {
                editColumn: item.startColumn,
                deleteCount: 1,
                insertText: firstMarker
              }
            });
          }
        }
      }
    }
  }
};
```

## Asynchronous Rules

### Basic Async Rule

```javascript
module.exports = {
  names: ["async-rule-example"],
  description: "Example asynchronous rule",
  tags: ["async", "custom"],
  parser: "none",
  asynchronous: true,
  function: async (params, onError) => {
    // Can use await
    const result = await someAsyncOperation();

    if (!result.valid) {
      onError({
        lineNumber: 1,
        detail: "Async validation failed"
      });
    }

    // Must return Promise (implicitly returned by async function)
  }
};
```

### Network Validation

```javascript
const https = require('https');

module.exports = {
  names: ["validate-external-links"],
  description: "Validate external HTTP links return 200",
  tags: ["links", "async"],
  parser: "markdownit",
  asynchronous: true,
  function: async (params, onError) => {
    const links = params.parsers.markdownit.tokens
      .filter(token => token.type === "link_open");

    const checkLink = (url) => {
      return new Promise((resolve) => {
        https.get(url, (res) => {
          resolve(res.statusCode === 200);
        }).on('error', () => {
          resolve(false);
        });
      });
    };

    for (const link of links) {
      const hrefToken = link.attrs.find(attr => attr[0] === "href");

      if (hrefToken) {
        const href = hrefToken[1];

        if (href.startsWith('http://') || href.startsWith('https://')) {
          const valid = await checkLink(href);

          if (!valid) {
            onError({
              lineNumber: link.lineNumber,
              detail: `External link may be broken: ${href}`,
              context: link.line
            });
          }
        }
      }
    }
  }
};
```

## Using Custom Rules

### In Configuration File

```javascript
// .markdownlint.js
const customRules = require('./custom-rules');

module.exports = {
  default: true,
  customRules: [
    customRules.headingCapitalization,
    customRules.blankLineBeforeHeading,
    customRules.codeBlockLanguage
  ],
  "heading-capitalization": true,
  "blank-line-before-heading": true,
  "code-block-language": {
    "allowed_languages": ["javascript", "typescript", "bash", "json"]
  }
};
```

### In Node.js Script

```javascript
const markdownlint = require('markdownlint');
const customRules = require('./custom-rules');

const options = {
  files: ['README.md'],
  customRules: [
    customRules.headingCapitalization,
    customRules.blankLineBeforeHeading
  ],
  config: {
    default: true,
    "heading-capitalization": true,
    "blank-line-before-heading": true
  }
};

markdownlint(options, (err, result) => {
  if (!err) {
    console.log(result.toString());
  }
});
```

### With markdownlint-cli

```bash
# Using custom rules with CLI
markdownlint -c .markdownlint.js -r ./custom-rules/*.js *.md
```

## TypeScript Support

### Type-Safe Rule Definition

```typescript
import { Rule } from 'markdownlint';

const rule: Rule = {
  names: ['typescript-rule', 'TS001'],
  description: 'Example TypeScript custom rule',
  tags: ['custom'],
  parser: 'markdownit',
  function: (params, onError) => {
    // Type-safe implementation
    params.parsers.markdownit.tokens.forEach(token => {
      if (token.type === 'heading_open') {
        onError({
          lineNumber: token.lineNumber,
          detail: 'Example error'
        });
      }
    });
  }
};

export default rule;
```

## When to Use This Skill

- Enforcing project-specific documentation standards
- Validating custom markdown patterns
- Checking domain-specific requirements
- Extending markdownlint beyond built-in rules
- Creating reusable rule packages
- Automating documentation quality checks
- Implementing team coding standards
- Building custom linting toolchains

## Best Practices

1. **Clear Rule Names** - Use descriptive names that indicate purpose
2. **Comprehensive Descriptions** - Document what the rule checks
3. **Appropriate Tags** - Categorize rules for easy filtering
4. **Choose Right Parser** - Use markdownit for most cases, micromark for precision
5. **Provide Information URLs** - Link to detailed rule documentation
6. **Support Configuration** - Allow rule customization via params.config
7. **Helpful Error Messages** - Provide clear detail and context
8. **Use Range When Possible** - Highlight exact problem location
9. **Implement fixInfo** - Enable automatic fixing when possible
10. **Handle Edge Cases** - Account for front matter, empty files, etc.
11. **Performance Consideration** - Avoid expensive operations in rules
12. **Test Thoroughly** - Test with various markdown files
13. **Version Documentation** - Document which markdownlint version required
14. **Export Properly** - Use module.exports or ES6 exports consistently
15. **Async When Needed** - Only use asynchronous for I/O operations

## Common Pitfalls

1. **Wrong Line Numbers** - Forgetting lines are 1-based, not 0-based
2. **Missing Parser** - Not specifying parser property
3. **Incorrect Token Types** - Using wrong token type names
4. **No Error Context** - Not providing helpful context in errors
5. **Synchronous I/O** - Using sync functions instead of async
6. **Ignoring Front Matter** - Not handling front matter correctly
7. **Hardcoded Values** - Not using configuration parameters
8. **Poor Performance** - Using inefficient algorithms on large files
9. **Missing Fixability** - Not implementing fixInfo when possible
10. **Incomplete Testing** - Not testing edge cases and error conditions
11. **Parser Mismatch** - Accessing wrong parser output
12. **Column Off-by-One** - Columns are 1-based like line numbers
13. **Memory Leaks** - Not cleaning up in async rules
14. **Blocking Operations** - Long-running synchronous operations
15. **Type Confusion** - Mixing up token properties between parsers

## Resources

- [markdownlint Custom Rules Guide](https://github.com/DavidAnson/markdownlint/blob/main/doc/CustomRules.md)
- [markdownlint GitHub Repository](https://github.com/DavidAnson/markdownlint)
- [markdown-it Parser](https://github.com/markdown-it/markdown-it)
- [micromark Parser](https://github.com/micromark/micromark)
- [Community Custom Rules on npm](https://www.npmjs.com/search?q=keywords:markdownlint-rule)
