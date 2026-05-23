---
name: perl-environment-setup
description: 'This skill should be used when the user asks to "install perlbrew", "set up Perl environment", "install Perl version", "manage Perl versions", "switch Perl version", "install plenv", or mentions Perl version management, development environment setup, or multiple Perl installations.'
---

# Perl Environment Setup

Guide for setting up Perl development environments using perlbrew for version management.

## perlbrew Overview

perlbrew manages multiple Perl installations in user space without root access.

### Benefits

- Install any Perl version without root
- Switch between versions instantly
- Isolated module installations per version
- Test against multiple Perl versions

## Installation

### Quick Install

```bash
# Download and run installer
curl -L https://install.perlbrew.pl | bash

# Initialize perlbrew
perlbrew init

# Add to shell profile (~/.bashrc or ~/.zshrc)
source ~/perl5/perlbrew/etc/bashrc
```

### Verify Installation

```bash
perlbrew version
perlbrew list
which perl
```

## Installing Perl Versions

### List Available Versions

```bash
# Show all available versions
perlbrew available

# Show only stable releases
perlbrew available | grep -E '^\s*perl-5\.\d+\.\d+$'
```

### Install a Version

```bash
# Install latest stable
perlbrew install perl-5.38.2

# Install with threading
perlbrew install perl-5.38.2 -Dusethreads

# Install with optimizations
perlbrew install perl-5.38.2 -Doptimize=-O2

# Quick install (skip tests)
perlbrew install perl-5.38.2 --notest

# Install with custom name
perlbrew install perl-5.38.2 --as perl-5.38-dev
```

### Common Build Options

| Option          | Purpose                    |
| --------------- | -------------------------- |
| `-Dusethreads`  | Enable thread support      |
| `-Duseithreads` | Enable interpreter threads |
| `--notest`      | Skip test suite (faster)   |
| `-j N`          | Parallel build with N jobs |
| `--as NAME`     | Custom installation name   |

## Switching Versions

```bash
# Switch for current shell
perlbrew use perl-5.38.2

# Set permanent default
perlbrew switch perl-5.38.2

# Temporary switch with command
perlbrew exec --with perl-5.38.2 perl -v

# Return to system Perl
perlbrew switch-off
perlbrew off  # Shortcut
```

## Managing Installations

```bash
# List installed versions
perlbrew list

# Show current version
perlbrew info

# Remove a version
perlbrew uninstall perl-5.36.0

# Upgrade perlbrew itself
perlbrew self-upgrade
```

## Library Management

perlbrew lib creates isolated module environments per Perl version.

### Create Libraries

```bash
# Create a library for a project
perlbrew lib create perl-5.38.2@myproject

# List libraries
perlbrew lib list

# Switch to library
perlbrew use perl-5.38.2@myproject

# Delete library
perlbrew lib delete perl-5.38.2@myproject
```

### Per-Project Libraries

```bash
# Create project-specific environment
perlbrew lib create perl-5.38.2@webapp

# Install modules to this library
perlbrew use perl-5.38.2@webapp
cpanm Mojolicious DBIx::Class

# Switch between project environments
perlbrew use perl-5.38.2@webapp
perlbrew use perl-5.38.2@cli-tools
```

## cpanm Integration

```bash
# Install cpanm for current Perl
perlbrew install-cpanm

# Now cpanm is available
cpanm Module::Name
```

## Testing Across Versions

```bash
# Run command with all installed Perls
perlbrew exec perl -v

# Run tests with all versions
perlbrew exec prove -l t/

# Run with specific versions
perlbrew exec --with perl-5.36.0,perl-5.38.2 prove t/
```

## Shell Integration

### Bash/Zsh

Add to `~/.bashrc` or `~/.zshrc`:

```bash
source ~/perl5/perlbrew/etc/bashrc
```

### Fish

Add to `~/.config/fish/config.fish`:

```fish
source ~/perl5/perlbrew/etc/perlbrew.fish
```

## Project Configuration

### .perl-version File

Create a `.perl-version` file in project root (for tools that support it):

```text
5.38.2
```

### Project Setup Script

```bash
#!/bin/bash
# setup-perl-env.sh

PERL_VERSION="perl-5.38.2"
PROJECT_LIB="myproject"

# Ensure perlbrew is loaded
source ~/perl5/perlbrew/etc/bashrc

# Install Perl if needed
if ! perlbrew list | grep -q "$PERL_VERSION"; then
    perlbrew install "$PERL_VERSION" --notest
fi

# Create project library if needed
if ! perlbrew lib list | grep -q "$PROJECT_LIB"; then
    perlbrew lib create "${PERL_VERSION}@${PROJECT_LIB}"
fi

# Switch to project environment
perlbrew use "${PERL_VERSION}@${PROJECT_LIB}"

# Install cpanm if needed
command -v cpanm >/dev/null || perlbrew install-cpanm

# Install project dependencies
cpanm --installdeps .

echo "Environment ready: $(perl -v | grep version)"
```

## Directory Structure

perlbrew creates this structure:

```text
~/perl5/perlbrew/
├── bin/           # perlbrew executable
├── build/         # Temporary build files
├── dists/         # Downloaded Perl sources
├── etc/           # Shell integration scripts
└── perls/         # Installed Perl versions
    ├── perl-5.36.0/
    └── perl-5.38.2/
```

## Troubleshooting

### Build Failures

```bash
# Check build log
less ~/perl5/perlbrew/build.perl-5.38.2.log

# Install build dependencies
# Debian/Ubuntu
sudo apt install build-essential

# Install with verbose output
perlbrew --verbose install perl-5.38.2
```

### Path Issues

```bash
# Verify perlbrew is loaded
which perl
# Should show ~/perl5/perlbrew/perls/...

# Check current environment
perlbrew info

# Force reload
source ~/perl5/perlbrew/etc/bashrc
```

### Cleanup

```bash
# Remove build artifacts
perlbrew clean

# Remove downloaded source archives
rm -rf ~/perl5/perlbrew/dists/*
```

## Recommended Setup

For new development machines:

```bash
# 1. Install perlbrew
curl -L https://install.perlbrew.pl | bash
source ~/perl5/perlbrew/etc/bashrc

# 2. Install latest stable Perl
perlbrew install perl-5.38.2 --notest
perlbrew switch perl-5.38.2

# 3. Install cpanm
perlbrew install-cpanm

# 4. Install essential modules
cpanm App::cpanoutdated
cpanm Perl::Critic
cpanm Perl::Tidy

# 5. Add to shell profile
echo 'source ~/perl5/perlbrew/etc/bashrc' >> ~/.bashrc
```

## Alternative: plenv

plenv is an alternative to perlbrew inspired by rbenv:

```bash
# Install plenv
git clone https://github.com/tokuhirom/plenv.git ~/.plenv
git clone https://github.com/tokuhirom/Perl-Build.git ~/.plenv/plugins/perl-build/

# Add to PATH
echo 'export PATH="$HOME/.plenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(plenv init -)"' >> ~/.bashrc

# Install Perl
plenv install 5.38.2
plenv global 5.38.2
plenv install-cpanm
```

plenv advantages:

- Simpler architecture (shims-based)
- Faster shell startup
- Per-directory version files (`.perl-version`)

perlbrew advantages:

- More mature and widely used
- Better library management
- More configuration options

## Additional Resources

For CPAN module management, see the **perl-cpan-ecosystem** skill.
