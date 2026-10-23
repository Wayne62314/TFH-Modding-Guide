"""Prepare a local GFS candidate; never install it or overwrite an existing output.

Uses only game data supplied by the caller. Not a general GFS editor.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import struct
import xml.etree.ElementTree as ET

from read_gfs_index import read_index

MENU = 'Trials/01 basic.xml'
SLOT = 'Trials/training/input_testing.lua'
ANCHOR = '<TrialGroup id="m6Basics" title="Basic" tag = "Tutorial">'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def prepare(original, fragment, script):
    index = read_index(io.BytesIO(original), len(original))
    entries = index['entries']
    names = [e['path'] for e in entries]
    if any(e['alignment'] > 1048576 for e in entries):
        raise ValueError('Alignment exceeds teaching-tool limit')
    if len(set(names)) != len(names):
        raise ValueError('Duplicate archive paths')
    if MENU not in names or SLOT not in names:
        raise ValueError('Required existing menu/script entries missing')
    if not script.strip() or b'\x00' in script:
        raise ValueError('Expected nonempty Lua text')
    script.decode('utf-8')
    menu_entry = next(e for e in entries if e['path'] == MENU)
    xml = original[menu_entry['offset']:menu_entry['offset'] + menu_entry['size']].decode('utf-8')
    old_tree, new_trial = ET.fromstring(xml), ET.fromstring(fragment)
    if new_trial.tag != 'Trial' or not new_trial.get('id'):
        raise ValueError('Expected one named Trial element')
    if any(e.get('id') == new_trial.get('id') for e in old_tree.iter()):
        raise ValueError('Trial id already exists')
    if any(new_trial.get(k) != 'trials/training/input_testing.lua' for k in ('tutorial', 'file')):
        raise ValueError('This sample only supports the existing input_testing slot')
    if xml.count(ANCHOR) != 1:
        raise ValueError('Expected unique known group anchor')
    changed_xml = xml.replace(ANCHOR, ANCHOR + '\n' + fragment, 1)
    ET.fromstring(changed_xml)
    replacements = {MENU: changed_xml.encode('utf-8'), SLOT: script}
    header = bytearray(original[:index['data_offset']])
    # Locate size fields without rebuilding names or changing index order.
    cursor = 4
    def skip_string():
        nonlocal cursor
        length = struct.unpack_from('>Q', header, cursor)[0]
        cursor += 8 + length
    skip_string()
    skip_string()
    cursor += 8  # entry count
    chunks = [header]
    offset = len(header)
    for entry in entries:
        skip_string()
        data = replacements.get(entry['path'], original[entry['offset']:entry['offset'] + entry['size']])
        struct.pack_into('>Q', header, cursor, len(data))
        cursor += 12  # size u64 + alignment u32
        padding = (-offset) % entry['alignment']
        chunks.extend((bytes(padding), data))
        offset += padding + len(data)
    old_end = max((e['offset'] + e['size'] for e in entries), default=index['data_offset'])
    chunks.append(original[old_end:])  # retain trailing bytes
    candidate = b''.join(chunks)
    checked = read_index(io.BytesIO(candidate), len(candidate))
    if len(checked['entries']) != len(entries):
        raise ValueError('Entry count changed')
    for before, after in zip(entries, checked['entries']):
        expected = replacements.get(before['path'], original[before['offset']:before['offset'] + before['size']])
        actual = candidate[after['offset']:after['offset'] + after['size']]
        if before['path'] != after['path'] or before['alignment'] != after['alignment'] or expected != actual:
            raise ValueError('Round-trip mismatch')
    return candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--expected-sha256', required=True)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    original = args.archive.read_bytes()
    if digest(original) != args.expected_sha256.lower():
        raise ValueError('Source hash mismatch; nothing written')
    root = Path(__file__).resolve().parent / 'lessons'
    candidate = prepare(original, (root / 'menu-entry.xml').read_text(encoding='utf-8'),
                        (root / 'hello.lua').read_bytes())
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'trials.gfs.original').write_bytes(original)
    (args.output / 'trials.gfs.candidate').write_bytes(candidate)
    manifest = {'original_sha256': digest(original), 'candidate_sha256': digest(candidate),
                'changed_entries': [MENU, SLOT], 'installed': False,
                'status': 'prepared only; requires in-game validation'}
    (args.output / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
