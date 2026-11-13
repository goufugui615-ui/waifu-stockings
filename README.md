# 老婆们的丝袜（waifu-stockings）

游戏角色**丝袜材质真人摄影**提示词工坊。把「角色 + 丝袜款式 + 场景 + 光线」转成可复现的中文提示词，并附带英文关键词、负面词、参数建议与自检结论。

- **风格定位**：真人写实 / 商业时尚材质特写。最终效果是「专业摄影师拍的真实照片」，不是数字绘画，也不是 3D CG 渲染。
- **内容来源**：基于提供的 PDF《真实摄影风格 · 游戏角色丝袜材质还原》提炼。`recipes.md` 的 R01 正文与英文关键词均逐字收录原文，R02–R05 是按同一骨架扩展的变体。
- **工坊层扩展**（非 PDF 原文）：`references/elements.md` 要素库、`references/compliance.md` 红线与自检、`scripts/` 下的两个校验脚本、`examples/` 示例，以及固定 5 段输出结构，都是为便于复用而新增的。
- **版本**：1.0.2

## 安装

### Claude Code
```bash
cp -r waifu-stockings ~/.claude/skills/          # 个人级
cp -r waifu-stockings <你的项目>/.claude/skills/  # 项目级
```

### Claude.ai（网页 / 桌面）
把仓库根目录的 `老婆们的丝袜.zip` 上传：Settings → Capabilities → Skills → Upload skill。
zip 内顶层目录为 `waifu-stockings/`，与 `SKILL.md` 的 `name` 一致，解压后可直接用。

若客户端要求 `SKILL.md` 必须位于压缩包**根目录**，改用 `老婆们的丝袜_根目录版.zip`（文件相同，只是去掉了顶层目录）。

### DSH / WorkBuddy 等支持 skills 的客户端
把整个 `waifu-stockings/` 目录（含 `SKILL.md` 与 `references/`）放进工作区的 `skills/` 下即可。

## 关于 frontmatter

`SKILL.md` 的 frontmatter **只保留 `name` 与 `description` 两个必需字段**：

- `description` 的值里不出现「冒号 + 空格」—— 这会被 YAML 当成嵌套映射，导致整个 frontmatter 解析失败（常见的 `Triggers: ...` 写法就是这么踩坑的）；
- `version`、`license` 移到正文首行，因为部分客户端不接受额外字段；
- 无 BOM、首行 `---`、字段值不加引号也能安全解析。

打包或上传前先跑一次 `python scripts/check_frontmatter.py` 兜底。

## 用法示例

- 「帮我按 R01 写一张丝袜材质特写（附角色参考图），20D 半透肤色、白床单卧室、9:16」
- 「这套配方的丝袜反光太硬，改成窗边柔光的纤维光泽」
- 「还原某角色黑色 80D 不透丝袜 + 蕾丝边缘，给我中文 prompt 和负面词」
- 「把这段提示词按 skill 的固定结构补全，并跑一遍自检」

> 示例一律使用占位角色，不预设任何具体游戏角色；实际角色与丝袜款式以用户提供的参考图为准。

## 输出结构（固定 5 段）

`【正向提示词】` `【英文关键词】` `【负面词】` `【参数建议】` `【自检结论】`

不合规请求不会直接输出，而是改写成合规版本后再给。

## 目录

```
SKILL.md                        技能说明、六步工作流、提示词模板、固定输出结构、自检清单（入口）
README.md                       本文件
references/elements.md          9 组要素库：材质 / 丹尼尔 / 颜色 / 花纹 / 边缘 / 场景 / 光线 / 镜头 / 负面词
references/recipes.md           5 套可直接复制的配方（R01 PDF 原文逐字版 + 4 套扩展变体）
references/compliance.md        合规红线、10 项自检 rubric、不合规请求改写示例
examples/sample_output.txt      一份完整的 5 段输出示例（可作 few-shot）
scripts/check_frontmatter.py    frontmatter 格式校验（纯标准库）
scripts/check_prompt.py         输出提示词的合规与结构自检（纯标准库）
```

## 自检脚本

```bash
python scripts/check_frontmatter.py            # 打包/上传前：校验 SKILL.md frontmatter
python scripts/check_prompt.py my_prompt.txt   # 出图前：校验提示词结构与合规
```

两个脚本都只用标准库，输出逐项结果与结论；不替代人工判断，只用于快速兜底。

## 使用边界

- 仅用于合法合规的个人创作与学习；
- 主体必须是**成年女性**，服装完整，不生成色情、性暗示、未成年相关内容；
- 不做真人明星换脸、不冒充他人真实照片、不绕过平台审核；
- 不生成数字绘画 / 3D CG 动画风内容（与真人写实互斥）；
- 角色版权归原作者，本工坊配方仅作创作参考，禁止商用与二次分发。
