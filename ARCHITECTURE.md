# 律师短视频文案创作系统 - 架构设计文档

## 📐 架构总览

### 设计原则

1. **模块化** - 功能独立，低耦合
2. **可扩展性** - 易于添加新功能
3. **可维护性** - 代码清晰，易于理解
4. **可测试性** - 每个模块独立测试
5. **版本兼容性** - 向下兼容

### 分层设计

```
┌─────────────────────────────────────┐
│  Layer 1: 输入层 (Input)            │
│  职责：接收和验证用户输入            │
│  模块：Module 1                     │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│  Layer 2: 处理层 (Processing)       │
│  包含：                             │
│  - Module 2 (Content Decomposition) │
│  - Module 3 (Copywriting Generation)│
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│  Layer 3: 输出层 (Output)           │
│  职责：格式化输出，准备发送          │
│  模块：Module 5 (Integration)       │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│  Layer 4: 存储层 (Storage)          │
│  职责：数据的持久化存储              │
│  系统：Obsidian / Codex / GitHub    │
└─────────────────────────────────────┘
```

---

## 🧩 5个核心模块

### Module 1: 输入管理 (Input Manager)

**位置**: `modules/01-input/`

**功能**:
- 解析各种输入格式（文本、链接、文件）
- 验证输入数据的完整性
- 数据预处理和清洗

**输入**: 用户输入（多种格式）
**输出**: 格式化、验证后的数据

### Module 2: 内容拆解 (Content Decomposition)

**位置**: `modules/02-decomposition/`

**功能**:
- 将案例/文章自动拆解为关键要素
- 识别可拆解的多个角度
- 为每个角度推荐最适合的文案类型

**输入**: 案例/文章内容
**输出**: 拆解结果（包含5个角度的建议）

### Module 3: 文案生成 (Copywriting Generation)

**位置**: `modules/03-generation/`

**功能**:
- 基于提示词生成高质量文案
- 支持多种文案类型和领域
- 批量生成多条文案

**输入**: 拆解结果 + 生成配置
**输出**: 完整的文案包（脚本、字幕、配图建议等）

### Module 4: 数据管理 (Data Management)

**位置**: `modules/04-data/`

**功能**:
- 定义所有数据的结构和格式
- Obsidian读写接口
- 双向链接管理

**职责**: 数据的持久化和关系管理

### Module 5: 集成管理 (Integration Management)

**位置**: `modules/05-integration/`

**功能**:
- Codex集成
- WorkBuddy集成
- Obsidian集成
- 版本管理

---

## 🔄 模块间通信

### 数据流向

```
Module 1 → Module 2 → Module 3 → Module 5 → Module 4
(输入)      (拆解)      (生成)      (集成)      (存储)
```

### 通信接口

| 从 | 到 | 接口 | 数据格式 |
|----|----|----|----------|
| M1 | M2 | input_parser.validate() | validated_input (JSON) |
| M2 | M3 | decompose_engine.extract_elements() | decomposed_elements (JSON) |
| M3 | M5 | generation_engine.generate() | copywriting_package (JSON) |
| M5 | M4 | data_manager.save_to_storage() | save_confirmation |

---

## 📂 项目结构

```
lawyer-short-video-skill/
│
├─ README.md                              # 项目总览
├─ ARCHITECTURE.md                        # 本文件
├─ VERSION.md                             # 版本说明
├─ CHANGELOG.md                           # 更新日志
├─ LICENSE                                # MIT License
├─ .gitignore                             # Git忽略
├─ CONTRIBUTING.md                        # 贡献指南
│
├─ modules/                               # 5个核心模块
│  ├─ 01-input/
│  │  ├─ README.md
│  │  ├─ input-parser.md
│  │  ├─ validation-rules.md
│  │  └─ preprocessing.md
│  │
│  ├─ 02-decomposition/
│  │  ├─ README.md
│  │  ├─ decompose-engine.md
│  │  ├─ decompose-templates/
│  │  ├─ decompose-rules/
│  │  └─ decompose-examples/
│  │
│  ├─ 03-generation/
│  │  ├─ README.md
│  │  ├─ generation-engine.md
│  │  ├─ prompts/
│  │  │  ├─ 00-main-prompt.md
│  │  │  ├─ 01-style-guide.md
│  │  │  ├─ 02-copywriting-templates/
│  │  │  ├─ 03-field-customization/
│  │  │  └─ 04-dynamic-adjustments/
│  │  ├─ libraries/
│  │  │  ├─ hook-library.md
│  │  │  ├─ case-library.md
│  │  │  ├─ cta-library.md
│  │  │  ├─ transition-words.md
│  │  │  ├─ emotion-words.md
│  │  │  └─ key-phrases.md
│  │  └─ quality-control.md
│  │
│  ├─ 04-data/
│  │  ├─ README.md
│  │  ├─ metadata-schema.md
│  │  ├─ data-flow-diagram.md
│  │  ├─ obsidian-interface.md
│  │  ├─ codex-interface.md
│  │  └─ workbuddy-interface.md
│  │
│  └─ 05-integration/
│     ├─ README.md
│     ├─ codex-integration-guide.md
│     ├─ workbuddy-integration-guide.md
│     ├─ obsidian-integration-guide.md
│     └─ version-management.md
│
├─ docs/                                  # 用户文档
│  ├─ 01-quick-start.md
│  ├─ 02-user-guide.md
│  ├─ 03-advanced-usage.md
│  ├─ 04-troubleshooting.md
│  ├─ 05-faq.md
│  └─ integration/
│     ├─ obsidian-guide.md
│     ├─ codex-guide.md
│     ├─ workbuddy-guide.md
│     └─ decomposition-guide.md
│
├─ examples/                              # 示例
│  ├─ decomposition-examples/
│  └─ generation-examples/
│
├─ templates/                             # 模板
│  ├─ obsidian-templates/
│  └─ task-templates/
│
├─ config/                                # 配置
│  ├─ version.json
│  ├─ parameter-defaults.json
│  ├─ field-settings.json
│  ├─ persona-settings.json
│  └─ integration-settings.json
│
and tools/                                # 工具脚本
   ├─ version-check.sh
   ├─ setup.sh
   └─ README.md
```

---

## 🔌 扩展点

如果未来要添加新功能，这些是扩展点：

### 新的文案类型

**修改位置**: `modules/03-generation/prompts/02-copywriting-templates/`

**操作**:
1. 创建新文件：`your-new-type.md`
2. 定义提示词框架
3. 不需要修改其他模块

### 新的法律领域

**修改位置**: 
- `modules/02-decomposition/decompose-rules/`
- `modules/03-generation/prompts/03-field-customization/`

**操作**:
1. 添加拆解规则
2. 添加领域特定提示词
3. 不影响其他模块

### 新的集成工具

**修改位置**: `modules/05-integration/`

**操作**:
1. 创建新的集成指南
2. 定义接口规范
3. 不影响其他模块

---

## ✅ 避免的问题

### ❌ 硬编码
✅ **解决**: 所有参数都在 `config/` 中定义

### ❌ 代码重复
✅ **解决**: 公用逻辑在各模块的 base 文件中

### ❌ 循环依赖
✅ **解决**: 数据流向是单向的

### ❌ 修改牵连
✅ **解决**: 修改某模块不影响其他模块（通过接口通信）

---

## 📝 版本管理

每个模块都有 `README.md`，记录：
- 模块功能
- 输入输出格式
- 依赖关系
- 修改历史
- 已知问题

主 `CHANGELOG.md` 记录：
- 整体版本
- 各模块变更
- 兼容性说明
- 升级指南

---

这就是完整的架构设计。如有问题，请查阅各模块的README或提交Issue。
