# 本仓库协作说明

## 本地 Skill 开发启动步骤

每次在本仓库启动一个新的 Codex 对话时，首先执行：

```bash
bash scripts/link-skills.sh
```

该脚本会扫描 `skills/*/SKILL.md`，并将每个一级 Skill 目录软链接到 `~/.codex/skills/`（或者由 `CODEX_HOME` 指定的目录）。因此新增 Skill 后，在下一次本仓库对话启动时会自动完成本地注册链接。

脚本不会删除全局目录中的 Skill；若同名目标是实体文件或目录，必须报告冲突并停止，不能覆盖。
