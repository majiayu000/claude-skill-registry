#!/usr/bin/env python3
"""枚举一个 GitHub 用户的仓库 + 暴露破绽的元数据。

用法:
    python github_enum.py <handle> [<handle> ...]

为什么有用:元数据本身就是照妖镜——
  - fork 占比高(知名项目的 fork 一堆)→ 把 GitHub 当书签,不是 builder
  - 体积异常小(号称"复杂系统"却只有几十 KB)→ 大概率套壳玩具
  - 账号/全部仓库都是最近建的 → 可能临投简历突击包装
  - 简历"代表作"在不在这里 → 不在=不可验证/注水

无需鉴权(未鉴权 GitHub API 60 次/小时)。Windows 下强制 UTF-8 输出,避免 GBK 报错。
"""
import urllib.request, json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def api(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "audit", "Accept": "application/vnd.github+json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return None, str(e)


def enum_user(h):
    st, u = api(f"https://api.github.com/users/{h}")
    if st != 200:
        print(f"### {h} -> HTTP {st} (账号不存在 / 错误: {u})")
        return
    print("=" * 92)
    print(f"### {h} | name={u.get('name')} | bio={u.get('bio')}")
    print(
        f"    created={u.get('created_at','')[:10]}  public_repos={u.get('public_repos')}  followers={u.get('followers')}"
    )
    st, repos = api(f"https://api.github.com/users/{h}/repos?per_page=100&sort=pushed")
    if not isinstance(repos, list):
        print(f"    [repos error] {repos}")
        return
    forks = sum(1 for r in repos if r.get("fork"))
    print(f"    repos shown={len(repos)} (forks={forks}, own={len(repos)-forks})")
    for r in repos:
        tag = "FORK" if r.get("fork") else "OWN "
        print(
            f"  [{tag}] {r['name']:38.38s} lang={str(r.get('language')):12s} "
            f"size={r.get('size'):>8}KB star={r.get('stargazers_count'):>3} "
            f"push={r.get('pushed_at','')[:10]} created={r.get('created_at','')[:10]}"
        )
        if r.get("description"):
            print(f"         {r['description']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python github_enum.py <handle> [<handle> ...]")
        sys.exit(1)
    for handle in sys.argv[1:]:
        enum_user(handle)
