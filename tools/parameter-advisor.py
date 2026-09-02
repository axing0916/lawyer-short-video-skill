#!/usr/bin/env python3
"""交互式参数选择顾问：帮助用户在填表前评估传播目标与内容类型的搭配。

只读取本仓库的 `config/content-types.json`，不访问网络、不上传内容。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_TYPES_PATH = ROOT / "config" / "content-types.json"

OBJECTIVE_LABELS = {
    "save": "收藏（承诺可复用的清单/步骤）",
    "discuss": "讨论（从常见误解出发的有条件纠正）",
    "share": "转发（可识别场景+不评判提醒）",
    "explore": "探索（悬念与条件揭示）",
    "trust": "专业信任（决策框架与判断过程）",
}

CONTENT_TYPE_LABELS = {
    "story": "故事驱动型（真实决策与后果，或明确标注的虚构教学）",
    "educational": "教育知识型（规则、程序、常见误区）",
    "comparison": "对比冲击型（同口径对比不同后果）",
    "practical": "干货实操型（材料保存、流程准备、风险检查）",
}

# 兼容性矩阵：(primary_objective, content_type) -> (score 1-5, reason)
# 评分含义：5=强烈推荐 4=推荐 3=可以谨慎使用 2=不建议 1=不推荐
COMPATIBILITY_MATRIX: dict[tuple[str, str], tuple[int, str]] = {
    ("save", "story"): (2, "故事型侧重情境与判断迁移，难以承载清单式收藏内容；如坚持使用，需额外提炼可复用步骤。"),
    ("save", "educational"): (4, "教育知识型自带核验/行动清单结构，便于观众收藏后按步骤操作。"),
    ("save", "comparison"): (3, "对比结构可以附带清单，但对比冲击力可能分散收藏所需的步骤感，需要收尾单独收敛为清单。"),
    ("save", "practical"): (5, "干货实操型的“先做什么/再做什么/保存什么”结构与收藏目标完全对应。"),
    ("discuss", "story"): (3, "真实案例能引发讨论，但要求来源完整、授权清楚，素材门槛较高。"),
    ("discuss", "educational"): (4, "教育知识型的“容易混淆之处”天然适合引出讨论。"),
    ("discuss", "comparison"): (5, "对比冲击型直接呈现条件差异，最容易引发“到底哪种情况适用”的讨论。"),
    ("discuss", "practical"): (3, "干货实操型偏执行导向，讨论空间有限，需要额外设计争议点。"),
    ("share", "story"): (4, "可识别场景+真实后果容易让观众转给身边有相似处境的人，但需确认授权与脱敏。"),
    ("share", "educational"): (3, "教育知识型信息密度高，转发意愿取决于是否解决了具体痛点。"),
    ("share", "comparison"): (3, "对比内容转发意愿中等，需要明确“转给谁看”的角色定位。"),
    ("share", "practical"): (4, "干货实操型的具体建议便于观众转给正在经历同类问题的人。"),
    ("explore", "story"): (5, "故事型的情境、选择、障碍结构天然带有悬念，最适合维持观看。"),
    ("explore", "educational"): (3, "教育知识型的“为什么不完整”可以制造悬念，但需要避免变成单纯说教。"),
    ("explore", "comparison"): (4, "对比冲击型“排除一个直觉答案”的结构与探索目标高度契合。"),
    ("explore", "practical"): (2, "干货实操型偏执行清单，天然张力不足，需要额外设计悬念钩子。"),
    ("trust", "story"): (4, "真实决策过程展示专业判断力，但对来源完整性和授权要求更高。"),
    ("trust", "educational"): (5, "决策框架、风险权衡与教育知识型的结构直接对应，最能展示专业判断而非结果承诺。"),
    ("trust", "comparison"): (4, "对比冲击型的“决策标准”环节可以直接展示专业权衡过程。"),
    ("trust", "practical"): (3, "干货实操型偏操作细节，专业信任感需要额外补充“为什么这样判断”。"),
}

SCORE_LABELS = {
    5: "⭐⭐⭐⭐⭐ 强烈推荐",
    4: "⭐⭐⭐⭐ 推荐",
    3: "⭐⭐⭐ 可以谨慎使用",
    2: "⭐⭐ 不建议",
    1: "⭐ 不推荐",
}


def load_content_types() -> dict:
    if CONTENT_TYPES_PATH.is_file():
        return json.loads(CONTENT_TYPES_PATH.read_text(encoding="utf-8"))
    return {
        "objectives": list(OBJECTIVE_LABELS),
        "content_types": list(CONTENT_TYPE_LABELS),
    }


def score_combination(objective: str, content_type: str) -> tuple[int, str]:
    """返回 (score, reason)；未知组合默认给出中性提示。"""
    key = (objective, content_type)
    if key in COMPATIBILITY_MATRIX:
        return COMPATIBILITY_MATRIX[key]
    return (3, "该组合暂无预设评估，建议参考对应目标与内容类型的提示词说明后谨慎使用。")


def format_recommendation(objective: str, content_type: str) -> str:
    score, reason = score_combination(objective, content_type)
    label = SCORE_LABELS.get(score, str(score))
    lines = [
        f"传播目标：{objective}（{OBJECTIVE_LABELS.get(objective, '未知')}）",
        f"内容类型：{content_type}（{CONTENT_TYPE_LABELS.get(content_type, '未知')}）",
        f"兼容性评分：{score}/5 —— {label}",
        f"理由：{reason}",
    ]
    return "\n".join(lines)


def print_matrix() -> None:
    objectives = list(OBJECTIVE_LABELS)
    content_types = list(CONTENT_TYPE_LABELS)
    print("传播目标 × 内容类型 兼容性评分表\n")
    for objective in objectives:
        for content_type in content_types:
            score, reason = score_combination(objective, content_type)
            print(f"[{objective} x {content_type}] {score}/5 - {reason}")


def choose_from(prompt: str, options: list[str], labels: dict[str, str]) -> str:
    print(prompt)
    for index, option in enumerate(options, start=1):
        print(f"  {index}. {option} - {labels.get(option, '')}")
    while True:
        raw = input("请输入编号: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print("输入无效，请重新输入编号。")


def build_front_matter(params: dict[str, str]) -> str:
    lines = ["---"]
    for key, value in params.items():
        lines.append(f"{key}: {value}" if value else f'{key}: "【待补充】"')
    lines.append("---")
    return "\n".join(lines)


def save_to_template(params: dict[str, str], output_path: Path) -> None:
    front_matter = build_front_matter(params)
    content = (
        f"{front_matter}\n\n# 内容简报\n\n"
        "> 如涉及客户或案件材料，请先由你自行脱敏，不要粘贴未脱敏原始案卷。\n\n"
        "## 来源\n\n- SRC-001：`【待补充：来源、日期、授权、脱敏状态】`\n\n"
        "## 已确认事实\n\n- `【待补充】`\n\n"
        "## 单方主张\n\n- `【待补充】`\n\n"
        "## 目标受众与问题\n\n- 受众：`【待补充】`\n- 想解决的问题：`【待补充】`\n\n"
        "## 不得披露\n\n- `【待补充】`\n"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"已保存参数模板至：{output_path}")


def interactive_main() -> int:
    data = load_content_types()
    objectives = data.get("objectives", list(OBJECTIVE_LABELS))
    content_types = data.get("content_types", list(CONTENT_TYPE_LABELS))

    print("=== 参数选择顾问 ===")
    print("本工具只做搭配建议，不替代法律核验和人工终审。\n")

    objective = choose_from("请选择传播目标：", objectives, OBJECTIVE_LABELS)
    content_type = choose_from("请选择内容类型：", content_types, CONTENT_TYPE_LABELS)

    print()
    print(format_recommendation(objective, content_type))
    print()

    save_choice = input("是否将该参数保存为输入模板？(y/N): ").strip().lower()
    if save_choice == "y":
        default_path = ROOT / "templates" / "input" / "content-brief.md"
        raw_path = input(f"保存路径（回车使用默认覆盖检查路径 {default_path}）: ").strip()
        output_path = Path(raw_path) if raw_path else default_path
        params = {
            "primary_objective": objective,
            "content_type": content_type,
        }
        save_to_template(params, output_path)

    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        print_matrix()
        # 校验矩阵完整性与评分范围
        objectives = list(OBJECTIVE_LABELS)
        content_types = list(CONTENT_TYPE_LABELS)
        missing = []
        for objective in objectives:
            for content_type in content_types:
                key = (objective, content_type)
                if key not in COMPATIBILITY_MATRIX:
                    missing.append(key)
                else:
                    score, _reason = COMPATIBILITY_MATRIX[key]
                    if not 1 <= score <= 5:
                        print(f"SELF-TEST FAILED: invalid score for {key}")
                        return 1
        if missing:
            print(f"SELF-TEST FAILED: missing combinations {missing}")
            return 1
        print("\nSELF-TEST PASSED")
        return 0

    if "--list" in argv:
        print_matrix()
        return 0

    try:
        return interactive_main()
    except (EOFError, KeyboardInterrupt):
        print("\n已取消。")
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
