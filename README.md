# Skills

Personal collection of reusable agent skills.

## Layout

- `skills/`: skill directories, each with its own `SKILL.md`.
- `docs/`: notes, conventions, and supporting documentation.

## Skill Template

Create a new skill under `skills/<skill-name>/SKILL.md`:

```markdown
---
name: skill-name
description: Use when...
---

# Skill Name

Instructions for when and how to use this skill.
```

Keep each skill focused, practical, and easy to skim.

## 本地调试

执行以下命令，将所有包含 `SKILL.md` 的一级目录软链接到本机 Codex 的 Skill 目录：

```bash
bash scripts/link-skills.sh
```

随后新开一个 Codex 任务，即可用 `$skill-name` 手动测试。修改仓库中的文件会直接反映到软链接目标；新增 Skill 后重新执行该命令即可。
