# 校验工具

工具只读取当前仓库，不访问网络、不上传内容、不修改用户文件。

- `validate.py`：总验收；
- `detect-pii.py`：离线正则扫描身份证号、手机号、案号、统一社会信用代码、银行卡号等可识别信息；
  支持 `--file`/`--dir`/`--text`/`--self-test`；
- `validate-schema.py`：按 `config/schema.json` 校验 `tests/fixtures/e2e/*/input.json`（无第三方依赖的
  最小 JSON Schema 子集实现）；
- `check-links.py`：Markdown 内部链接；
- `count-content.py`：文件、字符和分类统计；
- `content-audit.py`：检查错误日期、虚假支持信息和未标注教学情景；
- `setup.sh`：运行环境与仓库校验；
- `version-check.sh`：版本真源一致性。
