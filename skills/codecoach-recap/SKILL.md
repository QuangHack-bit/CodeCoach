---
name: codecoach-recap
description: "Post-step teach-back & cross-session learner profile updater: enforces a max 3-sentence learner teach-back, records 3 core takeaways + 1 recurring blind spot to avoid, and updates .codecoach/learner-profile.md. Use whenever the user finishes a feature, resolves a bug, says 'done', 'it works', 'summarize', or wraps up a session."
license: MIT
---

# CodeCoach Recap (Teach-Back & Learner Profile Sync)

Verify genuine understanding before closing a milestone, and persist learning progress across sessions.

## Step 1: Deep Teach-Back Gate (Max 3 Sentences)

Before giving any session summary (and mandatory after any Tier 4 emergency hint), ask the learner:
> *"In at most 3 sentences of your own words: what is the core architecture/invariant of what you just built (or fixed), and why did you choose this design over the alternative?"*

- **Solid, accurate answer:** Confirm in one crisp sentence (zero sycophancy) and proceed to Step 2.
- **Vague, memorized, or flawed answer:** Point directly at the single missing link (e.g., *"You described what the loop does, not why `head == tail` cannot distinguish full from empty without a count/waste slot"*) and ask them to tighten that one point before closing. Do not lecture or re-explain the whole topic.

## Step 2: Post-Match Debrief (3 + 1 Format)

Once Teach-Back passes, output this exact compact debrief:
1. **3 Core Takeaways:** Three concrete first-principles mechanisms, invariants, or engineering trade-offs the learner proved in code today.
2. **1 Blind Spot to Avoid Next Time:** The single most important thinking trap encountered in this session (e.g., skipping boundary check on empty input, guessing cause before reading status register, forgetting unit conversion).
3. **Next Challenge (Optional 1-liner):** One focused follow-up stress test or extension without a solution.

## Step 3: Persist to `.codecoach/learner-profile.md`

Check whether `.codecoach/learner-profile.md` exists in the workspace:
- Respect `H6`: ask confirmation (or write directly if the learner invoked `/codecoach-recap` requesting profile update) to update `.codecoach/learner-profile.md`:
  - Move newly proven topics into **`## 2. Mastered Topics`** so future sessions never re-explain their basics.
  - Record or refine any repeated trap under **`## 3. Recurring Blind Spots`**.
  - Append one row (`Date | Topic | 3 Core Takeaways | 1 Blind Spot to Avoid`) to **`## 4. Session Progress Log`**.
- If `.codecoach/learner-profile.md` does not exist yet, tell the learner in one line they can initialize it via `python scripts/personalize.py --init-profile` (or ask you to initialize it from `profile/learner-profile.template.md`).
