"""Attach a read-only tutorial observer to one explicitly selected Windows game PID."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

GAME_HASH = '03E20EECE23F39FB1012061A5A7FF92F4B63DA23EB8EB641CF6EE379CBCE373D'
GAME_NAME = "Them's Fightin' Herds.exe"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pid', type=int, required=True)
    args = parser.parse_args()
    if sys.platform != 'win32' or args.pid <= 0:
        raise ValueError('Use a positive PID on Windows')
    query = ("$ErrorActionPreference='Stop';"
             "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8;"
             f"$g=Get-Process -Id {args.pid};"
             "@{path=$g.Path}|ConvertTo-Json -Compress")
    result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', query],
                            check=True, capture_output=True, encoding='utf-8', timeout=15,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    path = Path(json.loads(result.stdout)['path'])
    if path.name != GAME_NAME:
        raise ValueError('PID is not the expected game executable')
    with path.open('rb') as handle:
        actual = hashlib.file_digest(handle, 'sha256').hexdigest().upper()
    if actual != GAME_HASH:
        raise ValueError('Unsupported executable; no attachment attempted')
    import frida  # optional dependency; --help does not require it
    source = (Path(__file__).parent / 'observe_training.js').read_text(encoding='utf-8')
    session = frida.attach(args.pid)
    script = None
    try:
        script = session.create_script(source)
        script.on('message', lambda message, data: print(json.dumps(message, ensure_ascii=False), flush=True))
        script.load()
        input('Observer loaded. Press Enter here to detach. No gameplay writes are performed.\n')
    finally:
        if script is not None:
            try:
                script.exports_sync.stop()
            except Exception:
                pass
        session.detach()


if __name__ == '__main__':
    main()
