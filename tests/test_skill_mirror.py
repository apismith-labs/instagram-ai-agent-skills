"""Check the distributable skill and Codex project copy remain identical."""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills' / 'instagram-transcript-extractor'
MIRROR = ROOT / '.agents' / 'skills' / 'instagram-transcript-extractor'


class SkillMirrorTests(unittest.TestCase):
    def test_skill_files_match(self):
        def files(root):
            return {p.relative_to(root) for p in root.rglob('*')
                    if p.is_file() and '__pycache__' not in p.parts
                    and p.suffix not in {'.pyc', '.pyo'}}

        source_files = files(SOURCE)
        self.assertTrue(source_files, 'Skill source is empty or missing')
        self.assertEqual(source_files, files(MIRROR), 'Skill file lists differ')
        for path in sorted(source_files):
            with self.subTest(path=str(path)):
                self.assertEqual((SOURCE / path).read_bytes(), (MIRROR / path).read_bytes())
