import io
from pathlib import Path
import struct
import unittest

from prepare_lesson import ANCHOR, MENU, SLOT, prepare
from read_gfs_index import read_index


def archive(entries):
    def string(text):
        data = text.encode()
        return struct.pack('>Q', len(data)) + data
    index = string('Reverge Package File') + string('1.1') + struct.pack('>Q', len(entries))
    for name, data in entries:
        index += string(name) + struct.pack('>QI', len(data), 16)
    chunks = [struct.pack('>I', 4 + len(index)) + index]
    offset = len(chunks[0])
    for _, data in entries:
        padding = (-offset) % 16
        chunks.extend((bytes(padding), data))
        offset += padding + len(data)
    return b''.join(chunks) + b'\0\0'


class Lesson(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).parent / 'lessons'
        self.fragment = (root / 'menu-entry.xml').read_text(encoding='utf-8')
        self.script = (root / 'hello.lua').read_bytes()
        self.original = archive([(MENU, ('<Root>' + ANCHOR + '</TrialGroup></Root>').encode()),
                                 (SLOT, b'-- synthetic original'), ('synthetic.txt', b'untouched')])

    def test_two_entries_and_alignment(self):
        candidate = prepare(self.original, self.fragment, self.script)
        entries = read_index(io.BytesIO(candidate), len(candidate))['entries']
        self.assertTrue(all(e['offset'] % 16 == 0 for e in entries))
        contents = {e['path']: candidate[e['offset']:e['offset'] + e['size']] for e in entries}
        self.assertEqual(contents[SLOT], self.script)
        self.assertEqual(contents['synthetic.txt'], b'untouched')
        self.assertIn(b'modAuthorHello', contents[MENU])
        self.assertTrue(candidate.endswith(b'\0\0'))

    def test_duplicate_lesson_refused(self):
        candidate = prepare(self.original, self.fragment, self.script)
        with self.assertRaises(ValueError):
            prepare(candidate, self.fragment, self.script)

    def test_wrong_script_route_refused(self):
        with self.assertRaises(ValueError):
            prepare(self.original, self.fragment.replace('input_testing.lua', 'unknown.lua'), self.script)

    def test_missing_anchor_refused(self):
        bad = self.original.replace(b'm6Basics', b'm7Basics')
        with self.assertRaises(ValueError):
            prepare(bad, self.fragment, self.script)

    def test_duplicate_paths_refused(self):
        with self.assertRaises(ValueError):
            prepare(archive([(MENU, b'<Root/>'), (MENU, b'<Root/>'), (SLOT, b'x')]), self.fragment, self.script)


if __name__ == '__main__':
    unittest.main()
