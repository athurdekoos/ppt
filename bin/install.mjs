#!/usr/bin/env node

import { execSync } from "child_process";
import { existsSync, mkdirSync, cpSync, renameSync } from "fs";
import { join, dirname } from "path";
import { homedir } from "os";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// ── Argument parsing ──────────────────────────────────────────

const args = process.argv.slice(2);
const wantPi = args.includes("--pi");
const wantClaude = args.includes("--claude");

if (!wantPi && !wantClaude) {
  console.log(`
OpenTeams PPTX Skill Installer

Usage:
  npx https://github.com/athurdekoos/ppt --pi       Install for pi coding agent
  npx https://github.com/athurdekoos/ppt --claude    Install for Claude Code

Options:
  --pi       Install to ~/.pi/agent/skills/openteams-pptx/
  --claude   Install to ~/.agents/skills/openteams-pptx/
`);
  process.exit(1);
}

if (wantPi && wantClaude) {
  console.error("Error: pick one — --pi or --claude, not both.");
  process.exit(1);
}

const home = homedir();
const target = wantPi
  ? join(home, ".pi", "agent", "skills", "openteams-pptx")
  : join(home, ".agents", "skills", "openteams-pptx");

// ── Step 1: Check Python 3 ───────────────────────────────────

process.stdout.write("◆ Checking Python 3...          ");
let pythonVersion;
try {
  pythonVersion = execSync("python3 --version", { encoding: "utf8" }).trim();
  console.log(`✓ ${pythonVersion}`);
} catch {
  console.log("✗ Not found");
  console.error(`
Error: Python 3 is required but not found.

Install it:
  Ubuntu/Debian:  sudo apt install python3
  macOS:          brew install python3
  Windows:        https://www.python.org/downloads/
`);
  process.exit(1);
}

// ── Step 2: Check / install python-pptx ──────────────────────

process.stdout.write("◆ Checking python-pptx...       ");
try {
  execSync('python3 -c "import pptx"', { stdio: "pipe" });
  console.log("✓ python-pptx available");
} catch {
  console.log("✗ Not installed");
  console.log("  Installing python-pptx...");
  try {
    execSync("pip3 install python-pptx", { stdio: "inherit" });
    console.log("  ✓ python-pptx installed");
  } catch {
    console.warn(
      "  ⚠ Could not auto-install python-pptx. Please run: pip3 install python-pptx"
    );
  }
}

// ── Step 3: Backup existing install ──────────────────────────

if (existsSync(target)) {
  const ts = new Date().toISOString().replace(/[:.]/g, "-");
  const backupPath = `${target}.backup.${ts}`;
  process.stdout.write("◆ Backing up existing install... ");
  renameSync(target, backupPath);
  console.log(`✓ Backed up to ${backupPath}`);
} else {
  console.log("◆ No existing install to back up.");
}

// ── Step 4: Copy skill files ─────────────────────────────────

process.stdout.write("◆ Installing skill files...     ");

const source = join(__dirname, "..", "openteams-pptx");

mkdirSync(target, { recursive: true });

const itemsToCopy = ["SKILL.md", "README.md", "scripts", "references", "assets", "docs"];

for (const item of itemsToCopy) {
  const src = join(source, item);
  const dest = join(target, item);
  if (!existsSync(src)) continue;
  cpSync(src, dest, {
    recursive: true,
    filter: (s) => !s.includes("__pycache__"),
  });
}

console.log(`✓ Copied to ${target}`);

// ── Step 5: Success ──────────────────────────────────────────

const agent = wantPi ? "pi" : "Claude Code";
console.log(`
✓ Installed openteams-pptx to ${target}

  For pi:          /skill:openteams-pptx in any session
  For Claude Code: Add to your project's CLAUDE.md available_skills

  To uninstall:    rm -rf ${target}
`);
