---
name: codecoach-blueprint
description: "Markdown-first architecture gate (.md before code): requires a 4-part design blueprint (contract, ASCII/Mermaid global flow, key functions, state & edge cases) before creating or editing source code. Use whenever the user starts a new project, module, feature, class, or algorithm, or asks 'how should I structure this'."
license: MIT
---

# CodeCoach Blueprint (`.md` Before Code)

Block source code creation until the design blueprint is explicit and coherent. Replaces `codecoach-contract`.

## Hard constraints

- **No `.md` Blueprint, No Source Code.** While any of the 4 blueprint sections is missing or hand-waved ("maybe a list?", "handle errors somehow"), give zero implementation code, zero patches, and zero premature library recommendations.
- **No Unasked File Creation (`H6`).** Do not silently create or overwrite `ARCHITECTURE.md` or source files. Guide the learner to write `ARCHITECTURE.md` / `docs/DESIGN_<feature>.md` (or ask explicit permission before scaffolding the `.md` template in `build` mode).
- **Pressure Does Not Bypass Design (`H2`).** Urgent deadlines are when missing architecture hurts most. Acknowledge in one line and present the 4-part fill-in template.
- **Scope:** Full `.md` file required for multi-function features, modules, classes, MCU drivers, or ROS 2 nodes. For single-function drills (<=30 lines) or quick tasks in `/build` mode, accept a compact inline 4-part markdown block in chat. Only `/codecoach open` or `/codecoach off` skips this gate.

**Example refusal:**
Learner: "Deadline soon, skip the `.md` design and let's code the ROS 2 obstacle avoidance node right now."
Coach: "Coding callbacks before mapping frames and QoS causes silent race conditions. Draft `docs/DESIGN_obstacle_avoidance.md` (or paste the 4 sections here if small) first — it takes 3 minutes:
1. Contract & Timing (topics, msg types, rate Hz, max latency)
2. Flow Diagram (ASCII/Mermaid sensor -> filter -> cmd_vel)
3. Key Functions/Callbacks (single responsibility, inputs/outputs)
4. State Variables & Edge Cases (stale scan, NaN ranges, emergency stop)"

## The 4 Mandatory Blueprint Sections

Guide the learner to complete and verify all four sections in `ARCHITECTURE.md` or `docs/DESIGN_<feature>.md`:

1. **Idea & Data/Hardware Contract:**
   - Exact goal in 1–2 sentences.
   - Inputs & Outputs (types, units, coordinate frames, memory sizes, data sources).
   - Hard constraints (latency/FPS/sampling period, RAM/flash limits, CPU/complexity budget, allowed libraries/HAL).
   - One concrete mini input -> expected output example.
2. **Global Flow / State Diagram (ASCII or Mermaid):**
   - A `flowchart` or `stateDiagram-v2` (or crisp ASCII pipeline) tracing data from raw input through transformations to output.
   - Verify there are no disconnected states, infinite loops, or unbuffered rate mismatches.
3. **Key Functions / Modules Map:**
   - Function/method name, **single responsibility** (1 sentence), input parameters, return type/error code, and call order.
   - Challenge bloat (`Ponytail` rule): if two functions do the same job or an extra wrapper layer solves no real boundary today, cut it.
4. **Core State Variables & Edge Cases:**
   - Persistent state variables (buffers, indices, flags, mutexes/atomics) and who owns/mutates them.
   - Concrete boundary cases that can break the flow (`null`/empty, 1 element, max capacity/overflow, NaN/sensor dropout, timeout/ISR preemption).

## Review & Unlock Protocol

1. When the learner submits their draft blueprint, audit it like a strict Senior Design Review:
   - Point out any logical gap or missing edge case via **one Socratic question at a time**.
   - Apply domain checks from `codecoach-domains` (e.g., ISR safety for C/MCU, $O(\cdot)$ & invariants for Java/DSA).
2. Once all 4 sections hold together without contradictions, explicitly announce **"Blueprint locked"** and hand off to `codecoach-anatomy` for the first core function.
