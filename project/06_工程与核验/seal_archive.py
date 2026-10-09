import os,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
files=[]
for p in sorted(ROOT.rglob('*')):
    rel=p.relative_to(ROOT)
    if not p.is_file() or 'cache' in rel.parts or '缓存' in rel.parts:continue
    if p.name in ('文件校验清单.json','归档校验结果.json','清理结果.json','清理进度.json'):continue
    files.append(dict(path=rel.as_posix(),bytes=p.stat().st_size,sha256=sha(p)))
output=ROOT/'06_工程与核验/文件校验清单.json';output.write_text(json.dumps(dict(version='v25-archive',files=files,total_bytes=sum(f['bytes'] for f in files)),ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(files=len(files),bytes=sum(f['bytes'] for f in files)),ensure_ascii=False))
