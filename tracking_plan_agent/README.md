# 埋点方案生成 Agent · 使用说明

产品在埋点需求文档（Excel）中填好需求 → agent 逐条生成符合规范的埋点事件设计 → 写回需求文档【埋点事件设计】列 → 确认后语料入库，形成闭环。

## 目录结构

```
tracking_plan_agent/
├── AGENT_DESIGN.md       # 设计方案 + 决策记录
├── conventions.md        # 埋点规范（工作副本，权威源是团队飞书文档）
├── corpus/               # 历史方案语料（一行一文件，含 yaml 结构化块）
├── agent/SKILL.md        # agent 工作流定义
├── agent/templates/      # 输出行模板
├── scripts/              # Excel 读写脚本
│   ├── inspect_excel.py  #   读取文档结构与内容
│   └── write_design.py   #   写回设计列（自动备份）
└── data/                 # 需求文档与全量埋点表存放处
```

## 使用方式

在 AI agent 工具（如 WorkBuddy）中按 `agent/SKILL.md` 定义的工作流对话：

1. 把填好需求的 Excel 文档放入 `data/`（或直接给路径）
2. 说"**处理这份埋点需求文档**"
3. Agent 会：解析文档 → 缺失信息批量向你澄清 → 生成设计 → 展示确认 → 写回 Excel
4. 你确认方案无误后说"**入库**"，agent 才把它沉淀到 `corpus/`

## 使用前准备（当前待补）

| 待办 | 说明 |
|---|---|
| 导出全量埋点表 | 放到 `data/all_events.xlsx`，用于查重与复用（R8） |
| 对齐飞书规范 | 把飞书文档内容与 `conventions.md` 对照，更新各规则的 ⏳ 状态 |
| 需求文档样例 | 提供一份真实需求文档确认列名（【埋点事件设计】列的准确叫法） |

## 已知风险

- **WPS 截图**：需求文档若含 `=DISPIMG()` 嵌入截图，脚本写回后嵌入图片可能丢失。脚本写回前会自动备份（`.bak-时间戳.xlsx`），写回后请在 WPS 中检查截图，丢失则从备份恢复并用 TSV 手动粘贴设计内容。
- **规范时效**：`conventions.md` 是从 1 条样本提炼的 v0.1，多项规则待与飞书文档对齐，生成结果请以飞书规范为准做最终校对。

## 环境

- Python 3.13 + `openpyxl`（脚本仅依赖 openpyxl）
