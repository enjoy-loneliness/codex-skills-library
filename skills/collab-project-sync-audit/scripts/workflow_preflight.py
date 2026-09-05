#!/usr/bin/env python3
"""Read-only repository preflight. Never stash, reset, install, fetch or deploy."""
import argparse,json,re,subprocess,sys
from pathlib import Path

def run(repo,*args):
 p=subprocess.run(['git','--no-optional-locks','-C',str(repo),*args],text=True,capture_output=True,timeout=15)
 return p.returncode,p.stdout.rstrip('\n'),p.stderr.strip()

def inspect(repo,files=(),required=()):
 repo=Path(repo).expanduser().resolve();code,root,_=run(repo,'rev-parse','--show-toplevel')
 if code:return {'repo':str(repo),'blockers':['not_a_git_repository'],'safe_to_edit_selected_files':False}
 repo=Path(root);_,head,_=run(repo,'rev-parse','HEAD');_,branch,_=run(repo,'branch','--show-current')
 _,raw,_=run(repo,'status','--porcelain=v1','-z','--untracked-files=all')
 # Parse porcelain -z without losing spaces or rename source fields.
 dirty=[];items=raw.split('\0');i=0
 while i<len(items):
  item=items[i];i+=1
  if len(item)<4:continue
  state=item[:2];path=item[3:];dirty.append({'status':state,'path':path})
  if 'R' in state or 'C' in state:
   if i<len(items) and items[i]:dirty.append({'status':state,'path':items[i]})
   i+=1
 blockers=[];selected=[]
 for value in [*files,*required]:
  p=(repo/value).resolve()
  try:p.relative_to(repo)
  except ValueError:blockers.append('path_outside_repository');continue
  if value in files:selected.append(p.relative_to(repo).as_posix())
  if value in required and not p.exists():blockers.append('missing_required_file:'+value)
 overlaps=[d for d in dirty if any(d['path']==f or d['path'].startswith(f.rstrip('/')+'/') for f in selected)]
 if overlaps:blockers.append('selected_files_have_existing_changes')
 staged=[d for d in dirty if d['status'][0] not in [' ','?']]
 if staged:blockers.append('existing_index_changes')
 _,upstream,_=run(repo,'rev-parse','--abbrev-ref','@{upstream}')
 divergence=None
 if upstream:
  rc,counts,_=run(repo,'rev-list','--left-right','--count','HEAD...'+upstream)
  if rc==0:
   a,b=map(int,counts.split());divergence={'ahead':a,'behind':b,'remote_fetched':False}
   if a and b:blockers.append('known_non_fast_forward_divergence')
 else:blockers.append('upstream_not_configured')
 runtime={}
 p=repo/'package.json'
 if p.exists():
  data=json.loads(p.read_text());runtime['node_engines']=data.get('engines',{});deps={**data.get('dependencies',{}),**data.get('devDependencies',{})}
  runtime['ui_stack']={k:deps[k] for k in ['vue','react','react-native','nuxt','next'] if k in deps}
 p=repo/'pyproject.toml'
 if p.exists():
  m=re.search(r'requires-python\s*=\s*["\']([^"\']+)',p.read_text());runtime['requires_python']=m.group(1) if m else None
 docker=[]
 for p in repo.glob('Dockerfile*'):
  if p.is_file():docker+=re.findall(r'^FROM\s+python:([^\s]+)',p.read_text(),re.M|re.I)
 if docker:runtime['docker_python']=docker
 local=repo/'.venv/bin/python'
 if local.exists():
  p=subprocess.run([str(local),'--version'],text=True,capture_output=True,timeout=10);runtime['venv_python']=(p.stdout+p.stderr).strip()
  actual=re.search(r'Python (\d+\.\d+)',runtime['venv_python'])
  expected=re.search(r'^(\d+\.\d+)',docker[0]) if docker else None
  if actual and expected and actual.group(1)!=expected.group(1):blockers.append('venv_does_not_match_docker_python')
 return {'repo':str(repo),'head':head,'branch':branch,'upstream':upstream,'divergence':divergence,'runtime':runtime,'dirty':dirty,'overlaps':overlaps,'blockers':blockers,'safe_to_edit_selected_files':bool(selected) and not blockers,'mode':'read_only','notes':['Remote state is cached; git pull --ff-only is still required before editing.','No production, credentials or raw conversation data are read.']}

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--file',action='append',default=[]);p.add_argument('--required',action='append',default=[]);p.add_argument('--report')
 a=p.parse_args();result=inspect(a.repo,a.file,a.required);text=json.dumps(result,ensure_ascii=False,indent=2)
 if a.report:Path(a.report).write_text(text+'\n')
 print(text);return 1 if result['blockers'] else 0
if __name__=='__main__':sys.exit(main())
