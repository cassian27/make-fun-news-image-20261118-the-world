// THE WORLD — 18 November 2026 front page (make.fun news-image-20261118).
//
// The entry image is entry.png beside this file, drawn at build time by
// render.py (Pillow + Liberation fonts, deterministic). This program runs
// offline with Node 22 stdlib only: it validates the PNG and copies it to
// /output/entry.png, byte for byte.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(src);

// Validate: PNG signature, then IHDR width/height (big-endian u32 at
// bytes 16 and 20). The gate takes at most 1 MiB and 1024x1024 px.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error('entry.png is not a PNG file');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(src, dest);
const written = statSync(dest).size;
if (written !== bytes.length) {
  throw new Error(`copy mismatch: wrote ${written} bytes, source is ${bytes.length}`);
}
if (!readFileSync(dest).equals(bytes)) {
  throw new Error('copied entry.png differs from the source bytes');
}
console.log(`Wrote entry.png (${written} bytes, ${width}x${height}) to ${dest}`);
