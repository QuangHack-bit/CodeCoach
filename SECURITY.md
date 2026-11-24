# Security Policy

CodeCoach contains only Markdown and JSON instructions and one standard-library Python validation script. It does not run code on your machine by itself, make network requests or collect data.

## What counts as a security issue

- A skill or rule that could cause a host agent to run destructive commands without warning (the safety rules say it must warn before delete, overwrite, network or costly operations).
- Instructions that could be abused for prompt injection against the host agent.
- Anything in `scripts/` that could execute untrusted input.

## Reporting

Please do not open a public issue for a vulnerability. Use GitHub's **Report a vulnerability** button under the repository's **Security** tab (private vulnerability reporting). Include the affected file, a description and steps to reproduce. You can expect an initial response within 7 days.

## Supported versions

Only the latest released version receives fixes.
