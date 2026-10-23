"""Regenerate the source README and bibliography from the single book manifest."""
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
book = json.loads((root / 'book.json').read_text())
lines = ['# ' + book['title'], '', '![程序结构、运行时与机器行为的视觉隐喻](assets/images/cover.png)', '', book['description'], '', '从[导读](appendices/reading-guide.md)开始，按以下目录阅读。章节文件与链接保持稳定，阅读顺序由统一清单维护。', '']
for part in sorted({c['part'] for c in book['chapters']}):
    chapters = [c for c in book['chapters'] if c['part'] == part]
    lines += ['## 第 ' + str(part) + ' 篇 ' + chapters[0]['part_title'], '']
    lines += [f'- [{c["number"]:02}　{c["title"]}]({c["source"]})' for c in chapters]
    lines.append('')
lines += ['## 附录与复现', '', '- [术语速查](appendices/glossary.md)', '- [延伸领域地图](appendices/frontiers.md)', '- [资料索引](references/source-index.md)', '- [Rocq扩展版审校记录](references/review-rocq.md)', '- [前版审校记录（历史）](references/review-expanded.md)', '- [展示编号与稳定身份对照](references/chapter-map.md)', '- [教学分析器](examples/README.md)', '- [Lean 证明文件与检查说明](examples/lean/README.md)', '- [Rocq 证明文件与检查说明](examples/rocq/README.md)', '', '```bash', 'python3 scripts/check_book.py', 'python3 -m unittest discover -s examples -p "test*.py"', 'python3 scripts/build_book.py', '```', '', '构建与内容检查仅需 Python 3.10+ 标准库；可选图像预览使用 Pillow 与 Inkscape，或 Pillow 与 PyMuPDF。Lean 与 Rocq 文件各按所附说明使用固定版本检查，不是普通书稿构建的必装依赖。', '', '构建输出合并 Markdown 和完整工程包，资源保留相对路径。工程包内的 build/history.bundle 可用 `git clone build/history.bundle restored-book` 恢复完整已提交历史；直接阅读无需恢复 Git。', '', '本次交付为 Markdown、SVG/封面与可运行示例；网页和 PDF 可复用相同主稿另行发布。']
(root / 'README.md').write_text('\n'.join(lines) + '\n')
sources = {}
for chapter in book['chapters']:
    path = root / chapter['source']
    if not path.exists():
        continue
    for label, url in re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)', path.read_text()):
        item = sources.setdefault(url, {'label': label, 'chapters': set()})
        item['chapters'].add(chapter['number'])
rows = ['# 资料索引', '', '由正文就近引用汇总，章号对应本扩展版目录。支持范围和必要限制请回到原章阅读；锚点不同的入口分别保留。', '', '| 资料 | 引用章号 |', '|---|---|']
for url, item in sorted(sources.items()):
    rows.append('| [' + item['label'].replace('|', '／') + '](' + url + ') | ' + '、'.join(str(n) for n in sorted(item['chapters'])) + ' |')
(root / 'references/source-index.md').write_text('\n'.join(rows) + '\n')
print(f'Catalog: {len(book["chapters"])} chapters, {len(sources)} source entries')
