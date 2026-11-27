// news-image-20261127 — entry program (Node 22, standard library only).
// The image is drawn at build time by render.py and committed as entry.png.
// This program only carries it to the grader's output directory, unchanged,
// so both runs write byte-identical output. Before copying it verifies the
// file really is a PNG within the gate's limits (<= 1 MiB, <= 1024x1024),
// reading the size straight out of the PNG's IHDR chunk.
//
// Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const here = dirname(fileURLToPath(import.meta.url));
const bytes = readFileSync(join(here, 'entry.png'));

if (bytes.length < 33 || !bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG');
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
// IHDR chunk: length (4) + 'IHDR' (4) + width (4, big-endian) + height (4).
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (bytes.subarray(12, 16).toString('ascii') !== 'IHDR') {
  throw new Error('entry.png has no IHDR chunk where one belongs');
}
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), bytes);
console.log(`wrote entry.png (${width}x${height}, ${bytes.length} bytes)`);
