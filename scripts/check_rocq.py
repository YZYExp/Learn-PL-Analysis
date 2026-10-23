"""Compile the book's three Rocq models with pinned Rocq 9.0.0 and Stdlib.

Compilation, Print Assumptions and independent rocq check rechecks are required.
This does not build or certify CompCert or VST.
"""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PINNED_VERSION = '9.0.0'
FILES = (
    ('Foundations.v', 5),
    ('CompilerModel.v', 5),
    ('HeapModel.v', 6),
)
CLOSED_MESSAGE = 'Closed under the global context'
ERROR_PATTERN = re.compile(
    r'(^|\n)\s*(?:Error|Anomaly|Fatal error)\s*(?::|\b)', re.IGNORECASE
)
AXIOM_PATTERN = re.compile(r'\bAxioms?\s*:', re.IGNORECASE)


def text(value):
    """TimeoutExpired may carry bytes even when text=True was requested."""
    if value is None:
        return ''
    return value.decode('utf-8', errors='replace') if isinstance(value, bytes) else value


def run(command, timeout):
    try:
        process = subprocess.run(
            command, cwd=ROOT, text=True, capture_output=True, timeout=timeout
        )
        stdout, stderr = process.stdout, process.stderr
        return {
            'command': command,
            'exit_code': process.returncode,
            'timed_out': False,
            'stdout': stdout,
            'stderr': stderr,
            'output': stdout + ('\n' if stdout and stderr else '') + stderr,
        }
    except subprocess.TimeoutExpired as error:
        stdout, stderr = text(error.stdout), text(error.stderr)
        return {
            'command': command,
            'exit_code': None,
            'timed_out': True,
            'stdout': stdout,
            'stderr': stderr,
            'output': stdout + ('\n' if stdout and stderr else '') + stderr,
            'error': f'Timeout after {timeout} seconds.',
        }
    except OSError as error:
        return {
            'command': command,
            'exit_code': None,
            'timed_out': False,
            'stdout': '',
            'stderr': str(error),
            'output': str(error),
            'error': 'Could not launch the requested Rocq executable.',
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--rocq', default=shutil.which('rocq'),
        help='Path to the Rocq 9.0.0 executable (the unified rocq command).'
    )
    parser.add_argument('--package-inventory', type=Path,
                        help='Optional inventory from this execution environment; see installation.json.')
    args = parser.parse_args()
    if not args.rocq:
        parser.error('Rocq is not on PATH; pass --rocq /path/to/rocq (version 9.0.0).')
    executable = shutil.which(args.rocq) or str(Path(args.rocq).expanduser().resolve())
    version = run([executable, '--version'], timeout=30)
    version_ok = (
        version['exit_code'] == 0
        and not version['timed_out']
        and re.search(r'\bversion\s+9\.0\.0(?=[\s,()]|$)',
                      version['output'], flags=re.IGNORECASE) is not None
    )
    result = {
        'toolchain': 'rocq-core/rocq-runtime/rocq-stdlib:9.0.0',
        'required_package_versions': {
            'rocq-core': '9.0.0',
            'rocq-runtime': '9.0.0',
            'rocq-stdlib': '9.0.0',
        },
        'package_installation_evidence': None,
        'package_version_note': (
            'The CLI version is checked below. Exact package installation inventory '
            'is separate evidence; package versions are not inferred from source text.'
        ),
        'required_version': PINNED_VERSION,
        'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'check_scope': 'compilation_Print_Assumptions_and_independent_rocq_check',
        'stdlib_only': True,
        'third_party_projects_built': [],
        'version_check': {**version, 'passed': version_ok},
        'version_output': version['output'].strip(),
        'staging_directory': 'build/rocq-check',
        'logical_prefix': 'BookRocq',
        'independent_kernel_recheck': {
            'performed': False,
            'files_checked': 0,
            'passed': False,
            'reason': 'Pending compilation and checker execution.',
        },
        'files': [],
        'passed': False,
    }
    if args.package_inventory:
        inventory_path = args.package_inventory.resolve()
        inventory_data = inventory_path.read_bytes()
        inventory = json.loads(inventory_data)
        matches = all(inventory.get('packages', {}).get(name) == expected
                      for name, expected in result['required_package_versions'].items())
        if not matches:
            raise SystemExit('Package inventory does not match pinned Rocq packages.')
        result['package_installation_evidence'] = {
            'file': str(inventory_path.relative_to(ROOT)),
            'sha256': hashlib.sha256(inventory_data).hexdigest(),
            'required_versions_matched': True,
        }
    destination = ROOT / 'examples/rocq/check-results.json'
    if version_ok:
        staging = ROOT / result['staging_directory']
        # Only this task-owned staging tree is reset; source .v files stay intact.
        if staging.exists():
            shutil.rmtree(staging)
        staging.mkdir(parents=True)
        for name, expected_count in FILES:
            source = ROOT / 'examples/rocq' / name
            staged = staging / name
            try:
                data = source.read_bytes()
                staged.write_bytes(data)
            except OSError as error:
                result['files'].append({
                    'file': 'examples/rocq/' + name,
                    'sha256': None,
                    'command': [],
                    'exit_code': None,
                    'output': str(error),
                    'expected_closed_count': expected_count,
                    'observed_closed_count': 0,
                    'passed': False,
                    'error': 'Unable to stage the source file.',
                })
                print(f'{name}: FAIL (unable to stage source)')
                continue
            command = [executable, 'compile', '-q', '-Q', str(staging),
                       'BookRocq', str(staged)]
            process = run(command, timeout=300)
            output = process['output']
            count = output.count(CLOSED_MESSAGE)
            has_axioms = AXIOM_PATTERN.search(output) is not None
            has_errors = ERROR_PATTERN.search(output) is not None
            artifact = staged.with_suffix('.vo')
            artifact_exists = artifact.is_file() and artifact.stat().st_size > 0
            compile_passed = (
                process['exit_code'] == 0
                and not process['timed_out']
                and count == expected_count
                and not has_axioms
                and not has_errors
                and artifact_exists
            )
            checker_command = [executable, 'check', '-silent', '-Q',
                               str(staging), 'BookRocq', 'BookRocq.' + staged.stem]
            if compile_passed:
                checker = run(checker_command, timeout=300)
                checker['performed'] = True
                checker['passed'] = (
                    checker['exit_code'] == 0
                    and not checker['timed_out']
                    and ERROR_PATTERN.search(checker['output']) is None
                    and AXIOM_PATTERN.search(checker['output']) is None
                )
            else:
                checker = {
                    'performed': False,
                    'command': checker_command,
                    'exit_code': None,
                    'output': '',
                    'passed': False,
                    'reason': 'Compilation or assumption-output checks did not pass.',
                }
            passed = compile_passed and checker['passed']
            result['files'].append({
                'file': 'examples/rocq/' + name,
                'sha256': hashlib.sha256(data).hexdigest(),
                'staged_file': str(staged.relative_to(ROOT)),
                **process,
                'expected_closed_count': expected_count,
                'observed_closed_count': count,
                'axioms_reported': has_axioms,
                'error_diagnostic_detected': has_errors,
                'compiled_artifact_exists': artifact_exists,
                'compile_passed': compile_passed,
                'kernel_recheck': checker,
                'passed': passed,
            })
            status = 'PASS' if passed else 'FAIL'
            checker_status = 'PASS' if checker['passed'] else ('FAIL' if checker['performed'] else 'SKIP')
            print(f'{name}: {status} ({count}/{expected_count} closed; kernel recheck {checker_status})')
        rechecks = [item.get('kernel_recheck', {}) for item in result['files']]
        checked_count = sum(bool(item.get('performed')) for item in rechecks)
        result['independent_kernel_recheck'] = {
            'performed': checked_count > 0,
            'files_checked': checked_count,
            'passed': (
                checked_count == len(FILES)
                and all(item.get('passed', False) for item in rechecks)
            ),
            'scope': 'rocq check on all three staged BookRocq modules; no -admit/-norec flags',
        }
        result['passed'] = (
            len(result['files']) == len(FILES)
            and all(item['passed'] for item in result['files'])
        )
    else:
        result['error'] = 'Pinned Rocq 9.0.0 is required; compilation was not attempted.'
        print('Rocq version check: FAIL (requires 9.0.0; see check-results.json)')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'Report: {destination.relative_to(ROOT)}')
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
