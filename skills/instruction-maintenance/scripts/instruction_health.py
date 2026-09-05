#!/usr/bin/env python3
"""Bounded, read-only instruction checks; state only when explicitly requested."""
import argparse,hashlib,json,os,re,sys,tempfile
from pathlib import Path

def atomic_write(path,data):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.NamedTemporaryFile('w',dir=path.parent,delete=False,encoding='utf-8') as f:
  f.write(json.dumps(data,ensure_ascii=False,indent=2)+'\n');name=f.name
 os.replace(name,path)

def check(manifest,home=None):
 home=Path(home or Path.home());issues=[];checked=0
 def issue(kind,path,detail):issues.append({'kind':kind,'path':str(path),'detail':detail})
 for spec in manifest.get('files',[]):
  p=home/spec['path'];checked+=1
  if not p.is_file():issue('missing',spec['path'],'Expected instruction file is missing');continue
  raw=p.read_bytes();text=raw.decode('utf-8')
  if spec.get('max_bytes') and len(raw)>spec['max_bytes']:issue('budget',spec['path'],f'{len(raw)} bytes > {spec["max_bytes"]}')
  for word in spec.get('forbid',[]):
   if word in text:issue('obsolete_rule',spec['path'],word)
  for word in spec.get('require',[]):
   if word not in text:issue('missing_invariant',spec['path'],word)
 for pair in manifest.get('mirrors',[]):
  a,b=home/pair['source'],home/pair['installed'];checked+=2
  if not a.is_file() or not b.is_file():issue('mirror_missing',pair['installed'],'Source or installed file is missing')
  elif hashlib.sha256(a.read_bytes()).digest()!=hashlib.sha256(b.read_bytes()).digest():issue('mirror_drift',pair['installed'],'Installed skill differs from source')
 for spec in manifest.get('provider_globs',[]):
  if not any(home.glob(spec)):issue('provider_missing',spec,'No retained plugin provider found; restore archived user skill or reconnect plugin before use')
 root=home/'.codex/skills';hashes={}
 if root.exists():
  for p in sorted(root.glob('*/SKILL.md')):
   if p.parent.name.startswith('.'):continue
   checked+=1;text=p.read_text();m=re.match(r'---\s*\n(.*?)\n---(?:\n|$)',text,re.S)
   if not m or not all(re.search(r'^'+k+r':\s*\S',m.group(1),re.M) for k in ['name','description']):issue('metadata',p.relative_to(home),'Missing name/description frontmatter')
   digest=hashlib.sha256(text.encode()).hexdigest()
   if digest in hashes:issue('duplicate_entry',p.relative_to(home),str(hashes[digest]))
   hashes[digest]=p.relative_to(home)
 issues.sort(key=lambda x:(x['kind'],x['path'],x['detail']))
 fingerprint=hashlib.sha256(json.dumps(issues,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
 return {'schema_version':1,'checked':checked,'issues':issues,'issue_count':len(issues),'fingerprint':fingerprint,'status':'pass' if not issues else 'action_required'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--home');p.add_argument('--state');p.add_argument('--report')
 a=p.parse_args();result=check(json.loads(Path(a.manifest).read_text()),a.home)
 previous=None
 if a.state and Path(a.state).exists():previous=json.loads(Path(a.state).read_text())
 result['changed']=previous is None or previous.get('fingerprint')!=result['fingerprint']
 result['notify']=result['changed'] and (bool(result['issues']) or bool(previous and previous.get('issue_count')))
 if a.state:atomic_write(a.state,{'fingerprint':result['fingerprint'],'issue_count':result['issue_count']})
 if a.report:atomic_write(a.report,result)
 print(json.dumps(result,ensure_ascii=False,indent=2));return 1 if result['issues'] else 0
if __name__=='__main__':sys.exit(main())
