"""Superpowers portable resources and helper behavior in disposable workspaces."""
import hashlib
import json
import os
from pathlib import Path
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / 'skills/superpowers'
PROFILES = SUITE / 'upstream/skills'
NODE = os.environ.get('NODE_BINARY') or shutil.which('node')
git = shutil.which('git')
git_bash = Path(git).parent.parent / 'bin/bash.exe' if git else Path('missing-bash')
BASH = os.environ.get('BASH_BINARY') or (str(git_bash) if os.name == 'nt' and git_bash.is_file() else shutil.which('bash'))


class SuperpowersTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='superpowers-bundle-')
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)

    def run_tool(self, args, code=0, env=None):
        p = subprocess.run(list(map(str,args)), cwd=self.work, capture_output=True,
                           text=True, encoding='utf-8', timeout=30, env=env)
        self.assertEqual(p.returncode,code,p.stdout+p.stderr)
        return p.stdout

    def test_profile_inventory_provenance_and_local_links(self):
        index = json.loads((SUITE/'profiles.json').read_text(encoding='utf-8'))
        self.assertEqual(len(index['profiles']),15)
        self.assertEqual(len(list(SUITE.rglob('SKILL.md'))),1)
        for name,relative in index['profiles'].items():
            p=SUITE/relative
            self.assertEqual(p.parent.name,name)
            self.assertTrue(p.is_file())
        lock=json.loads((ROOT/'third-party-skills.lock.json').read_text(encoding='utf-8'))
        record=next(s for s in lock['skills'] if s['folder']=='superpowers')
        self.assertEqual(record['upstream_version'],'7.0.2')
        actual={p.relative_to(SUITE).as_posix() for p in SUITE.rglob('*') if p.is_file()}
        self.assertEqual(actual,set(record['sha256']))
        for name,digest in record['sha256'].items():
            self.assertEqual(hashlib.sha256((SUITE/name).read_bytes()).hexdigest(),digest)
        for p in [SUITE/'SKILL.md',SUITE/'references/compatibility.md',*[SUITE/r for r in index['profiles'].values()]]:
            for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
                if '://' not in target and not target.startswith('#'):
                    self.assertTrue((p.parent/target.split('#')[0]).is_file(),f'{p}: {target}')

    @unittest.skipUnless(BASH,'Bash required for find-polluter verification')
    def test_find_polluter_never_reports_clean_without_running_tests(self):
        script=str(PROFILES/'systematic-debugging/find-polluter.sh').replace('\\','/')
        # No matching tests: must not print the clean verdict.
        p=subprocess.run([BASH,script,'.pollution','tests/**/*.test.ts'],cwd=self.work,capture_output=True,text=True,encoding='utf-8',timeout=30)
        self.assertEqual(p.returncode,2,p.stdout+p.stderr)
        self.assertNotIn('No polluter found',p.stdout)
        # Pollution present before any test ran: no test can be blamed.
        (self.work/'tests').mkdir();(self.work/'tests/a.test.ts').write_text('',encoding='utf-8')
        (self.work/'.pollution').write_text('',encoding='utf-8')
        p=subprocess.run([BASH,script,'.pollution','tests/**/*.test.ts'],cwd=self.work,capture_output=True,text=True,encoding='utf-8',timeout=30)
        self.assertEqual(p.returncode,2,p.stdout+p.stderr)
        self.assertNotIn('No polluter found',p.stdout)

    @unittest.skipUnless(BASH and git,'Bash and Git required for optional plan helper verification')
    def test_plan_helpers_after_zip_style_copy(self):
        self.run_tool([git,'init','-q'])
        self.run_tool([git,'-c','user.name=Fixture','-c','user.email=fixture@example.invalid',
                       'commit','--allow-empty','-qm','fixture'])
        plan=self.work/'Kế hoạch có dấu.md'
        plan.write_text('# Plan\n\n### Task 1: Fix validation\nKeep brand.\n\n### Task 2: Review\nVerify focus.\n',encoding='utf-8')
        # read/write copy intentionally drops executable mode like many ZIP extractors.
        copied=self.work/'suite'
        for p in PROFILES.rglob('*'):
            if p.is_file():
                out=copied/p.relative_to(PROFILES);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(p.read_bytes())
        def bash(script,*args,code=0):
            return self.run_tool([BASH,str(copied/script).replace('\\','/'),*args],code)
        result=bash('executing-plans/scripts/task-start',plan.as_posix(),'1')
        self.assertIn('brief:',result)
        briefs=list(self.work.glob('.superpowers/sdd/**/task-1-brief.md'))
        self.assertEqual(len(briefs),1)
        self.assertIn('Keep brand.',briefs[0].read_text(encoding='utf-8'))
        self.assertNotIn('Task 2:',briefs[0].read_text(encoding='utf-8'))
        base=re.search(r'^base: ([0-9a-f]+)$',result,re.M).group(1)
        shell=str(BASH).replace('\\','/')
        bash('executing-plans/scripts/task-done',plan.as_posix(),'1',base,'--',shell,'-c','exit 7',code=7)
        ledger=briefs[0].parent/'progress.md'
        self.assertFalse(ledger.exists())
        bash('executing-plans/scripts/task-done',plan.as_posix(),'1',base,'--',shell,'-c','echo verified')
        self.assertIn('Task 1: complete',ledger.read_text(encoding='utf-8'))
        self.assertIn('verified',ledger.read_text(encoding='utf-8'))
        bash('subagent-driven-development/scripts/review-package',plan.as_posix(),base,base,code=3)
        (self.work/'change.txt').write_text('review fixture',encoding='utf-8')
        self.run_tool([git,'add','change.txt'])
        self.run_tool([git,'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','change'])
        bash('subagent-driven-development/scripts/review-package',plan.as_posix(),base,'HEAD')
        diffs=list(briefs[0].parent.glob('review-*.diff'))
        self.assertEqual(len(diffs),1)
        self.assertIn('+review fixture',diffs[0].read_text(encoding='utf-8'))
        bash('subagent-driven-development/scripts/task-brief',plan.as_posix(),'99',code=3)

    @unittest.skipUnless(NODE,'Node required for renderer prerequisite verification')
    def test_renderer_reads_guide_and_reports_missing_graphviz(self):
        # Deliberately hide Graphviz; this is a failure-path check, not SVG rendering.
        guide=self.work/'profile';guide.mkdir()
        (guide/'GUIDE.md').write_text('```dot\ndigraph example { a -> b; }\n```\n',encoding='utf-8')
        p=subprocess.run([NODE,str(PROFILES/'writing-skills/render-graphs.js'),str(guide)],
                         cwd=self.work,capture_output=True,text=True,encoding='utf-8',
                         env=dict(os.environ,PATH=str(self.work)),timeout=20)
        self.assertEqual(p.returncode,1,p.stdout+p.stderr)
        self.assertIn('graphviz (dot) not found',p.stderr)
        self.assertFalse((guide/'diagrams').exists())

    @unittest.skipUnless(NODE,'Node required for companion verification')
    def test_companion_auth_and_no_brand_telemetry(self):
        scripts=PROFILES/'brainstorming/scripts'
        state=self.work/'companion'
        env=dict(os.environ,BRAINSTORM_DIR=str(state),BRAINSTORM_PORT='0',
                 BRAINSTORM_HOST='127.0.0.1',BRAINSTORM_URL_HOST='127.0.0.1',BRAINSTORM_OPEN='0')
        p=subprocess.Popen([NODE,str(scripts/'server.cjs')],cwd=self.work,env=env,
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8')
        messages=queue.Queue()
        threading.Thread(target=lambda: [messages.put(line) for line in p.stdout],daemon=True).start()
        try:
            for _ in range(10):
                line=messages.get(timeout=15)
                try: info=json.loads(line)
                except json.JSONDecodeError: continue
                if info.get('url'): break
            else: self.fail('Companion did not report URL')
            url=info['url']
            with self.assertRaises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(url.split('?')[0],timeout=5)
            self.assertEqual(error.exception.code,403)
            with urllib.request.urlopen(url,timeout=5) as r:
                html=r.read().decode()
            self.assertNotIn('primeradiant.com/brand/',html)
            self.assertNotIn('<img src="https://',html)
        finally:
            p.terminate();p.wait(timeout=10)
            p.stdout.close();p.stderr.close()

    @unittest.skipUnless(NODE,'Node required for helper syntax verification')
    def test_javascript_syntax(self):
        for p in PROFILES.rglob('*'):
            if p.suffix in ('.js','.cjs','.mjs'):
                self.run_tool([NODE,'--check',p])


if __name__=='__main__':
    unittest.main()
