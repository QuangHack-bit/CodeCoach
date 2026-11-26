# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-11-26

### Added
- **CodeCoach Custom v2 Core Upgrade (`AGENTS.md`, `skills/codecoach/SKILL.md`):** Strict Senior PR reviewer persona (zero sycophancy), Ponytail scope lock, Core Logic vs. Boilerplate split, 3-step First-Principles explanation pipeline (`Analogy -> Diagram -> First-Principles`), `H6` no-unasked-file-edits lock, and emergency brakes (`/focus`, `/strict`, `/build`, `/source`).
- **`codecoach-blueprint` skill:** Replaces `codecoach-contract` with a `.md`-before-code architecture gate (`ARCHITECTURE.md` / `docs/DESIGN_<feature>.md`) covering Contract, ASCII/Mermaid Global Flow, Key Functions, and State/Edge Cases.
- **`codecoach-anatomy` skill:** 3-layer code frame dissection (Mandatory Variable Table, Isolated/Analogous Snippet, and Low/Nominal/High Parameter Selection Matrix).
- **`codecoach-domains` skill:** Specialized domain packs — **Pack A** (`*.java`, OOP encapsulation, loop invariants, $O(\cdot)$, DSA boundary suite) and **Pack B** (`*.c/*.cpp/*.h/*.py` for MCU/STM32, `SPI/I2C/UART/DMA`, ISR hygiene, Computer Vision, and `ROS 2`).
- **Cross-session learner memory (`profile/learner-profile.template.md` & `.codecoach/learner-profile.md`):** Tracks Habits, `Mastered Topics`, `Recurring Blind Spots`, and `Session Progress Log`; integrated into `scripts/personalize.py` (`--init-profile`, `--add-mastered`, `--add-blind-spot`), `codecoach-recap`, and the `learner_profile` MCP tool.
- **Modular Multi-IDE Rule Compiler (`scripts/sync_rules.py`):** Generates split & glob-scoped Cursor rules (`.cursor/rules/00-core-ponytail.mdc` .. `31-java-dsa.mdc`), GitHub Copilot scoped instructions (`.github/instructions/*.instructions.md`), and a token-deduplicated `GEMINI.md` companion.
- Real-world v2 test scenarios (31–33) in `tests/scenarios.md` covering Java DSA invariants, STM32/ROS 2 control loops, and Gate-1 missing-log evidence locking.

### Changed
- **`codecoach-debug` upgraded to 3 Evidence Gates + `H4+` Citation Gate:** Requires Evidence Lock -> Experimental Verification -> Verified Fix Direction, plus `[Source: ... — Location: ...]` citations or explicit `[UNVERIFIED]` (`[CHƯA KIỂM CHỨNG]`).
- **`codecoach-recap` upgraded:** Enforces a max 3-sentence learner teach-back and `3 Core Takeaways + 1 Blind Spot to Avoid` synced to `.codecoach/learner-profile.md`.
- **`mcp/server.mjs` upgraded to `0.2.0`:** Added `build` mode support, `learner_profile` tool, and backward-compatible `codecoach-contract` -> `codecoach-blueprint` alias.
- **`scripts/validate.py` upgraded:** Validates all 9 v2 skills, `H4+` citation rules, anti-drift triggers, `learner-profile.template.md` sections, version sync across Claude/Gemini/MCP manifests, and multi-IDE rule deduplication.

### Removed
- Replaced legacy `skills/codecoach-contract` and monolithic `.cursor/rules/codecoach.mdc` with `skills/codecoach-blueprint` and modular `.cursor/rules/*.mdc`.

## [0.1.0] - 2026-11-24

### Added
- Initial release with seven v1 skills, `AGENTS.md`, Claude Code & Gemini manifests, minimal MCP server, English/Vietnamese READMEs, and `scripts/validate.py`.
