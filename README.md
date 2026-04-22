# skill-collection

A curated collection of **skill files** for use with AI coding agents such as [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and [Jupyter AI QuickAgent](https://github.com/srdas/jupyter-ai-quickagent).

## What are skills?

Skills are markdown files that give an AI agent specialized instructions, domain knowledge, or workflows. Instead of repeating detailed guidance every time you start a conversation, you point the agent at a skill file and it adopts that expertise automatically.

A single skill file can encode anything from a house style for writing code, to a step-by-step troubleshooting runbook, to the criteria for evaluating work in a specific domain. The agent consults the skill during its operation, so the knowledge persists across sessions without being baked into the model itself.

Skills work across multiple agent frameworks:

- **Claude Code** loads skills from a `.claude/skills/` directory (or via `--add-dir`) and can trigger them automatically or through slash commands.
- **Jupyter AI QuickAgent** accepts a `skills_dir` parameter during agent creation, pointing to a folder of `.md` files that the agent references when responding.

In both cases the mechanism is the same: the agent reads the markdown at runtime and follows the instructions it finds there.

## Repository structure

Each subfolder in this repository represents a single skill topic. The recommended layout for a skill subfolder is:

```
skill-topic/
├── README.md              # Human-readable overview: what the skill does,
│                          #   where it came from, and how to use it
├── skills/
│   └── SKILL.md           # The skill file itself — this is what the agent reads
│                          #   (additional SKILL files may be added here if the
│                          #   topic requires more than one)
└── (supporting files)     # Any data, scripts, or reference material the skill
                           #   depends on (e.g., a helper script, a PDF, a dataset)
```

### Key conventions

| Item | Purpose |
|------|---------|
| `skills/SKILL.md` | The primary skill file. It should be self-contained: an agent that reads only this file should have everything it needs to act. |
| `README.md` | Documentation for humans — origin of the material, setup steps, usage examples. |
| Supporting files | Anything the skill references at runtime (scripts, sample data, exported documents). Keep these in the subfolder root or in clearly named subdirectories. |

### Writing a good SKILL.md

A well-structured skill file typically includes:

1. **Purpose** — a concise statement of what the skill does and when it should activate.
2. **Core instructions** — the detailed guidance, principles, or workflow steps the agent should follow.
3. **Constraints** — boundaries on behavior (e.g., never fabricate data, keep output under N sentences).
4. **Examples** — concrete input/output pairs so the agent can calibrate tone, format, and depth.

Optional YAML front matter (`name`, `description`) at the top of the file helps agent frameworks index and select skills programmatically.

## Usage

**With Claude Code** — copy or symlink a skill subfolder into your project's `.claude/skills/` directory, or point to it with `--add-dir`:

```bash
claude --add-dir /path/to/skill-collection/my-skill
```

**With Jupyter AI QuickAgent** — supply the subfolder path as the `skills_dir` when creating an agent. The agent will read every `.md` file in that directory.

## Contributing

To add a new skill, create a subfolder following the structure above. The most important file is `skills/SKILL.md` — start there, then add a `README.md` explaining the skill's origin and intended use.
