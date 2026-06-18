# Security Policy

agentops-healthkit is designed to avoid collecting secrets.

## Supported Scope

The current project checks command availability, local TCP ports, and sanitized agent roster files. It should not inspect secret stores, OAuth files, `.env` values, API keys, chat ids, or private request bodies.

## Reporting a Security Issue

Please open a GitHub issue with a minimal reproduction that does not include real credentials or private infrastructure details. If you need to describe sensitive behavior, replace values with placeholders before sharing.

## Maintainer Notes

- Keep examples sanitized.
- Treat accidental secret exposure as a bug.
- Prefer read-only checks unless a future feature clearly requires an explicit opt-in.
