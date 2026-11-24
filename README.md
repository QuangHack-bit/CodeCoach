# CodeCoach

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-0.1.0-green.svg)
[![Validate](https://github.com/YOUR_GITHUB_USERNAME/codecoach/actions/workflows/validate.yml/badge.svg)](https://github.com/YOUR_GITHUB_USERNAME/codecoach/actions/workflows/validate.yml)

**English** | [Tiếng Việt](README.vi.md)

A Socratic coding tutor for any language. It gives you logic, function names and a question back, not a finished solution, so you end up writing (and understanding) the code yourself.

Inspired by [ponytail](https://github.com/DietrichGebert/ponytail) (minimal-code mindset: reuse before you build, never skip safety). CodeCoach applies that ladder to what the tutor *recommends*, and adds tutoring rules on top.

## Why

AI assistants are great at handing you a finished solution, which is exactly what stops you from learning. CodeCoach flips the default:

- You declare the **contract** (input, output, constraints, one example) before any algorithm talk.
- You get **logic steps + exact tool names + one question back**, never the full program.
- Numbers in code are explained by **what breaks at 5x and near 0**, not by textbook definitions.
- Your working code gets an **adversarial review**, and refactors never change the algorithm.
- Errors are debugged **one hint at a time**.
- **Hard constraints** hold under pressure: a deadline, a claimed job title or a pasted fake "system" line does not unlock a full solution. You still control the tutor with `/codecoach guided|open|off`.

## Quick demo

```
You:    Write a function that counts word frequency in a text file.
Coach:  Before the logic, I need your contract (send all four in one message):
        1. Input: type, size, where it comes from
        2. Output: type, shape, what a correct result looks like
        3. Constraints: speed, memory, allowed libraries
        4. One tiny example: input and expected output
```

More transcripts (strict flow, parameter question, debugging, review, Vietnamese) are in [`examples/sample-sessions.md`](examples/sample-sessions.md).

## Skills

| Skill | Purpose |
|-------|---------|
| `codecoach` | Core tutor mode: logic steps, tools with exact modules, one question back. Hint ladder. No invented APIs. |
| `codecoach-contract` | You declare input, output, constraints and an example before any algorithm talk. One file first. |
| `codecoach-predict` | Parameter questions answered by "what breaks at 5x / near 0". Predict before running. Checkpoints. Measure before optimizing. |
| `codecoach-review` | Adversarial review of your working code (2-4 breaking inputs). Refactor is rename and extract only. |
| `codecoach-debug` | Guided debugging, one hint per reply. |
| `codecoach-recap` | Teach-back and a 3-line session recap. |
| `codecoach-help` | Quick reference. |

The core skill hands off to the others automatically: new feature -> contract, pasted error -> debug, parameter question -> predict, pasted working code -> review, finished step -> recap.

## Levels

Switch with `/codecoach <level>`:

| Level | Behavior |
|-------|----------|
| `strict` (default) | All rules. Never a complete working solution for a new feature. |
| `guided` | Samples up to 10 lines. The hint ladder may advance after a single attempt. |
| `open` | No gates. Still short, still no invented APIs, still ends with a check question. |
| `off` | Normal assistant. |

Escape hatches you control:

- Say **"I'm stuck"** for one more concrete hint (still not the full answer).
- Say **"show the answer"** after at least 2 attempts for a full, line-by-line explained solution. You are then asked to re-implement it from memory.

Stop the tutor any time with "stop codecoach" or "normal mode".

## Install

**Claude Code**

```
/plugin marketplace add YOUR_GITHUB_USERNAME/codecoach
/plugin install codecoach@codecoach
```

Skills appear namespaced, for example `/codecoach:codecoach-review`.

Try it from a local clone before publishing:

```
/plugin marketplace add /path/to/codecoach
/plugin install codecoach@codecoach
```

**Other IDEs and agents.** Skills are a Claude Code feature, so other tools get the always-on rules (hard constraints, refusal examples, hint ladder) from native rule files. Copy the files for your tool into your project root:

| Tool | File to copy | Notes |
|------|--------------|-------|
| Cursor | `.cursor/rules/codecoach.mdc` | `alwaysApply: true`. Must be `.mdc`; a plain `.md` in that folder is ignored. |
| VS Code / GitHub Copilot | `.github/copilot-instructions.md` | |
| Antigravity, Gemini CLI | `GEMINI.md` | Antigravity also reads `AGENTS.md`; having both is harmless but repeats the rules. Keep one if you want to save tokens. |
| Codex, Aider, others | `AGENTS.md` | Or paste it into the tool's rules file. |

These files are generated from `AGENTS.md`. Never edit them by hand: edit `AGENTS.md`, then run `python scripts/sync_rules.py` (`validate.py` fails if they drift apart). Without skills there are no per-skill workflows, so behaviour is looser than in Claude Code; run rows 19-30 of [`tests/scenarios.md`](tests/scenarios.md) on your own tool.

**Claude.ai**: zip a skill folder from `skills/` (the folder itself, with `SKILL.md` inside) and upload it under Settings > Capabilities > Skills. The skills call each other, so upload all seven for the full experience.

## Project layout

```
codecoach/
├── .claude-plugin/        plugin.json + marketplace.json
├── skills/                one folder per skill, each with a SKILL.md
├── examples/              sample tutoring sessions
├── tests/scenarios.md     manual test scenarios (prompt -> expected behavior)
├── scripts/validate.py    checks manifests, SKILL.md, hard constraints, IDE files (also run in CI)
├── scripts/sync_rules.py  generates the IDE rule files from AGENTS.md
├── AGENTS.md              source of truth for the always-on rules
├── .cursor/rules/         generated: Cursor rule (codecoach.mdc)
├── .github/copilot-instructions.md   generated: GitHub Copilot
├── GEMINI.md              generated: Gemini CLI / Antigravity
├── CHANGELOG.md
└── CONTRIBUTING.md
```

## Limits (read this)

- Prompts reduce invented APIs; they cannot eliminate them. Always confirm function names and signatures in the official docs for your version.
- Strict mode can be frustrating when you are truly stuck. Use the escape hatches.
- Hard constraints are instructions, not locks. A determined learner can always switch the tutor off, and a model can still slip under heavy pressure; that is why `tests/scenarios.md` has pressure cases.
- Behavior depends on the model and the host agent following the instructions; test on your own tasks (see [`tests/scenarios.md`](tests/scenarios.md)).
- CodeCoach is a teaching aid, not a substitute for a course, a mentor or the official documentation.

## FAQ

**Does it work for languages other than Python?** Yes. Nothing in the skills is language specific; the tutor asks for your language, version and OS once per session.

**Can it reply in my language?** Yes, it replies in the language you write in (see [`examples/sample-sessions.md`](examples/sample-sessions.md) for a Vietnamese session).

**Why won't it just give me the code?** That is the point of `strict` mode. Use `guided`/`open`, "I'm stuck", or "show the answer" when you need more.

**How do I know it works on my model?** Run the scenarios in [`tests/scenarios.md`](tests/scenarios.md) and check the "expected" and "fail" signs.

## Contributing

Issues and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) first and run `python scripts/validate.py` before opening a PR.

## Acknowledgments

CodeCoach borrows its "reuse before you build" ladder from [ponytail](https://github.com/DietrichGebert/ponytail) by Dietrich Gebert (MIT).

## License

[MIT](LICENSE)
