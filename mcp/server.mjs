import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const SKILLS_DIR = path.join(ROOT, "skills");
const PROFILE_TEMPLATE = path.join(ROOT, "profile", "learner-profile.template.md");
const DEFAULT_PROFILE = path.join(ROOT, ".codecoach", "learner-profile.md");
const SKILL_NAME_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const SKILL_ALIASES = { "codecoach-contract": "codecoach-blueprint" };

const session = {
  level: "strict",
  attempts: 0,
};

function textResult(text, isError = false) {
  return { content: [{ type: "text", text }], ...(isError ? { isError: true } : {}) };
}

function parseDescription(markdown) {
  const match = markdown.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return "";
  const descLine = match[1].split(/\r?\n/).find((l) => l.startsWith("description:"));
  if (!descLine) return "";
  return descLine.slice("description:".length).trim().replace(/^["']|["']$/g, "");
}

function answerUnlocked() {
  if (session.level === "open" || session.level === "off") return true;
  if (session.level === "build" || session.level === "guided") return session.attempts >= 1;
  return session.attempts >= 2;
}

const server = new McpServer({
  name: "codecoach",
  version: "0.2.0",
});

server.tool(
  "get_rules",
  "Return the CodeCoach Custom v2 core rules, Ponytail scope lock, and H1-H6 / H4+ citation gates from AGENTS.md.",
  {},
  async () => {
    const content = await fs.readFile(path.join(ROOT, "AGENTS.md"), "utf8");
    return textResult(content);
  }
);

server.tool(
  "list_skills",
  "List all available CodeCoach v2 tutoring skills (blueprint, anatomy, debug, domains, predict, review, recap, help) and their descriptions.",
  {},
  async () => {
    const entries = await fs.readdir(SKILLS_DIR, { withFileTypes: true });
    const lines = [];
    for (const entry of entries.sort((a, b) => a.name.localeCompare(b.name))) {
      if (!entry.isDirectory()) continue;
      const skillPath = path.join(SKILLS_DIR, entry.name, "SKILL.md");
      try {
        const md = await fs.readFile(skillPath, "utf8");
        const desc = parseDescription(md);
        lines.push(`- **${entry.name}**: ${desc || "(no description)"}`);
      } catch {
        // skip folders without SKILL.md
      }
    }
    return textResult(lines.join("\n") || "No skills found.");
  }
);

server.tool(
  "get_skill",
  "Read the full SKILL.md instructions for a CodeCoach v2 skill (e.g. codecoach, codecoach-blueprint, codecoach-anatomy, codecoach-debug, codecoach-domains).",
  { name: z.string().describe("Skill folder name, e.g. 'codecoach-blueprint'") },
  async ({ name }) => {
    if (!SKILL_NAME_RE.test(name)) {
      return textResult(`Invalid skill name: '${name}'. Use lowercase letters, digits, and hyphens only.`, true);
    }
    const resolved = SKILL_ALIASES[name] ?? name;
    const skillPath = path.join(SKILLS_DIR, resolved, "SKILL.md");
    try {
      const md = await fs.readFile(skillPath, "utf8");
      return textResult(md);
    } catch {
      return textResult(`Skill '${name}' not found. Call list_skills to see valid names.`, true);
    }
  }
);

server.tool(
  "session_state",
  "Get or update the current CodeCoach v2 session state (mode: strict | build | guided | open | off, real attempt counter, and Tier-4 unlock status).",
  {
    action: z.enum(["get", "set_level", "record_attempt", "reset"]),
    level: z
      .enum(["strict", "build", "guided", "open", "off"])
      .optional()
      .describe("Required when action is 'set_level' ('build' and 'guided' both select Guided Build Mode)"),
  },
  async ({ action, level }) => {
    if (action === "set_level") {
      if (!level) return textResult("Missing 'level' for action 'set_level'.", true);
      session.level = level;
    } else if (action === "record_attempt") {
      session.attempts += 1;
    } else if (action === "reset") {
      session.level = "strict";
      session.attempts = 0;
    }
    return textResult(
      JSON.stringify({
        level: session.level,
        attempts: session.attempts,
        answerUnlocked: answerUnlocked(),
      })
    );
  }
);

server.tool(
  "learner_profile",
  "Read or initialize the cross-session learner profile (.codecoach/learner-profile.md) tracking Habits, Mastered Topics, Recurring Blind Spots, and Progress Log.",
  {
    action: z.enum(["get", "init"]),
    workspaceDir: z.string().optional().describe("Optional workspace path; defaults to CodeCoach root"),
  },
  async ({ action, workspaceDir }) => {
    const baseDir = workspaceDir ? path.resolve(workspaceDir) : ROOT;
    try {
      const stat = await fs.stat(baseDir);
      if (!stat.isDirectory()) {
        return textResult(`Invalid workspaceDir '${baseDir}': not a directory.`, true);
      }
    } catch {
      return textResult(`Workspace directory not found: '${baseDir}'.`, true);
    }
    const profilePath = path.join(baseDir, ".codecoach", "learner-profile.md");
    if (action === "init") {
      try {
        await fs.access(profilePath);
        const existing = await fs.readFile(profilePath, "utf8");
        return textResult(existing);
      } catch {
        const tpl = await fs.readFile(PROFILE_TEMPLATE, "utf8");
        const today = new Date().toISOString().slice(0, 10);
        const initialized = tpl.replaceAll("YYYY-MM-DD", today);
        await fs.mkdir(path.dirname(profilePath), { recursive: true });
        await fs.writeFile(profilePath, initialized, "utf8");
        return textResult(initialized);
      }
    }
    try {
      const content = await fs.readFile(profilePath, "utf8");
      return textResult(content);
    } catch {
      const fallback = await fs.readFile(
        baseDir === ROOT ? PROFILE_TEMPLATE : DEFAULT_PROFILE,
        "utf8"
      ).catch(() => fs.readFile(PROFILE_TEMPLATE, "utf8"));
      return textResult(fallback);
    }
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
