---
name: kubectl-port-forward
description: Use kpf, a fast, idempotent drop-in replacement for kubectl port-forward that manages and reuses port-forward sessions. Use when a user needs repeatable Kubernetes port forwarding with quick startup.
---

# kubectl-port-forward

Use this skill when you need to run Kubernetes port-forwarding commands.

`kpf` is a fast, idempotent, non-blocking, drop-in replacement for `kubectl port-forward`.
It manages background port-forward sessions and reuses them for identical requests,
which speeds up connection time and reduces complexity of port forwarding in scripts.

Example use cases:

- Port-forwarding to an internal service that is not yet exposed via a domain.
- Port-forwarding to a service that has a domain but requires SSO auth (for example, Vouch proxy), making automation harder.

Use `kpf` when running ad-hoc commands, but do NOT commit scripts that depend on `kpf`
as it's not a standard tool in the developer toolbox and may not be available in all environments.

## Run

Use `kpf` with the same argument style as `kubectl port-forward`.
Prefer using a random port (by omitting the local port), to avoid port conflicts.
Example usage:

```shell
PORT=$(kpf --context=<context> --namespace=<ns> service/<name> 8481)
curl "http://127.0.0.1:${PORT}/example"
```

If you _want_ the `kpf` session to be kept alive indefinitely, use `kubectl port-forward` instead,
since `kpf` sessions have a TTL.

## Troubleshooting

If you run into issues with the `kpf` tool itself, first try `kubectl port-forward`
with the same arguments to verify that the issue is with `kpf` and not your cluster or network.
Then consult https://github.com/bduffany/kpf/blob/main/README.md for more technical details
that may help with debugging.
