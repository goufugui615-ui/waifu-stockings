#!/usr/bin/env python3
"""老婆们的丝袜 · 提示词合规与结构自检

用法:
    python check_prompt.py prompt.txt
    type prompt.txt | python check_prompt.py     (Windows)
    python check_prompt.py -                    (从标准输入读)

纯标准库，无第三方依赖。只做快速兜底，不替代人工判断。
注意：合规词只扫描【正向提示词】段，避免把【负面词】里列出的禁用词误判为违规。
"""

import sys
import argparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SECTIONS = ["【正向提示词】", "【英文关键词】", "【负面词】", "【参数建议】", "【自检结论】"]

# 一票否决：出现在正向提示词里即不合规
VETO_WORDS = ["未成年", "色情", "裸露", "性暗示", "换脸", "女明星", "萝莉", "幼女"]

# 画风冲突词：本 skill 只做真人写实
CG_WORDS = [
    "3D CG animation", "soft painted CG", "semi-realistic stylized CG",
    "luminous rim light", "glowing bokeh", "Cooke lens",
]

# 正向提示词里必须出现的结构项：(名称, 任一命中即可的关键词组, 级别)
REQUIRED = [
    ("成年主体", ["成年女性", "成年模特"], "veto"),
    ("真实照片排除句", ["真实照片", "专业摄影师拍摄"], "veto"),
    ("明确排除绘画与渲染", ["不是任何形式", "非数字绘画", "3D 渲染"], "veto"),
    ("下半身构图", ["腰部以下", "下半身"], "normal"),
    ("完整双腿与脚", ["完整双腿", "脚部"], "normal"),
    ("编织结构", ["编织结构", "尼龙纤维", "Fine nylon weave"], "normal"),
    ("透肤与厚度", ["透肤", "织物厚度", "不透明度"], "normal"),
    ("纤维光泽", ["纤维光泽"], "normal"),
    ("排除塑料橡胶", ["塑料或橡胶", "塑料", "橡胶"], "normal"),
    ("皮肤纹理", ["皮肤纹理", "自然毛孔", "Natural skin pores"], "normal"),
    ("85mm 镜头", ["85mm"], "normal"),
    ("真实光学景深", ["光学景深", "depth of field"], "normal"),
    ("RAW 质感", ["RAW"], "normal"),
    ("真实环境反射", ["环境反射", "environment reflection"], "normal"),
]


def split_sections(text):
    """把全文切成 5 段，返回 {段标题: 段内容或 None}。"""
    positions = [(s, text.find(s)) for s in SECTIONS]
    result = {}
    for i, (name, pos) in enumerate(positions):
        if pos < 0:
            result[name] = None
            continue
        start = pos + len(name)
        end = len(text)
        for _, next_pos in positions[i + 1:]:
            if next_pos > pos:
                end = next_pos
                break
        result[name] = text[start:end].strip()
    return result


def extract_positive(text):
    """只取【正向提示词】段做合规与要素检查。"""
    sections = split_sections(text)
    return sections.get(SECTIONS[0]) or text


def check(text: str) -> int:
    scope = extract_positive(text)
    sections = split_sections(text)

    print("=" * 52)
    print("老婆们的丝袜 · 提示词自检")
    print("=" * 52)

    veto_bad = [w for w in VETO_WORDS if w in scope]
    print("\n[一票否决词]（仅扫描正向提示词）")
    print("  通过：未发现" if not veto_bad else "  不通过：发现 " + "、".join(veto_bad))

    cg_bad = [w for w in CG_WORDS if w in scope]
    print("\n[画风冲突词]")
    print("  通过：未发现 CG 动画风词块" if not cg_bad else "  不通过：发现 " + "、".join(cg_bad))

    print("\n[输出结构 5 段]")
    missing_sections = []
    for name in SECTIONS:
        content = sections.get(name)
        ok = bool(content)
        print(f"  {'OK  ' if ok else 'MISS'}  {name}")
        if not ok:
            missing_sections.append(name)

    print("\n[正向提示词必需项]")
    failed = []
    for name, keys, level in REQUIRED:
        ok = any(k in scope for k in keys)
        tag = "OK  " if ok else "MISS"
        mark = " (一票否决)" if level == "veto" else ""
        print(f"  {tag}  {name}{mark}")
        if not ok:
            failed.append((name, level))

    veto_failed = [n for n, lv in failed if lv == "veto"]
    total = len(REQUIRED) + len(SECTIONS)
    passed = (len(REQUIRED) - len(failed)) + (len(SECTIONS) - len(missing_sections))
    score = round(passed / total * 100)

    print("\n" + "-" * 52)
    print(f"得分：{score}/100")
    if veto_bad or cg_bad or veto_failed or missing_sections:
        print("结论：不通过 —— 请按 SKILL.md 的固定模板补齐后重新生成，不要直接出图。")
        return 1
    if failed:
        print("结论：基本通过，但有一般项缺失，建议在【自检结论】里注明调整。")
        return 0
    print("结论：全部通过。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="丝袜材质提示词合规与结构自检")
    ap.add_argument("path", nargs="?", default="-", help="提示词文本文件路径，省略或 - 表示标准输入")
    args = ap.parse_args()

    if args.path == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(args.path, "r", encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            print(f"读取失败：{e}", file=sys.stderr)
            return 2

    if not text.strip():
        print("输入为空。", file=sys.stderr)
        return 2
    return check(text)


if __name__ == "__main__":
    sys.exit(main())
