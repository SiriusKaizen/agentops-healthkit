# agentops-healthkit

Small local health checks for people running AI agents, CLIs, MCP servers, n8n, and webhook tools on their own machine.

## What it does

- Checks whether expected commands exist.
- Checks whether local TCP ports are reachable.
- Prints human-readable or JSON output.
- Avoids reading secrets, environment values, or private config files.

## Status

Early development. The first goal is a safe `doctor` command that helps operators understand what is running locally.

## Quick Start

```bash
python3 agentops_healthkit.py doctor
python3 agentops_healthkit.py doctor --json
python3 agentops_healthkit.py doctor --profile profiles/local-agentops.json
```

## Example Checks

Default checks look for common local automation commands such as `codex`, `claude`, `n8n`, `node`, `python3`, and `gh`. Default port checks cover common local app and bridge ports: `3000`, `3417`, and `5678`.

## Safety

This tool only checks command availability and local port connectivity. It does not print tokens, `.env` values, OAuth files, or request bodies.

## License

MIT
