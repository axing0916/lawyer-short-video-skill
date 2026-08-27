# Obsidian 集成

## v1.0 支持范围

Obsidian vault 本质上是一个 Markdown 文件夹。本项目提供目录、模板、属性字段和文件命名规则。默认不包含云同步、双向数据库同步或后台监听服务。

## 推荐目录

```text
Lawyer-Video/
├── 00-Inbox/
├── 10-Sources/
├── 20-Ideas/
├── 30-Drafts/
├── 40-Review/
├── 50-Published/
├── 60-Metrics/
└── 90-Templates/
```

## 首次配置

1. 在 Obsidian 新建或选择 vault；
2. 手工创建上述目录；
3. 将 `templates/obsidian/` 中的文件复制到 `90-Templates/`；
4. 在 Obsidian 设置中指定模板目录；
5. 用虚构教学情景测试，不要先放入客户材料。

## 文件命名

`YYYY-MM-DD-内容ID-短标题.md`，例如 `2026-08-27-LSV-0001-借条证据清单.md`。

## Codex 写回

只有在你明确提供 vault 内目标路径并授权写入时，Codex 才能直接创建文件。先写入 `30-Drafts/`，通过人工终审后再移动到 `50-Published/`。不要让自动化覆盖已有笔记。

## 同步选择

Obsidian Sync、Git 或第三方云盘是独立方案，权限、冲突和隐私风险不同。本项目不默认选择，也不声称已经启用。包含客户信息的 vault 不应未经评估同步到外部服务。
