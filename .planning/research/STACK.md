# Technology Stack

**Project:** OpenTeams PPTX Skill — Installer & Skill Factory
**Researched:** 2026-02-28

## Recommended Stack

### Shell Scripting
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Bash | 4.0+ | Installer scripts | Universal on Linux/macOS, no dependencies |
| cp -r | built-in | File copying | Simple, reliable, no extra tools needed |

### Skill Targets
| Platform | Skill Location | Discovery Mechanism |
|----------|---------------|---------------------|
| Pi coding agent | `~/.pi/agent/skills/<name>/` or `~/.agents/skills/<name>/` | Scans for `SKILL.md` in subdirectories |
| Claude Code | `~/.claude/commands/<name>.md` + shared skill files | Markdown files with frontmatter become `/` commands |

### Python (existing, unchanged)
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| python-pptx | >=1.0.0 | PPTX generation | Already in use, proven |
| Pillow | >=10.0.0 | Image handling for logos | Already in use |

## Key Architecture Insight

**Pi** and **Claude Code** have different skill mechanisms:

- **Pi:** Directory with `SKILL.md` → auto-discovered as `/skill:<name>`
- **Claude Code:** `.md` file in `~/.claude/commands/` → becomes `/<name>` slash command. The command file can reference external scripts/files.

**Shared location `~/.agents/skills/`** is read by pi natively. Claude Code needs either a settings entry or a command file that points to the skill.

## Installer Strategy

| Installer | Copies skill to | Also does |
|-----------|----------------|-----------|
| `install_pi_plugin.sh` | `~/.pi/agent/skills/openteams-pptx/` | Nothing else needed — pi auto-discovers |
| `install_claude_plugin.sh` | `~/.claude/commands/openteams-pptx.md` + `~/.local/share/openteams-pptx/` | Creates command file pointing to skill scripts |

## Sources

- Pi skills docs: `/home/mia/.npm-global/lib/node_modules/@mariozechner/pi-coding-agent/docs/skills.md`
- Claude Code commands: observed pattern in `~/.claude/commands/gsd/`
- Agent Skills specification: https://agentskills.io/specification
