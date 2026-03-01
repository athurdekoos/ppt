# Personal Showcase Generator

Generate a polished, self-contained HTML portfolio page with OpenTeams-inspired branding, animated project cards, and social links.

## Features

- **Animated hero section** with gradient avatar ring, name, handle, and tagline
- **Social link pills** for GitHub, LinkedIn, and Discord with branded hover effects
- **Project cards** with tags, highlights, and repo links
- **Three themes:** dark (Night Navy), light (clean white), glass (frosted blur)
- **Floating ambient orbs** in the OpenTeams accent palette
- **Fully responsive** — works on desktop and mobile
- **No dependencies at runtime** — just open the `.html` file in a browser

## Prerequisites

- Python 3.8+
- No pip dependencies required (uses only the standard library)

## Usage

```bash
# Basic — dark theme (default)
python3 personal-showcase/scripts/generate_showcase.py \
  --profile profile.json --out showcase.html

# Choose a theme
python3 personal-showcase/scripts/generate_showcase.py \
  --profile profile.json --out showcase.html --theme glass
```

### Themes

| Theme | Description |
|-------|-------------|
| `dark` | Night Navy background with bright accent text (default) |
| `light` | Clean white background with navy text |
| `glass` | Frosted glassmorphism with blurred background orbs |

### Profile JSON Format

```json
{
  "name": "Your Name",
  "handle": "@yourhandle",
  "tagline": "Your tagline here",
  "avatar_url": "https://example.com/avatar.jpg",
  "socials": {
    "github": "https://github.com/yourname",
    "linkedin": "https://linkedin.com/in/yourname",
    "discord": "https://discord.gg/invite"
  },
  "projects": [
    {
      "name": "Project Name",
      "description": "What it does",
      "tags": ["python", "automation"],
      "url": "https://github.com/yourname/project"
    }
  ]
}
```

## Agent Skill Usage

This is also available as a pi / Claude Code agent skill. See [`SKILL.md`](SKILL.md) for trigger phrases and skill integration details.

---

<p align="center">
  <sub>Built by <a href="https://openteams.com">OpenTeams</a></sub>
</p>
