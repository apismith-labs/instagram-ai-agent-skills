"""Check the distributable skill and Codex project copy remain identical."""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
class SkillMirrorTests(unittest.TestCase):
    def test_skill_files_match(self):
        def files(root):
            return {p.relative_to(root) for p in root.rglob('*')
                    if p.is_file() and '__pycache__' not in p.parts
                    and p.suffix not in {'.pyc', '.pyo'}}

        source_root = ROOT / 'skills'
        mirror_root = ROOT / '.agents' / 'skills'
        source_slugs = {p.name for p in source_root.iterdir() if (p / 'SKILL.md').is_file()}
        mirror_slugs = {p.name for p in mirror_root.iterdir() if (p / 'SKILL.md').is_file()}
        self.assertEqual(source_slugs, mirror_slugs, 'Every canonical skill needs exactly one Codex mirror')
        for slug in sorted(source_slugs):
            source = ROOT / 'skills' / slug
            mirror = ROOT / '.agents' / 'skills' / slug
            source_files = files(source)
            self.assertTrue(source_files, f'{slug}: Skill source is empty or missing')
            self.assertEqual(source_files, files(mirror), f'{slug}: Skill file lists differ')
            for path in sorted(source_files):
                with self.subTest(skill=slug, path=str(path)):
                    self.assertEqual((source / path).read_bytes(), (mirror / path).read_bytes())
