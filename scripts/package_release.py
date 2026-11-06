#!/usr/bin/env python3
"""Create a reproducible ZIP containing one top-level skill directory."""
import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILL = 'instagram-transcript-extractor'
EXCLUDED_DIRS = {'__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.git'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True,
                        help='New ZIP path outside the repository')
    parser.add_argument('--skill', default=DEFAULT_SKILL,
                        help='Skill slug under skills/ (default: instagram-transcript-extractor)')
    args = parser.parse_args()
    if not args.skill or '/' in args.skill or args.skill in {'.', '..'}:
        parser.error('--skill must be a skill slug')
    skill = ROOT / 'skills' / args.skill
    required = ('SKILL.md', 'references/workflow.md', 'scripts/workflow.py',
                'agents/openai.yaml', f'assets/{args.skill}-icon.svg')
    prefix = args.skill + '/'
    output = args.output.resolve()
    if output == ROOT.resolve() or ROOT.resolve() in output.parents:
        parser.error('Output must be outside the repository')
    if output.exists():
        parser.error('Output already exists; choose a new path')
    for name in required:
        if not (skill / name).is_file():
            parser.error(f'Missing required skill file: {name}')
    if any(p.is_symlink() for p in skill.rglob('*')):
        parser.error('Skill source must not contain symbolic links')
    files = set()
    for p in skill.rglob('*'):
        rel = p.relative_to(skill)
        if (any(part in EXCLUDED_DIRS for part in rel.parts)
                or p.name == '.DS_Store' or p.suffix in ('.pyc', '.pyo')):
            continue
        if p.is_file():
            files.add(rel.as_posix())
    if files != set(required):
        parser.error('Skill file list differs from the release manifest; review it before packaging')
    entries = {prefix + name: (skill / name).read_bytes() for name in required}
    entries[prefix + 'LICENSE'] = (ROOT / 'LICENSE').read_bytes()
    with output.open('xb') as stream:
        with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, data in sorted(entries.items()):
                info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data, compresslevel=9)
    try:
        with zipfile.ZipFile(output, 'r') as archive:
            names = archive.namelist()
            if (len(names) != len(entries) or set(names) != set(entries)
                    or archive.testzip() is not None
                    or any(archive.read(name) != data for name, data in entries.items())):
                raise RuntimeError('release ZIP manifest or content verification failed')
    except Exception as exc:
        output.unlink(missing_ok=True)
        raise SystemExit(f'error: self-check failed; removed {output}: {exc}') from exc
    print(f'Created and verified {output} with {len(entries)} files')


if __name__ == '__main__':
    main()
