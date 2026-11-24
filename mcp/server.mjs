import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const SKILLS_DIR = path.join(ROOT, "skills");
const SKILL_NAME_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

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
  if (session.level === "guided") return session.attempts >= 1;
  return session.attempts >= 2;
}

const server = new McpServer({
  name: "codecoach",
  version: "0.1.0",
});

server.tool(
  "get_rules",
  "Return the CodeCoach always-on tutoring rules and hard constraints from AGENTS.md.",
  {},
  async () => {
    const content = await fs.readFile(path.join(ROOT, "AGENTS.md"), "utf8");
    return textResult(content);
  }
);

server.tool(
  "list_skills",
  "List all available CodeCoach tutoring skills and their descriptions.",
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
  "Read the full SKILL.md instructions for a specific CodeCoach skill (e.g. codecoach, codecoach-contract, codecoach-debug).",
  { name: z.string().describe("Skill folder name, e.g. 'codecoach-debug'") },
  async ({ name }) => {
    if (!SKILL_NAME_RE.test(name)) {
      return textResult(`Invalid skill name: '${name}'. Use lowercase letters, digits, and hyphens only.`, true);
    }
    const skillPath = path.join(SKILLS_DIR, name, "SKILL.md");
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
  "Get or update the current CodeCoach tutor session state (level and real attempt count for hint-ladder / answer-unlock tracking).",
  {
    action: z.enum(["get", "set_level", "record_attempt", "reset"]),
    level: z.enum(["strict", "guided", "open", "off"]).optional().describe("Required when action is 'set_level'"),
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

const transport = new StdioServerTransport();
await server.connect(transport);
