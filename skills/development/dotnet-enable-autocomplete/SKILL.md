---
name: dotnet-enable-autocomplete
description: Enables tab autocomplete for the dotnet CLI. Use when the user wants to set up shell completion for dotnet commands.
license: MIT
metadata:
  author: Im5tu
  version: "1.0"
  repositoryUrl: https://github.com/im5tu/dotnet-skills
allowed-tools: Bash(dotnet:*) Read AskUserQuestion
---

# .NET CLI Tab Completion

Enable tab autocomplete for the `dotnet` CLI in your preferred shell.

## Steps

1. **Determine .NET version** (CRITICAL - commands differ by version)
   ```bash
   dotnet sdk check
   ```
   - Parse output to identify installed SDK versions
   - **.NET 10+**: Uses `dotnet completions script <shell>` (native completions)
   - **Pre-.NET 10**: Uses `dotnet complete --position` (dynamic completions)

2. **Ask user which shells** they use, allowing multi-select:
   - PowerShell
   - bash
   - zsh
   - fish
   - nushell

For each user shell:

1. **Detect profile file location** based on shell:

   | Shell | Profile Path |
   |-------|--------------|
   | PowerShell | `$PROFILE` |
   | bash | `~/.bashrc` |
   | zsh | `~/.zshrc` |
   | fish | `~/.config/fish/config.fish` |
   | nushell | `~/.config/nushell/config.nu` |

2. **Check if completion already configured**
   - Read the profile file
   - Search for existing dotnet completion setup
   - If found, inform user and ask if they want to replace it

3. **Append completion script** to profile based on .NET version and shell

4. **Inform user** to restart their shell or source the profile

## Completion Scripts

### .NET 10+ (Native Completions)

**PowerShell:**
```powershell
dotnet completions script pwsh | Out-String | Invoke-Expression
```

**bash:**
```bash
eval "$(dotnet completions script bash)"
```

**zsh:**
```zsh
eval "$(dotnet completions script zsh)"
```

**fish:**
```fish
dotnet completions script fish | source
```

**nushell:**
See [.NET CLI docs](https://learn.microsoft.com/dotnet/core/tools/enable-tab-autocomplete) for config.nu setup.

### Pre-.NET 10 (Dynamic Completions)

**PowerShell:**
```powershell
# dotnet CLI tab completion
Register-ArgumentCompleter -Native -CommandName dotnet -ScriptBlock {
    param($wordToComplete, $commandAst, $cursorPosition)
    dotnet complete --position $cursorPosition "$commandAst" | ForEach-Object {
        [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
    }
}
```

**bash:**
```bash
# dotnet CLI tab completion
_dotnet_bash_complete() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local IFS=$'\n'
    local candidates
    read -d '' -ra candidates < <(dotnet complete --position "${COMP_POINT}" "${COMP_LINE}" 2>/dev/null)
    read -d '' -ra COMPREPLY < <(compgen -W "${candidates[*]}" -- "$cur")
}
complete -f -F _dotnet_bash_complete dotnet
```

**zsh:**
```zsh
# dotnet CLI tab completion
_dotnet_zsh_complete() {
    local completions=("$(dotnet complete --position ${CURSOR} "${BUFFER}" 2>/dev/null)")
    reply=("${(ps:\n:)completions}")
}
compctl -K _dotnet_zsh_complete dotnet
```

**fish:**
```fish
# dotnet CLI tab completion
complete -f -c dotnet -a "(dotnet complete --position (commandline -cp) (commandline -op))"
```

**nushell:**
```nu
# Add to external_completer in config.nu
let external_completer = {|spans|
    match $spans.0 {
        dotnet => (
            dotnet complete (
                $spans | skip 1 | str join " "
            ) | lines
        )
    }
}
```

## Error Handling

- **If `dotnet sdk check` fails**: Ensure .NET SDK is installed
- **If profile file doesn't exist**: Create it with the completion script
- **If profile file is read-only**: Warn user and provide script to add manually

## Notes

- .NET 10+ provides native `dotnet completions` command
- Pre-.NET 10 uses `dotnet complete` with dynamic scripts
- Always back up profile before modifying
- User must restart shell or source profile for changes to take effect
