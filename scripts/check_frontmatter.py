#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 SKILL.md frontmatter（无第三方依赖）：打包或上传前跑一下。

用法:
    python scripts/check_frontmatter.py

检查项：BOM、首尾 --- 标记、name/description 是否存在、name 格式与目录名一致性、
纯量值里是否混入「: 」、以及是否被塞进客户端不支持的字段。
"""
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(HERE, "SKILL.md")
ALLOWED = {"name", "description"}


def main():
    if not os.path.isfile(SKILL):
        print("找不到 SKILL.md:", SKILL, file=sys.stderr)
        return 2
    raw = open(SKILL, "rb").read()
    errs, warns = [], []

    if raw.startswith(b"\xef\xbb\xbf"):
        errs.append("文件带 UTF-8 BOM，会被解析器当成正文内容")
    text = raw.decode("utf-8").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        errs.append("第一行必须是 ---，且后面直接换行")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        errs.append("找不到 frontmatter 结束标记 ---")
    fm = parts[1] if len(parts) >= 3 else ""

    if "name:" not in fm:
        errs.append("缺少 name 字段")
    if "description:" not in fm:
        errs.append("缺少 description 字段")

    m = re.search(r"^name:\s*(.+)$", fm, re.M)
    if m:
        name = m.group(1).strip()
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            errs.append("name 必须是小写字母数字与连字符：" + name)
        dirname = os.path.basename(HERE)
        if name != dirname:
            warns.append("name 与目录名不一致（部分客户端要求一致）：%s != %s" % (name, dirname))

    for line in fm.splitlines():
        if ":" not in line or line.lstrip().startswith(("-", "#")):
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        if key not in ALLOWED:
            warns.append("frontmatter 含非必需字段 %s，部分客户端不支持，建议移到正文" % key)
        # 纯量值里出现 ": " 会把 YAML 解析成嵌套映射
        if ": " in val and not val.strip().startswith((">", "|", '"', "'")):
            errs.append("字段 %s 的纯量值含「: 」，请加引号或改用 >- 块标量" % key)

    print("== frontmatter 校验 ==")
    for e in errs:
        print("  [错误]", e)
    for w in warns:
        print("  [提醒]", w)
    if not errs:
        print("  [通过] frontmatter 可安全解析")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
