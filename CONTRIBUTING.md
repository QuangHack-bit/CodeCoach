# Contributing to CodeCoach

Thanks for helping! CodeCoach is a set of prompts, so most contributions are changes to Markdown files.

## Ground rules

1. **Keep skills short and exact.** Every sentence in a `SKILL.md` costs tokens on every use. Prefer a rule over an explanation.
2. **Stay consistent.** If you change a rule, change it everywhere it appears: the relevant `SKILL.md`, `AGENTS.md`, both READMEs and `tests/scenarios.md`.
3. **Do not weaken the core promise.** In `strict` mode the tutor never hands over a full solution for a new feature and never invents APIs. Changes that loosen this belong in `guided` or `open`.
4. **`AGENTS.md` is the source of truth for IDE rules.** After editing it, run `python scripts/sync_rules.py`. Never edit `.cursor/rules/codecoach.mdc`, `.github/copilot-instructions.md` or `GEMINI.md` by hand.
5. **No dependencies.** The plugin is plain Markdown + JSON. The validation script uses only the Python standard library.

## Skill file checklist

Each skill lives in `skills/<name>/SKILL.md` and must have:

- Frontmatter with `name` (equal to the folder name, lowercase letters, digits and hyphens), `description` (what it does **and** when to use it, under 1024 characters) and `license`.
- A body that starts with a one-line purpose.
- For `codecoach`, `-contract`, `-debug`, `-review`, `-predict`: a `## Hard constraints` section and at least one `Example refusal`. `validate.py` enforces this.
- Trigger phrases in the `description` that real learners would type.

## Workflow

1. Fork and create a branch: `git checkout -b feat/short-name`.
2. Make your change.
3. Run `python scripts/sync_rules.py` if you touched `AGENTS.md`, then `python scripts/validate.py` (Python 3.8+). It must print no errors.
4. Run the relevant rows of [`tests/scenarios.md`](tests/scenarios.md) against a real model and note the result in your PR.
5. Add a line under `## [Unreleased]` in `CHANGELOG.md`.
6. Open a pull request using the template.

## Reporting bugs

Use the bug report issue template. Include the model/agent and version, your prompt, what the tutor did, and what you expected. Transcripts are the most useful evidence.

## Commit style

Short imperative subject, for example `fix(review): align description with 2-4 breaking inputs`. Prefixes `feat`, `fix`, `docs`, `chore` are welcome but not required.
