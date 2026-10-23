"""Optional visual QA: Inkscape (preferred), or PyMuPDF, plus Pillow."""
from pathlib import Path
import json
import shutil
import subprocess
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
out = root / 'build/figure-previews'
out.mkdir(parents=True, exist_ok=True)
paths = sorted((root / 'assets/images').glob('*.svg'))
previews = []
for path in paths:
    destination = out / (path.stem + '.png')
    if shutil.which('inkscape'):
        subprocess.run(['inkscape', str(path), '--export-type=png', '--export-filename=' + str(destination)], check=True, capture_output=True)
    else:
        import fitz
        with fitz.open(path) as doc:
            pix = doc[0].get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
        pix.save(destination)
    previews.append(destination)
for start in range(0, len(previews), 9):
    sheet = Image.new('RGB', (1500, 1080), '#e6eaf0')
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(previews[start:start+9]):
        im = Image.open(path).convert('RGB')
        im.thumbnail((488, 320))
        x, y = (index % 3) * 500, (index // 3) * 360
        sheet.paste(im, (x+(500-im.width)//2, y+28))
        draw.text((x+10,y+8), path.stem, fill='#17334d')
    sheet.save(out / f'sheet-{start//9+1:02}.png')
print(json.dumps({'rendered': len(previews), 'sheets': (len(previews)+8)//9}))
