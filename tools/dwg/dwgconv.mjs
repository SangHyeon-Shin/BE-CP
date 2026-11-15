#!/usr/bin/env node
// DWG <-> DXF converter for AutoCAD files.
//
//   node tools/dwg/dwgconv.mjs dwg2dxf <in.dwg> [out.dxf]
//   node tools/dwg/dwgconv.mjs dxf2dwg <in.dxf> [out.dwg] [--version 2018|2013|2010|2007|2004|2000]
//   node tools/dwg/dwgconv.mjs info <file.dwg|file.dxf>
//
// Reading DWG uses LibreDWG (WebAssembly), with acad-ts as a fallback.
// Writing DWG uses acad-ts, then the written file is read back with LibreDWG
// and its entity counts are compared with the source, so a broken write is
// reported instead of handed over. Existing output files are never overwritten.
// Setup once: npm ci --ignore-scripts --prefix tools/dwg

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { DxfReader, DwgReader, DwgWriter, DxfWriter, ACadVersion } from '@node-projects/acad-ts';
import { LibreDwg } from '@mlightcad/libredwg-web';

const here = path.dirname(fileURLToPath(import.meta.url));
const WASM_DIR = path.join(here, 'node_modules/@mlightcad/libredwg-web/wasm/');
const VERSIONS = { 2018: 'AC1032', 2013: 'AC1027', 2010: 'AC1024', 2007: 'AC1021', 2004: 'AC1018', 2000: 'AC1015' };

const ab = (b) => b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength);
const fail = (msg) => { console.error(`오류: ${msg}`); process.exit(1); };

function outPath(input, given, ext) {
  const out = given ?? input.replace(/\.[^.]+$/, '') + ext;
  if (path.resolve(out) === path.resolve(input)) fail('입력 파일과 출력 파일이 같습니다.');
  if (fs.existsSync(out)) fail(`출력 파일이 이미 있습니다(덮어쓰지 않음): ${out}`);
  return out;
}

let libredwg;
async function lib() {
  libredwg ??= await LibreDwg.create(WASM_DIR);
  return libredwg;
}

function countEntities(doc) {
  const c = {};
  for (const e of doc.modelSpace.entities) {
    // DXF entity type (LINE, DIMENSION, ...). Class names are not stable across
    // readers: a rotated dimension can come back as an aligned one.
    const k = e.objectName ?? e.constructor.name;
    c[k] = (c[k] ?? 0) + 1;
  }
  return c;
}

function dxfBytes(doc) {
  let size = 16 * 1024 * 1024;
  for (;;) {
    const buf = new Uint8Array(size);
    try {
      new DxfWriter(buf, doc).write();
      let n = buf.length;
      while (n > 0 && buf[n - 1] === 0) n--;
      if (n < buf.length) return buf.subarray(0, n);
    } catch (e) {
      if (size >= 512 * 1024 * 1024) throw e;
    }
    size *= 2;
  }
}

async function dwg2dxf(input, given) {
  const out = outPath(input, given, '.dxf');
  const data = fs.readFileSync(input);
  let bytes = null, engine = 'LibreDWG';
  try {
    bytes = (await lib()).dwg_write_dxf(ab(data));
  } catch (e) {
    console.error(`LibreDWG 읽기 실패: ${e.message ?? e}`);
  }
  if (!bytes || bytes.length === 0) {
    engine = 'acad-ts';
    const doc = DwgReader.readFromStream(ab(data), () => {});
    bytes = dxfBytes(doc);
  }
  fs.writeFileSync(out, bytes);
  console.log(`DWG → DXF 완료 (${engine}): ${out} (${bytes.length.toLocaleString()} bytes)`);
}

async function dxf2dwg(input, given, versionArg) {
  const out = outPath(input, given, '.dwg');
  const ver = VERSIONS[versionArg ?? '2018'];
  if (!ver) fail(`지원 버전: ${Object.keys(VERSIONS).join(', ')}`);
  const warnings = [];
  const doc = DxfReader.readFromStream(new Uint8Array(ab(fs.readFileSync(input))), (s, e) => warnings.push(e.message));
  doc.header.version = ACadVersion[ver];
  const dwg = DwgWriter.writeToBuffer(doc);

  // Verify: read the written DWG back with the independent LibreDWG reader.
  const back = (await lib()).dwg_write_dxf(ab(Buffer.from(dwg)));
  if (!back || back.length === 0) fail('작성한 DWG를 LibreDWG로 다시 읽지 못했습니다. DWG를 저장하지 않았습니다.');
  const before = countEntities(doc);
  const after = countEntities(DxfReader.readFromStream(back, () => {}));
  const diff = Object.keys({ ...before, ...after }).filter((k) => (before[k] ?? 0) !== (after[k] ?? 0));
  if (diff.length) fail(`다시 읽은 엔티티 수가 다릅니다: ${diff.map((k) => `${k} ${before[k] ?? 0}→${after[k] ?? 0}`).join(', ')}. DWG를 저장하지 않았습니다.`);

  fs.writeFileSync(out, dwg);
  const total = Object.values(before).reduce((a, b) => a + b, 0);
  console.log(`DXF → DWG 완료 (AutoCAD ${versionArg ?? '2018'} 형식): ${out}`);
  console.log(`검증: LibreDWG로 다시 읽어 엔티티 ${total}개 일치`);
  if (warnings.length) console.log(`읽기 경고 ${warnings.length}건: ${warnings.slice(0, 5).join(' / ')}`);
  console.log('주의: AutoCAD에서 열어 최종 확인하세요.');
}

async function info(input) {
  const data = fs.readFileSync(input);
  const isDwg = input.toLowerCase().endsWith('.dwg');
  const doc = isDwg ? DwgReader.readFromStream(ab(data), () => {}) : DxfReader.readFromStream(new Uint8Array(ab(data)), () => {});
  const year = { AC1032: '2018~', AC1027: '2013~2017', AC1024: '2010~2012', AC1021: '2007~2009', AC1018: '2004~2006', AC1015: '2000~2002' };
  const code = ACadVersion[doc.header.version] ?? String(doc.header.version);
  console.log(`형식: ${isDwg ? 'DWG' : 'DXF'} ${code}${year[code] ? ` (AutoCAD ${year[code]})` : ''}`);
  console.log('모델 공간 엔티티:', countEntities(doc));
}

const [cmd, a, b, ...rest] = process.argv.slice(2);
const vIdx = process.argv.indexOf('--version');
const versionArg = vIdx > 0 ? process.argv[vIdx + 1] : undefined;
const positional = [a, b].filter((x) => x && !x.startsWith('--') && x !== versionArg);
if (!cmd || !positional[0]) {
  console.log('사용법:\n  node tools/dwg/dwgconv.mjs dwg2dxf <in.dwg> [out.dxf]\n  node tools/dwg/dwgconv.mjs dxf2dwg <in.dxf> [out.dwg] [--version 2018]\n  node tools/dwg/dwgconv.mjs info <file>');
  process.exit(cmd ? 1 : 0);
}
if (!fs.existsSync(positional[0])) fail(`파일이 없습니다: ${positional[0]}`);
if (cmd === 'dwg2dxf') await dwg2dxf(positional[0], positional[1]);
else if (cmd === 'dxf2dwg') await dxf2dwg(positional[0], positional[1], versionArg);
else if (cmd === 'info') await info(positional[0]);
else fail(`알 수 없는 명령: ${cmd}`);
