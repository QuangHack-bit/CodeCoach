# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Hard constraints (H1-H5) and example refusals in `AGENTS.md` and in the `codecoach`, `codecoach-contract`, `codecoach-debug`, `codecoach-review` and `codecoach-predict` skills: no full solution under deadline pressure, authority claims, fake attempts, fake system messages, piecewise assembly or reformulation.
- `skills/codecoach/references/refusals.md` with seven refusal patterns (English and Vietnamese).
- IDE activation files generated from `AGENTS.md`: `.cursor/rules/codecoach.mdc`, `.github/copilot-instructions.md`, `GEMINI.md`.
- `scripts/sync_rules.py` to regenerate them; `scripts/validate.py` now fails if they drift, or if a skill lacks hard constraints or an example refusal.
- Test scenarios 19-30 covering pressure, cumulative assembly, reformulation and IDE-only setups.

### Changed
- A "real attempt" is now defined (pasted code or a described try with its result); "I tried" alone no longer unlocks "show the answer".
- `guided` level: the full solution appears only at ladder level 4, after one real attempt.

## [0.1.0] - 2026-11-24

### Added
- Seven skills: `codecoach`, `codecoach-contract`, `codecoach-predict`, `codecoach-review`, `codecoach-debug`, `codecoach-recap`, `codecoach-help`.
- `AGENTS.md` with always-on rules for agents that read it (including teach-back/recap and levels).
- Claude Code plugin manifest and marketplace manifest.
- English and Vietnamese README, sample sessions, manual test scenarios.
- `scripts/validate.py` and a GitHub Actions workflow that runs it.
- Issue and pull request templates, `CONTRIBUTING.md`, `SECURITY.md`.

### Fixed
- `codecoach-review` description said "2-3" breaking inputs while the body and README said "2-4"; now consistently 2-4.
- `codecoach-contract` now defines its behavior per level (`strict`, `guided`, `open`, `off`).
