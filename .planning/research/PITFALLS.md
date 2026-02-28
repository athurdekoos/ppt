# Domain Pitfalls

**Domain:** Agent skill packaging & distribution
**Researched:** 2026-02-28

## Critical Pitfalls

### Pitfall 1: Hardcoded Paths Survive into Installers
**What goes wrong:** SKILL.md and scripts contain paths like `/home/mia/.venvs/pptx/bin/python` or `<skill-dir>` placeholders that don't resolve on other machines.
**Why it happens:** Developed on one machine, paths work locally, nobody tests on a clean install.
**Consequences:** Skill installs but fails silently — scripts can't find Python, logos, or brand.json.
**Prevention:** Use `python3` (system PATH), `os.path.dirname(__file__)` in Python, and `$(dirname "$0")` in bash. Search all files for absolute paths before packaging.
**Detection:** Grep for `/home/` in all skill files.

### Pitfall 2: Symlinks Break on Copy
**What goes wrong:** `cp -r` copies the symlink target on some systems, follows it on others, or fails if the target doesn't exist.
**Consequences:** `assets/logos` is empty or missing after install.
**Prevention:** Replace symlink with actual files before distribution. Use `cp -rL` (follow symlinks) in installer as defense-in-depth.
**Detection:** `find . -type l` to check for symlinks in skill directory.

### Pitfall 3: Claude Code Command File Gets the Skill Wrong
**What goes wrong:** The `.claude/commands/openteams-pptx.md` file has different content format than SKILL.md. It's not a direct copy — Claude Code uses frontmatter differently.
**Why it happens:** Assuming pi and Claude Code use the same format.
**Consequences:** Command doesn't trigger, or triggers without the right instructions.
**Prevention:** Study the existing Claude Code commands format (e.g., `~/.claude/commands/gsd/*.md`). Generate a proper command file, not just copy SKILL.md.
**Detection:** Test the command in Claude Code after install.

## Moderate Pitfalls

### Pitfall 4: Python Dependency Hell
**What goes wrong:** User has Python 3.8 (too old for python-pptx 1.0), or pip installs to wrong location, or venv isn't activated.
**Prevention:** Check Python version in installer, print clear error with minimum version. Don't try to manage venvs — just document requirements.

### Pitfall 5: Logo File Names Don't Match brand.json
**What goes wrong:** Rename PNGs to friendly names but forget to update brand.json paths, or vice versa.
**Prevention:** Single source of truth — update brand.json paths first, then copy files to match. Test with `generate_deck.py --demo` after changes.

### Pitfall 6: README Gets Out of Sync
**What goes wrong:** Install process changes but README still shows old steps.
**Prevention:** README install section should be generated/templated, or at minimum tested as part of the packaging workflow.

## Minor Pitfalls

### Pitfall 7: Installer Doesn't Handle Existing Install
**What goes wrong:** User re-runs installer, gets duplicated files or partial overwrites.
**Prevention:** Detect existing install, ask or auto-overwrite with backup.

### Pitfall 8: Missing `.claude/commands/` Directory
**What goes wrong:** Claude Code installer assumes `~/.claude/commands/` exists.
**Prevention:** `mkdir -p` before copying.

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Bundle assets | Symlink breaks (#2) | Replace with actual PNGs |
| Update paths | Hardcoded paths survive (#1) | Grep audit before packaging |
| Claude Code installer | Wrong format (#3) | Study existing command files |
| Skill packager | Path detection is fragile | Use conservative regex + manual override |
