# 输入阶段来源锁定

为每个来源分配 `SRC-001` 格式的 ID，记录类型、取得日期、脱敏确认、公开权限和备注。

把每项输入写成：

```text
statement: 甲方称已交付货物
kind: party_claim
source_id: SRC-001
support_status: unverified
public_use: paraphrase_only
```

没有来源 ID 的细节不能进入案例叙事。模型自身输出永远不是新的事实来源。
