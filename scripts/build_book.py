"""Build a combined Markdown reader and a complete source archive; stdlib only."""
from pathlib import Path
import json
import re
import subprocess
import zipfile
from check_book import ROOT, check

if not check():
    raise SystemExit('Book validation failed')
book = json.loads((ROOT / 'book.json').read_text())
build = ROOT / 'build'
blocks = ['# ' + book['title'], book['description'], '![封面：程序结构、运行时与机器行为的视觉隐喻](../' + book['cover'] + ')\n\n封面为 AI 教学插画，正文精确关系以 SVG 图解为准。']
contents = ['## 目录', '以下链接可打开独立章节；也可继续向下通读。']
for part in range(1, 7):
    chapters = [c for c in book['chapters'] if c['part'] == part]
    contents += ['', '### 第 ' + str(part) + ' 篇 ' + chapters[0]['part_title'], '']
    contents += [f'- [{c["id"][2:]}　{c["title"]}](../{c["source"]})' for c in chapters]
blocks.append('\n'.join(contents))
for path in [ROOT / 'appendices/reading-guide.md'] + [ROOT / c['source'] for c in book['chapters']] + [ROOT / 'appendices/glossary.md']:
    text = path.read_text()
    def relink(match):
        prefix, url = match.groups()
        if re.match(r'https?://|mailto:|#', url):
            return match.group(0)
        base, sep, fragment = url.partition('#')
        local = (path.parent / base).resolve()
        if local.is_relative_to(ROOT):
            return prefix + '../' + str(local.relative_to(ROOT)) + (sep + fragment if sep else '') + ')'
        return match.group(0)
    blocks.append(re.sub(r'(\]\()([^)]+)\)', relink, text))
(build / '程序分析图解.md').write_text('\n\n---\n\n'.join(blocks) + '\n')
subprocess.run(['git', 'bundle', 'create', str(build / 'history.bundle'), '--all'], cwd=ROOT, check=True)
archive = build / '程序分析图解-完整工程.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=7) as z:
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in {'.git', '__pycache__'} for part in rel.parts):
            continue
        if rel.parts[0] == 'build' and path.name not in {'程序分析图解.md', 'checks.json', 'history.bundle'}:
            continue
        z.write(path, 'program-analysis-book/' + str(rel))
print(f'Archive: {archive}')
