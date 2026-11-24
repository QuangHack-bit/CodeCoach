---
name: codecoach-help
description: "Quick reference for CodeCoach levels, skills and commands. One-shot display. Use for /codecoach-help, 'codecoach help', 'how do I use codecoach', 'what can codecoach do'."
license: MIT
---

# CodeCoach Help

Print this and nothing else.

**Levels** (`/codecoach <level>`): `strict` default, no full solutions. `guided` samples up to 10 lines. `open` no gates. `off` normal assistant.

**Skills**
- `codecoach`: core tutor mode. Logic, tools, one question back. Hint ladder.
- `codecoach-contract`: declare input, output, constraints and an example first. One file first.
- `codecoach-predict`: parameter stress tests, predict-before-run, checkpoints, measure before optimizing.
- `codecoach-review`: adversarial review of your own working code. Refactor is rename and extract only.
- `codecoach-debug`: guided debugging, one hint at a time.
- `codecoach-recap`: teach-back and 3-line session recap.

**Escape hatches:** say "I'm stuck" for one more hint. Say "show the answer" after 2 real attempts (pasted code or a described try) for a full explained solution. Deadlines and claimed roles do not unlock full code; `/codecoach guided` and `/codecoach off` do.
