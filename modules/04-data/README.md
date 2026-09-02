# 数据模块

数据模块只记录已发生的发布结果，并把事实、计算和解释分开。

流程：导入原始数据 → 校验口径 → 计算指标 → 与自身基线比较 → 形成下一轮单变量假设。没有数据时保持空值，不填充“行业平均”。

## 因果论断禁止清单

不得把同时发生或前后发生直接写成因果关系。反面表述：“发布视频后咨询增加，因此视频带来咨询”“某标题使转化率提升”。正面表述：“发布后观察到咨询数变化；该变化与同期投放、节假日等因素共同出现，不能据此确认因果”“相对既有基线的关联值得在后续控制变量的测试中观察”。

禁止以单条内容、单一时间段或虚构“行业平均”得出效果结论；也不得以数据推断个案法律结果。

## 合规记录格式

每条观察记录必须有比较基线和混淆变量。缺失的真实数据填 `null`，不得以估计值补齐。

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["period", "metric", "observed_value", "baseline", "confounders"],
  "properties": {
    "period": {"type": "string"},
    "metric": {"type": "string"},
    "observed_value": {"type": ["number", "null"]},
    "baseline": {"type": ["number", "null"]},
    "confounders": {"type": "array", "items": {"type": "string"}},
    "interpretation": {"type": ["string", "null"]}
  }
}
```

```json
{
  "period": "2026-08-01 至 2026-08-31",
  "metric": "已记录咨询数",
  "observed_value": null,
  "baseline": null,
  "confounders": ["同期投放情况【待补充】", "节假日", "平台推荐波动"],
  "interpretation": null
}
```

只有在记录了相同口径基线、完整观察值及混淆变量后，才可提出待验证的相关性假设；仍不得将其表述为因果结论。
