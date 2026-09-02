# 参数顾问工具测试用例

针对 `tools/parameter-advisor.py` 的手动/半自动测试用例。工具无网络访问，测试可在本地或 CI 沙箱中直接执行。

## 用例 1：评分表完整性自检

```bash
python3 tools/parameter-advisor.py --self-test
```

**预期**：
- 打印全部 5×4=20 组"传播目标 × 内容类型"组合及各自的评分（1-5）和理由；
- 每组评分均在 1-5 范围内，不存在缺失组合；
- 最后一行输出 `SELF-TEST PASSED`，退出码为 0。

## 用例 2：直接打印评分表

```bash
python3 tools/parameter-advisor.py --list
```

**预期**：
- 不进入交互流程，直接打印完整评分表；
- 退出码为 0。

## 用例 3：交互式选择与推荐

```bash
printf "4\n1\nN\n" | python3 tools/parameter-advisor.py
```

输入含义：传播目标选第 4 项（explore），内容类型选第 1 项（story），不保存模板。

**预期输出包含**：

```
传播目标：explore（探索（悬念与条件揭示））
内容类型：story（故事驱动型（真实决策与后果，或明确标注的虚构教学））
兼容性评分：5/5 —— ⭐⭐⭐⭐⭐ 强烈推荐
理由：故事型的情境、选择、障碍结构天然带有悬念，最适合维持观看。
```

- 提示"是否将该参数保存为输入模板？"，输入 `N` 后不生成任何文件；
- 退出码为 0。

## 用例 4：低分组合应显示警示理由

```bash
printf "1\n1\nN\n" | python3 tools/parameter-advisor.py
```

输入含义：传播目标选第 1 项（save），内容类型选第 1 项（story）。

**预期**：
- 评分为 2/5，标签为"⭐⭐ 不建议"；
- 理由文本说明故事型难以承载清单式收藏内容。

## 用例 5：保存参数到输入模板

```bash
printf "1\n4\ny\n/tmp/parameter-advisor-test.md\n" | python3 tools/parameter-advisor.py
cat /tmp/parameter-advisor-test.md
rm /tmp/parameter-advisor-test.md
```

输入含义：传播目标选第 1 项（save），内容类型选第 4 项（practical），保存到指定路径。

**预期**：
- 终端打印"已保存参数模板至：/tmp/parameter-advisor-test.md"；
- 生成的文件包含 YAML front matter，其中 `primary_objective: save`、`content_type: practical`；
- 文件结构与 `templates/input/content-brief.md` 一致，包含"来源""已确认事实""单方主张""目标受众与问题""不得披露"等章节，未确认信息标注为 `【待补充】`。

## 用例 6：非法输入处理

```bash
printf "abc\n1\n1\nN\n" | python3 tools/parameter-advisor.py
```

**预期**：
- 输入非数字或超出范围时提示"输入无效，请重新输入编号。"，并重新等待输入；
- 后续合法输入（`1`）后流程正常继续。

## 用例 7：中途取消（EOF）

```bash
printf "1\n" | python3 tools/parameter-advisor.py
```

（只提供传播目标输入，内容类型选择时遇到 EOF）

**预期**：
- 工具捕获 `EOFError`，打印"已取消。"；
- 退出码为 1，不生成任何文件、不抛出未捕获异常。

## 回归检查

修改评分矩阵或交互逻辑后，至少重新运行用例 1（自检）和用例 3（基本交互）确认没有破坏既有行为，并运行：

```bash
python3 tools/validate.py
```

确认仓库结构校验仍然通过。
