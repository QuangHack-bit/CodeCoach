# CodeCoach Learner Profile

> Active cross-session memory for CodeCoach v2. Copy to `.codecoach/learner-profile.md` (via `python scripts/personalize.py --init-profile`) so the tutor adapts to your baseline without repeating basics.

## Owner & Environment
- **Learner:** QuangHack-bit (`@QuangHack-bit`)
- **Primary Domains:** Embedded C/C++ (MCU, Firmware), AI & Robotics (Python, Computer Vision, ROS 2), Software Foundations (Java, OOP, DSA)
- **Preferred IDEs:** Antigravity IDE / Gemini CLI, Cursor, VS Code + GitHub Copilot
- **Default Mode:** `strict` (`Strict Study Mode`; switchable via `/build`, `/strict`, `/focus`, `/source`)

## 1. Learning Habits & Preferences
- **Explanation Pipeline:** `Real-World Analogy (2-3 sentences)` -> `ASCII / Mermaid Flow or Memory Diagram` -> `First-Principles & Hardware/Complexity Trade-offs`.
- **Workflow Gate:** `.md` Blueprint (`ARCHITECTURE.md` or `docs/DESIGN_<feature>.md`) before source code.
- **Coaching Tone:** Strict Senior PR Reviewer — zero sycophancy, direct Socratic counter-questions, Ponytail scope lock (one step deep, zero unasked tangents).
- **Evidence Standard:** 3-gate debugging + mandatory citations (`[Source: ... — Location: ...]`) or explicit `[UNVERIFIED]` / `[CHƯA KIỂM CHỨNG]`.

## 2. Mastered Topics (Do NOT re-explain basics)
<!-- Coach reads this at session start and skips introductory definitions for listed items. -->
- *(Add mastered topics here, e.g., Basic C pointer syntax, Java class/interface syntax, Python list comprehensions)*

## 3. Recurring Blind Spots (Proactively probe early)
<!-- Coach watches for these traps during Blueprint, Anatomy, and Review steps. -->
- Jumping from vague idea/math straight to code without mapping data flow and module boundaries first.
- Missing boundary conditions (`null`/empty/1-element, integer overflow, ring-buffer wrap-around, ISR timing/blocking).
- Trial-and-error edits during debugging before isolating root cause with intermediate logs/signals.

## 4. Session Progress Log
<!-- Updated after `codecoach-recap`: Date | Topic | 3 Core Takeaways | 1 Blind Spot to Avoid -->
| Date | Topic / Module | 3 Core Takeaways | 1 Blind Spot to Avoid |
| :--- | :--- | :--- | :--- |
| YYYY-MM-DD | *(Initial setup)* | Profile initialized for CodeCoach v2 | Skipping blueprint `.md` under time pressure |
