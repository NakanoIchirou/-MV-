import os,sys,json,hashlib
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent.parent
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as fp:
        for b in iter(lambda:fp.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def main():
    inventory=json.loads((ROOT/'06_工程与核验/文件校验清单.json').read_text(encoding='utf-8'))
    for f in inventory['files']:
        p=ROOT/f['path'];assert p.is_file(),str(p);assert p.stat().st_size==f['bytes'] and sha(p)==f['sha256'],str(p)
    engine=json.loads((ROOT/'06_工程与核验/工程.json').read_text(encoding='utf-8'))
    for j in engine['jobs']:
        assert (ROOT/j['file']).is_file()
        for slot in j.get('slots',[]):assert (ROOT/slot['file']).is_file() and sha(ROOT/slot['file'])==slot['source_sha256']
    assert len(engine['jobs'])==28 and sum(j['frames'] for j in engine['jobs'])==6532
    assert (ROOT/engine['audio']).is_file() and (ROOT/engine['output']).is_file()
    page=ROOT/'03_审片/硅晶之梦-逐M审片.html';refs=[]
    class Parser(HTMLParser):
        def handle_starttag(self,tag,attrs):
            a=dict(attrs)
            for key in ('src','href'):
                if key in a:
                    assert not a[key].startswith(('file:','D:','C:','http:','https:')),a[key]
                    p=(page.parent/a[key]).resolve();assert p.is_relative_to(ROOT) and p.is_file(),str(p);refs.append(str(p))
    Parser().feed(page.read_text(encoding='utf-8'))
    print(f'归档校验通过：{len(inventory["files"])}个文件，{len(refs)}个审片资源引用；28段时间轴完整。',flush=True)
if __name__=='__main__':main()
