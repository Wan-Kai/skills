# 调研来源路由

只选择与用户目标匹配的来源，并回到项目官方站点或官方仓库完成核验。

| 目标 | 首选来源 | 检索要点 |
|---|---|---|
| 最新产品和产品体验 | Product Hunt 的 Open Source、AI Agents、LLMs、开发者工具等主题 | 发布时间、评论、官网和关联的 GitHub 仓库 |
| GitHub 社区热度 | GitHub Trending 与 GitHub 搜索 | 按语言/周期；核验 Release、贡献者、Issue 和文档 |
| 商业产品的开源替代 | AlternativeTo、OpenAlternative | 名称、功能类别、平台、许可证、自托管需求 |
| 自托管服务 | awesome-selfhosted 和垂直 Awesome List | 部署要求、数据存储、认证、备份和升级路径 |
| Agent 能力 | Awesome Agent Skills、skills.sh、官方组织的 Skill/MCP 仓库 | 运行时兼容性、权限、维护者、安装脚本、外部 API 依赖 |

## 建议检索组合

1. 先从产品问题或竞品名称检索目录，建立候选池。
2. 补查 Product Hunt 和 GitHub Trending，捕捉近期值得关注的新品。
3. 回到每个候选的官网和 GitHub 仓库做最终核验。
4. 只有在用户需要自动化、Agent 集成或开发提效时，再为产品寻找 Skill/MCP；两者分别评价。

## 最低核验项

- **真实性**：是否有官方仓库或官方开发文档；避免仅依据聚合站信息。
- **授权**：明确 SPDX 许可证或官方授权说明；警惕“source-available”被误判为开源。
- **维护度**：关注近期 Release/提交、Issue 响应、依赖状态和升级说明，而非只看 Star。
- **可用性**：确认部署文档、最低运行环境、认证、备份恢复与迁移接口。
- **成本**：区分软件许可证免费与托管、模型、第三方 API、存储或人力成本。
- **安全**：检查 CVE/安全公告、权限模型、默认网络暴露面、Skill/MCP 是否请求敏感凭据。
