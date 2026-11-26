#!/usr/bin/env python3
"""Validate the CodeCoach Custom v2 plugin, skills, profile template, and multi-IDE rules.

Usage:
    python scripts/validate.py            # errors fail, placeholders only warn
    python scripts/validate.py --release  # placeholders also fail (used in CI)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

PLACEHOLDERS = ("YOUR_NAME", "YOUR_GITHUB_USERNAME")
EXPECTED_SKILLS = (
    "codecoach",
    "codecoach-anatomy",
    "codecoach-blueprint",
    "codecoach-debug",
    "codecoach-domains",
    "codecoach-help",
    "codecoach-predict",
    "codecoach-recap",
    "codecoach-review",
)
HARD_SKILLS = (
    "codecoach",
    "codecoach-anatomy",
    "codecoach-blueprint",
    "codecoach-debug",
    "codecoach-domains",
    "codecoach-predict",
    "codecoach-review",
)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
errors, warnings = [], []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def load_json(rel: str):
    path = ROOT / rel
    if not path.exists():
        err(f"{rel}: missing")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        err(f"{rel}: invalid JSON ({e})")
        return None


def parse_frontmatter(text: str):
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
    return None


def check_manifests():
    plugin = load_json(".claude-plugin/plugin.json")
    market = load_json(".claude-plugin/marketplace.json")
    gemini = load_json("gemini-extension.json")
    mcp_pkg = load_json("mcp/package.json")

    version = None
    if plugin:
        for key in ("name", "description", "version", "license"):
            if not plugin.get(key):
                err(f"plugin.json: missing '{key}'")
        if plugin.get("name") and not NAME_RE.match(plugin["name"]):
            err("plugin.json: 'name' must be lowercase letters, digits and hyphens")
        version = plugin.get("version")
        if version and not re.match(r"^\d+\.\d+\.\d+", version):
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
                if entry.get("version") and entry["version"] != version:
                    err("marketplace.json and plugin.json versions differ")

    if gemini and version and gemini.get("version") != version:
        err("gemini-extension.json and plugin.json versions differ")
    if mcp_pkg and version and mcp_pkg.get("version") != version:
        err("mcp/package.json and plugin.json versions differ")


def check_skills():
    skills_dir = ROOT / "skills"
    if (skills_dir / "codecoach-contract").exists():
        err("skills/codecoach-contract: legacy v1 skill must be replaced by codecoach-blueprint")

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

    for expected in EXPECTED_SKILLS:
        if expected not in names:
            err(f"skills/{expected}: expected v2 skill is missing")
    return names


def check_v2_gates_and_profile():
    for name in HARD_SKILLS:
        rel = f"skills/{name}/SKILL.md"
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if "## Hard constraints" not in text:
            err(f"{rel}: missing '## Hard constraints' section")
        if "Example refusal" not in text:
            err(f"{rel}: missing an 'Example refusal' block")

    if not (ROOT / "skills/codecoach/references/refusals.md").exists():
        err("skills/codecoach/references/refusals.md: missing")

    agents = ROOT / "AGENTS.md"
    if agents.exists():
        text = agents.read_text(encoding="utf-8")
        if "## Hard Constraints" not in text and "## Hard constraints" not in text:
            err("AGENTS.md: missing hard constraints section")
        if "Example refusal" not in text:
            err("AGENTS.md: missing example refusal")
        if "H4+" not in text or "[UNVERIFIED]" not in text:
            err("AGENTS.md: missing H4+ citation / [UNVERIFIED] rule")
        for trigger in ("/focus", "/strict", "/build", "/source"):
            if trigger not in text:
                err(f"AGENTS.md: missing anti-drift trigger '{trigger}'")

    debug_path = ROOT / "skills/codecoach-debug/SKILL.md"
    if debug_path.exists():
        dtext = debug_path.read_text(encoding="utf-8")
        for gate in ("Gate 1", "Gate 2", "Gate 3", "H4+", "[UNVERIFIED]"):
            if gate not in dtext:
                err(f"skills/codecoach-debug/SKILL.md: missing '{gate}'")

    profile_tpl = ROOT / "profile/learner-profile.template.md"
    if not profile_tpl.exists():
        err("profile/learner-profile.template.md: missing")
    else:
        ptext = profile_tpl.read_text(encoding="utf-8")
        for sec in (
            "## 1. Learning Habits",
            "## 2. Mastered Topics",
            "## 3. Recurring Blind Spots",
            "## 4. Session Progress Log",
        ):
            if sec not in ptext:
                err(f"profile/learner-profile.template.md: missing section '{sec}'")


def check_ide_files():
    from sync_rules import LEGACY_FILES, render_all

    for legacy in LEGACY_FILES:
        if (ROOT / legacy).exists():
            err(f"{legacy}: legacy v1 file still present (run python scripts/sync_rules.py)")

    for rel, content in render_all().items():
        path = ROOT / rel
        if not path.exists():
            err(f"{rel}: missing (run python scripts/sync_rules.py)")
        elif path.read_text(encoding="utf-8") != content:
            err(f"{rel}: out of sync with AGENTS.md/skills (run python scripts/sync_rules.py)")

    gemini_path = ROOT / "GEMINI.md"
    agents_path = ROOT / "AGENTS.md"
    if gemini_path.exists() and agents_path.exists():
        if agents_path.read_text(encoding="utf-8") in gemini_path.read_text(encoding="utf-8"):
            err("GEMINI.md duplicates full AGENTS.md body (violates v2 token deduplication rule)")


def check_docs(names):
    for rel in ("README.md", "README.vi.md"):
        path = ROOT / rel
        if not path.exists():
            err(f"{rel}: missing")
            continue
        text = path.read_text(encoding="utf-8")
        for n in names:
            if f"`{n}`" not in text:
                err(f"{rel}: skill '{n}' is not documented")
    for rel in ("LICENSE", "AGENTS.md", "CHANGELOG.md", "CONTRIBUTING.md"):
        if not (ROOT / rel).exists():
            err(f"{rel}: missing")


def check_placeholders(release: bool):
    found = {}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "scripts" in path.parts or "node_modules" in path.parts:
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
    check_v2_gates_and_profile()
    check_ide_files()
    check_placeholders(release)
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)
    print(f"OK: {len(names)} v2 skills & multi-IDE rules validated, {len(warnings)} warning(s)")


if __name__ == "__main__":
    main()
