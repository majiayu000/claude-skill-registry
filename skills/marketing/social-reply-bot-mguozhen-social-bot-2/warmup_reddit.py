#!/usr/bin/env python3
"""
Reddit 账号养号脚本 — 在通用版块发真实评论积累 Karma
"""
import sys, time, re, logging, os
from pathlib import Path
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")
sys.path.insert(0, str(Path(__file__).parent))

import anthropic
from bot import browser as B
from bot.reddit_bot import _ensure_logged_in, _post_comment

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("warmup")

BASE_URL = "https://old.reddit.com"

WARMUP_SUBREDDITS = [
    "FreeKarma4U",          # 专为新账号互赞设计
    "karma",                # 同上
    "newreddits",           # 新版块，门槛低
    "CasualConversation",   # 轻松聊天，对新账号友好
    "self",                 # 自我分享，极少 automod
    "NoStupidQuestions",    # 问答，友好社区
    "mildlyinteresting",    # 轻度过滤
    "Showerthoughts",       # 脑洞，低门槛
]

MAX_COMMENTS = int(sys.argv[1]) if len(sys.argv) > 1 else 8
DELAY_SUCCESS = 90    # 两条评论之间间隔
DELAY_FAIL    = 15


def generate_comment(post_title: str, post_content: str, subreddit: str) -> Optional[str]:
    """用 Claude Haiku 生成一条真实评论（不带任何产品推广）"""
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    system = """You are a genuine Reddit user. Write short, authentic comments.
Rules:
- Never mention products, companies, or services
- Sound like a real person, not AI
- Be conversational, curious, or share a relatable experience
- 1-3 sentences is ideal
- Casual tone, can use lowercase
- No hashtags, no bullet points
- Never start with "I" as the first word"""

    user = f"""Subreddit: r/{subreddit}
Post: {post_title}
Content: {post_content[:500]}

Write one genuine comment. If too political/controversial/personal, reply: SKIP"""

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=120,
            messages=[{"role": "user", "content": user}],
            system=system,
        )
        text = msg.content[0].text.strip()
        # Remove any leading SKIP explanation
        if text.upper().startswith("SKIP"):
            return None
        return text
    except Exception as e:
        logger.error(f"Claude error: {e}")
        return None


def get_post_urls(subreddit: str, count: int = 8) -> List[dict]:
    """
    访问版块 /hot/，收集帖子 URL 列表。
    策略：依次点击 comment 链接获取 URL，再返回列表页。
    """
    B.open_url(f"{BASE_URL}/r/{subreddit}/hot/")
    time.sleep(3)

    # 先收集所有帖子标题 + comment 数量
    tree = B.snapshot()
    submitted_positions = [m.start() for m in re.finditer(r'\bsubmitted\b', tree)]

    candidates = []
    seen_titles = set()
    skip_words = ["Submit a new", "Welcome to", "About /r/", "wiki",
                  "Discord", "/r/", "http", "View Poll", "rules", "moderator"]

    for pos in submitted_positions[:30]:
        before = tree[max(0, pos - 1500):pos]
        links = re.findall(r'\[(\d+-\d+)\] link: ([^\n]{15,200})', before)
        if not links:
            continue
        _, title = links[-1]
        title = title.strip()
        if any(s.lower() in title.lower() for s in skip_words):
            continue
        if title in seen_titles:
            continue

        # Comment count
        after = tree[pos:pos + 400]
        cm = re.search(r'\[(\d+-\d+)\] link: (\d+) comments?', after)
        if not cm:
            continue
        n = int(cm.group(2))
        if n < 1 or n > 500:
            continue

        seen_titles.add(title)
        candidates.append({"title": title, "comment_count": n})
        if len(candidates) >= count:
            break

    if not candidates:
        return []

    # 逐一点击 comment 链接获取真实 URL
    posts = []
    for idx in range(min(len(candidates), count)):
        # 每次都要重新获取 snapshot（因为导航后 refs 变了）
        B.open_url(f"{BASE_URL}/r/{subreddit}/hot/")
        time.sleep(3)
        tree = B.snapshot()

        comment_links = re.findall(r'\[(\d+-\d+)\] link: \d+ comments?', tree)
        if idx >= len(comment_links):
            break

        B.click(comment_links[idx])
        time.sleep(4)

        url = B.get_url()
        if not url or subreddit.lower() not in url.lower():
            continue

        # 确保是 old.reddit.com 格式
        url = url.replace("www.reddit.com", "old.reddit.com")

        candidates[idx]["url"] = url
        posts.append(candidates[idx])
        logger.info(f"  [{idx+1}] {candidates[idx]['title'][:55]}")

    return posts


def warmup_post(post: dict, subreddit: str) -> bool:
    """
    访问帖子页面，生成评论，发出。
    假设我们已经在热帖列表页。
    """
    url = post.get("url", "")
    if not url:
        return False

    B.open_url(url)
    time.sleep(5)  # 多等一点，让评论框加载

    tree = B.snapshot()

    # 提取帖子内容（跳过 sidebar，从标题后开始）
    title_idx = tree.find(post["title"][:35])
    if title_idx > 0:
        chunk = tree[title_idx: title_idx + 3000]
    else:
        chunk = tree[3000:6000]  # fallback

    text_blocks = re.findall(r'StaticText: ([^\n]{20,})', chunk)
    meta = {"submitted", "by", "share", "save", "hide", "report",
            "crosspost", "sorted by:", "best", "formatting help"}
    clean = [t for t in text_blocks if t.strip().lower() not in meta]
    snippet = " ".join(clean[:10])[:600]

    # 生成评论
    comment = generate_comment(post["title"], snippet, subreddit)
    if not comment:
        logger.info("  → SKIP")
        return False

    logger.info(f"  Comment: {comment[:90]}")

    # 检查是否有评论框（说明已登录且帖子未锁定）
    textarea_refs = re.findall(r'\[(\d+-\d+)\] textbox(?!: search)', tree)
    if not textarea_refs:
        # 尝试等待更长时间再次检查
        logger.info("  → no textarea, waiting 3s and retrying...")
        time.sleep(3)
        tree = B.snapshot()
        textarea_refs = re.findall(r'\[(\d+-\d+)\] textbox(?!: search)', tree)

    if not textarea_refs:
        logger.warning("  → textarea still not found (locked/not logged in?)")
        # Debug: show what's in tree
        logger.debug(f"Tree sample: {tree[3000:4500]}")
        return False

    return _post_comment(comment)


def main():
    logger.info(f"=== Reddit 养号开始，目标 {MAX_COMMENTS} 条评论 ===")

    if not _ensure_logged_in():
        logger.error("Reddit 未登录，退出")
        return

    posted = 0
    failed = 0
    skipped = 0

    for subreddit in WARMUP_SUBREDDITS:
        if posted >= MAX_COMMENTS:
            break

        logger.info(f"\n[r/{subreddit}] 获取帖子列表...")
        posts = get_post_urls(subreddit, count=4)
        logger.info(f"  找到 {len(posts)} 个帖子")

        for post in posts:
            if posted >= MAX_COMMENTS:
                break

            logger.info(f"\n  » {post['title'][:60]} ({post['comment_count']} 评论)")

            success = warmup_post(post, subreddit)

            if success:
                posted += 1
                logger.info(f"  ✓ 评论发出！累计 {posted}/{MAX_COMMENTS}")
                wait = DELAY_SUCCESS + posted * 15
                logger.info(f"  等待 {wait}s...")
                time.sleep(wait)
            else:
                skipped_or_failed = "skipped" if not post.get("url") else "failed"
                if skipped_or_failed == "failed":
                    failed += 1
                else:
                    skipped += 1
                time.sleep(DELAY_FAIL)

    logger.info(f"\n=== 完成 === ✓posted={posted}  ✗failed={failed}  skip={skipped}")
    logger.info("Karma 查看: https://www.reddit.com/user/mguozhen/")


if __name__ == "__main__":
    main()
