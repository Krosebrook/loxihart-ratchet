# Security and trust boundaries

The runtime helper and installer use the Python standard library and make no network/model calls. They do not execute instructions from reports. The host agent and its tools still control shell execution, network access, provider calls, and permissions.

The ledger is local, editable bookkeeping. It checks content freshness and declared session differences, not truthfulness, identity, or authorization. Use independent reviewers and external CI/branch protection when enforcement matters. Keep `.ratchet/` artifacts and secrets out of public commits.

Report a reproducible vulnerability using this repository's GitHub private vulnerability reporting option if enabled; otherwise contact the maintainer through their GitHub profile before sharing sensitive exploit details in a public issue.
