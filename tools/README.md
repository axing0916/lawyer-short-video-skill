# 校验工具

工具只读取当前仓库，不访问网络、不上传内容、不修改用户文件。

- `validate.py`：总验收；
- `check-links.py`：Markdown 内部链接；
- `count-content.py`：文件、字符和分类统计；
- `content-audit.py`：检查错误日期、虚假支持信息和未标注教学情景；
- `parameter-advisor.py`：交互式参数选择顾问，评估传播目标与内容类型的搭配；
- `setup.sh`：运行环境与仓库校验；
- `version-check.sh`：版本真源一致性。

## 参数选择顾问（`parameter-advisor.py`）

在填写 `templates/input/content-brief.md` 前，用它评估传播目标与内容类型的搭配是否合理，避免前期投入后才发现组合不推荐。

```bash
python3 tools/parameter-advisor.py
```

工具会依次要求选择传播目标（收藏/讨论/转发/探索/专业信任）和内容类型（故事/教育/对比/实操），然后输出：

```
传播目标：explore（探索（悬念与条件揭示））
内容类型：story（故事驱动型（真实决策与后果，或明确标注的虚构教学））
兼容性评分：5/5 —— ⭐⭐⭐⭐⭐ 强烈推荐
理由：故事型的情境、选择、障碍结构天然带有悬念，最适合维持观看。
```

评分为 5 分制，1-2 分为不建议、3 分为可以谨慎使用、4-5 分为推荐；每个组合都附带具体理由，而非单纯打分。选择完成后可以选择将参数保存为输入模板（默认写入与 `templates/input/content-brief.md` 相同的结构），也可以指定其他保存路径。

其他用法：

- `python3 tools/parameter-advisor.py --list`：直接打印完整兼容性评分表，不进入交互流程；
- `python3 tools/parameter-advisor.py --self-test`：校验评分表完整性，用于自动化检查。

该工具只读取本仓库的 `config/content-types.json`，不访问网络、不上传内容，也不能替代法律核验和人工终审。
