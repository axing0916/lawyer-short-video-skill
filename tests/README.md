# 测试

## 目录内容

- `fixtures/*.json`：结构不变量测试用输入，由 `tools/validate.py` 间接覆盖 JSON 有效性，
  语义仍需人工核对：
  - `unredacted.json`：未脱敏，预期 blocked；
  - `missing-source.json`：无来源，预期 blocked；
  - `fictional-scenario.json`：明确虚构，可进入生成但需法律核验；
  - `legal-review.json`：法律规则未核验，预期 needs_legal_review；
- `fixtures/e2e/`：4 个端到端场景（`input.json` + `expected-output.json`），见
  `e2e-test-cases.md`；
- `e2e-test-cases.md`：端到端测试场景说明、预期输出和验证步骤；
- `e2e_runner.py`：端到端测试执行引擎，按 `QUALITY-GATES.md` 门槛规则计算路由状态并与预期比对；
- `run-e2e-tests.sh`：`e2e_runner.py` 的 shell 包装，供本地或 CI 调用；
- `performance-testing.md`：性能测试框架、场景与 v1.0 基线（PII 扫描、Schema 校验、内存）；
- `run-all-tests.sh`：统一测试入口，见下文。

## 运行方式

**运行全部测试（推荐）：**

```sh
./tests/run-all-tests.sh
```

依次执行：仓库结构校验（`tools/validate.py`）→ PII 检测自检（`tools/detect-pii.py --self-test`）
→ Schema 校验（`tools/validate-schema.py`）→ 端到端测试（`tests/e2e_runner.py`）→ 性能冒烟测试。

**快速模式（跳过性能测试）：**

```sh
./tests/run-all-tests.sh --quick
```

**生成 HTML 报告**（写入 `tests/report.html`，已加入 `.gitignore`，不会被提交）：

```sh
./tests/run-all-tests.sh --report html
```

**只运行端到端测试：**

```sh
./tests/run-e2e-tests.sh
# 或
python3 tests/e2e_runner.py
```

**只运行某一个端到端场景**（直接用 Python 检查单个 fixture，不新增脚本参数）：

```sh
python3 -c "
import json, importlib.util
spec = importlib.util.spec_from_file_location('e2e_runner', 'tests/e2e_runner.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
data = json.load(open('tests/fixtures/e2e/case-03-high-risk-info/input.json'))
print(m.evaluate(data))
"
```

**只运行 PII 检测：**

```sh
python3 tools/detect-pii.py --self-test
python3 tools/detect-pii.py --file <path>
python3 tools/detect-pii.py --dir <目录>
```

自动测试目前验证结构不变量与路由决策；语义质量仍需律师盲测。

