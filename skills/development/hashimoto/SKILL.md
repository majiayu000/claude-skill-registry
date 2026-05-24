---
name: hashimoto-cli-ux
description: Design CLI tools in the style of Mitchell Hashimoto, founder of HashiCorp. Emphasizes consistent command patterns, helpful error messages, progressive disclosure, and machine-readable output. Use when building command-line tools that developers will love.
---

# Mitchell Hashimoto CLI UX Style Guide

## Overview

Mitchell Hashimoto founded HashiCorp and created some of the most beloved developer tools: Vagrant, Terraform, Consul, Vault, and Nomad. These tools share a consistent, thoughtful CLI design that has become the gold standard for developer experience. Hashimoto's CLIs are famous for being discoverable, helpful, and powerful without being overwhelming.

## Core Philosophy

> "A CLI should be a conversation, not a puzzle."

> "Error messages are documentation. Write them like you're helping a colleague."

> "The best CLI is one you can use without reading the docs first."

Hashimoto believes that CLIs should respect the user's time and intelligence. They should be easy to explore, provide helpful feedback, and never leave the user guessing what went wrong or what to do next.

## Design Principles

1. **Consistent Command Structure**: `<tool> <noun> <verb> [options]` or `<tool> <command> [options]`

2. **Progressive Disclosure**: Simple by default, powerful when needed.

3. **Helpful Error Messages**: Tell users what went wrong AND how to fix it.

4. **Machine-Readable Output**: Always support `--json` or `-o json` for scripting.

5. **Discoverability**: `--help` at every level, tab completion, command suggestions.

## Command Structure

```
HashiCorp Command Pattern:
──────────────────────────

terraform <command> [options] [args]
    │         │         │       │
    │         │         │       └── Positional arguments
    │         │         └── Flags modify behavior
    │         └── The action (init, plan, apply, destroy)
    └── The tool name

Examples:
  terraform init
  terraform plan -out=tfplan
  terraform apply tfplan
  terraform destroy -auto-approve

  vault secrets list
  vault secrets enable -path=secret kv
  vault kv put secret/myapp password=s3cr3t
  vault kv get -format=json secret/myapp

  consul services register web.json
  consul services deregister web
  consul kv put config/db/host 10.0.0.1
  consul kv get -recurse config/
```

## When Designing CLIs

### Always

- Provide `--help` at every command level
- Support `-h` as alias for `--help`
- Include examples in help text
- Support `--version` and `-v`
- Provide JSON output option (`--json` or `-format=json`)
- Use exit codes consistently (0=success, 1=error)
- Show progress for long operations
- Suggest corrections for typos

### Never

- Require reading docs to use basic features
- Output errors without suggested fixes
- Mix output and errors on stdout
- Require interactive input without a non-interactive option
- Break backward compatibility silently
- Use inconsistent flag names across commands
- Ignore terminal width when formatting

### Prefer

- Subcommands over many flags
- Long flags over short for clarity (`--verbose` over `-v`)
- Confirmation prompts for destructive actions
- Color output (with `--no-color` option)
- Table output for humans, JSON for machines
- Stdin support for piping

## Code Patterns

### Command Structure with Clap (Rust)

```rust
use clap::{Parser, Subcommand, Args, ValueEnum};

/// A package manager for AI coding skills
#[derive(Parser)]
#[command(name = "sk1llz")]
#[command(author, version, about, long_about = None)]
#[command(propagate_version = true)]
#[command(after_help = "Examples:
  sk1llz list                    List all available skills
  sk1llz search rust             Search for Rust-related skills
  sk1llz install torvalds        Install a skill by name
  sk1llz info lamport            Show details about a skill

Use 'sk1llz <command> --help' for more information about a command.")]
struct Cli {
    /// Output format
    #[arg(long, short = 'o', global = true, value_enum, default_value = "text")]
    format: OutputFormat,
    
    /// Disable color output
    #[arg(long, global = true)]
    no_color: bool,
    
    #[command(subcommand)]
    command: Commands,
}

#[derive(ValueEnum, Clone, Copy)]
enum OutputFormat {
    Text,
    Json,
}

#[derive(Subcommand)]
enum Commands {
    /// List all available skills
    #[command(visible_alias = "ls")]
    List(ListArgs),
    
    /// Search skills by name, description, or tags
    Search(SearchArgs),
    
    /// Show detailed information about a skill
    Info(InfoArgs),
    
    /// Install a skill to your project or global directory
    Install(InstallArgs),
    
    /// Remove an installed skill
    Uninstall(UninstallArgs),
    
    /// Initialize skill directory in current project
    Init,
    
    /// Update the skill index from remote
    Update,
    
    /// Show installation locations
    Where,
    
    /// Check your setup for common issues
    Doctor,
    
    /// Generate shell completions
    Completions {
        #[arg(value_enum)]
        shell: Shell,
    },
}

#[derive(Args)]
struct ListArgs {
    /// Filter by category
    #[arg(short, long)]
    category: Option<String>,
    
    /// Filter by tag
    #[arg(short, long)]
    tag: Option<String>,
}

#[derive(Args)]
struct InstallArgs {
    /// Skill name or ID
    name: String,
    
    /// Install to global ~/.claude/skills instead of project-local
    #[arg(short, long)]
    global: bool,
    
    /// Skip confirmation prompt
    #[arg(short = 'y', long)]
    yes: bool,
}
```

### Helpful Error Messages

```rust
use thiserror::Error;
use colored::Colorize;

#[derive(Error, Debug)]
enum CliError {
    #[error("Skill '{name}' not found")]
    SkillNotFound { 
        name: String,
        suggestions: Vec<String>,
    },
    
    #[error("No .claude directory found")]
    NoClaudeDir,
    
    #[error("Network error: {message}")]
    Network { message: String },
    
    #[error("Manifest is stale")]
    StaleManifest { days_old: u64 },
}

impl CliError {
    /// Format error with helpful suggestions - Hashimoto style
    pub fn display(&self) -> String {
        match self {
            CliError::SkillNotFound { name, suggestions } => {
                let mut msg = format!(
                    "{} Skill '{}' not found.\n",
                    "Error:".red().bold(),
                    name.yellow()
                );
                
                if !suggestions.is_empty() {
                    msg.push_str(&format!(
                        "\n{}\n",
                        "Did you mean one of these?".cyan()
                    ));
                    for suggestion in suggestions.iter().take(3) {
                        msg.push_str(&format!("  • {}\n", suggestion.green()));
                    }
                }
                
                msg.push_str(&format!(
                    "\n{} Use '{}' to see all available skills.",
                    "Hint:".blue().bold(),
                    "sk1llz list".cyan()
                ));
                
                msg
            }
            
            CliError::NoClaudeDir => {
                format!(
                    "{} No .claude directory found in current project.\n\n\
                     {} To use project-local skills, initialize first:\n\n\
                     {}\n\n\
                     {} Or use {} to install globally.",
                    "Error:".red().bold(),
                    "Fix:".green().bold(),
                    "  sk1llz init".cyan(),
                    "Alternatively:".blue().bold(),
                    "--global".cyan()
                )
            }
            
            CliError::Network { message } => {
                format!(
                    "{} Network error: {}\n\n\
                     {} Check your internet connection and try again.\n\
                     {} If the problem persists, the skill repository may be down.",
                    "Error:".red().bold(),
                    message,
                    "Hint:".blue().bold(),
                    "Note:".dimmed()
                )
            }
            
            CliError::StaleManifest { days_old } => {
                format!(
                    "{} Skill index is {} days old.\n\n\
                     {} Run '{}' to get the latest skills.",
                    "Warning:".yellow().bold(),
                    days_old,
                    "Fix:".green().bold(),
                    "sk1llz update".cyan()
                )
            }
        }
    }
}


/// Find similar skill names for "did you mean?" suggestions
fn find_similar_skills(query: &str, skills: &[Skill]) -> Vec<String> {
    use fuzzy_matcher::skim::SkimMatcherV2;
    use fuzzy_matcher::FuzzyMatcher;
    
    let matcher = SkimMatcherV2::default();
    
    let mut scored: Vec<_> = skills
        .iter()
        .filter_map(|s| {
            let score = matcher.fuzzy_match(&s.name, query)?;
            if score > 20 {
                Some((s.name.clone(), score))
            } else {
                None
            }
        })
        .collect();
    
    scored.sort_by(|a, b| b.1.cmp(&a.1));
    scored.into_iter().take(3).map(|(name, _)| name).collect()
}
```

### JSON Output Support

```rust
use serde::Serialize;

#[derive(Serialize)]
struct SkillInfo {
    name: String,
    id: String,
    category: String,
    description: String,
    tags: Vec<String>,
    installed: bool,
    path: Option<String>,
}

fn cmd_info(name: &str, format: OutputFormat) -> Result<()> {
    let skill = find_skill(name)?;
    
    let info = SkillInfo {
        name: skill.name.clone(),
        id: skill.id.clone(),
        category: skill.category.clone(),
        description: skill.description.clone(),
        tags: skill.tags.clone(),
        installed: check_installed(&skill),
        path: get_install_path(&skill),
    };
    
    match format {
        OutputFormat::Json => {
            // Machine-readable: clean JSON
            println!("{}", serde_json::to_string_pretty(&info)?);
        }
        OutputFormat::Text => {
            // Human-readable: formatted with colors
            println!("\n{}", info.name.bold().cyan().underline());
            println!("{}: {}", "ID".bold(), info.id);
            println!("{}: {}", "Category".bold(), info.category);
            println!("\n{}", "Description".bold());
            println!("  {}", info.description);
            
            if info.installed {
                println!("\n{} {}", "✓".green(), "Installed".green());
                if let Some(path) = info.path {
                    println!("  {}", path.dimmed());
                }
            }
        }
    }
    
    Ok(())
}


fn cmd_list(args: ListArgs, format: OutputFormat) -> Result<()> {
    let manifest = load_manifest()?;
    let skills = filter_skills(&manifest.skills, &args);
    
    match format {
        OutputFormat::Json => {
            // Return structured data
            let output = serde_json::json!({
                "count": skills.len(),
                "skills": skills,
            });
            println!("{}", serde_json::to_string_pretty(&output)?);
        }
        OutputFormat::Text => {
            // Human-friendly table
            print_skills_table(&skills);
        }
    }
    
    Ok(())
}
```

### Init Command

```rust
fn cmd_init() -> Result<()> {
    let cwd = std::env::current_dir()?;
    let claude_dir = cwd.join(".claude");
    let skills_dir = claude_dir.join("skills");
    
    if skills_dir.exists() {
        println!(
            "{} Project already initialized at {}",
            "✓".green().bold(),
            skills_dir.display().to_string().cyan()
        );
        return Ok(());
    }
    
    // Create directories
    fs::create_dir_all(&skills_dir)?;
    
    // Create .gitkeep to ensure directory is tracked
    fs::write(skills_dir.join(".gitkeep"), "")?;
    
    println!(
        "{} Initialized sk1llz in {}\n",
        "✓".green().bold(),
        skills_dir.display().to_string().cyan()
    );
    
    println!("{}", "Next steps:".bold());
    println!("  1. Install some skills:");
    println!("     {}", "sk1llz install torvalds".cyan());
    println!("  2. View installed skills:");
    println!("     {}", "sk1llz where".cyan());
    println!("  3. Skills will be used by Claude automatically");
    
    Ok(())
}
```

### Uninstall Command

```rust
fn cmd_uninstall(name: &str, yes: bool) -> Result<()> {
    let (local, global) = get_skill_locations();
    
    // Find where the skill is installed
    let mut found_at: Option<PathBuf> = None;
    
    if let Some(local_path) = &local {
        let skill_path = local_path.join(name);
        if skill_path.exists() {
            found_at = Some(skill_path);
        }
    }
    
    if found_at.is_none() {
        let skill_path = global.join(name);
        if skill_path.exists() {
            found_at = Some(skill_path);
        }
    }
    
    let path = found_at.ok_or_else(|| {
        anyhow::anyhow!(
            "Skill '{}' is not installed.\n\n\
             {} Use '{}' to see installed skills.",
            name,
            "Hint:".blue().bold(),
            "sk1llz where".cyan()
        )
    })?;
    
    // Confirm unless --yes
    if !yes {
        println!(
            "{} Remove skill '{}' from {}?",
            "Confirm:".yellow().bold(),
            name.cyan(),
            path.display().to_string().dimmed()
        );
        print!("  Type 'yes' to confirm: ");
        io::stdout().flush()?;
        
        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        
        if input.trim().to_lowercase() != "yes" {
            println!("{}", "Cancelled.".dimmed());
            return Ok(());
        }
    }
    
    // Remove the directory
    fs::remove_dir_all(&path)?;
    
    println!(
        "{} Removed {} from {}",
        "✓".green().bold(),
        name.cyan(),
        path.display().to_string().dimmed()
    );
    
    Ok(())
}
```

### Doctor Command

```rust
fn cmd_doctor() -> Result<()> {
    println!("\n{}", "sk1llz doctor".bold().cyan());
    println!("{}\n", "Checking your setup...".dimmed());
    
    let mut issues = Vec::new();
    
    // Check 1: Cache directory
    print!("  Checking cache directory... ");
    match get_cache_dir() {
        Ok(path) if path.exists() => {
            println!("{}", "OK".green());
        }
        Ok(path) => {
            println!("{}", "MISSING".yellow());
            issues.push(format!(
                "Cache directory doesn't exist: {}\n  Fix: Run 'sk1llz update'",
                path.display()
            ));
        }
        Err(e) => {
            println!("{}", "ERROR".red());
            issues.push(format!("Cannot determine cache directory: {}", e));
        }
    }
    
    // Check 2: Manifest freshness
    print!("  Checking skill index... ");
    match check_manifest_age() {
        Ok(days) if days < 7 => {
            println!("{} ({} days old)", "OK".green(), days);
        }
        Ok(days) => {
            println!("{} ({} days old)", "STALE".yellow(), days);
            issues.push("Skill index is stale.\n  Fix: Run 'sk1llz update'".to_string());
        }
        Err(_) => {
            println!("{}", "MISSING".yellow());
            issues.push("No local skill index.\n  Fix: Run 'sk1llz update'".to_string());
        }
    }
    
    // Check 3: Installation locations
    print!("  Checking installation directories... ");
    let (local, global) = get_skill_locations();
    if local.is_some() || global.exists() {
        println!("{}", "OK".green());
    } else {
        println!("{}", "NONE".yellow());
        issues.push(
            "No skill directories found.\n  Fix: Run 'sk1llz init' or 'sk1llz install <skill> --global'"
                .to_string()
        );
    }
    
    // Check 4: Network connectivity
    print!("  Checking network... ");
    match reqwest::blocking::get(MANIFEST_URL) {
        Ok(r) if r.status().is_success() => {
            println!("{}", "OK".green());
        }
        _ => {
            println!("{}", "FAILED".red());
            issues.push("Cannot reach skill repository.\n  Check your internet connection.".to_string());
        }
    }
    
    // Summary
    println!();
    if issues.is_empty() {
        println!("{} All checks passed!", "✓".green().bold());
    } else {
        println!("{} {} issue(s) found:\n", "⚠".yellow().bold(), issues.len());
        for issue in issues {
            println!("  • {}", issue);
        }
    }
    
    Ok(())
}

fn check_manifest_age() -> Result<u64> {
    let path = get_manifest_path()?;
    let metadata = fs::metadata(&path)?;
    let modified = metadata.modified()?;
    let age = SystemTime::now().duration_since(modified)?;
    Ok(age.as_secs() / 86400) // days
}
```

### Progress and Confirmation

```rust
use dialoguer::{Confirm, theme::ColorfulTheme};
use indicatif::{ProgressBar, ProgressStyle};

fn confirm_destructive_action(message: &str) -> bool {
    Confirm::with_theme(&ColorfulTheme::default())
        .with_prompt(message)
        .default(false)
        .interact()
        .unwrap_or(false)
}

fn create_progress_bar(len: u64, message: &str) -> ProgressBar {
    let pb = ProgressBar::new(len);
    pb.set_style(
        ProgressStyle::default_bar()
            .template("{spinner:.green} [{bar:40.cyan/blue}] {pos}/{len} {msg}")
            .unwrap()
            .progress_chars("█▓░"),
    );
    pb.set_message(message.to_string());
    pb
}

fn create_spinner(message: &str) -> ProgressBar {
    let pb = ProgressBar::new_spinner();
    pb.set_style(
        ProgressStyle::default_spinner()
            .template("{spinner:.green} {msg}")
            .unwrap(),
    );
    pb.set_message(message.to_string());
    pb.enable_steady_tick(std::time::Duration::from_millis(100));
    pb
}
```

## Mental Model

Hashimoto approaches CLI design by asking:

1. **Can a new user figure this out?** Discoverability is key
2. **What will they try first?** Support the obvious path
3. **What goes wrong?** Write errors that help, not blame
4. **Can it be scripted?** Always support machine output
5. **Is it consistent?** Same patterns across all commands

## The CLI UX Checklist

```
□ --help at every command level with examples
□ --version returns clean version string
□ --json or -o json for machine output
□ Errors include what went wrong AND how to fix
□ Tab completion script generation
□ Confirmation for destructive actions
□ Progress indicators for slow operations
□ "Did you mean?" for typos
□ Consistent flag names across commands
□ Non-zero exit codes on error
□ Stdin support where it makes sense
□ --no-color for accessibility
```

## Signature Hashimoto Moves

- Consistent `<tool> <command> [args]` pattern
- Error messages with fix suggestions
- Machine-readable `--json` output
- Progressive disclosure (simple defaults, powerful options)
- Tab completion for all commands
- `doctor` command for diagnosing issues
- Confirmation prompts for destructive actions
- Examples in `--help` output
