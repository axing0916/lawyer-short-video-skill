# 律师短视频文案创作系统 Skill v1.0

## 📺 项目简介

这是一个**完整的律师短视频文案创作系统**，帮助律师（以及需要创建视频内容的专业人士）通过**结构化的流程**快速创建高质量的短视频文案。

### 核心特性

✅ **模块化架构** - 5个独立的核心模块，易于维护和扩展  
✅ **内容拆解引擎** - 自动将案例/文章拆解为多个文案角度  
✅ **文案生成系统** - 基于提示词的批量文案生成  
✅ **Obsidian集成** - 与个人知识库无缝集成  
✅ **Codex集成** - 快速启动和批量生成  
✅ **WorkBuddy自动化** - 周度复盘和数据分析自动化  
✅ **完整的工作流** - 从灵感到发布的完整流程  

---

## 🎯 系统设计

### 整体架构

```
输入层 (Module 1)
    ↓
拆解层 (Module 2)
    ↓
生成层 (Module 3)
    ↓
数据层 (Module 4)
    ↓
集成层 (Module 5)
    ↓
存储 (Obsidian/Codex/GitHub)
```

### 5个核心���块

| 模块 | 功能 | 负责 |
|------|------|------|
| Module 1 | 输入管理 | 接收和验证用户输入 |
| Module 2 | 内容拆解 | 将案例/文章拆解为多个角度 |
| Module 3 | 文案生成 | 基于拆解结果生成完整文案 |
| Module 4 | 数据管理 | 元数据和Obsidian集成 |
| Module 5 | 集成管理 | 与外部工具的集成 |

---

## 🚀 快速开始

### 前置要求

- GitHub账户（用于存储仓库）
- Obsidian（用于内容管理）
- Codex账户（用于文案生成）
- ChatGPT/Claude账户（用于LLM调用）

### 5分钟快速开始

#### 第一步：克隆仓库

```bash
git clone https://github.com/axing0916/lawyer-short-video-skill.git
cd lawyer-short-video-skill
```

#### 第二步：查看快速开始指南

```
docs/01-quick-start.md
```

#### 第三步：准备Obsidian

按照以下结构创建您的Obsidian仓库：

```
lawyer-content-vault/
├─ 00-Inbox/          # 日常积累区
├─ 01-Cases/          # 案例库（已整理）
├─ 02-Articles/       # 文章库
├─ 03-Drafts/         # 草稿区
├─ 04-Published/      # 发布区
├─ 05-Analytics/      # 数据分析区
└─ 06-Templates/      # 模板库
```

详见：`docs/integration/obsidian-guide.md`

#### 第四步：在Codex中配置Skill

1. 打开 [Codex](https://codex.openai.com)
2. 创建新项目：`lawyer-short-video-skill`
3. 导入提示词：`modules/03-generation/prompts/00-main-prompt.md`
4. 配置参数（详见集成指南）

详见：`docs/integration/codex-guide.md`

#### 第五步：生成第一条文案

在Codex中：
1. 选择文案类型：故事驱动型
2. 选择法律领域：民间借贷
3. 选择时长：60秒
4. 点击生成

✅ 完成！您的第一条文案已生成

---

## 📚 文档导航

### 用户文档

| 文档 | 内容 | 适合人群 |
|------|------|--------|
| [快速开始](docs/01-quick-start.md) | 5分钟快速上手 | 新用户 |
| [使用指南](docs/02-user-guide.md) | 详细的使用说明 | 日常用户 |
| [高级用法](docs/03-advanced-usage.md) | 进阶功能和优化 | 高级用户 |
| [故障排查](docs/04-troubleshooting.md) | 常见问题解决 | 遇到问题 |
| [常见问题](docs/05-faq.md) | Q&A | 快速查询 |

### 集成指南

| 工具 | 指南 | 用途 |
|------|------|------|
| Obsidian | [集成指南](docs/integration/obsidian-guide.md) | 内容管理和存储 |
| Codex | [集成指南](docs/integration/codex-guide.md) | 快速文案生成 |
| WorkBuddy | [集成指南](docs/integration/workbuddy-guide.md) | 自动化复盘 |
| 拆解流程 | [拆解指南](docs/integration/decomposition-guide.md) | 案例/文章拆解 |

### 架构文档

| 文档 | 内容 |
|------|------|
| [架构设计](ARCHITECTURE.md) | 系统架构和设计原则 |
| [版本说明](VERSION.md) | 版本历史和更新说明 |
| [更新日志](CHANGELOG.md) | 每个版本的改动 |

---

## 📊 核心功能

### 1. 文案生成

支持4种文案类型 × 4个法律领域 × 3种时长

---

## 🚀 立即开始

[快速开始](docs/01-quick-start.md) | [使用指南](docs/02-user-guide.md) | [架构设计](ARCHITECTURE.md)
