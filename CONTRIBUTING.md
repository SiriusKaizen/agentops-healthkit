# Contributing

Thanks for helping improve agentops-healthkit.

## Local Setup

This project uses the Python standard library only.

```bash
python3 -m unittest discover -s tests
python3 agentops_healthkit.py doctor --no-default-ports --command python3
python3 agentops_healthkit.py roster-check examples/agent-roster.sample.json
```

## Contribution Guidelines

- Keep checks local-first and safe by default.
- Do not read `.env` files, OAuth files, tokens, or private config unless a future feature has explicit opt-in behavior.
- Prefer small changes with tests.
- Use placeholder data in examples. Do not add real hostnames, routes, chat ids, credentials, or operator topology.

## Useful Areas

- Additional local health checks.
- More roster validation rules.
- Better JSON output for automation.
- Clearer troubleshooting messages for non-programmer operators.
