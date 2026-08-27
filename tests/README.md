# 测试夹具

这些输入用于验证阻断和状态路由，不用于生成可发布内容。

- `unredacted.json`：未脱敏，预期 blocked；
- `missing-source.json`：无来源，预期 blocked；
- `fictional-scenario.json`：明确虚构，可进入生成但需法律核验；
- `legal-review.json`：法律规则未核验，预期 needs_legal_review。

自动测试目前验证结构不变量；语义质量仍需律师盲测。
