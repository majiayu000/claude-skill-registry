---
name: signing-preflight
description: Before the first commit of a session, check that commit signing will work — the key is loaded and unlocked — and ask the operator to unlock it once, up front, instead of discovering it after a hundred unsigned commits. Never disables signing silently, never re-signs history without asking. Use at the start of implementation work in a repo that signs commits ("коммиты не подписаны", "ssh-keygen висит", "gpg failed to sign"). Loaded by senior-dev, devops.
when_to_use: |
  Apply when:
  - you are about to make the first commit of a session in a repository
  - `git commit` hangs, or fails with "gpg failed to sign the data" / "error: signing failed"
  - the operator reports commits arriving unsigned
  Do NOT apply to:
  - repositories where commit.gpgsign is off and no branch protection requires signatures
effort: low
allowed-tools: Read, Bash
---

# signing-preflight — find the locked key before the first commit, not after the hundredth

On real projects: an agent committed unsigned without asking to unlock the key; a
signing call on a locked SSH key hung the session; 121 commits had to be re-signed after
the fact — and the key turned out to have no passphrase at all. Each was a two-second
question at the start of the session.

## Check (read-only, bounded)

```bash
git config --get commit.gpgsign          # true → signing is expected
git config --get gpg.format              # ssh | openpgp (empty = openpgp)
git config --get user.signingkey
```

**SSH signing** — does a test signature finish? (`user.signingkey` may be a key file or a
literal `key::ssh-…`; the test signature is the check that works for both.)

```bash
K="$(git config --get user.signingkey)"; case "$K" in key::*) printf '%s\n' "${K#key::}" > /tmp/sigpre.pub; K=/tmp/sigpre.pub ;; esac
echo preflight | perl -e 'alarm 5; exec @ARGV' ssh-keygen -Y sign -n git -f "$K" >/dev/null 2>&1 && echo signs || echo CANNOT-SIGN
```

**OpenPGP** — a batch signature that refuses to prompt:

```bash
echo preflight | perl -e 'alarm 5; exec @ARGV' gpg --batch --pinentry-mode error --clearsign -u "$(git config --get user.signingkey)" >/dev/null 2>&1 && echo signs || echo CANNOT-SIGN
```

Always bound the test with a timeout: an unbounded signing call on a locked key waits
for a passphrase nobody will type, and the session stalls.

## Then

- **signs** → proceed; nothing to say.
- **CANNOT-SIGN** → one question to the operator, before any work:
  "Commit signing is on and the key is locked / not loaded. Unlock it (`ssh-add` /
  gpg-agent) and I will continue — or tell me to commit unsigned for this session."
  Wait for the answer. This is the one question worth stopping for at the start.

## Never, without being told

- `git -c commit.gpgsign=false commit …` or `--no-gpg-sign` — an unsigned commit on a
  branch that requires signatures is a push that will be refused, or worse, accepted.
- Re-signing history (`rebase --exec 'git commit --amend -S'`) — it rewrites every hash
  after the first commit it touches; on a pushed branch that is a force-push.

## Report unsigned work

If commits were made unsigned anyway, say so with the list:

```bash
git log --format='%h %G? %s' @{upstream}..HEAD | awk '$2!="G"'
```
