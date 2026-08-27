# Codex 集成

## 正确定位

Codex 可以把本地文件夹作为项目上下文，并通过 `SKILL.md` 识别可复用工作流。一个 Skill 通常由必需的 `SKILL.md` 以及可选的 `scripts/`、`references/`、`assets/` 和界面元数据组成。本仓库依照这种渐进加载结构组织。

官方说明：

- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Projects and chats](https://learn.chatgpt.com/docs/projects)

## 本地使用

1. 将仓库克隆或下载到有权限的目录；
2. 在 Codex 中打开仓库根目录；
3. 确认根目录存在 `SKILL.md`；
4. 用自然语言说明任务，并要求先执行来源和脱敏检查；
5. 对文件改动先查看差异，再由你决定是否提交。

示例请求：

> 使用本项目的律师短视频工作流处理 `inputs/brief.md`。先检查脱敏和来源；通过后生成 60 秒收藏型干货口播。任何缺失事实标【待补充】，法律结论标出核验来源需求。结果写入 `outputs/drafts/`，不要发布。

## GitHub 工作流

Codex 能否读写 GitHub 取决于本机 Git 凭据、GitHub 连接和仓库权限。推荐在独立分支提交并创建 Pull Request，不直接推送主分支。GitHub 集成不能替代分支保护、代码审查和秘密扫描。

## API Key 说明

本地打开项目和调用 Skill 不要求你把 API Key 写进配置。若另行开发调用 OpenAI API 的脚本，应使用环境变量或秘密管理服务，并遵守对应 API 文档；不要提交密钥。

## 能力边界

- 仓库规则不能自动证明法律结论正确；
- 未提供 Obsidian vault 路径和写权限时，不能自动保存到该 vault；
- 不会自动发布到短视频平台；
- 不应把生成的教学情景冒充真实案例。
