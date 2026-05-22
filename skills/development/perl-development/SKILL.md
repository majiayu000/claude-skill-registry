---
name: perl-development
description: 'This skill should be used when the user asks to "write a Perl script", "create Perl code", "modern Perl best practices", "Perl 5.30+", "use strict warnings autodie", or mentions Perl pragmas, subroutines, error handling, or scripting patterns. Provides comprehensive Perl 5.30+ development guidance.'
---

# Modern Perl 5.30+ Development

Procedural guidance for writing secure, maintainable Perl scripts following modern best practices.

## Essential Script Header

Every Perl script MUST begin with these elements:

```perl
#!/usr/bin/env perl

use strict;
use warnings;
use autodie;
```

**Pragma purposes:**

| Pragma     | Effect                                                             |
| ---------- | ------------------------------------------------------------------ |
| `strict`   | Enforces variable declarations, prevents barewords, restricts refs |
| `warnings` | Enables compile-time and runtime warning messages                  |
| `autodie`  | Converts failed builtins (open, close, etc.) to exceptions         |

## Standard Module Imports

Import modules in logical groups:

```perl
# Core pragmas
use strict;
use warnings;
use autodie;

# Feature pragmas (Perl 5.10+)
use feature qw(say state signatures);

# Standard library
use Getopt::Long qw(GetOptions);
use Pod::Usage qw(pod2usage);
use File::Basename qw(basename dirname);
use Cwd qw(abs_path getcwd);
use FindBin;
use lib $FindBin::Bin;

# Third-party modules
use Path::Tiny;
use Try::Tiny;
```

## Variable Declaration Patterns

Declare variables with appropriate scope:

```perl
# Script constants (use constant or Readonly)
use constant {
    SCRIPT_NAME    => basename($0),
    SCRIPT_VERSION => "1.0.0",
};

# Lexical variables (preferred)
my $config_file = 'config.yaml';
my @input_files = ();
my %options = ();

# State variables (persist across calls)
sub get_counter {
    state $count = 0;
    return ++$count;
}
```

## Error Handling Patterns

### Using autodie

With `autodie`, failed system calls throw exceptions automatically:

```perl
use autodie;

# These throw on failure - no explicit check needed
open my $fh, '<', $filename;
close $fh;
chdir $directory;
```

### Using Try::Tiny for complex error handling

```perl
use Try::Tiny;

try {
    process_file($filename);
}
catch {
    my $error = $_;
    $error =~ s/ at \S+ line \d+\.?\n?$//;
    warn "Failed to process: $error\n";
}
finally {
    cleanup_resources();
};
```

### Using eval blocks (built-in)

```perl
eval {
    risky_operation();
    1;
} or do {
    my $error = $@ || 'Unknown error';
    warn "Operation failed: $error\n";
};
```

## Subroutine Patterns

### Modern signatures (Perl 5.20+)

```perl
use feature 'signatures';
no warnings 'experimental::signatures';

sub greet ($name, $greeting = 'Hello') {
    return "$greeting, $name!";
}

sub process_files (@files) {
    for my $file (@files) {
        process_single_file($file);
    }
}
```

### Traditional parameter handling

```perl
sub process_data {
    my ($input, $options) = @_;
    $options //= {};

    my $verbose = $options->{verbose} // 0;
    my $output  = $options->{output}  // '-';

    # ... implementation
}
```

## File Operations

### Modern file handling with Path::Tiny

```perl
use Path::Tiny;

my $file = path($filename);

# Read entire file
my $content = $file->slurp_utf8;
my @lines   = $file->lines_utf8;

# Write file
$file->spew_utf8($content);
$file->append_utf8("New line\n");

# Path manipulation
my $parent = $file->parent;
my $name   = $file->basename;
my $abs    = $file->absolute;
```

### Traditional three-argument open

```perl
# Reading
open my $fh, '<:encoding(UTF-8)', $filename;
my @lines = <$fh>;
close $fh;

# Writing
open my $out, '>:encoding(UTF-8)', $output_file;
print $out $content;
close $out;

# Appending
open my $log, '>>:encoding(UTF-8)', $log_file;
```

## Argument Parsing with Getopt::Long

```perl
use Getopt::Long qw(GetOptions);
use Pod::Usage qw(pod2usage);

my ($help, $version, $verbose, $config_file);

GetOptions(
    'help|h'     => \$help,
    'version|v'  => \$version,
    'verbose|V'  => \$verbose,
    'config|c=s' => \$config_file,
) or pod2usage(2);

pod2usage(-exitval => 0, -verbose => 1) if $help;

if ($version) {
    say SCRIPT_NAME . " version " . SCRIPT_VERSION;
    exit 0;
}

# Validate required arguments
pod2usage(-message => "Missing required argument", -exitval => 1)
    unless @ARGV >= 1;
```

## POD Documentation Template

Include documentation at the end of scripts:

```perl
__END__

=head1 NAME

script-name.pl - Brief description of what the script does

=head1 SYNOPSIS

B<script-name.pl> [OPTIONS] <argument>

=head1 DESCRIPTION

Detailed description of the script's purpose and behavior.

=head1 OPTIONS

=over 4

=item B<-h>, B<--help>

Show this help message and exit.

=item B<-v>, B<--version>

Show version information and exit.

=item B<-c>, B<--config>=I<FILE>

Path to configuration file.

=back

=head1 EXAMPLES

    # Basic usage
    script-name.pl input.txt

    # With options
    script-name.pl --verbose --config=my.conf input.txt

=head1 AUTHOR

Your Name <email@example.com>

=cut
```

## Security Best Practices

### Taint Mode

Enable for scripts handling external input:

```perl
#!/usr/bin/env perl -T

use strict;
use warnings;

# Untaint validated data
if ($input =~ /^(\w+)$/) {
    my $clean = $1;  # Now untainted
}
```

### Avoiding shell injection

```perl
# WRONG - shell interpolation risk
my $output = `grep $pattern $file`;
system("rm $file");

# CORRECT - list form avoids shell
system('grep', $pattern, $file);
my @result = capturex('grep', $pattern, $file);

# CORRECT - IPC::System::Simple for capture
use IPC::System::Simple qw(capture capturex);
my $output = capturex('grep', $pattern, $file);
```

### Secure temporary files

```perl
use File::Temp qw(tempfile tempdir);

my ($fh, $filename) = tempfile(UNLINK => 1);
my $tmpdir = tempdir(CLEANUP => 1);
```

## Logging Pattern

```perl
use Term::ANSIColor qw(colored);

sub log_info    { say colored(['cyan'],   "INFO: $_[0]"); }
sub log_success { say colored(['green'],  "SUCCESS: $_[0]"); }
sub log_warning { say colored(['yellow'], "WARNING: $_[0]"); }
sub log_error   { say STDERR colored(['red'], "ERROR: $_[0]"); }
sub log_debug   { say colored(['blue'],   "DEBUG: $_[0]") if $ENV{DEBUG}; }
```

## Script Template

Refer to the complete example template:

- [Perl Example Script](./references/perl_example_file.pl) - Full working template

## Additional Resources

### Reference Files

- [Modern Perl Modules](./references/modern-modules.md) - Recommended CPAN modules
- [Perl Truthiness Gotchas](./references/truthiness.md) - Common pitfalls with Perl values

### Related Skills

For CPAN module management, activate the **perl-cpan-ecosystem** skill.
For environment setup with perlbrew, activate the **perl-environment-setup** skill.
For testing patterns, activate the **perl-testing** skill.
