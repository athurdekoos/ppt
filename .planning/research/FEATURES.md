# Feature Landscape

**Domain:** Agent skill packaging & distribution
**Researched:** 2026-02-28

## Table Stakes

Features users expect. Missing = installer feels broken.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| One-command install | The entire point — `./install_pi_plugin.sh` and done | Low | cp -r to correct directory |
| Idempotent install | Safe to re-run without breaking things | Low | Overwrite or skip-if-exists |
| Self-contained skill | No symlinks or external dependencies to break | Low | Bundle the 6 PNGs |
| Dependency check | Warn if Python/pip missing | Low | `which python3` check |
| Success confirmation | Tell user what was installed and how to use it | Low | Echo the `/skill:` command |
| Uninstall guidance | How to remove if needed | Low | Just mention `rm -rf` the directory |

## Differentiators

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Reusable skill-packager | Package ANY skill, not just this one | Medium | The Part 2 goal |
| Scaffold new skills | Generate SKILL.md + directory structure from prompts | Medium | Template-based |
| Auto-detect assets | Find referenced files and bundle them | Medium | Parse SKILL.md + scripts for paths |
| Path rewriting | Convert absolute/symlink paths to relative | Medium | sed/python transform |
| README generation | Auto-generate install docs section | Low | Template with skill name |

## Anti-Features

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Auto-update mechanism | Complexity, security concerns | Manual re-run of installer |
| Package registry publishing | Over-engineering for internal tool | Share repo, run installer |
| Python venv management | Too many edge cases across systems | Document prerequisites, let user handle |
| Windows support | Different shell, different paths | Document as Linux/macOS only |

## Feature Dependencies

```
Self-contained skill → Path rewriting (paths must work from install location)
Reusable skill-packager → Auto-detect assets + Path rewriting + README generation
```

## MVP Recommendation

Prioritize:
1. Self-contained PPTX skill (bundle PNGs, fix paths)
2. Two installer scripts (pi + Claude Code)
3. Updated README/docs

Defer: Skill-packager (Part 2 — build after Part 1 validates the pattern)
