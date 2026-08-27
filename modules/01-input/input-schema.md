# 输入字段

## 必填

- `content_id`：唯一标识；
- `input_type`：case/article/idea/metrics；
- `source_ids`：来源列表；
- `deidentified`：是否已由用户确认脱敏；
- `permission_status`：允许范围；
- `legal_field`：法律领域；
- `jurisdiction`：适用地区或 `【待补充】`；
- `legal_timepoint`：法律适用时点或 `【待补充】`；
- `audience`：目标受众；
- `primary_objective`：主传播目标；
- `content_type`：内容类型；
- `duration`：60s/90s/3min；
- `persona`：人设；
- `must_not_disclose`：禁止披露信息。

## 案例追加字段

案件阶段、角色映射、时间线、金额口径、证据状态、对方主张、已确认结果。未知字段不得以模型推测补齐。
