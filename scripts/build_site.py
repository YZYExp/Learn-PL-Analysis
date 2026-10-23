"""Build the static reading site from the canonical book manifest."""
from pathlib import Path
from urllib.parse import urlsplit, unquote, quote
from html import escape
from html.parser import HTMLParser
import argparse
import json
import re
import shutil
import markdown
from check_book import ROOT, check

parser = argparse.ArgumentParser()
parser.add_argument('--base-path', default='/')
args = parser.parse_args()
base = '/' + args.base_path.strip('/') + '/' if args.base_path.strip('/') else '/'
if not check():
    raise SystemExit('Book validation failed')
book = json.loads((ROOT / 'book.json').read_text())
out = ROOT / 'build/site'
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)
shutil.copytree(ROOT / 'assets', out / 'assets')
for name in ('style.css', 'app.js'):
    shutil.copyfile(ROOT / 'site' / name, out / name)
chapters = book['chapters']
extras = [{'source': f'appendices/{slug}.md', 'slug': slug, 'title': title} for slug, title in [('reading-guide', '阅读路线'), ('glossary', '术语表'), ('frontiers', '前沿与延伸')]]
pages = chapters + extras
routes = {str((ROOT / p['source']).resolve()): p['slug'] + '.html' for p in pages}
repo = 'https://github.com/YZYExp/Learn-PL-Analysis'
def href(p):
    return base + p['slug'] + '.html'
def shell(title, content, active='', toc=''):
    nav = ''.join(f'<a {"aria-current=page" if p["slug"] == active else ""} href="{href(p)}">{escape(p["title"])}</a>' for p in extras)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{escape(book['description'])}"><title>{escape(title)} · 程序分析图解</title><link rel="stylesheet" href="{base}style.css"><script src="{base}app.js" defer></script></head><body><header><a class="brand" href="{base}">PA / 程序分析图解</a><nav><a href="{base}#contents">全书目录</a>{nav}<a href="{repo}">GitHub ↗</a></nav></header>{content}<footer>程序分析图解 · 语言、运行时与机器行为<br>正文、图解与示例来自同一份书稿 · <a href="{repo}">查看源码与验证记录</a></footer></body></html>'''
def render(p):
    text = (ROOT / p['source']).read_text()
    def link(m):
        target = m.group(2)
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith('#'):
            return m.group(0)
        local = ((ROOT / p['source']).parent / unquote(parsed.path)).resolve()
        if not local.is_relative_to(ROOT) or not local.exists():
            raise ValueError(f'Invalid local link: {p["source"]}: {target}')
        route = routes.get(str(local))
        if route:
            dest = base + route
        elif local.is_relative_to(ROOT / 'assets'):
            dest = base + quote(str(local.relative_to(ROOT)))
        else:
            dest = repo + '/blob/main/' + quote(str(local.relative_to(ROOT)))
        return m.group(1) + dest + ('#' + parsed.fragment if parsed.fragment else '') + ')'
    text = re.sub(r'(\]\()([^)]+)\)', link, text)
    md = markdown.Markdown(extensions=['extra', 'toc', 'sane_lists'], extension_configs={'toc': {'permalink': '¶'}})
    html = md.convert(text)
    html = re.sub(r'<table>(.*?)</table>', r'<div class="table-scroll"><table>\1</table></div>', html, flags=re.S)
    html = html.replace('<img ', '<img loading="lazy" decoding="async" ')
    return html, md.toc
for i, p in enumerate(pages):
    body, toc = render(p)
    prev = chapters[i-1] if 0 < i < len(chapters) else None
    nxt = chapters[i+1] if i < len(chapters)-1 else None
    pager = '<div class="pager">' + (f'<a href="{href(prev)}">← 上一章<br>{escape(prev["title"])}</a>' if prev else '<span></span>') + (f'<a href="{href(nxt)}">下一章 →<br>{escape(nxt["title"])}</a>' if nxt else '<a href="' + base + '#contents">返回目录 →</a>') + '</div>'
    label = f'第 {p["part"]} 篇 · {p["part_title"]}' if 'part' in p else '阅读辅助'
    content = f'<div class="reader-layout"><main class="reader"><p class="eyebrow">{label}</p><article>{body}</article>{pager}</main><aside><details open><summary>本章目录</summary>{toc}</details><a href="{repo}/blob/main/{p["source"]}">查看 Markdown 原稿 ↗</a></aside></div>'
    (out / (p['slug'] + '.html')).write_text(shell(p['title'], content, p['slug']))
sections = []
for part in sorted({p['part'] for p in chapters}):
    group = [p for p in chapters if p['part'] == part]
    cards = ''.join(f'<a class="chapter-card" data-search="{escape(p["title"] + " " + p["part_title"])}" href="{href(p)}"><span>{p["number"]:02}</span><strong>{escape(p["title"])}</strong><b aria-hidden="true">↗</b></a>' for p in group)
    sections.append(f'<section class="part"><h3><small>PART {part:02}</small>{escape(group[0]["part_title"])}</h3><div class="chapter-grid">{cards}</div></section>')
cover = base + book['cover']
content = f'''<main class="home"><section class="hero"><div><p class="eyebrow">AN ILLUSTRATED GUIDE TO PROGRAM ANALYSIS</p><h1>从一行代码，<br>看懂程序的行为。</h1><p class="intro">{escape(book['description'])}</p><div class="actions"><a class="button" href="{href(chapters[0])}">开始阅读 →</a><a href="{base}reading-guide.html">选择阅读路线 ↗</a></div><div class="stats"><span><b>55</b> 章系统讲解</span><span><b>98</b> 张教学图解</span><span>Lean / Rocq 实作</span></div></div><figure><img src="{cover}" alt="程序结构、运行时与机器行为的视觉隐喻"><figcaption>AI 教学插画 · 精确关系请参阅正文图解</figcaption></figure></section><section class="orientation"><p class="eyebrow">全书主线</p><h2>理解行为，建立模型，检查证据。</h2><p>从语言与程序表示出发，逐步进入静态推理、动态观察、形式化证明与机器执行，最后连接真实工程和分析器构建。</p></section><section id="contents"><div class="contents-head"><div><p class="eyebrow">CONTENTS / 九篇 · 五十五章</p><h2>沿着问题，进入程序内部。</h2></div><label>查找章节<input id="chapter-search" type="search" placeholder="搜索：类型、GPU、Rocq…" aria-label="查找章节"></label></div><p id="search-status" aria-live="polite"></p>{''.join(sections)}</section><section class="resources"><h2>边读，边验证。</h2><p>教学分析器、Lean / Rocq 证明源码、工具版本和机器检查记录均随工程公开。</p><a href="{repo}/tree/main/examples">查看配套示例 →</a>　<a href="{repo}/archive/refs/heads/main.zip">下载源码 ZIP ↓</a></section></main>'''
(out / 'index.html').write_text(shell(book['title'], content))
(out / '.nojekyll').write_text('')
class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key not in ('href', 'src') or not value or not value.startswith(base):
                continue
            path = unquote(urlsplit(value).path[len(base):]) or 'index.html'
            if not (out / path).exists():
                raise ValueError(f'Broken website link: {value}')
for page in out.glob('*.html'):
    Links().feed(page.read_text())
print(f'Built and link-checked {len(pages)+1} pages at {out}')
