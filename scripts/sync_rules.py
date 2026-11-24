#!/usr/bin/env python3
"""Generate IDE-specific rule files from AGENTS.md (the single source of truth).

Usage:
    python scripts/sync_rules.py           # write the generated files
    python scripts/sync_rules.py --check   # exit 1 if any file is out of date (used by validate.py)

Generated files:
    .cursor/rules/codecoach.mdc            Cursor (alwaysApply rule)
    .github/copilot-instructions.md        GitHub Copilot (VS Code, github.com)
    GEMINI.md                              Gemini CLI / Antigravity
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "AGENTS.md"
BANNER = "<!-- GENERATED from AGENTS.md by scripts/sync_rules.py. Edit AGENTS.md, then run the script. -->\n\n"
CURSOR_HEADER = (
    "---\n"
    "description: CodeCoach Socratic coding tutor rules. Hard constraints against handing over full solutions.\n"
    "alwaysApply: true\n"
    "---\n"
)


def render_all():
    body = SOURCE.read_text(encoding="utf-8")
    return {
        ".cursor/rules/codecoach.mdc": CURSOR_HEADER + BANNER + body,
        ".github/copilot-instructions.md": BANNER + body,
        "GEMINI.md": BANNER + body,
    }


def main():
    check = "--check" in sys.argv
    stale = []
    for rel, content in render_all().items():
        path = ROOT / rel
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        stale.append(rel)
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    if check:
        if stale:
            print("Out of sync with AGENTS.md:", ", ".join(stale))
            print("Run: python scripts/sync_rules.py")
            sys.exit(1)
        print("IDE rule files are in sync with AGENTS.md")
    else:
        print("Updated:", ", ".join(stale) if stale else "nothing (already in sync)")


if __name__ == "__main__":
    main()
