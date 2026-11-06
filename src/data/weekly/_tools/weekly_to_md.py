#!/usr/bin/env python3
"""把週報純文字檔轉成網站用的 markdown。

用法（在專案根目錄執行）：
    python3 src/data/weekly/_tools/weekly_to_md.py 週報.txt

會在 src/data/weekly/ 產生 <系列>-<年>-w<週>.md，例如 museum-2026-w45.md。
同一期重複執行會覆蓋舊檔。
"""
import datetime
import json
import pathlib
import re
import sys

SERIES = [
    ("世界博物館週報", "museum", "世界博物館週報"),
    ("自然科學周報", "nature", "自然科學週報"),
    ("自然科學週報", "nature", "自然科學週報"),
    ("科學漫畫", "comic", "科學漫畫工作室"),
]

SEP = re.compile(r"^[━─═=\-]{6,}$")
CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩"
ITEM = re.compile(r"^\S{1,4}\s+(\d{1,3})\.\s+(.+)$")  # 🔬 1. 標題


def esc(s: str) -> str:
    s = s.replace("\\", "\\\\")
    s = re.sub(r"([*<>\[\]`])", r"\\\1", s)
    s = re.sub(r"^(\d+)([.)])", r"\1\\\2", s)
    s = re.sub(r"^([#>+\-])", r"\\\1", s)
    return s


def is_boundary(line: str) -> bool:
    return bool(
        SEP.match(line)
        or line.startswith(("▸", "【", "編輯｜"))
        or line[:1] in CIRCLED
        or re.match(r"^\d{2}｜", line)
        or ITEM.match(line)
        or line.startswith("📖")
    )


def convert(text: str):
    lines = [l.strip() for l in text.replace("﻿", "").splitlines()]
    lines = [l for l in lines if l]
    if len(lines) < 5:
        sys.exit("檔案太短，不像週報。")

    series_slug, series_name = "weekly", "週報"
    for key, slug, name in SERIES:
        if key in lines[0]:
            series_slug, series_name = slug, name
            break

    period = None
    m = re.search(r"(\d{4})\s*年\s*第\s*(\d+)\s*週\s*[｜|]\s*第\s*(\d+)\s*期", lines[1])
    if m:
        # 格式 A：世界博物館週報
        year, week, issue = int(m.group(1)), int(m.group(2)), int(m.group(3))

        date = None
        head_end = 1
        for idx in range(2, min(len(lines), 8)):
            d = re.search(r"編輯日期[：:]\s*(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日", lines[idx])
            if d:
                date = f"{int(d.group(1)):04d}-{int(d.group(2)):02d}-{int(d.group(3)):02d}"
                head_end = idx
                break
        if not date:
            sys.exit("找不到「編輯日期：2026年11月6日」這一行。")

        title = None
        title_idx = None
        for idx in range(head_end + 1, len(lines)):
            t = re.match(r"^【(.+)】$", lines[idx])
            if t:
                title, title_idx = t.group(1), idx
                break
        if not title:
            sys.exit("日期後面找不到【標題】這一行。")
    else:
        # 格式 B：自然科學週報（第一行「【自然科學週報 No.001】」，第二行為日期區間）
        n = re.search(r"No\.?\s*(\d+)", lines[0])
        r = re.search(
            r"(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日\s*[－\-–~～]\s*(?:(\d{4})\s*年\s*)?(\d{1,2})\s*月\s*(\d{1,2})\s*日",
            lines[1],
        )
        if not (n and r):
            sys.exit("第二行找不到「2026年第45週｜第003期」或「2026 年 10 月 26 日－11 月 1 日」這種格式。")
        issue = int(n.group(1))
        y1, m1, d1 = int(r.group(1)), int(r.group(2)), int(r.group(3))
        y2 = int(r.group(4)) if r.group(4) else (y1 + 1 if int(r.group(5)) < m1 else y1)
        m2, d2 = int(r.group(5)), int(r.group(6))
        end = datetime.date(y2, m2, d2)
        year, week = end.isocalendar()[0], end.isocalendar()[1]
        date = end.isoformat()
        period = f"{y1} 年 {m1} 月 {d1} 日－{m2} 月 {d2} 日"
        title = f"{m1}/{d1}－{m2}/{d2} 本週自然科學新發現"
        title_idx = 1

    body = lines[title_idx + 1 :]
    n = len(body)
    blocks = []  # (kind, text)

    def add(kind, text):
        blocks.append((kind, text))

    hr_done = False
    i = 0
    while i < n:
        line = body[i]

        if SEP.match(line):
            if i + 2 < n and SEP.match(body[i + 2]) and not SEP.match(body[i + 1]):
                add("h2", "## " + esc(body[i + 1]))
                i += 3
            elif i + 1 < n and re.match(r"^\S{1,3}【.+】$", body[i + 1]):
                add("h2", "## " + esc(body[i + 1]))  # 最後一段只有上分隔線
                i += 2
            else:
                i += 1
            continue

        m = re.match(r"^【(.+)】$", line)
        if m:
            add("h3", "### " + esc(m.group(1)))
            i += 1
            if i < n and not is_boundary(body[i]):
                add("p", "**" + esc(body[i]) + "**")
                i += 1
            continue

        m = re.match(r"^(\d{2})｜(.+)$", line)
        if m:
            add("h3", f"### {m.group(1)}｜{esc(m.group(2))}")
            i += 1
            if i < n and not is_boundary(body[i]) and re.match(r"^[^｜]{1,20}｜.+$", body[i]):
                add("p", "*" + esc(body[i]) + "*")
                i += 1
            add("p", f"IMG:{int(m.group(1))}")
            continue

        m = ITEM.match(line)
        if m:
            add("h3", f"### {line.split()[0]} {m.group(1)}\\. {esc(m.group(2))}")
            add("p", f"IMG:{m.group(1)}")
            i += 1
            continue

        if line.startswith("📖"):
            i += 1
            cont = []
            while i < n and not is_boundary(body[i]):
                cont.append(body[i])
                i += 1
            add("p", "**" + esc(line.replace("📖", "").strip()) + "**")
            if cont:
                cites = [re.sub(r"DOI[：:]\s*(\S+)", lambda mm: f"DOI：[{mm.group(1)}](https://doi.org/{mm.group(1)})", esc(c)) for c in cont]
                add("p", "  \n".join(cites))
            continue

        if line.startswith("▸"):
            head = line[1:].strip()
            i += 1
            cont = []
            while i < n and not is_boundary(body[i]):
                cont.append(body[i])
                i += 1
            text = "- **" + esc(head) + "**" + "".join("  \n  " + esc(c) for c in cont)
            add("li", text)
            continue

        if line[:1] in CIRCLED:
            add("h3", "### " + esc(line))
            i += 1
            continue

        if line.startswith("•"):
            add("li", "- " + esc(line[1:].strip()))
            i += 1
            continue

        if line.startswith("編輯｜") and not hr_done:
            add("hr", "---")
            hr_done = True

        add("p", esc(line))
        i += 1

    # 圖片：public/weekly/<系列>-<年>-w<週>/<篇號>.jpg（多張用 <篇號>-2.jpg）存在時，插在該篇標題下方
    img_dir = pathlib.Path("public/weekly") / f"{series_slug}-{year}-w{week:02d}"
    resolved = []
    for kind, text in blocks:
        if kind == "p" and text.startswith("IMG:"):
            num = text[4:]
            found = []
            if img_dir.is_dir():
                found = sorted(
                    list(img_dir.glob(f"{num}.*")) + list(img_dir.glob(f"{num}-*.*")),
                    key=lambda f: (int(f.stem.split('-')[0]), int(f.stem.split('-')[1]) if '-' in f.stem else 1),
                )
            if found:
                imgs = "\n\n".join(f"![第 {num} 篇的圖片 {k}](/weekly/{img_dir.name}/{f.name})" for k, f in enumerate(found, 1))
                resolved.append(("p", imgs + "\n\n*圖片來源：原始資料*"))
            continue
        resolved.append((kind, text))
    blocks = resolved

    parts = []
    prev = None
    for kind, text in blocks:
        if parts:
            parts.append("\n" if (kind == "li" and prev == "li") else "\n\n")
        parts.append(text)
        prev = kind
    body_md = "".join(parts)

    summary = next((b[1] for b in blocks if b[0] == "p" and not b[1].startswith(("**", "*"))), "")
    fm = {
        "series": series_slug,
        "seriesName": series_name,
        "year": year,
        "week": week,
        "issue": issue,
        "date": date,
        "title": title,
        "summary": summary.replace("\\", ""),
    }
    if period:
        fm["period"] = period
    front = "---\n" + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in fm.items()) + "---\n\n"
    return series_slug, year, week, front + body_md + "\n"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    out_dir = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path("src/data/weekly")
    if sys.argv[1] == "-":
        text = sys.stdin.read()
    else:
        text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    slug, year, week, md = convert(text)
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / f"{slug}-{year}-w{week:02d}.md"
    dst.write_text(md, encoding="utf-8")
    print("寫入", dst)


if __name__ == "__main__":
    main()
