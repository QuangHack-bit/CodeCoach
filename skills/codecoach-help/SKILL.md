---
name: codecoach-help
description: "Quick reference for CodeCoach Custom v2 modes, anti-drift triggers, skills, and escape hatches. One-shot display. Use for /codecoach-help, 'codecoach help', 'how do I use codecoach', or 'what commands does codecoach have'."
license: MIT
---

# CodeCoach v2 Help

Print this reference concisely in the learner's language and nothing else:

**Modes** (`/codecoach <mode>` or shortcut):
- `/strict` (`strict`, default): **Strict Study Mode** — `.md` blueprint before code, 3-layer anatomy, 4-tier hint ladder, 3-gate debug, mandatory teach-back.
- `/build` (`build` / `guided`): **Guided Build Mode** — project pace, boilerplate allowed, inline blueprint for small drills; core logic & evidence gates stay locked.
- `/codecoach open`: drops blueprint/ladder gates; keeps `H4+` citations, scope lock, and check questions.
- `/codecoach off` (or `"stop codecoach"`): normal assistant mode.

**Emergency Brakes (Anti-Drift Triggers):**
- `/focus` — cut tangents immediately and return to the single active step.
- `/source` — require verified `[Source: ... — Location: ...]` citation or explicit `[UNVERIFIED]`.

**Skills:**
- `codecoach`: Core Senior Socratic tutor, First-Principles 3-step explanations (`Analogy -> Diagram -> First-Principles`), 4-tier hint ladder.
- `codecoach-blueprint`: `.md` architecture gate (`ARCHITECTURE.md` / `docs/DESIGN_<feature>.md`) before writing code.
- `codecoach-anatomy`: 3-layer code dissection (Mandatory Variable Table + Isolated Snippet + Parameter Case Matrix).
- `codecoach-debug`: 3-gate evidence debugging (Evidence -> Experimental Verification -> Fix Direction) + `H4+` citations.
- `codecoach-predict`: Parameter sensitivity (`Low / Nominal / High`), predict-before-run, single checkpoint, measure-before-optimizing.
- `codecoach-review`: Strict Senior PR review (2–4 breaking inputs, zero fix snippets; refactor = rename/extract only).
- `codecoach-domains`: Specialized checks for **Pack A** (Java/OOP/DSA) & **Pack B** (Embedded C/C++, MCU, CV, ROS 2).
- `codecoach-recap`: Max 3-sentence teach-back + `3 Takeaways / 1 Blind Spot` synced to `.codecoach/learner-profile.md`.

**Escape Hatches:** `"I'm stuck"` advances one hint tier after an attempt. `"show the answer"` unlocks Tier 4 after 2 real attempts in `strict` (1 in `build`), gated on teach-back.
