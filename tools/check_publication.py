"""Check publication allowlist, credential patterns and local Markdown links."""
import re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
secret=re.compile(r'gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
userpath=re.compile(r'[A-Za-z]:[\\/]+Users[\\/]',re.I)
allowed={'.md','.py','.json','.yml','.yaml'}
problems=[];files=[]
for path in root.rglob('*'):
    relative=path.relative_to(root)
    if any(p in ('.git','__pycache__') for p in relative.parts) or not path.is_file():continue
    files.append(path)
    if path.name not in ('.gitignore',) and path.suffix not in allowed:problems.append(('unexpected_file',str(relative)));continue
    text=path.read_text(encoding='utf-8')
    if secret.search(text) or userpath.search(text):problems.append(('sensitive_pattern',str(relative)))
    if path.suffix=='.md':
        for target in re.findall(r'\]\(([^)]+)\)',text):
            target=target.strip('<>').split('#',1)[0]
            if not target or re.match(r'[a-z][a-z0-9+.-]*:',target,re.I):continue
            if not (path.parent/target).resolve().is_relative_to(root) or not (path.parent/target).exists():problems.append(('broken_local_link',str(relative),target))
if problems:raise SystemExit(str(problems))
print('PASS publication allowlist / credential-pattern scan / local links:',len(files),'files')
print('Markdown characters:',sum(len(p.read_text(encoding='utf-8')) for p in files if p.suffix=='.md'))
