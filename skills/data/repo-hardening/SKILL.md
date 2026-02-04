---
name: repo-hardening
description: Best practices for setting up quality tooling across different language stacks.
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Repo Hardening Skill

Best practices for setting up quality tooling across different language stacks.

---

## Language Detection

Detect stack from project files:

| File | Language | Package Manager |
|------|----------|-----------------|
| `package.json` | JavaScript/TypeScript | npm/yarn/pnpm/bun |
| `pyproject.toml` | Python | pip/poetry/uv |
| `requirements.txt` | Python | pip |
| `Cargo.toml` | Rust | cargo |
| `go.mod` | Go | go |
| `pom.xml` | Java | Maven |
| `build.gradle` | Java/Kotlin | Gradle |
| `build.gradle.kts` | Kotlin | Gradle |
| `Gemfile` | Ruby | Bundler |
| `composer.json` | PHP | Composer |
| `*.csproj` / `*.sln` | C#/.NET | dotnet |
| `Package.swift` | Swift | SwiftPM |
| `mix.exs` | Elixir | Mix |
| `CMakeLists.txt` | C/C++ | CMake |
| `Makefile` | C/C++ | Make |
| `build.sbt` | Scala | sbt |

---

## Language References

Per-language tooling configs (linting, formatting, type checking, hooks, coverage):

| Language | Reference |
|----------|-----------|
| JavaScript/TypeScript | skills/repo-hardening/references/javascript-typescript.md |
| Python | skills/repo-hardening/references/python.md |
| Rust | skills/repo-hardening/references/rust.md |
| Go | skills/repo-hardening/references/go.md |
| Java | skills/repo-hardening/references/java.md |
| Kotlin | skills/repo-hardening/references/kotlin.md |
| Ruby | skills/repo-hardening/references/ruby.md |
| PHP | skills/repo-hardening/references/php.md |
| C#/.NET | skills/repo-hardening/references/csharp-dotnet.md |
| Swift | skills/repo-hardening/references/swift.md |
| Elixir | skills/repo-hardening/references/elixir.md |
| C/C++ | skills/repo-hardening/references/c-cpp.md |
| Scala | skills/repo-hardening/references/scala.md |

---

## .editorconfig

Universal editor settings:

```ini
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.{py,rs}]
indent_size = 4

[*.go]
indent_style = tab
indent_size = 4

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

---

## .gitattributes

Normalize line endings:

```text
* text=auto eol=lf
*.{cmd,[cC][mM][dD]} text eol=crlf
*.{bat,[bB][aA][tT]} text eol=crlf
*.pdf binary
*.png binary
*.jpg binary
*.gif binary
```

---

## Setup Priority

1. **.editorconfig** - Universal, no dependencies
2. **Linter** - Catches bugs early
3. **Formatter** - Consistent style
4. **Git hooks** - Enforce on commit
5. **Type checker** - Optional but recommended
6. **Test coverage** - Enforce minimum threshold (default: 80%)

---

## Common Mistakes

1. **Conflicting rules** - Ensure linter and formatter agree (use eslint-config-prettier)
2. **Missing hook permissions** - `chmod +x .git/hooks/*`
3. **Hook not running** - Ensure `.git/hooks/pre-commit` exists (not `.git/hooks/pre-commit.sample`)
4. **Too strict initially** - Start with warnings, graduate to errors
