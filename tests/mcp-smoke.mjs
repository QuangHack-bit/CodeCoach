import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const serverPath = path.resolve(__dirname, "..", "mcp", "server.mjs");

const child = spawn(process.execPath, [serverPath], { stdio: ["pipe", "pipe", "pipe"] });
let buffer = "";
const pending = new Map();

child.stdout.on("data", (chunk) => {
  buffer += chunk.toString("utf8");
  const lines = buffer.split(/\r?\n/);
  buffer = lines.pop() ?? "";
  for (const line of lines) {
    if (!line.trim()) continue;
    const msg = JSON.parse(line);
    if (msg.id !== undefined && pending.has(msg.id)) {
      pending.get(msg.id)(msg);
      pending.delete(msg.id);
    }
  }
});

let nextId = 1;
function request(method, params = {}) {
  const id = nextId++;
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`Timeout on ${method}`)), 5000);
    pending.set(id, (msg) => {
      clearTimeout(timer);
      resolve(msg);
    });
    child.stdin.write(JSON.stringify({ jsonrpc: "2.0", id, method, params }) + "\n");
  });
}

try {
  const init = await request("initialize", {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: { name: "smoke-test", version: "0.2.0" },
  });
  assert.equal(init.result.serverInfo.name, "codecoach");
  assert.equal(init.result.serverInfo.version, "0.2.0");

  child.stdin.write(JSON.stringify({ jsonrpc: "2.0", method: "notifications/initialized" }) + "\n");

  const tools = await request("tools/list");
  const names = tools.result.tools.map((t) => t.name).sort();
  assert.deepEqual(names, ["get_rules", "get_skill", "learner_profile", "list_skills", "session_state"]);

  const badSkill = await request("tools/call", { name: "get_skill", arguments: { name: "../AGENTS" } });
  assert.equal(badSkill.result.isError, true);

  const blueprintSkill = await request("tools/call", { name: "get_skill", arguments: { name: "codecoach-blueprint" } });
  assert.equal(Boolean(blueprintSkill.result.isError), false);
  assert.match(blueprintSkill.result.content[0].text, /CodeCoach Blueprint/);

  // Legacy v1 alias compatibility
  const aliasSkill = await request("tools/call", { name: "get_skill", arguments: { name: "codecoach-contract" } });
  assert.match(aliasSkill.result.content[0].text, /CodeCoach Blueprint/);

  const state0 = await request("tools/call", { name: "session_state", arguments: { action: "get" } });
  assert.deepEqual(JSON.parse(state0.result.content[0].text), {
    level: "strict",
    attempts: 0,
    answerUnlocked: false,
  });

  // Guided Build mode ('build') unlocks after 1 real attempt
  await request("tools/call", { name: "session_state", arguments: { action: "set_level", level: "build" } });
  const buildState = await request("tools/call", { name: "session_state", arguments: { action: "record_attempt" } });
  assert.equal(JSON.parse(buildState.result.content[0].text).answerUnlocked, true);

  // Strict mode requires 2 real attempts
  await request("tools/call", { name: "session_state", arguments: { action: "reset" } });
  const strict1 = await request("tools/call", { name: "session_state", arguments: { action: "record_attempt" } });
  assert.equal(JSON.parse(strict1.result.content[0].text).answerUnlocked, false);
  const strict2 = await request("tools/call", { name: "session_state", arguments: { action: "record_attempt" } });
  assert.equal(JSON.parse(strict2.result.content[0].text).answerUnlocked, true);

  const profileRes = await request("tools/call", { name: "learner_profile", arguments: { action: "get" } });
  assert.match(profileRes.result.content[0].text, /CodeCoach Learner Profile/);

  console.log("OK: CodeCoach v2 MCP smoke test passed");
} finally {
  child.kill();
}
