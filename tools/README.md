# 校验工具

工具只读取当前仓库，不访问网络、不上传内容、不修改用户文件。

- `validate.py`：总验收；追加一个或多个 `--output <输出 JSON>` 时也会调用输出 Schema 校验；
- `check-links.py`：Markdown 内部链接；
- `count-content.py`：文件、字符和分类统计；
- `content-audit.py`：检查错误日期、虚假支持信息和未标注教学情景；
- `setup.sh`：运行环境与仓库校验；
- `version-check.sh`：版本真源一致性。
- `validate-output.py <输出 JSON>`：按 `config/output-schema.json` 检查生成交付包；`--schema-check` 检查内置 draft-07 声明。
- `version-tracking.py --init <文件> --template <模板> --modifier <修改人>`：从模板创建含 YAML frontmatter 的首版；编辑正文后用 `--update <文件> --modifier <修改人> --type human_edit` 记录新版本；`--diff <旧文件> <新文件>` 比较两个版本正文。元数据记录时间、修改人、修改类型和 SHA-256 内容 hash。
