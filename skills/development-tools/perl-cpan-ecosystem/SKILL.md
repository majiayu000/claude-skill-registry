---
name: perl-cpan-ecosystem
description: 'This skill should be used when the user asks to "install Perl modules", "use cpanm", "create a cpanfile", "manage Perl dependencies", "set up Carton", "configure local::lib", or mentions CPAN, cpanminus, module installation, or Perl package management.'
---

# CPAN Ecosystem Guide

Comprehensive guide for managing Perl modules using cpanm, cpanfile, Carton, and local::lib.

## cpanm (cpanminus)

The recommended tool for installing CPAN modules.

### Installation

```bash
# Using curl
curl -L https://cpanmin.us | perl - --self-upgrade

# Using system package manager
# Debian/Ubuntu
sudo apt install cpanminus

# macOS
brew install cpanminus

# From CPAN
cpan App::cpanminus
```

### Basic Usage

```bash
# Install a module
cpanm Module::Name

# Install specific version
cpanm Module::Name@1.23

# Install with dependencies only (for testing)
cpanm --installdeps .

# Quiet installation
cpanm --quiet --notest Module::Name

# Install to local directory
cpanm --local-lib=~/perl5 Module::Name
```

### Common Flags

| Flag               | Purpose                        |
| ------------------ | ------------------------------ |
| `--notest`         | Skip tests (faster, less safe) |
| `--quiet`          | Minimal output                 |
| `--verbose`        | Detailed output                |
| `--force`          | Install despite test failures  |
| `--installdeps`    | Install dependencies only      |
| `--local-lib=DIR`  | Install to specific directory  |
| `--self-upgrade`   | Update cpanm itself            |
| `--mirror URL`     | Use specific CPAN mirror       |
| `--skip-satisfied` | Skip already installed         |

### Mirror Configuration

```bash
# Use a specific mirror
cpanm --mirror https://cpan.metacpan.org Module::Name

# Use mirror only (no fallback)
cpanm --mirror https://cpan.metacpan.org --mirror-only Module::Name
```

## cpanfile

Declare dependencies in a `cpanfile` for reproducible installations.

### Basic cpanfile

```perl
# cpanfile
requires 'Moo';
requires 'Path::Tiny';
requires 'Try::Tiny';

# Version constraints
requires 'DBI', '1.643';           # Exact version
requires 'JSON::XS', '>= 4.0';     # Minimum version
requires 'Plack', '< 2.0';         # Maximum version
requires 'Moose', '>= 2.0, < 3.0'; # Range

# Development dependencies
on 'develop' => sub {
    requires 'Perl::Critic';
    requires 'Perl::Tidy';
};

# Test dependencies
on 'test' => sub {
    requires 'Test::More', '0.98';
    requires 'Test::Exception';
    requires 'Test::Deep';
};

# Build dependencies
on 'build' => sub {
    requires 'Module::Build';
};

# Recommended (not required)
recommends 'JSON::XS';
suggests 'IO::Socket::SSL';
```

### Feature Phases

| Phase     | Purpose         | When Installed   |
| --------- | --------------- | ---------------- |
| `runtime` | Production deps | Always (default) |
| `test`    | Testing deps    | `--with-test`    |
| `develop` | Dev tools       | `--with-develop` |
| `build`   | Build tools     | During build     |

### Install from cpanfile

```bash
# Install all runtime dependencies
cpanm --installdeps .

# Include test dependencies
cpanm --installdeps --with-test .

# Include all phases
cpanm --installdeps --with-develop --with-test .
```

## Carton

Lock dependencies to exact versions for reproducible deployments.

### Installation

```bash
cpanm Carton
```

### Basic Workflow

```bash
# Create cpanfile.snapshot from cpanfile
carton install

# Install to local/ directory
carton install --deployment

# Update dependencies
carton update

# Run script with locked dependencies
carton exec perl script.pl

# Run with specific local path
carton exec --path local perl app.pl
```

### Generated Files

| File                | Purpose                | Git    |
| ------------------- | ---------------------- | ------ |
| `cpanfile`          | Dependency declaration | Commit |
| `cpanfile.snapshot` | Locked versions        | Commit |
| `local/`            | Installed modules      | Ignore |

### .gitignore for Carton

```gitignore
/local/
/.carton/
```

### Deployment Pattern

```bash
# Development machine
carton install
git add cpanfile cpanfile.snapshot
git commit -m "Update dependencies"

# Production machine
git pull
carton install --deployment --without develop,test
carton exec perl app.pl
```

## local::lib

Install modules in user directory without root access.

### Setup

```bash
# Install local::lib
cpanm local::lib

# Initialize (add to shell profile)
eval $(perl -I$HOME/perl5/lib/perl5 -Mlocal::lib)

# Add to ~/.bashrc or ~/.zshrc
echo 'eval $(perl -I$HOME/perl5/lib/perl5 -Mlocal::lib)' >> ~/.bashrc
```

### Environment Variables

local::lib sets these variables:

```bash
PERL5LIB=$HOME/perl5/lib/perl5
PERL_LOCAL_LIB_ROOT=$HOME/perl5
PERL_MB_OPT="--install_base $HOME/perl5"
PERL_MM_OPT="INSTALL_BASE=$HOME/perl5"
PATH=$HOME/perl5/bin:$PATH
```

### Custom Installation Path

```bash
# Use different directory
eval $(perl -Mlocal::lib=$HOME/myperllib)

# Project-specific
eval $(perl -Mlocal::lib=./local)
```

## Module Resolution Order

Perl searches for modules in this order:

1. Directories in `@INC`
2. `PERL5LIB` paths
3. Site lib (system-wide)
4. Core modules

Check current `@INC`:

```bash
perl -V  # Full config including @INC
perl -e 'print join("\n", @INC)'
```

## Finding Modules

### Search MetaCPAN

```bash
# Using mccpan (if installed)
cpanm App::cpanminus::reporter
cpan-outdated

# Or use web: https://metacpan.org/
```

### Check Installed Modules

```bash
# List all installed
perldoc perllocal

# Check specific module
perl -MModule::Name -e 'print $Module::Name::VERSION'

# Using cpan
cpan -l

# Using pmvers (from pmtools)
pmvers Module::Name
```

## Troubleshooting

### Common Issues

**Module not found after install:**

```bash
# Check PERL5LIB
echo $PERL5LIB

# Verify module location
perl -MModule::Name -e 'print $INC{"Module/Name.pm"}'
```

**Permission denied:**

```bash
# Use local::lib instead of sudo
eval $(perl -Mlocal::lib)
cpanm Module::Name
```

**Build failures:**

```bash
# Install build tools
# Debian/Ubuntu
sudo apt install build-essential

# Check build log
less ~/.cpanm/build.log
```

**XS module compilation:**

```bash
# Install development headers
sudo apt install libssl-dev  # For SSL modules
sudo apt install libxml2-dev # For XML modules
```

## Project Setup Example

Initialize a new Perl project with proper dependency management:

```bash
# Create project structure
mkdir -p myapp/{lib,t,bin}
cd myapp

# Create cpanfile
cat > cpanfile << 'EOF'
requires 'Moo';
requires 'Path::Tiny';
requires 'Try::Tiny';

on 'test' => sub {
    requires 'Test::More', '0.98';
};
EOF

# Install with Carton
carton install

# Add to .gitignore
echo '/local/' >> .gitignore
echo '/.carton/' >> .gitignore

# Commit dependency spec
git add cpanfile cpanfile.snapshot
```

## Additional Resources

For Perl version management with perlbrew, see the **perl-environment-setup** skill.
