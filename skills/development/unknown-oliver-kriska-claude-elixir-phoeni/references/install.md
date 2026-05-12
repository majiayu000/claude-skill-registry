# Installing rtk

[rtk (Rust Token Killer)](https://github.com/rtk-ai/rtk) is a CLI proxy that
intercepts terminal commands, runs them, and filters output through TOML rules
before returning to the caller. For Claude Code, this means mix output gets
compressed *before* it reaches the transcript — the only architectural layer
where token savings are possible.

## Install

### macOS (homebrew)

```bash
brew install rtk-ai/tap/rtk
rtk --version    # verify (expect 0.39.0+)
```

### Other platforms

See the [rtk README](https://github.com/rtk-ai/rtk#install) for Linux and
manual install options.

## Shell hook (required)

rtk only intercepts commands when its shell hook is installed. The hook
rewrites `mix X` to `rtk mix X` transparently — no manual prefixing.

```bash
rtk init zsh  # or `rtk init bash`
```

This adds a hook to `~/.zshrc` (or `~/.bashrc`). Reload your shell:

```bash
exec $SHELL -l
```

Verify the hook works:

```bash
mix --help    # should run normally — rtk passes through commands without filters
```

If you see `rtk: command not found` or `mix` runs raw without filtering, the
hook didn't install. Check `~/.zshrc` for an `rtk init` block.

## Verify filters

After dropping filters into `.rtk/filters.toml`:

```bash
rtk test mix-test       # runs [[tests.mix-test]] fixtures from filters.toml
rtk test mix-credo
rtk test mix-dialyzer
rtk test mix-compile
rtk test mix-deps-get
rtk test mix-ecto-migrate
```

Each should report "passed" for every test fixture. If any fail, the regex
patterns may not match your rtk version's regex engine — file an issue on
the rtk repo.

## Measure the win

```bash
rtk gain                  # token savings summary
rtk gain --history        # per-command breakdown
rtk cc-economics          # spending vs savings analysis
```

Run after a week of normal usage to see actual reduction. Expected ranges
for Phoenix projects:

| Command | Typical compression | Big win cases |
|---------|-------------------:|---------------|
| `mix test` (passing) | 90%+ | All-green runs collapse to one line |
| `mix credo` (clean) | 95%+ | Clean runs collapse to one line |
| `mix dialyzer` (clean) | 95%+ | PLT progress disappears |
| `mix compile` (no warnings) | 70-90% | Worker-prefix noise stripped |
| `mix test` (failures) | 10-30% | Failure blocks preserved verbatim |

## Telemetry

rtk has telemetry **disabled by default**. Verify in
`~/Library/Application Support/rtk/config.toml`:

```toml
[telemetry]
enabled = false
consent_given = false
```

Filters run locally. No command output, file paths, or filter content leaves
your machine.

## Disable / uninstall

To disable temporarily without uninstalling:

```bash
# Remove the rtk init line from ~/.zshrc, then:
exec $SHELL -l
```

To uninstall:

```bash
brew uninstall rtk
rm -rf ~/Library/Application\ Support/rtk
rm -rf .rtk    # in any project that has one
```

## Troubleshooting

**Filter not applying**: rtk only filters when the command matches a filter's
`match_command` regex. Check `rtk config show-filters` to list registered
filters in the current directory.

**Test fixtures fail after copying**: rtk uses Rust's regex crate which does
NOT support backreferences (`\1`, `\2`). If you wrote your own patterns, avoid
them.

**Want raw output for one command**: prefix with `command`:

```bash
command mix test    # bypasses rtk
```
