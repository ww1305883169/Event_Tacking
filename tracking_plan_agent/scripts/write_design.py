# -*- coding: utf-8 -*-
"""把生成的埋点事件设计写回需求文档的【埋点事件设计】列。

用法：
    python write_design.py <需求文档.xlsx> --designs designs.json [--column 埋点事件设计] [--sheet Sheet1]

designs.json 格式：
    [
      {"row": 3, "text": "http://... 页面/组件 曝光和点击都要报\\n参数：\\n..."},
      {"row": 5, "text": "..."}
    ]
    row 是 Excel 实际行号（与 inspect_excel.py 输出一致）。

安全规则：
    1. 写回前自动备份为 <文件名>.bak-<时间戳>.xlsx
    2. 只写入目标列，不改动其他任何单元格
    3. 以 keep formulas 模式打开（不传 data_only），保留已有公式
    4. ⚠️ 若原文件含 WPS =DISPIMG() 嵌入图片，openpyxl 保存可能丢失嵌入图片数据。
       脚本检测到 DISPIMG 时会打印警告，写回后请在 WPS 中检查截图是否完好。
"""
import argparse
import json
import os
import shutil
import sys
import time

import openpyxl

DEFAULT_COLUMN = "埋点事件设计"
COLUMN_ALIASES = ["埋点事件设计", "事件设计", "埋点设计", "事件设计方案"]
MAX_HEADER_SCAN = 10


def find_target_column(ws):
    """在前 10 行中查找目标列（按别名模糊匹配），返回 (header_row, col_idx)。"""
    best = None
    for i, row in enumerate(ws.iter_rows(min_row=1, max_row=MAX_HEADER_SCAN, values_only=True), start=1):
        for j, cell in enumerate(row, start=1):
            if cell is None:
                continue
            text = str(cell)
            for alias in COLUMN_ALIASES:
                if alias in text:
                    # 更精确的别名优先（更长的别名覆盖更短的）
                    if best is None or len(alias) > best[2]:
                        best = (i, j, len(alias))
    return (best[0], best[1]) if best else (None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="需求文档 xlsx 路径")
    ap.add_argument("--designs", required=True, help="designs.json 文件路径")
    ap.add_argument("--column", default=DEFAULT_COLUMN, help=f"目标列名，默认 {DEFAULT_COLUMN}")
    ap.add_argument("--sheet", help="sheet 名称，默认活动 sheet")
    ap.add_argument("--no-backup", action="store_true", help="跳过备份（不建议）")
    args = ap.parse_args()

    with open(args.designs, "r", encoding="utf-8") as f:
        designs = json.load(f)
    if not isinstance(designs, list) or not designs:
        print("ERROR: designs.json 必须是非空数组", file=sys.stderr)
        sys.exit(1)
    for d in designs:
        if "row" not in d or "text" not in d:
            print(f"ERROR: 每条设计必须含 row 和 text 字段: {d}", file=sys.stderr)
            sys.exit(1)

    # 备份
    if not args.no_backup:
        ts = time.strftime("%Y%m%d%H%M%S")
        backup = f"{args.path}.bak-{ts}.xlsx"
        shutil.copy2(args.path, backup)
        print(f"已备份: {backup}")

    # 打开（保留公式，不带 data_only）
    wb = openpyxl.load_workbook(args.path)
    ws = wb[args.sheet] if args.sheet else wb.active

    header_row, col_idx = find_target_column(ws)
    if col_idx is None:
        print(
            f"ERROR: 前 {MAX_HEADER_SCAN} 行未找到目标列（匹配: {COLUMN_ALIASES}）。\n"
            f"请用 --column 指定确切列名，或人工确认表头。",
            file=sys.stderr,
        )
        sys.exit(2)
    header_text = str(ws.cell(row=header_row, column=col_idx).value)
    print(f"目标列: 第 {col_idx} 列「{header_text}」（表头在第 {header_row} 行）")

    # 检测 DISPIMG 风险
    dispimg_count = 0
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str) and "DISPIMG" in cell.value:
                dispimg_count += 1
    if dispimg_count:
        print(f"⚠️ 警告：文档含 {dispimg_count} 处 =DISPIMG() 公式。openpyxl 保存可能丢失 WPS 嵌入图片，"
              f"写回后请在 WPS 中检查截图；如有丢失，从备份恢复截图列并改用 TSV 手动粘贴。")

    # 写入
    written = 0
    for d in designs:
        r = int(d["row"])
        old = ws.cell(row=r, column=col_idx).value
        ws.cell(row=r, column=col_idx).value = d["text"]
        written += 1
        preview = str(d["text"]).replace("\n", "⏎")[:60]
        print(f"  行 {r}: 已写入（原值: {str(old)[:30] if old else '空'}）→ {preview}...")

    wb.save(args.path)
    print(f"完成：写入 {written} 条 → {args.path}")


if __name__ == "__main__":
    main()
