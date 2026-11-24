#!/usr/bin/env python3
"""Replace the YOUR_NAME / YOUR_GITHUB_USERNAME placeholders in one go.

Usage:
    python scripts/personalize.py --name "Nguyen Van Quang" --github your-username
"""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="Your real name, used in LICENSE and manifests")
    ap.add_argument("--github", required=True, help="Your GitHub username")
    args = ap.parse_args()

    changed = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "scripts" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new = text.replace("YOUR_GITHUB_USERNAME", args.github).replace("YOUR_NAME", args.name)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))
    print("Updated:", ", ".join(sorted(changed)) or "nothing (already personalized?)")


if __name__ == "__main__":
    main()
