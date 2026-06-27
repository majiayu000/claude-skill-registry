#!/usr/bin/env python3
"""锁定/核验候选人的真实 GitHub 账号。

用法:
    python find_github.py <handle|email|name> [更多线索 ...]
例:
    python find_github.py octocat octocat@example.com "The Octocat"

为什么有用:简历上的 GitHub 链接是第一可验证物,但常常失效或改名——
这本身就是信号。本脚本:
  - 直连核验声称的 handle(死链=HTTP 404)
  - 从邮箱前缀派生 handle(octocat@example.com -> octocat)
  - 试常见变体(去点/去下划线 / <handle>-commits 这类被改名/镜像账号)
  - 按姓名/handle 搜索用户,列出候选

找不到 ≠ 造假;但要先穷尽搜索再下"不可验证"结论。

无需鉴权。Windows 下强制 UTF-8 输出。
"""
import urllib.request, json, sys, io, urllib.parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def api(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "audit", "Accept": "application/vnd.github+json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return None, str(e)


def check(h):
    st, u = api(f"https://api.github.com/users/{h}")
    flag = ""
    if st == 200:
        flag = f"  <-- EXISTS (name={u.get('name')}, repos={u.get('public_repos')}, created={u.get('created_at','')[:10]})"
    print(f"  github.com/{h:26s} -> HTTP {st}{flag}")
    return st == 200


def search_users(q):
    st, r = api(
        "https://api.github.com/search/users?q=" + urllib.parse.quote(q) + "&per_page=8"
    )
    if isinstance(r, dict):
        items = ", ".join(i["login"] for i in r.get("items", [])[:8])
        print(f"  search '{q}': total={r.get('total_count')} -> {items}")
    else:
        print(f"  search '{q}': HTTP {st}")


def main(terms):
    print("== 直连 handle 核验(含邮箱派生 + 常见变体)==")
    seen = set()
    for t in terms:
        base = t.split("@")[0] if "@" in t else t
        for h in [base, base.replace(".", ""), base.replace("_", ""), base + "-commits"]:
            if h and h not in seen:
                seen.add(h)
                check(h)
    print("== 用户搜索(姓名/handle 变体)==")
    for t in terms:
        search_users(t)
    print("\n提示:若声称的 handle 是 404,真号常是邮箱派生名 / <handle>-commits / 姓名拼音号;")
    print("      留意账号创建时间(最近才建=可能突击包装)与账号名是否对得上简历真名。")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python find_github.py <handle|email|name> [更多线索 ...]")
        sys.exit(1)
    main(sys.argv[1:])
