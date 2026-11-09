#!/usr/bin/env node
// Trusted-parent JSON transport; never opens a target-controlled input path.
const {TextDecoder} = require('node:util');
const findings = require('./validate-findings.cjs');
const coverage = require('./validate-coverage-ledger.cjs');
const schema = require('./report-schema.json');
const MAX_BYTES = 5 * 1024 * 1024;
const INPUT_TIMEOUT_MS = 10000;

function validateBuffer(kind, bytes) {
  if (!['findings', 'coverage'].includes(kind)) return {ok:false, errors:['Expected findings or coverage mode']};
  if (bytes.length > MAX_BYTES) return {ok:false, errors:['Input exceeds 5 MiB limit']};
  let text, data;
  try { text = new TextDecoder('utf-8', {fatal:true, ignoreBOM:true}).decode(bytes); }
  catch { return {ok:false, errors:['Input is not valid UTF-8']}; }
  try {
    (kind === 'findings' ? findings.enforceJsonTextLimits : coverage.preflightJsonText)(text);
    data = JSON.parse(text);
  } catch { return {ok:false, errors:['Invalid JSON syntax or structural limit exceeded']}; }
  try {
    const errors = kind === 'findings' ? findings.validateDocument(data, schema) : coverage.validateDocument(data);
    return {ok:errors.length===0, kind, records:Array.isArray(data)?data.length:null, errors};
  } catch { return {ok:false, errors:['Validation could not complete']}; }
}

function safeJSON(result) {
  return JSON.stringify(result).replace(/[\p{Cc}\p{Cf}\p{Cs}\p{Zl}\p{Zp}\p{Default_Ignorable_Code_Point}]/gu,
    char => char.split('').map(unit => `\\u${unit.charCodeAt(0).toString(16).padStart(4,'0')}`).join(''));
}

function main(args) {
  if (args.length !== 1 || !['findings','coverage'].includes(args[0])) {
    process.stdout.write(safeJSON({ok:false, errors:['Usage: node validate-stdin.cjs findings|coverage; JSON on stdin only']})+'\n');
    process.exitCode=2; return;
  }
  let size=0, done=false;
  const chunks=[];
  const finish=result=>{
    if(done)return;
    done=true;clearTimeout(timer);
    process.stdout.write(safeJSON(result)+'\n');
    process.exitCode=result.ok?0:1;
    process.stdin.destroy();
  };
  const timer=setTimeout(()=>finish({ok:false,errors:['Input timed out after 10 seconds']}),INPUT_TIMEOUT_MS);
  process.stdin.on('data',chunk=>{
    if(done)return;
    size+=chunk.length;
    if(size>MAX_BYTES) return finish({ok:false,errors:['Input exceeds 5 MiB limit']});
    chunks.push(chunk);
  });
  process.stdin.on('end',()=>finish(validateBuffer(args[0],Buffer.concat(chunks))));
  process.stdin.on('error',()=>finish({ok:false,errors:['Input stream failed']}));
}

module.exports={validateBuffer,safeJSON,MAX_BYTES};
if(require.main===module)main(process.argv.slice(2));
