#!/usr/bin/env python3
"""Personalize CodeCoach manifests and manage cross-session learner profiles (.codecoach/learner-profile.md).

Usage:
    python scripts/personalize.py --name "QuangHack-bit" --github QuangHack-bit
    python scripts/personalize.py --init-profile
    python scripts/personalize.py --init-profile --workspace D:/MyProject
    python scripts/personalize.py --add-mastered "Java ArrayList vs LinkedList complexity"
    python scripts/personalize.py --add-blind-spot "Forgetting volatile on shared ISR flags"
"""
import argparse
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "profile" / "learner-profile.template.md"


def replace_placeholders(name: str, github: str) -> list[str]:
    changed = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "scripts" in path.parts or "node_modules" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new = text.replace("YOUR_GITHUB_USERNAME", github).replace("YOUR_NAME", name)
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n")
            changed.append(str(path.relative_to(ROOT)))
    return sorted(changed)


def init_profile(workspace: Path, force: bool = False) -> Path:
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"Missing profile template: {TEMPLATE}")
    dest = workspace / ".codecoach" / "learner-profile.md"
    if dest.exists() and not force:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    content = TEMPLATE.read_text(encoding="utf-8").replace("YYYY-MM-DD", date.today().isoformat())
    dest.write_text(content, encoding="utf-8", newline="\n")
    return dest


def append_bullet_under_heading(profile_path: Path, heading_prefix: str, item: str) -> None:
    lines = profile_path.read_text(encoding="utf-8").splitlines()
    bullet = f"- {item.strip()}"
    if bullet in lines:
        return
    insert_idx = None
    for idx, line in enumerate(lines):
        if line.startswith(heading_prefix):
            insert_idx = idx + 1
            while insert_idx < len(lines) and (
                lines[insert_idx].startswith("<!--") or lines[insert_idx].startswith("- ")
            ):
                insert_idx += 1
            break
    if insert_idx is None:
        raise ValueError(f"Heading '{heading_prefix}' not found in {profile_path}")
    lines.insert(insert_idx, bullet)
    profile_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser(description="Personalize CodeCoach and manage .codecoach/learner-profile.md")
    ap.add_argument("--name", help="Author/learner name used in LICENSE, manifests, and profile")
    ap.add_argument("--github", help="GitHub username")
    ap.add_argument("--init-profile", action="store_true", help="Initialize .codecoach/learner-profile.md")
    ap.add_argument("--force-profile", action="store_true", help="Overwrite existing .codecoach/learner-profile.md")
    ap.add_argument("--workspace", default=str(ROOT), help="Target workspace directory for .codecoach/learner-profile.md")
    ap.add_argument("--add-mastered", help="Append a mastered topic to .codecoach/learner-profile.md")
    ap.add_argument("--add-blind-spot", help="Append a recurring blind spot to .codecoach/learner-profile.md")
    args = ap.parse_args()

    if not any([args.name, args.github, args.init_profile, args.add_mastered, args.add_blind_spot]):
        ap.error("Provide --name/--github, --init-profile, --add-mastered, or --add-blind-spot.")

    if bool(args.name) ^ bool(args.github):
        ap.error("--name and --github must be provided together.")

    if args.name and args.github:
        changed = replace_placeholders(args.name, args.github)
        print("Personalized files:", ", ".join(changed) or "nothing (already personalized)")

    ws = Path(args.workspace).resolve()
    profile_path = ws / ".codecoach" / "learner-profile.md"

    if args.init_profile or ((args.add_mastered or args.add_blind_spot) and not profile_path.exists()):
        existed = profile_path.exists()
        profile_path = init_profile(ws, force=args.force_profile)
        status = "Overwrote" if (existed and args.force_profile) else ("Kept existing" if existed else "Initialized")
        print(f"{status} learner profile: {profile_path}")

    if args.add_mastered:
        append_bullet_under_heading(profile_path, "## 2. Mastered Topics", args.add_mastered)
        print(f"Added mastered topic to {profile_path}")

    if args.add_blind_spot:
        append_bullet_under_heading(profile_path, "## 3. Recurring Blind Spots", args.add_blind_spot)
        print(f"Added blind spot to {profile_path}")


if __name__ == "__main__":
    main()
