#!/usr/bin/env bash
# doc2md — пакетная конвертация документов в Markdown.
# Обёртка над firecrawl/anydoc (npx -y @firecrawl/anydoc).
# Поведение категоризации держится идентичным convert.js — при правке одного
# скрипта синхронизируй второй.
set -uo pipefail

SUPPORTED_EXT="doc docx docm odt rtf epub pdf ppt pps pot pptx pptm ppsx ppsm odp xls xlsx xlsm xlsb ods csv"

usage() {
  cat <<'EOF'
doc2md — конвертирует документы в Markdown перед тем, как их читает агент.

Использование:
  convert.sh <файл-или-папка> [ещё файлы/папки...] [-o ВЫХОДНАЯ_ПАПКА]

Примеры:
  convert.sh договор.docx
  convert.sh ~/Downloads/акты/ -o ~/Downloads/акты-md/
  convert.sh a.pdf b.xlsx "отчёт за март.pptx"

Без -o каждый файл.md пишется рядом с исходником.
Папка сканируется рекурсивно по поддерживаемым расширениям.
EOF
}

OUT_DIR=""
ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--output) OUT_DIR="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) ARGS+=("$1"); shift ;;
  esac
done

if [[ ${#ARGS[@]} -eq 0 ]]; then
  usage
  exit 2
fi

if [[ -n "$OUT_DIR" ]]; then
  mkdir -p "$OUT_DIR"
fi

# Собираем find-предикат по расширениям безопасно, через массив (не через eval).
FIND_PREDICATE=()
first=true
for ext in $SUPPORTED_EXT; do
  if $first; then
    FIND_PREDICATE+=( -iname "*.$ext" )
    first=false
  else
    FIND_PREDICATE+=( -o -iname "*.$ext" )
  fi
done

FILES=()
for arg in "${ARGS[@]}"; do
  if [[ -d "$arg" ]]; then
    while IFS= read -r -d '' f; do
      FILES+=("$f")
    done < <(find "$arg" -type f \( "${FIND_PREDICATE[@]}" \) -print0)
  elif [[ -f "$arg" ]]; then
    FILES+=("$arg")
  else
    echo "doc2md: пропускаю, не найден: $arg" >&2
  fi
done

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "doc2md: подходящих файлов не найдено" >&2
  exit 1
fi

OK=0
SKIP=0
FAIL=0

for f in "${FILES[@]}"; do
  base="$(basename "$f")"
  # Полное имя файла + .md (не срезаем расширение): "отчёт.csv" и "отчёт.docx"
  # иначе оба лягут в "отчёт.md" и второй перезапишет первый.
  if [[ -n "$OUT_DIR" ]]; then
    out="$OUT_DIR/$base.md"
  else
    out="$(dirname "$f")/$base.md"
  fi

  err_output=$(npx -y @firecrawl/anydoc "$f" -o "$out" 2>&1 >/dev/null)
  code=$?

  # Категоризация исхода — идентична convert.js:
  #   0        → OK
  #   126/127  → ОШИБКА (не удалось запустить npx/anydoc, а не «файл — скан»)
  #   иначе    → ПРОПУСК (скан/шифр/битый файл; печатаем stderr как есть)
  if [[ $code -eq 0 ]]; then
    echo "OK      $f -> $out"
    OK=$((OK + 1))
  elif [[ $code -eq 127 || $code -eq 126 ]]; then
    echo "ОШИБКА  $f — не удалось запустить anydoc: ${err_output:-npx недоступен}" >&2
    FAIL=$((FAIL + 1))
  else
    echo "ПРОПУСК $f — $err_output" >&2
    SKIP=$((SKIP + 1))
  fi
done

echo ""
echo "Готово: $OK конвертировано, $SKIP пропущено (не читается/зашифровано/скан), $FAIL ошибок вызова"
if [[ $SKIP -gt 0 ]]; then
  echo "Пропущенные, скорее всего, сканы или PDF-картинки без текстового слоя — прогони их через OCR (скилл pdf, шаг «сделать PDF searchable») и повтори."
fi

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
exit 0
