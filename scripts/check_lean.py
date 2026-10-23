"""Check the book's Lean files with the pinned toolchain; no Mathlib required."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--lean', default=shutil.which('lean'))
parser.add_argument('--linux-app-path-compat', action='store_true',
                    help='Optional adapter for runtimes exposing /proc/self/exe only')
args = parser.parse_args()
if not args.lean:
    raise SystemExit('Lean is not on PATH; pass --lean /path/to/lean (version 4.19.0).')
build = ROOT / 'build'
build.mkdir(exist_ok=True)
env = os.environ.copy()
if args.linux_app_path_compat:
    adapter = build / 'lean-app-path-compat.so'
    subprocess.run(['cc', '-shared', '-fPIC', str(ROOT / 'examples/lean/linux_app_path_compat.c'),
                    '-o', str(adapter), '-ldl'], check=True)
    env['LD_PRELOAD'] = str(adapter) + (':' + env['LD_PRELOAD'] if env.get('LD_PRELOAD') else '')
version = subprocess.run([args.lean, '--version'], env=env, text=True, capture_output=True, timeout=30)
if version.returncode or not re.search(r'version 4\.19\.0(?:,|\))', version.stdout):
    raise SystemExit('Pinned Lean 4.19.0 required. ' + version.stdout + version.stderr)
results = []
for name in ['Foundations.lean', 'ProgramProofs.lean']:
    path = ROOT / 'examples/lean' / name
    process = subprocess.run([args.lean, str(path.relative_to(ROOT))], cwd=ROOT,
                             env=env, capture_output=True, text=True, timeout=120)
    output = process.stdout + process.stderr
    passed = process.returncode == 0 and 'sorryAx' not in output
    results.append({'file': 'examples/lean/' + name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'exit_code': process.returncode,
                    'passed': passed, 'output': output})
result = {'toolchain': 'leanprover/lean4:v4.19.0', 'version_output': version.stdout.strip(),
          'mathlib_required': False, 'linux_app_path_compat_used': args.linux_app_path_compat,
          'compatibility_scope': 'current-process executable path discovery only; unmodified Lean kernel and libraries',
          'files': results, 'passed': all(r['passed'] for r in results)}
destination = ROOT / 'examples/lean/check-results.json'
destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if result['passed'] else 1)
