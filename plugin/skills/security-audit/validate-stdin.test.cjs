const test=require('node:test');
const assert=require('node:assert/strict');
const path=require('node:path');
const {spawnSync}=require('node:child_process');
const {validateBuffer,safeJSON,MAX_BYTES}=require('./validate-stdin.cjs');
const script=path.join(__dirname,'validate-stdin.cjs');
const check=(kind,text)=>validateBuffer(kind,Buffer.from(text));

test('stdin CLI validates both parent-owned record types without file input',()=>{
  for(const kind of ['findings','coverage']){
    const p=spawnSync(process.execPath,[script,kind],{input:'[]',encoding:'utf8',timeout:5000});
    assert.equal(p.status,0,p.stderr+p.stdout);assert.equal(JSON.parse(p.stdout).records,0);
  }
});
test('stdin rejects malformed JSON and wrong schema',()=>{
  assert.equal(check('findings','{').ok,false);
  assert.equal(check('findings','{}').ok,false);
  assert.equal(check('coverage','[{}]').ok,false);
});
test('stdin rejects invalid UTF-8',()=>assert.equal(validateBuffer('findings',Buffer.from([0xff])).ok,false));
test('stdin enforces byte limit in parser and live stream',()=>{
  const data=Buffer.alloc(MAX_BYTES+1,32);
  assert.equal(validateBuffer('findings',data).ok,false);
  const p=spawnSync(process.execPath,[script,'findings'],{input:data,encoding:'utf8',timeout:5000});
  assert.equal(p.status,1);assert.equal(JSON.parse(p.stdout).ok,false);
});
test('stdin preserves upstream nesting and array limits',()=>{
  assert.equal(check('findings','['.repeat(70)+']'.repeat(70)).ok,false);
  assert.equal(check('findings',JSON.stringify(Array(1001).fill(null))).ok,false);
});
test('stdin preserves rejected-record contract and rejects an invented severity',()=>{
  const f={verdict:'rejected',fingerprint:'candidate-a',title:'Rejected candidate',description:'The candidate is refuted by source.',claimed_root_cause:'A missing authorization check was suspected.',trace:[{kind:'sink',file:'src/a.js',line:1,scope:'handle',description:'The guard runs before the operation.'}],evidence:[{file:'src/a.js',line:1,description:'The authorization guard is present.'}],reason:'The guard prevents the claimed operation.'};
  assert.equal(check('findings',JSON.stringify([f])).ok,true);
  f.severity='high';assert.equal(check('findings',JSON.stringify([f])).ok,false);
});
test('stdin never accepts a file argument',()=>{
  const p=spawnSync(process.execPath,[script,'findings','untrusted.json'],{input:'[]',encoding:'utf8',timeout:5000});
  assert.equal(p.status,2);
});
test('stdin diagnostics escape terminal controls and bidi characters',()=>{
  const out=safeJSON({ok:false,errors:['bad\u001b\u202e\ud800\u{e0100}']});
  assert.ok(!out.includes('\u001b')&&!out.includes('\u202e'));
  assert.doesNotThrow(()=>JSON.parse(out));
});
