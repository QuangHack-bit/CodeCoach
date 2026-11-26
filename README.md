# CodeCoach Custom (v2)

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-0.2.0-green.svg)
[![Validate](https://github.com/QuangHack-bit/CodeCoach/actions/workflows/validate.yml/badge.svg)](https://github.com/QuangHack-bit/CodeCoach/actions/workflows/validate.yml)

**English** | [Tiếng Việt](README.vi.md)

A strict **Senior Socratic Coding Tutor** built for first-principles engineering mastery across **Embedded C/C++ (MCU/Firmware)**, **AI & Robotics (Python, CV, ROS 2)**, and **Software Foundations (Java, OOP, DSA)**.

Inspired by [ponytail](https://github.com/DietrichGebert/ponytail) (minimal code, reuse before building, scope lock, zero sycophancy), **CodeCoach v2** enforces **`.md` Blueprint before Code**, **3-Layer Code Anatomy**, **3-Gate Evidence Debugging**, **Mandatory Citations (`H4+`)**, and **Cross-Session Learner Memory**.

## What Changed in v2

- **`.md` Blueprint Before Code (`codecoach-blueprint`):** Replaces `codecoach-contract`. Locks source code until `ARCHITECTURE.md` / `docs/DESIGN_<feature>.md` maps Contract, ASCII/Mermaid Flow, Key Functions, and State/Edge Cases.
- **3-Layer Code Anatomy (`codecoach-anatomy`):** Dissects frames via a **Mandatory Variable Table**, an **Isolated/Analogous Snippet**, and a **Parameter Selection Matrix** (`Low / Nominal / High`) — without writing your core logic.
- **First-Principles Triad:** Explains concepts via `Real-World Analogy (2-3 sentences)` -> `ASCII/Mermaid Diagram` -> `First-Principles (CPU, memory, hardware, math)`.
- **3-Gate Evidence Debugging & `H4+` Citations (`codecoach-debug`):** Bans blind guessing. Requires (1) Evidence Lock -> (2) Experimental Verification -> (3) Root-Cause Fix Direction, plus `[Source: <Doc/Datasheet + Version> — Location: <Section/Symbol>]` or explicit `[UNVERIFIED]`.
- **Specialized Domain Packs (`codecoach-domains`):** Pack A (`*.java`, DSA invariants, $O(\cdot)$, OOP) & Pack B (`*.c/*.cpp/*.h/*.py` for MCU, `SPI/I2C/UART/DMA`, ISR hygiene, CV, ROS 2).
- **Cross-Session Learner Profile (`.codecoach/learner-profile.md`):** Skips re-explaining `Mastered` topics and proactively probes `Recurring Blind Spots`.
- **Smart Multi-IDE Rule Compiler (`scripts/sync_rules.py`):** Generates glob-scoped Cursor `.mdc` rules, GitHub Copilot `.instructions.md`, and deduplicated `GEMINI.md` (zero duplicate token drain alongside `AGENTS.md`).

## Skills (v2 Suite)

| Skill | Purpose |
| :--- | :--- |
| `codecoach` | Core Senior Socratic orchestrator: zero sycophancy, Ponytail scope lock, 3-step First-Principles pipeline, 4-tier hint ladder, `H1`–`H6` & `H4+` gates. |
| `codecoach-blueprint` | `.md` architecture gate (`ARCHITECTURE.md` / `docs/DESIGN_<feature>.md`): Contract, ASCII/Mermaid Flow, Key Functions, State & Edge Cases before coding. |
| `codecoach-anatomy` | 3-layer code frame dissection: Mandatory Variable Table + Isolated Mechanism Snippet + Low/Nominal/High Parameter Case Matrix. |
| `codecoach-debug` | 3-gate evidence debugging (Evidence -> Experimental Verification -> Verified Fix Direction) + `H4+` mandatory citations or `[UNVERIFIED]`. |
| `codecoach-domains` | Domain packs: **Pack A** (Java/OOP/DSA invariants & boundary suite) and **Pack B** (Embedded C/C++, MCU/STM32, ISR/DMA, CV & ROS 2). |
| `codecoach-predict` | Parameter sensitivity interrogation (`Low / Nominal / High` & `5x / near-0`), predict-before-run, single checkpoint, measure-before-optimizing. |
| `codecoach-review` | Strict Senior PR review of your working code (2–4 realistic breaking inputs/hazards, zero fix snippets; refactor = rename/extract only). |
| `codecoach-recap` | Max 3-sentence learner teach-back + `3 Core Takeaways / 1 Blind Spot to Avoid` persisted to `.codecoach/learner-profile.md`. |
| `codecoach-help` | One-shot quick reference for modes, emergency brakes, skills, and escape hatches. |

## Modes & Anti-Drift Emergency Brakes

Switch modes anytime:

| Command | Mode / Action |
| :--- | :--- |
| `/strict` or `/codecoach strict` | **Strict Study Mode (default):** Full `.md` blueprint gate, 4-tier hint ladder, zero core/boilerplate hand-holding, mandatory teach-back. |
| `/build` or `/codecoach build` (`guided`) | **Guided Build Mode:** Project pace — assists with boilerplate/config and allows compact inline blueprints for <=30-line tasks; core logic & evidence gates remain locked. |
| `/codecoach open` | Drops blueprint/ladder gates; keeps `H4+` citations, scope lock, and check questions. |
| `/codecoach off` | Normal assistant mode (also `"stop codecoach"`). |
| `/focus` | **Brake:** Immediately cut tangents and return to the single active step. |
| `/source` | **Brake:** Stop and cite `[Source: ... — Location: ...]` or label `[UNVERIFIED]`. |

**Escape hatches:** `"I'm stuck"` advances one hint tier after an attempt. `"show the answer"` unlocks Tier 4 after 2 real attempts in `strict` (1 in `build`), gated on a mandatory 3-sentence teach-back.

## Install & Multi-IDE Setup

### 1. Antigravity IDE / MCP Server + Global Skills
1. Copy `skills/*` into `~/.gemini/config/skills/` (or Windows `%USERPROFILE%\.gemini\config\skills\`).
2. Add the MCP server (`get_rules`, `list_skills`, `get_skill`, `session_state`, `learner_profile`) to `~/.gemini/config/mcp_config.json`:
   ```json
   "codecoach": {
     "command": "node",
     "args": ["/path/to/CodeCoach/mcp/server.mjs"]
   }
   ```

### 2. Claude Code
```bash
/plugin marketplace add QuangHack-bit/CodeCoach
/plugin install codecoach@codecoach
```

### 3. Project-Level Rules (Cursor, VS Code Copilot, Gemini CLI, Antigravity)
Generated automatically from `AGENTS.md` + `skills/` via `python scripts/sync_rules.py`:
- **Cursor:** Copy `.cursor/rules/*.mdc` (`00-core-ponytail.mdc`, `10-blueprint-md.mdc`, `20-debug-evidence.mdc`, `30-embedded-robotics.mdc`, `31-java-dsa.mdc`).
- **VS Code / GitHub Copilot:** Copy `.github/copilot-instructions.md` and `.github/instructions/*.instructions.md`.
- **Gemini CLI / Antigravity:** Copy `AGENTS.md` (and optional deduplicated companion `GEMINI.md`).

### 4. Initialize Cross-Session Learner Profile
```bash
python scripts/personalize.py --init-profile --workspace /path/to/your/project
```

## Project Layout

```text
CodeCoach/
├── AGENTS.md                        # Core Senior + Ponytail + H1-H6 / H4+ laws
├── GEMINI.md                        # Deduplicated Gemini/Antigravity routing companion
├── profile/
│   └── learner-profile.template.md  # Cross-session learner memory template
├── mcp/                             # Node.js MCP server (get_rules, get_skill, learner_profile, ...)
├── skills/                          # 9 modular v2 skills (blueprint, anatomy, debug, domains, ...)
├── .cursor/rules/                   # Generated split & glob-scoped Cursor rules (.mdc)
├── .github/                         # copilot-instructions.md + instructions/*.instructions.md + CI
├── scripts/
│   ├── personalize.py               # Author personalization + learner-profile CLI manager
│   ├── sync_rules.py                # Multi-IDE rule compiler
│   └── validate.py                  # Automated validator for skills, H4+, profile & IDE sync
└── tests/
    ├── mcp-smoke.mjs                # Automated MCP server smoke test
    └── scenarios.md                 # 33 behavioral & domain test scenarios
```

## License

[MIT](LICENSE)
