# Research Summary: OpenTeams PPTX Skill — Installer & Skill Factory

**Domain:** Agent skill packaging & distribution (pi coding agent + Claude Code)
**Researched:** 2026-02-28
**Overall confidence:** HIGH

## Executive Summary

The project involves packaging an existing pi skill for one-click installation and then building a reusable tool to repeat this process. The domain is well-understood — pi and Claude Code have documented skill/command systems with clear directory conventions.

Pi discovers skills automatically from `~/.pi/agent/skills/<name>/SKILL.md`. Claude Code uses markdown files in `~/.claude/commands/` with frontmatter as slash commands. The two systems need different installer approaches but can share the same skill files.

The main technical challenges are: (1) making the skill self-contained by replacing the symlinked logo assets with bundled PNGs and rewriting paths, (2) handling the format difference between pi SKILL.md and Claude Code command files, and (3) eliminating hardcoded paths like `/home/mia/.venvs/pptx/bin/python` that won't work on other machines.

The skill-packager (Part 2) generalizes this pattern into a reusable skill that can scaffold new skills and generate installers for any skill directory.

## Key Findings

**Stack:** Pure bash for installers, no additional dependencies needed. Python paths must use `python3` not hardcoded venv paths.
**Table Stakes:** Self-contained directory (no symlinks), idempotent install, dependency warnings, success confirmation.
**Watch Out For:** Hardcoded paths surviving into distributed files, symlink behavior differences across systems, Claude Code command format differs from pi SKILL.md format.

## Implications for Roadmap

Based on research, suggested phase structure:

1. **Self-Contained Skill** — Bundle 6 PNGs, rewrite brand.json paths, remove symlink, eliminate hardcoded paths
   - Addresses: asset bundling, path portability
   - Avoids: symlink breakage pitfall, hardcoded path pitfall

2. **Installer Scripts** — Create install_pi_plugin.sh and install_claude_plugin.sh with prereq checks
   - Addresses: one-click install for both platforms
   - Avoids: wrong Claude Code format pitfall

3. **Documentation** — Update README.md, SKILL.md, and CLAUDE.md with install instructions
   - Addresses: user-facing docs
   - Avoids: README out-of-sync pitfall

4. **Skill Packager** — Build reusable `/skill:skill-packager` for scaffolding and packaging any skill
   - Addresses: repeatability goal
   - Avoids: manual process each time

**Phase ordering rationale:**
- Phase 1 must come first (installers need self-contained directory to copy)
- Phase 2 depends on Phase 1 (needs the bundled skill to install)
- Phase 3 can parallel with Phase 2 but benefits from knowing final install commands
- Phase 4 comes last (generalizes the pattern proven in Phases 1-3)

**Research flags for phases:**
- Phase 2: Needs investigation into exact Claude Code command file format
- Phase 4: May need research into asset detection heuristics

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Bash + cp, well-understood |
| Features | HIGH | Requirements are clear from user conversation |
| Architecture | HIGH | Pi and Claude Code patterns observed directly on this machine |
| Pitfalls | HIGH | Common packaging issues, verified against actual skill structure |

## Gaps to Address

- Exact minimum Python version needed by python-pptx 1.0 (likely 3.8+)
- Whether Claude Code needs a settings.json entry in addition to the command file for skills with scripts
- How the skill-packager should detect which files are "assets" vs "code" in arbitrary skill directories
