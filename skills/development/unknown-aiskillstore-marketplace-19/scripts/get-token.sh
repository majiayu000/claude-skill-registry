#!/usr/bin/env bash
# 获取禅道 API 调用所需的 URL、token 和用户名，按优先级：缓存文件 > 环境变量 > 账号密码登录。
# 用法：eval "$(bash get-token.sh)"  → 设置 ZENTAO_URL、ZENTAO_TOKEN、ZENTAO_ACCOUNT
# 依赖：curl, node
# 缓存文件 ~/.zentao-token.json 保存 token、url、account，下次可免密直接使用。
# 注：禅道 token 永久有效；如需切换账号/服务器，删除缓存文件后重新运行即可。

set -euo pipefail

CACHE_FILE="${HOME}/.zentao-token.json"

# 输出三元组（KEY=VALUE 格式，可直接 eval）并退出
output_and_exit() {
  local url="$1" token="$2" account="$3"
  echo "ZENTAO_URL=${url}"
  echo "ZENTAO_TOKEN=${token}"
  echo "ZENTAO_ACCOUNT=${account}"
  exit 0
}

# ── 1. 优先：从缓存文件读取 url、token、account（单次 node 调用）────────────
if [[ -f "$CACHE_FILE" ]]; then
  _cache_url='' _cache_token='' _cache_account=''
  {
    IFS= read -r _cache_url
    IFS= read -r _cache_token
    IFS= read -r _cache_account
  } < <(node -e "
try {
  const d = JSON.parse(require('fs').readFileSync(process.argv[1], 'utf8'));
  process.stdout.write((d.url||'') + '\n' + (d.token||'') + '\n' + (d.account||'') + '\n');
} catch(e) { process.stdout.write('\n\n\n'); }
" "$CACHE_FILE" 2>/dev/null || printf '\n\n\n')

  # 用缓存补全缺失的环境变量
  [[ -z "${ZENTAO_URL:-}"     && -n "$_cache_url"     ]] && ZENTAO_URL="$_cache_url"
  [[ -z "${ZENTAO_ACCOUNT:-}" && -n "$_cache_account" ]] && ZENTAO_ACCOUNT="$_cache_account"

  # 缓存 token 有效且 url/account 均匹配，直接输出三元组（无需密码）
  if [[ -n "$_cache_token" \
     && "${ZENTAO_URL:-}" == "$_cache_url" \
     && ( -z "${ZENTAO_ACCOUNT:-}" || "${ZENTAO_ACCOUNT:-}" == "$_cache_account" ) ]]; then
    output_and_exit "$_cache_url" "$_cache_token" "$_cache_account"
  fi
fi

# ── 2. 其次：从环境变量读取 token（仍需 ZENTAO_URL）────────────────────────
if [[ -n "${ZENTAO_TOKEN:-}" ]]; then
  if [[ -z "${ZENTAO_URL:-}" ]]; then
    echo "错误：设置了 ZENTAO_TOKEN 但缺少 ZENTAO_URL，请同时提供服务器地址。" >&2
    exit 1
  fi
  # 写入缓存，方便下次无需环境变量直接使用
  node - "$CACHE_FILE" "${ZENTAO_TOKEN}" "${ZENTAO_URL}" "${ZENTAO_ACCOUNT:-}" <<'JSEOF'
const [,, cachePath, token, url, account] = process.argv;
const fs = require('fs');
fs.writeFileSync(cachePath, JSON.stringify({ token, url, account }, null, 2));
JSEOF
  output_and_exit "${ZENTAO_URL}" "${ZENTAO_TOKEN}" "${ZENTAO_ACCOUNT:-}"
fi

# ── 3. 再次：用账号密码重新登录（需 ZENTAO_URL、ZENTAO_ACCOUNT、ZENTAO_PASSWORD）
if [[ -z "${ZENTAO_URL:-}" || -z "${ZENTAO_ACCOUNT:-}" || -z "${ZENTAO_PASSWORD:-}" ]]; then
  echo "错误：Token 获取失败。请通过以下任一方式提供鉴权信息：" >&2
  echo "  · 缓存文件 ~/.zentao-token.json（含 url、token、account 字段）" >&2
  echo "  · 环境变量 ZENTAO_TOKEN + ZENTAO_URL（直接提供 token 和服务器地址）" >&2
  echo "  · 环境变量 ZENTAO_URL、ZENTAO_ACCOUNT、ZENTAO_PASSWORD（账号密码登录）" >&2
  exit 1
fi

RESPONSE=$(curl -s -X POST "${ZENTAO_URL}/api.php/v2/users/login" \
  -H "Content-Type: application/json" \
  -d "{\"account\": \"${ZENTAO_ACCOUNT}\", \"password\": \"${ZENTAO_PASSWORD}\"}")

TOKEN=$(echo "$RESPONSE" | node -e "
const chunks = [];
process.stdin.on('data', d => chunks.push(d));
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(chunks.join(''));
    const token = (data.data && data.data.token) || data.token || '';
    if (!token) {
      process.stderr.write('登录失败，服务器响应：' + JSON.stringify(data) + '\n');
      process.exit(1);
    }
    process.stdout.write(token);
  } catch (e) {
    process.stderr.write('解析登录响应失败：' + e.message + '\n');
    process.exit(1);
  }
});
") || { echo "错误：登录失败，请查看上方错误信息" >&2; exit 1; }

# ── 4. 缓存：写入 token、url、account ────────────────────────────────────────
node - "$CACHE_FILE" "$TOKEN" "$ZENTAO_URL" "$ZENTAO_ACCOUNT" <<'JSEOF'
const [,, cachePath, token, url, account] = process.argv;
const fs = require('fs');
fs.writeFileSync(cachePath, JSON.stringify({ token, url, account }, null, 2));
JSEOF

output_and_exit "$ZENTAO_URL" "$TOKEN" "$ZENTAO_ACCOUNT"
