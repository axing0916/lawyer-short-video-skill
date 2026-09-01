# 端到端测试用例

本文件描述 `tests/fixtures/e2e/` 下 4 个完整的"输入 → 预期输出"场景。每个场景包含：

- `input.json`：符合 `config/schema.json` 输入结构的素材（含 `narrative_text` 正文片段）；
- `expected-output.json`：按 `QUALITY-GATES.md` 门槛规则推导出的预期路由结果（`status` + `reasons`）。

自动化验证由 `tests/e2e_runner.py`（经 `tests/run-e2e-tests.sh` 调用）执行：脚本读取每个
`input.json`，应用门槛规则计算实际状态，并与 `expected-output.json` 比对。测试只验证**路由决策**
是否正确，不生成、不发布任何文案；语义质量仍需律师盲测（见 `tests/README.md`）。

可能的 `status` 取值对应 `QUALITY-GATES.md` 的四类最终状态：

| status（机器可读） | 对应中文状态 |
|---|---|
| `ready_for_legal_review` | 可进入人工终审 |
| `needs_supplement` | 需补充后再写 |
| `needs_legal_review` | 需法律核验 |
| `blocked` | 不得发布 |

## 场景 1：真实案例完全脱敏（`case-01-fully-deidentified`）

**背景**：一份已完成脱敏的真实民间借贷调解案例，来源、脱敏确认、法律核验均齐备，关键事实完整。

**输入要点**：`deidentified=true`、`source_ids` 非空、`fictional=false`、`legal_source_verified=true`，
`key_facts` 各字段均为具体内容（无 `【待补充】`）。

**预期输出**：`status=ready_for_legal_review`，`reasons=[]`。

**验证步骤**：
1. 运行 `python3 tests/e2e_runner.py`；
2. 确认 `case-01-fully-deidentified` 一行输出 `PASS`，状态为 `ready_for_legal_review`；
3. 人工确认：即使自动检查全部通过，仍需人工终审才能发布，不可跳过。

## 场景 2：虚构教学未标记（`case-02-fictional-unlabeled`）

**背景**：一个用于讲解合同审查要点的虚构人物案例，`fictional=true`，但正文缺少强制的
「虚构教学情景」标记。

**预期输出**：`status=blocked`，`reasons=["fictional_label_required"]`。

**验证步骤**：
1. 运行测试，确认该场景标记为 `blocked`；
2. 对照 `templates/output/fictional-scenario-marker.md`（如已存在）确认标记规范；
3. 修复方式：在正文中加入「虚构教学情景」标记后重新运行，应转为 `ready_for_legal_review`
   （可在本地手动验证，不修改仓库内固定的 fixture）。

## 场景 3：高风险信息（`case-03-high-risk-info`）

**背景**：素材声明 `deidentified=true`，但正文中仍残留身份证号、手机号和案号等可直接识别信息。

**预期输出**：`status=blocked`，`reasons=["pii_detected"]`。

**验证步骤**：
1. 运行 `python3 tools/detect-pii.py --file tests/fixtures/e2e/case-03-high-risk-info/input.json`，
   确认检测到 `id_card` / `phone` / `case_number` 等命中项；
2. 运行 `tests/e2e_runner.py`，确认状态为 `blocked`；
3. 确认该场景说明"用户自称已脱敏"不能替代实际检测，工具应独立复核。

## 场景 4：事实缺失（`case-04-missing-facts`）

**背景**：一起股权代持纠纷案例，来源与脱敏确认齐备，但 `legal_timepoint` 与多个 `key_facts`
字段仍为 `【待补充】`，`evidence_status=unknown`。

**预期输出**：`status=needs_supplement`，`reasons=["missing_key_facts"]`。

**验证步骤**：
1. 运行测试，确认该场景标记为 `needs_supplement`；
2. 确认输出中未编造任何缺失事实（对照 `AGENTS.md` 第 2 条）；
3. 确认后续动作是"补充材料"而非直接生成内容。

## 运行全部场景

```sh
./tests/run-e2e-tests.sh
```

或直接调用 Python 引擎（等效）：

```sh
python3 tests/e2e_runner.py
```

新增场景时，在 `tests/fixtures/e2e/` 下新建目录，放入 `input.json` 与 `expected-output.json`，
脚本会自动发现并纳入测试，无需修改测试代码。
