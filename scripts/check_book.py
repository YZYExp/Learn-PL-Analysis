"""Validate the book manifest, local links, SVGs and chapter completeness."""
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

def check():
    book = json.loads((ROOT / 'book.json').read_text())
    errors, metrics = [], []
    ids, slugs = set(), set()
    for chapter in book['chapters']:
        path = ROOT / chapter['source']
        for key, seen in [('id', ids), ('slug', slugs)]:
            if chapter[key] in seen:
                errors.append(f'duplicate {key}: {chapter[key]}')
            seen.add(chapter[key])
        if not path.exists():
            errors.append(f'missing {path.relative_to(ROOT)}')
            continue
        text = path.read_text()
        han = len(re.findall(r'[\u4e00-\u9fff]', text))
        images = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text)
        sources = re.findall(r'https?://[^\s)\]>]+', text)
        if han < 1000:
            errors.append(f'{path.name}: too short ({han} Han characters)')
        if not images:
            errors.append(f'{path.name}: no teaching image')
        if not sources:
            errors.append(f'{path.name}: no source URL')
        if re.search(r'\bTODO\b|待补充|占位图', text):
            errors.append(f'{path.name}: unfinished marker')
        for url in re.findall(r'\]\(([^)]+)\)', text):
            if re.match(r'https?://|mailto:|#', url):
                continue
            target = (path.parent / url.split('#')[0]).resolve()
            if not target.exists():
                errors.append(f'{path.name}: broken local reference {url}')
        metrics.append({'id': chapter['id'], 'han': han, 'images': len(images), 'sources': len(set(sources))})
    for path in (ROOT / 'assets/images').glob('*.svg'):
        try:
            svg = ET.parse(path).getroot()
            if not (svg.get('viewBox') or (svg.get('width') and svg.get('height'))):
                errors.append(f'{path.name}: no SVG dimensions')
        except ET.ParseError as error:
            errors.append(f'{path.name}: invalid SVG: {error}')
    result = {'chapters': len(metrics), 'han': sum(m['han'] for m in metrics), 'images_in_chapters': sum(m['images'] for m in metrics), 'unique_svg_files': len(list((ROOT / 'assets/images').glob('*.svg'))), 'metrics': metrics, 'errors': errors}
    (ROOT / 'build').mkdir(exist_ok=True)
    (ROOT / 'build/checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'metrics'}, ensure_ascii=False, indent=2))
    return not errors

if __name__ == '__main__':
    raise SystemExit(0 if check() else 1)
