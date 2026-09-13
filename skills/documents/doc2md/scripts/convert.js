#!/usr/bin/env node
// doc2md — пакетная конвертация документов в Markdown.
// Обёртка над firecrawl/anydoc (npx -y @firecrawl/anydoc).
// Кросс-платформенная версия: работает одинаково на Windows/macOS/Linux,
// нужен только Node.js (тот же, что уже требуется для npx/anydoc).
'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const SUPPORTED_EXT = new Set([
  'doc', 'docx', 'docm', 'odt', 'rtf', 'epub', 'pdf',
  'ppt', 'pps', 'pot', 'pptx', 'pptm', 'ppsx', 'ppsm', 'odp',
  'xls', 'xlsx', 'xlsm', 'xlsb', 'ods', 'csv',
]);

function usage() {
  console.log(`doc2md — конвертирует документы в Markdown перед тем, как их читает агент.

Использование:
  node convert.js <файл-или-папка> [ещё файлы/папки...] [-o ВЫХОДНАЯ_ПАПКА]

Примеры:
  node convert.js договор.docx
  node convert.js ~/Downloads/акты/ -o ~/Downloads/акты-md/
  node convert.js a.pdf b.xlsx "отчёт за март.pptx"

Без -o каждый файл.md пишется рядом с исходником.
Папка сканируется рекурсивно по поддерживаемым расширениям.`);
}

function walk(dir, out, seen) {
  // Защита от циклов по симлинкам: запоминаем реальные пути каталогов.
  let real;
  try {
    real = fs.realpathSync(dir);
  } catch {
    return;
  }
  if (seen.has(real)) return;
  seen.add(real);

  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const e of entries) {
    const full = path.join(dir, e.name);
    let st;
    try {
      st = fs.statSync(full); // statSync резолвит симлинки — на папки заходим, файлы проверяем по расширению
    } catch {
      continue;
    }
    if (st.isDirectory()) {
      walk(full, out, seen);
    } else if (st.isFile()) {
      const ext = path.extname(e.name).toLowerCase().replace(/^\./, '');
      if (SUPPORTED_EXT.has(ext)) out.push(full);
    }
  }
}

function main() {
  const argv = process.argv.slice(2);
  let outDir = null;
  const args = [];

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-o' || a === '--output') {
      outDir = argv[++i];
    } else if (a === '-h' || a === '--help') {
      usage();
      process.exit(0);
    } else {
      args.push(a);
    }
  }

  if (args.length === 0) {
    usage();
    process.exit(2);
  }

  if (outDir) fs.mkdirSync(outDir, { recursive: true });

  const files = [];
  const seen = new Set();
  for (const a of args) {
    let st = null;
    try {
      st = fs.statSync(a);
    } catch {
      st = null;
    }
    if (st && st.isDirectory()) {
      walk(a, files, seen);
    } else if (st && st.isFile()) {
      files.push(a);
    } else {
      console.error(`doc2md: пропускаю, не найден: ${a}`);
    }
  }

  if (files.length === 0) {
    console.error('doc2md: подходящих файлов не найдено');
    process.exit(1);
  }

  let ok = 0;
  let skip = 0;
  let fail = 0;
  const isWin = process.platform === 'win32';

  for (const f of files) {
    // Полное имя файла + .md (не срезаем расширение): "отчёт.csv" и "отчёт.docx"
    // иначе оба лягут в "отчёт.md" и второй перезапишет первый.
    const base = path.basename(f);
    const out = outDir ? path.join(outDir, `${base}.md`) : path.join(path.dirname(f), `${base}.md`);

    // shell:true на Windows обязателен — npx там резолвится как npx.cmd,
    // без shell Node его не находит через PATH.
    const res = spawnSync('npx', ['-y', '@firecrawl/anydoc', f, '-o', out], {
      shell: isWin,
      encoding: 'utf8',
    });

    const errOutput = (res.stderr || res.error?.message || '').trim();

    // Категоризация исхода. Контракт кодов возврата anydoc формально не
    // задокументирован, поэтому различаем консервативно:
    //   • не удалось ДАЖE запустить npx (ENOENT / нет в PATH / 126/127) — это
    //     ОШИБКА окружения, а НЕ «файл — скан». Иначе полный отказ npx выглядел
    //     бы как «все ваши документы нечитаемы» и увёл бы на бессмысленный OCR.
    //   • код 0 — OK.
    //   • прочий ненулевой код (файл дошёл до anydoc, но не сконвертировался) —
    //     ПРОПУСК: скорее всего скан/шифр/битый файл; печатаем stderr как есть.
    if (res.error || res.status === 127 || res.status === 126) {
      console.error(`ОШИБКА  ${f} — не удалось запустить anydoc: ${errOutput || 'npx недоступен'}`);
      fail++;
    } else if (res.status === 0) {
      console.log(`OK      ${f} -> ${out}`);
      ok++;
    } else {
      console.error(`ПРОПУСК ${f} — ${errOutput}`);
      skip++;
    }
  }

  console.log('');
  console.log(`Готово: ${ok} конвертировано, ${skip} пропущено (не читается/зашифровано/скан), ${fail} ошибок вызова`);
  if (skip > 0) {
    console.log('Пропущенные, скорее всего, сканы или PDF-картинки без текстового слоя — прогони их через OCR (скилл pdf, шаг «сделать PDF searchable») и повтори.');
  }

  process.exit(fail > 0 ? 1 : 0);
}

main();
