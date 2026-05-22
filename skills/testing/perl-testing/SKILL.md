---
name: perl-testing
description: 'This skill should be used when the user asks to "write Perl tests", "test Perl code", "use Test::More", "run prove", "create test suite", "mock Perl", or mentions Perl testing, TAP, Test::Class, Test::Deep, or test-driven development in Perl.'
---

# Perl Testing Guide

Comprehensive guide for testing Perl code using Test::More, Test::Class, and related modules.

## Test::More Basics

The foundation of Perl testing.

### Simple Test File

```perl
#!/usr/bin/env perl
use strict;
use warnings;
use Test::More;

# Basic assertions
ok(1, 'truth is true');
ok(!0, 'false is not true');

# Equality
is($got, $expected, 'values are equal');
isnt($got, $unexpected, 'values differ');

# String comparison
is($string, 'expected', 'string matches');
like($string, qr/pattern/, 'matches regex');
unlike($string, qr/bad/, 'does not match regex');

# Numeric comparison
cmp_ok($num, '>', 10, 'greater than 10');
cmp_ok($num, '==', 42, 'equals 42');

# Data structures
is_deeply(\@got, \@expected, 'arrays match');
is_deeply(\%got, \%expected, 'hashes match');

done_testing();
```

### Test Planning

```perl
# Declare expected test count
use Test::More tests => 5;

# Or count at end
use Test::More;
# ... tests ...
done_testing();

# Skip remaining tests
use Test::More;
# ... tests ...
done_testing(10);  # Explicit count
```

## Running Tests

### prove Command

```bash
# Run all tests in t/
prove

# Verbose output
prove -v

# Run specific test
prove t/basic.t

# Recursive with color
prove -r --color

# With library path
prove -l t/  # Adds lib/ to @INC

# Parallel execution
prove -j4

# Shuffle order
prove --shuffle
```

### Common prove Flags

| Flag           | Purpose                    |
| -------------- | -------------------------- |
| `-v`           | Verbose TAP output         |
| `-l`           | Add lib/ to @INC           |
| `-b`           | Add blib/ to @INC          |
| `-r`           | Recursive directory search |
| `-j N`         | Run N tests in parallel    |
| `--color`      | Colored output             |
| `--shuffle`    | Randomize test order       |
| `--state=save` | Save test state            |

## Test Organization

### Directory Structure

```text
project/
├── lib/
│   └── MyApp/
│       ├── Module.pm
│       └── Utils.pm
├── t/
│   ├── 00-compile.t
│   ├── 01-basic.t
│   ├── 02-module.t
│   └── lib/
│       └── Test/
│           └── MyApp.pm
└── xt/
    ├── author/
    │   └── pod.t
    └── release/
        └── manifest.t
```

### Compile Test (t/00-compile.t)

```perl
#!/usr/bin/env perl
use strict;
use warnings;
use Test::More;

use_ok('MyApp::Module');
use_ok('MyApp::Utils');

done_testing();
```

## Test::More Functions

### Assertions

```perl
# Boolean
ok($condition, $description);

# Equality
is($got, $expected, $desc);       # String comparison
isnt($got, $expected, $desc);
cmp_ok($got, $op, $expected, $desc);  # Any operator

# Pattern matching
like($got, qr/pattern/, $desc);
unlike($got, qr/pattern/, $desc);

# Data structures
is_deeply($got, $expected, $desc);

# Reference type
isa_ok($obj, 'ClassName');
can_ok($obj, 'method1', 'method2');

# Pass/fail
pass($desc);
fail($desc);
```

### Diagnostics

```perl
# Additional output on failure
is($got, $expected, 'test') or diag("Got: $got");

# Always print
note("Debug info: $value");

# Dump structure
use Data::Dumper;
diag(Dumper($complex_structure));
```

### Skipping and TODO

```perl
# Skip tests conditionally
SKIP: {
    skip "No database connection", 3 unless $db;

    ok($db->ping, 'database responds');
    is($db->version, '5.7', 'correct version');
    ok($db->tables > 0, 'has tables');
}

# Mark tests as TODO
TODO: {
    local $TODO = "Feature not implemented";

    is(new_feature(), 'expected', 'new feature works');
}

# Skip all tests in file
plan skip_all => 'Module not installed' unless eval { require Optional::Module };
```

## Test::Exception

Test that code dies or lives correctly.

```perl
use Test::More;
use Test::Exception;

# Test that code dies
dies_ok { divide(1, 0) } 'division by zero dies';

# Test that code lives
lives_ok { safe_operation() } 'safe operation lives';

# Test specific exception
throws_ok { bad_call() } qr/invalid argument/i, 'throws expected error';

# Test exception type
throws_ok { bad_call() } 'MyApp::Exception', 'throws correct class';

# Combine with return value
lives_and { is(calc(2, 2), 4) } 'calc lives and returns correct value';

done_testing();
```

## Test::Deep

Deep structure comparison with flexibility.

```perl
use Test::More;
use Test::Deep;

# Ignore certain values
cmp_deeply(
    $got,
    {
        id => ignore(),        # Any value
        name => 'test',
        created => re(qr/^\d{4}-\d{2}-\d{2}$/),  # Pattern match
    },
    'structure matches'
);

# Bag comparison (order doesn't matter)
cmp_deeply(
    \@got,
    bag(1, 2, 3),  # Same elements, any order
    'contains all elements'
);

# Subset matching
cmp_deeply(
    $got,
    superhashof({ required => 'value' }),
    'contains required keys'
);

# Type checking
cmp_deeply(
    $data,
    {
        count => code(sub { $_[0] > 0 }),
        items => array_each(isa('MyApp::Item')),
    },
    'types correct'
);

done_testing();
```

## Test::MockModule

Mock module behavior for isolation.

```perl
use Test::More;
use Test::MockModule;

# Mock a module
my $mock = Test::MockModule->new('MyApp::Database');

# Replace a method
$mock->mock('connect', sub { return 'fake_handle' });

# Mock with return value
$mock->mock('fetch', sub { return { id => 1, name => 'test' } });

# Verify mock was called
my $called = 0;
$mock->mock('save', sub { $called++; return 1 });

# Run code under test
my $result = MyApp::Service->new->process();

is($called, 1, 'save was called');

# Restore original
$mock->unmock('connect');

done_testing();
```

## Test::Class

Object-oriented testing with setup/teardown.

```perl
package Test::MyApp::User;
use parent 'Test::Class';
use Test::More;
use MyApp::User;

# Run before each test method
sub setup : Test(setup) {
    my $self = shift;
    $self->{user} = MyApp::User->new(name => 'Test');
}

# Run after each test method
sub teardown : Test(teardown) {
    my $self = shift;
    $self->{user} = undef;
}

# Test methods
sub test_creation : Test(2) {
    my $self = shift;
    isa_ok($self->{user}, 'MyApp::User');
    is($self->{user}->name, 'Test', 'name is set');
}

sub test_validation : Test(1) {
    my $self = shift;
    ok($self->{user}->is_valid, 'user is valid');
}

# Run all Test::Class tests
Test::Class->runtests;
```

### Test::Class Runner

```perl
#!/usr/bin/env perl
# t/run_all.t
use strict;
use warnings;

use lib 't/lib';
use Test::MyApp::User;
use Test::MyApp::Order;

Test::Class->runtests;
```

## Fixtures and Test Data

### Test Data Files

```perl
use Path::Tiny;
use JSON::PP;

sub load_fixture {
    my ($name) = @_;
    my $file = path("t/fixtures/$name.json");
    return decode_json($file->slurp_utf8);
}

# In test
my $data = load_fixture('users');
```

### Database Fixtures

```perl
use Test::More;
use DBI;

my $dbh;

sub setup_test_db {
    $dbh = DBI->connect('dbi:SQLite::memory:', '', '');
    $dbh->do('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)');
    $dbh->do("INSERT INTO users VALUES (1, 'test')");
}

sub teardown_test_db {
    $dbh->disconnect if $dbh;
}

# Use in tests
setup_test_db();
# ... run tests ...
teardown_test_db();
```

## Coverage

```bash
# Install Devel::Cover
cpanm Devel::Cover

# Run tests with coverage
cover -test

# Generate HTML report
cover -report html

# View report
open cover_db/coverage.html
```

## Additional Resources

### Reference Files

- [Test Examples](./references/test-examples/) - Complete working test files
- [Mock Patterns](./references/mock-patterns.md) - Common mocking strategies

### Related Skills

For modern Perl coding patterns, see the **perl-development** skill.
