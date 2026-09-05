import importlib.util,json,subprocess,tempfile,unittest
from pathlib import Path

def load(name):
 p=Path(__file__).parent/(name+'.py');spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
preflight=load('workflow_preflight');health=load('instruction_health')

class ToolsTests(unittest.TestCase):
 def git(self,root,*args):return subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True,text=True)
 def repo(self,root):
  self.git(root,'init','-q');self.git(root,'config','user.email','test@example.invalid');self.git(root,'config','user.name','Fixture')
  (root/'mine.md').write_text('initial');(root/'someone else.md').write_text('initial');self.git(root,'add','.');self.git(root,'commit','-qm','fixture')
 def test_dirty_scope_and_spaces(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);self.repo(p);(p/'someone else.md').write_text('changed')
   r=preflight.inspect(p,['mine.md']);self.assertEqual(r['overlaps'],[]);self.assertEqual((p/'someone else.md').read_text(),'changed')
   r=preflight.inspect(p,['someone else.md']);self.assertTrue(r['overlaps']);self.assertIn('selected_files_have_existing_changes',r['blockers'])
 def test_missing_required_and_escape(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);self.repo(p);(p/'mine.md').unlink();r=preflight.inspect(p,[],['mine.md','../outside']);self.assertIn('missing_required_file:mine.md',r['blockers']);self.assertIn('path_outside_repository',r['blockers'])
 def test_mirror_and_budget(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'source').write_text('new');(p/'installed').write_text('old');m={'files':[{'path':'source','max_bytes':1}],'mirrors':[{'source':'source','installed':'installed'}]}
   r=health.check(m,p);self.assertEqual({i['kind'] for i in r['issues']},{'budget','mirror_drift'});(p/'installed').write_text('new');m['files'][0]['max_bytes']=99;self.assertEqual(health.check(m,p)['status'],'pass')
 def test_unchanged_health_does_not_notify(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);manifest=p/'manifest.json';manifest.write_text(json.dumps({'files':[{'path':'absent'}]}));state=p/'state.json'
   cmd=['python3',str(Path(__file__).parent/'instruction_health.py'),'--manifest',str(manifest),'--home',d,'--state',str(state)]
   a=json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout);b=json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout)
   self.assertTrue(a['notify']);self.assertFalse(b['notify']);(p/'absent').write_text('ok');c=json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout);self.assertTrue(c['notify']);self.assertEqual(c['status'],'pass')
 def test_root_budget_guard(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'AGENTS.md').write_text('中'*12000);self.assertEqual(health.check({'files':[{'path':'AGENTS.md','max_bytes':32768}]},p)['issues'][0]['kind'],'budget')
if __name__=='__main__':unittest.main()
