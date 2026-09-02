#!/usr/bin/env node

/*
 * Evidence-only browser compositor review for PetDex v2 atlases.
 *
 * This deliberately renders the formal WebP files through Chromium CSS
 * background positioning instead of resizing cells with Pillow.  It covers
 * the renderer-specific risks that raster-only reviews cannot prove:
 * neighbouring-cell sampling, fractional background-position phases,
 * device-pixel-ratio rounding, and the CSS clipping boundary.
 *
 * Formal assets are never modified.  The script writes only screenshots and
 * a relative-path JSON report under the requested QA output directory.
 */

import { createRequire } from "node:module";
import { readFile, mkdir, writeFile } from "node:fs/promises";
import { basename, dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const scriptDir = dirname(fileURLToPath(import.meta.url));
let playwright;
const playwrightCandidates = [
  process.env.PLAYWRIGHT_PACKAGE,
  "playwright",
].filter(Boolean);
for (const candidate of playwrightCandidates) {
  try {
    playwright = require(candidate);
    break;
  } catch {
    // Try the next package location. The report records only QA artifacts.
  }
}
if (!playwright) {
  throw new Error("Playwright package not found; set PLAYWRIGHT_PACKAGE or NODE_PATH before running this review.");
}
const { chromium } = playwright;

const ROLES = [
  "hei-mao",
  "hei-mao-quality",
  "hei-mao-butler",
  "hei-mao-chef",
  "hei-mao-foodie",
  "hei-mao-delivery",
  "hei-mao-fortune",
  "hei-mao-traveler",
];

const ROWS = [
  ["idle", 6],
  ["running-right", 8],
  ["running-left", 8],
  ["waving", 4],
  ["jumping", 5],
  ["failed", 8],
  ["waiting", 6],
  ["running", 6],
  ["review", 6],
  ["look-row-9", 8],
  ["look-row-10", 8],
];

const CELL_W = 192;
const CELL_H = 208;
const ATLAS_W = 1536;
const ATLAS_H = 2288;

function parseArgs(argv) {
  const args = {
    repo: resolve(scriptDir, "../.."),
    outputDir: scriptDir,
  };
  for (let index = 2; index < argv.length; index += 1) {
    const item = argv[index];
    if (item === "--repo") args.repo = resolve(argv[++index]);
    else if (item === "--output-dir") args.outputDir = resolve(argv[++index]);
    else if (item === "--json-out") args.jsonOut = resolve(argv[++index]);
    else if (item === "--full-sheet-out") args.fullSheetOut = resolve(argv[++index]);
    else if (item === "--candidate-sheet-out") args.candidateSheetOut = resolve(argv[++index]);
    else throw new Error(`unknown argument: ${item}`);
  }
  args.jsonOut ??= join(args.outputDir, "browser-css-compositor-review-20260831-v1.json");
  args.fullSheetOut ??= join(args.outputDir, "browser-css-compositor-full-v1.png");
  args.candidateSheetOut ??= join(args.outputDir, "browser-css-compositor-candidates-v1.png");
  return args;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function atlasDataUri(buffer) {
  return `data:image/webp;base64,${buffer.toString("base64")}`;
}

function checkerCss() {
  return [
    "background-color:#f4f5f7",
    "background-image:linear-gradient(45deg,#d7dbe1 25%,transparent 25%),linear-gradient(-45deg,#d7dbe1 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#d7dbe1 75%),linear-gradient(-45deg,transparent 75%,#d7dbe1 75%)",
    "background-size:12px 12px",
    "background-position:0 0,0 6px,6px -6px,-6px 0",
  ].join(";");
}

function renderStyle(frame, row, scale, phaseX, phaseY, width, height) {
  const bgWidth = ATLAS_W * scale;
  const bgHeight = ATLAS_H * scale;
  const x = -(frame * CELL_W * scale) + phaseX;
  const y = -(row * CELL_H * scale) + phaseY;
  return [
    `width:${width}px`,
    `height:${height}px`,
    `background-size:${bgWidth}px ${bgHeight}px`,
    `background-position:${x}px ${y}px`,
    "background-repeat:no-repeat",
    "image-rendering:pixelated",
  ].join(";");
}

function fullSheetHtml(atlases, scale, phaseX, phaseY) {
  const displayW = CELL_W * scale;
  const displayH = CELL_H * scale;
  const atlasStyles = ROLES.map((role) => `.role-${role.replaceAll("-", "_")}{background-image:url('${atlases.get(role)}')}`).join("");
  const sections = ROLES.map((role) => {
    const cells = ROWS.map(([rowName, frameCount], rowIndex) => {
      const frames = Array.from({ length: frameCount }, (_, frame) => {
        const style = renderStyle(frame, rowIndex, scale, phaseX, phaseY, displayW, displayH);
        return `<div class="frame-wrap" data-role="${escapeHtml(role)}" data-row="${escapeHtml(rowName)}" data-frame="${frame}" style="${checkerCss()}"><div class="sprite role-${role.replaceAll("-", "_")}" style="${style}"></div></div>`;
      }).join("");
      return `<div class="row-line"><div class="row-label">${escapeHtml(rowName)}</div><div class="frames">${frames}</div></div>`;
    }).join("");
    return `<section><h2>${escapeHtml(role)}</h2>${cells}</section>`;
  }).join("");
  return `<!doctype html><html><head><meta charset="utf-8"><style>
    *{box-sizing:border-box}html,body{margin:0;padding:0;background:#171a21;color:#f2f4f8;font:12px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    main{padding:14px 18px 24px;display:flex;flex-direction:column;gap:20px}
    section{border:1px solid #3a4050;border-radius:8px;padding:8px 10px 12px;background:#222733}
    h2{font-size:14px;line-height:20px;margin:0 0 7px;color:#ffffff}
    .row-line{display:flex;align-items:center;gap:8px;min-height:${displayH + 4}px;margin:2px 0}
    .row-label{width:104px;color:#b8c1d4;white-space:nowrap;font-size:11px}
    .frames{display:flex;gap:3px;align-items:center}
    .frame-wrap{display:block;padding:1px;line-height:0;border:1px solid rgba(255,255,255,.1)}
    .sprite{display:block}
    ${atlasStyles}
  </style></head><body><main>${sections}</main></body></html>`;
}

const CANDIDATES = [
  ["hei-mao", "jumping", 2],
  ["hei-mao-quality", "jumping", 2],
  ["hei-mao-foodie", "waiting", 2],
  ["hei-mao-foodie", "waiting", 3],
  ["hei-mao-delivery", "failed", 0],
  ["hei-mao-delivery", "failed", 4],
  ["hei-mao-fortune", "idle", 0],
  ["hei-mao-fortune", "look-row-10", 7],
  ["hei-mao-chef", "look-row-9", 7],
  ["hei-mao-traveler", "failed", 4],
  ["hei-mao-butler", "waiting", 0],
  ["hei-mao-quality", "running-right", 4],
  ["hei-mao-delivery", "look-row-9", 7],
  ["hei-mao-foodie", "look-row-10", 0],
  ["hei-mao-chef", "waving", 0],
  ["hei-mao-traveler", "look-row-10", 0],
];

function candidateSheetHtml(atlases, scale, phaseX, phaseY) {
  const displayW = CELL_W * scale;
  const displayH = CELL_H * scale;
  const atlasStyles = ROLES.map((role) => `.role-${role.replaceAll("-", "_")}{background-image:url('${atlases.get(role)}')}`).join("");
  const cards = CANDIDATES.map(([role, rowName, frame]) => {
    const rowIndex = ROWS.findIndex(([name]) => name === rowName);
    if (rowIndex < 0) throw new Error(`unknown row ${rowName}`);
    const style = renderStyle(frame, rowIndex, scale, phaseX, phaseY, displayW, displayH);
    const spriteClass = `role-${role.replaceAll("-", "_")}`;
    return `<article><div class="title">${escapeHtml(role)} / ${escapeHtml(rowName)} / f${frame}</div><div class="pair"><div class="frame-wrap" style="${checkerCss()}"><div class="sprite ${spriteClass}" style="${style}"></div></div><div class="frame-wrap" style="background:#11141b"><div class="sprite ${spriteClass}" style="${style}"></div></div></div></article>`;
  }).join("");
  return `<!doctype html><html><head><meta charset="utf-8"><style>
    *{box-sizing:border-box}html,body{margin:0;padding:0;background:#171a21;color:#f2f4f8;font:12px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    main{padding:14px;display:grid;grid-template-columns:repeat(4,${displayW * 2 + 18}px);gap:12px}
    article{border:1px solid #414957;border-radius:8px;padding:6px;background:#242a36}.title{font-size:10px;line-height:16px;color:#d5dbea;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pair{display:flex;gap:5px}.frame-wrap{padding:1px;border:1px solid rgba(255,255,255,.15);line-height:0}.sprite{display:block}
    ${atlasStyles}
  </style></head><body><main>${cards}</main></body></html>`;
}

async function loadAtlases(repo) {
  const atlases = new Map();
  for (const role of ROLES) {
    const path = join(repo, "pets", role, "spritesheet.webp");
    atlases.set(role, atlasDataUri(await readFile(path)));
  }
  return atlases;
}

async function capture(browser, atlases, html, outputPath, deviceScaleFactor, viewportWidth, viewportHeight) {
  const context = await browser.newContext({ deviceScaleFactor, viewport: { width: viewportWidth, height: viewportHeight } });
  const page = await context.newPage();
  await page.setContent(html, { waitUntil: "load" });
  await page.waitForTimeout(80);
  await page.screenshot({ path: outputPath, fullPage: true, animations: "disabled" });
  const geometry = await page.locator(".frame-wrap").evaluateAll((nodes) => nodes.slice(0, 12).map((node) => {
    const rect = node.getBoundingClientRect();
    return {
      role: node.dataset.role ?? null,
      row: node.dataset.row ?? null,
      frame: node.dataset.frame === undefined ? null : Number(node.dataset.frame),
      x: Number(rect.x.toFixed(4)),
      y: Number(rect.y.toFixed(4)),
      width: Number(rect.width.toFixed(4)),
      height: Number(rect.height.toFixed(4)),
    };
  }));
  await context.close();
  return geometry;
}

async function main() {
  const args = parseArgs(process.argv);
  await mkdir(args.outputDir, { recursive: true });
  const atlases = await loadAtlases(args.repo);
  const browser = await chromium.launch({ headless: true });
  const screenshots = [];
  const geometrySamples = [];

  const variants = [
    { id: "dpr1-scale1-phase0", dpr: 1, scale: 1, phaseX: 0, phaseY: 0 },
    { id: "dpr1-scale1-phase05", dpr: 1, scale: 1, phaseX: 0.5, phaseY: 0.5 },
    { id: "dpr15-scale1-phase0", dpr: 1.5, scale: 1, phaseX: 0, phaseY: 0 },
    { id: "dpr15-scale1-phase05", dpr: 1.5, scale: 1, phaseX: 0.5, phaseY: 0.5 },
    { id: "dpr2-scale075-phase0", dpr: 2, scale: 0.75, phaseX: 0, phaseY: 0 },
    { id: "dpr2-scale125-phase05", dpr: 2, scale: 1.25, phaseX: 0.5, phaseY: 0.5 },
  ];

  for (const variant of variants) {
    const html = fullSheetHtml(atlases, variant.scale, variant.phaseX, variant.phaseY);
    const outputPath = join(args.outputDir, `browser-css-compositor-${variant.id}.png`);
    const geometry = await capture(browser, atlases, html, outputPath, variant.dpr, 2400, 900);
    screenshots.push(relative(args.outputDir, outputPath));
    geometrySamples.push({ variant: variant.id, dpr: variant.dpr, scale: variant.scale, phase: [variant.phaseX, variant.phaseY], samples: geometry });
  }

  const candidateVariant = variants[3];
  const candidateHtml = candidateSheetHtml(atlases, 0.5, candidateVariant.phaseX, candidateVariant.phaseY);
  const candidateGeometry = await capture(browser, atlases, candidateHtml, args.candidateSheetOut, candidateVariant.dpr, 2400, 900);
  const candidateFullHtml = fullSheetHtml(atlases, candidateVariant.scale, candidateVariant.phaseX, candidateVariant.phaseY);
  await capture(browser, atlases, candidateFullHtml, args.fullSheetOut, candidateVariant.dpr, 2400, 900);
  await browser.close();

  const report = {
    schema_version: 1,
    checked_at: new Date().toISOString(),
    scope: "asset-only Chromium CSS compositor replay; evidence only",
    method: {
      name: "native browser CSS background-position and DPR replay",
      renderer_assumptions: [
        "192x208 clipped sprite element",
        "1536x2288 atlas background with width-proportional scaling",
        "image-rendering: pixelated",
        "fractional background-position phases",
        "Chromium deviceScaleFactor 1, 1.5, and 2",
      ],
      purpose: "detect browser-specific neighbouring-cell sampling, clipping, phase rounding, and display-scale distortion that Pillow-only rehearsal cannot prove",
      interpretation: "screenshots and geometry are candidate evidence; no metric is an automatic asset failure",
    },
    coverage: {
      roles: ROLES.length,
      rows: ROLES.length * ROWS.length,
      frames: ROWS.reduce((total, [, count]) => total + count, 0) * ROLES.length,
      variants: variants.map(({ id, dpr, scale, phaseX, phaseY }) => ({ id, dpr, scale, phase: [phaseX, phaseY] })),
      candidate_frames: CANDIDATES.length,
    },
    result: {
      formal_assets_modified: false,
      new_hard_failures: [],
      release_effect: "supplemental evidence only; requires normal-size review and does not replace live Codex App playback",
    },
    visual_review: {
      status: "pending_normal_size_review",
      note: "The browser-rendered sheets were captured successfully; candidate promotion requires visual inspection of the generated sheets.",
    },
    artifacts: [
      ...screenshots,
      relative(args.outputDir, args.fullSheetOut),
      relative(args.outputDir, args.candidateSheetOut),
      basename(args.jsonOut),
    ],
    geometry_samples: geometrySamples,
    candidate_geometry: candidateGeometry,
    limitations: [
      "This is a headless Chromium capture, not a live Codex App or GPU capture on macOS, Windows, or Linux.",
      "The exact PetDex CSS declaration may evolve; renderer assumptions are recorded above.",
      "Browser screenshots expose visual candidates but do not by themselves prove window z-order, bubble tracking, or cross-screen behavior.",
    ],
  };
  await writeFile(args.jsonOut, `${JSON.stringify(report, null, 2)}\n`, "utf8");
  process.stdout.write(`${JSON.stringify({ json: relative(args.outputDir, args.jsonOut), full_sheet: relative(args.outputDir, args.fullSheetOut), candidate_sheet: relative(args.outputDir, args.candidateSheetOut), variants: variants.length, frames: report.coverage.frames })}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error.stack ?? error}\n`);
  process.exitCode = 1;
});
