#!/usr/bin/env python3
"""Validate the CodeCoach plugin. Standard library only.

Usage:
    python scripts/validate.py            # errors fail, placeholders only warn
    python scripts/validate.py --release  # placeholders also fail (use before publishing)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
PLACEHOLDERS = ("YOUR_NAME", "YOUR_GITHUB_USERNAME")
# Skills that must carry a "Hard constraints" section and at least one example refusal.
HARD_SKILLS = ("codecoach", "codecoach-contract", "codecoach-debug", "codecoach-review", "codecoach-predict")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load_json(rel):
    path = ROOT / rel
    if not path.exists():
        err(f"{rel}: missing")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        err(f"{rel}: invalid JSON ({e})")
        return None


def parse_frontmatter(text):
    """Very small YAML subset: `key: value` lines between the first two `---`."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    data = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            value = m.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            data[m.group(1)] = value
    return None  # closing --- never found


def check_manifests():
    plugin = load_json(".claude-plugin/plugin.json")
    market = load_json(".claude-plugin/marketplace.json")
    if plugin:
        for key in ("name", "description", "version", "license"):
            if not plugin.get(key):
                err(f"plugin.json: missing '{key}'")
        if plugin.get("name") and not NAME_RE.match(plugin["name"]):
            err("plugin.json: 'name' must be lowercase letters, digits and hyphens")
        if plugin.get("version") and not re.match(r"^\d+\.\d+\.\d+", plugin["version"]):
            err("plugin.json: 'version' must look like 1.2.3")
    if market:
        for key in ("name", "owner", "plugins"):
            if not market.get(key):
                err(f"marketplace.json: missing '{key}'")
        plugins = market.get("plugins") or []
        if not plugins:
            err("marketplace.json: 'plugins' is empty")
        for entry in plugins:
            if not entry.get("name") or not entry.get("source"):
                err("marketplace.json: each plugin needs 'name' and 'source'")
            elif plugin and entry["name"] == plugin.get("name"):
                if entry.get("version") and entry["version"] != plugin.get("version"):
                    err("marketplace.json and plugin.json versions differ")
        if plugin and plugin.get("name") not in [e.get("name") for e in plugins]:
            err("marketplace.json does not list the plugin from plugin.json")
    return plugin


def check_skills():
    skills_dir = ROOT / "skills"
    folders = sorted(p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.exists() else []
    if not folders:
        err("skills/: no skill folders found")
    names = []
    for folder in folders:
        skill = folder / "SKILL.md"
        rel = f"skills/{folder.name}/SKILL.md"
        if not skill.exists():
            err(f"{rel}: missing")
            continue
        fm = parse_frontmatter(skill.read_text(encoding="utf-8"))
        if fm is None:
            err(f"{rel}: frontmatter missing or not closed with ---")
            continue
        names.append(folder.name)
        if fm.get("name") != folder.name:
            err(f"{rel}: frontmatter name '{fm.get('name')}' != folder '{folder.name}'")
        if not NAME_RE.match(folder.name) or len(folder.name) > 64:
            err(f"{rel}: folder/name must be lowercase-hyphen, max 64 chars")
        desc = fm.get("description", "")
        if not desc:
            err(f"{rel}: missing description")
        elif len(desc) > 1024:
            err(f"{rel}: description is {len(desc)} chars (max 1024)")
        elif "use" not in desc.lower():
            warn(f"{rel}: description should say when to use the skill")
        if not fm.get("license"):
            warn(f"{rel}: no license in frontmatter")
    return names


def check_hard_constraints():
    for name in HARD_SKILLS:
        rel = f"skills/{name}/SKILL.md"
        path = ROOT / rel
        if not path.exists():
            continue  # already reported by check_skills
        text = path.read_text(encoding="utf-8")
        if "## Hard constraints" not in text:
            err(f"{rel}: missing '## Hard constraints' section")
        if "Example refusal" not in text:
            err(f"{rel}: missing an 'Example refusal' block")
    if not (ROOT / "skills/codecoach/references/refusals.md").exists():
        err("skills/codecoach/references/refusals.md: missing (core skill points to it)")
    agents = ROOT / "AGENTS.md"
    if agents.exists():
        text = agents.read_text(encoding="utf-8")
        if "## Hard constraints" not in text or "Example refusal" not in text:
            err("AGENTS.md: missing hard constraints or example refusal")


def check_ide_files():
    """Generated IDE rule files must match AGENTS.md (run scripts/sync_rules.py to fix)."""
    from sync_rules import render_all
    for rel, content in render_all().items():
        path = ROOT / rel
        if not path.exists():
            err(f"{rel}: missing (run python scripts/sync_rules.py)")
        elif path.read_text(encoding="utf-8") != content:
            err(f"{rel}: out of sync with AGENTS.md (run python scripts/sync_rules.py)")


def check_docs(names):
    for rel in ("README.md", "README.vi.md"):
        path = ROOT / rel
        if not path.exists():
            err(f"{rel}: missing")
            continue
        text = path.read_text(encoding="utf-8")
        for n in names:
            if f"`{n}`" not in text:
                err(f"{rel}: skill '{n}' is not listed")
    for rel in ("LICENSE", "AGENTS.md", "CHANGELOG.md", "CONTRIBUTING.md"):
        if not (ROOT / rel).exists():
            err(f"{rel}: missing")


def check_placeholders(release):
    found = {}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "scripts" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for token in PLACEHOLDERS:
            if token in text:
                found.setdefault(token, []).append(str(path.relative_to(ROOT)))
    for token, files in found.items():
        msg = f"placeholder {token} still present in: {', '.join(sorted(files))}"
        (err if release else warn)(msg)


def main():
    release = "--release" in sys.argv
    check_manifests()
    names = check_skills()
    check_docs(names)
    check_hard_constraints()
    check_ide_files()
    check_placeholders(release)
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)
    print(f"OK: {len(names)} skills validated, {len(warnings)} warning(s)")


if __name__ == "__main__":
    main()
