# 贡献指南

感谢您对本项目的兴趣！如果您想为律师短视频文案创作系统作出贡献，请阅读以下指南。

---

## 📋 如何贡献

### 报告Bug

如果您发现了Bug，请：

1. 检查 [Issues](https://github.com/axing0916/lawyer-short-video-skill/issues) 确保未被重复报告
2. 创建新Issue，包含：
   - Bug的清晰描述
   - 复现步骤
   - 预期行为 vs 实际行为
   - 您的系统/工具信息

### 提交改进建议

如果您有改进建议：

1. 查看 [Discussions](https://github.com/axing0916/lawyer-short-video-skill/discussions)
2. 如果是新想法，可以：
   - 在Discussions中讨论
   - 或直接创建Issue标记为"enhancement"

### 提交代码或文档改进

对于代码或文档的改进：

1. Fork本仓库
2. 创建特性分支：`git checkout -b feature/your-feature-name`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature-name`
5. 提交Pull Request

---

## 💡 贡献类型

我们欢迎以下类型的贡献：

- 🐛 **Bug修复** - 修复现有功能中的问题
- ✨ **新功能** - 添加新的文案类型或优化流程
- 📚 **文档改进** - 改进或补充文档
- 🎨 **界面优化** - 改进用户体验
- 🔍 **代码审查** - 审查和改进现有代码
- 🌍 **国际化** - 添加新的语言支持
- 📖 **示例补充** - 添加新的使用示例

---

## 🎨 代码规范

### Markdown规范

- 使用标准Markdown格式
- 标题使用 `#` 表示，确保结构清晰
- 代码块使用三反引号 \`\`\` 并指定语言
- 列表使用 `-` 或数字

### 文件命名规范

- 文档文件：使用 `kebab-case`（如 `quick-start.md`）
- 配置文件：使用 `kebab-case`（如 `parameter-defaults.json`）
- 提示词文件：描述性名称（如 `story-driven-60s.md`）

### 内容规范

- 使用清晰的标题和子标题
- 添加适当的代码示例
- 包含说明和最佳实践
- 链接到相关文档

---

## 📝 提交信息规范

请使用以下格式的提交信息：

```
<type>: <subject>

<body>

<footer>
```

### Type

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 格式调整（不改变功能）
- `refactor`: 代码重构
- `test`: 添加或修改测试
- `chore`: 构建工具或依赖变更

### Subject

- 使用祈使句（"Add feature" 而不是 "Added feature"）
- 不以句号结尾
- 简洁清晰

### Body

- 解释是什么和为什么，而不是怎么做
- 如果是Bug修复，说明原因
- 参考相关的Issue

### Footer

- 关闭相关Issue：`Closes #123`
- 破坏性变更的说明

---

## 🔄 Pull Request流程

1. **创建分支**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **做出更改**
   - 确保代码符合规范
   - 更新相关文档
   - 添加示例（如果适用）

3. **提交分支**
   ```bash
   git push origin feature/your-feature
   ```

4. **创建Pull Request**
   - 填写PR模板
   - 链接相关Issue
   - 说明改动内容

5. **等待审查**
   - 响应审查意见
   - 进行必要的调整

6. **合并**
   - 获得批准后合并到main分支

---

## 📚 项目结构指南

在提交改进时，请确保：

- **模块分离** - 新功能放在正确的模块中
- **文档完整** - 每个模块都有README.md说明
- **向下兼容** - 不破坏现有功能
- **版本更新** - 更新VERSION.md和CHANGELOG.md

---

## ❓ 需要帮助？

- 📖 查看 [文档](docs/)
- 💬 在 [Discussions](https://github.com/axing0916/lawyer-short-video-skill/discussions) 提问
- 🐛 查看 [已知问题](CHANGELOG.md#已知问题)

---

感谢您的贡献！🎉
