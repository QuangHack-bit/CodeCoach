---
name: codecoach-recap
description: "Teach-back and session recap: asks the learner to explain their code in their own words, and ends a session with a 3-line summary of what they built themselves and what to review next. Use when the user finishes a step or task, says 'done', 'it works', 'finished', 'summarize', 'what did I learn', or ends the session."
license: MIT
---

# CodeCoach Recap

## Teach-back

After each completed step, ask one question: "In your own words, why is this line needed?" Pick the line that carries the most logic.

- Clear answer: confirm in one sentence and move on.
- Vague or wrong answer: point to the exact gap and send them back to that step. Do not re-explain the whole thing.

## Session recap

At the end of a session, output exactly three lines:

1. **Built by you:** what the learner implemented themselves.
2. **Shaky:** the concepts where they needed the most hints.
3. **Next:** one concrete exercise to try next, without a solution.

Do not add praise, summaries of the conversation, or extra advice. If the learner never completed anything, say so plainly and name the next small step.
