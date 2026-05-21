#!/usr/bin/env python3
"""Shared utilities for stock-monitor skill: DB, Shopify parsing, notifications."""

import json
import os
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'stock_monitor.db')
SMS_SCRIPT = os.path.expanduser('~/.claude/skills/sms/scripts/sms_send.py')
SLACK_SCRIPT = os.path.expanduser('~/.claude/skills/slack/scripts/slack_post.py')
DEFAULT_PHONE = ''  # Set your phone number here for SMS notifications


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('''CREATE TABLE IF NOT EXISTS watches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        variant_id TEXT,
        name TEXT,
        store_type TEXT DEFAULT 'shopify',
        notify_channel TEXT DEFAULT 'terminal',
        notify_target TEXT,
        last_status TEXT,
        last_checked_at TEXT,
        paused INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS check_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        watch_id INTEGER REFERENCES watches(id),
        status TEXT,
        changed INTEGER DEFAULT 0,
        notified INTEGER DEFAULT 0,
        checked_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    return conn


def parse_shopify_url(url):
    parsed = urlparse(url)
    domain = parsed.hostname
    path_parts = parsed.path.strip('/').split('/')
    handle = None
    for i, part in enumerate(path_parts):
        if part == 'products' and i + 1 < len(path_parts):
            handle = path_parts[i + 1]
            break
    if not handle:
        return None
    qs = parse_qs(parsed.query)
    variant_id = qs.get('variant', [None])[0]
    return {'domain': domain, 'handle': handle, 'variant_id': variant_id}


def fetch_shopify_js(domain, handle):
    url = f'https://{domain}/products/{handle}.js'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (stock-monitor)'})
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except (URLError, json.JSONDecodeError) as e:
        print(f'Error fetching {url}: {e}', file=sys.stderr)
        return None


def check_shopify_variant(url):
    info = parse_shopify_url(url)
    if not info:
        return {'error': 'Could not parse Shopify URL', 'available': None}

    data = fetch_shopify_js(info['domain'], info['handle'])
    if not data:
        return {'error': 'Could not fetch product data', 'available': None}

    variants = data.get('variants', [])
    target_id = info['variant_id']

    if target_id:
        for v in variants:
            if str(v['id']) == str(target_id):
                return {
                    'available': v.get('available', False),
                    'title': v.get('title', 'Unknown'),
                    'price': v.get('price', '0'),
                    'product_title': data.get('title', ''),
                    'variant_id': str(v['id']),
                    'url': url,
                }
        return {'error': f'Variant {target_id} not found', 'available': None}

    results = []
    for v in variants:
        results.append({
            'available': v.get('available', False),
            'title': v.get('title', 'Unknown'),
            'price': v.get('price', '0'),
            'product_title': data.get('title', ''),
            'variant_id': str(v['id']),
        })
    return {'variants': results}


def auto_detect_name(url):
    info = parse_shopify_url(url)
    if not info:
        return None
    data = fetch_shopify_js(info['domain'], info['handle'])
    if not data:
        return None
    product_title = data.get('title', '')
    if info['variant_id']:
        for v in data.get('variants', []):
            if str(v['id']) == str(info['variant_id']):
                return f"{product_title} — {v.get('title', '')}"
    return product_title


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def send_notification(name, price, url, channel, target):
    p = float(price) / 100
    price_str = f'${p:.2f}'
    msg = f'BACK IN STOCK: {name} — {price_str}\n{url}'

    if channel == 'sms':
        phone = target or DEFAULT_PHONE
        try:
            subprocess.run(
                ['python3', SMS_SCRIPT, phone, msg],
                capture_output=True, text=True, timeout=30
            )
            print(f'  SMS sent to {phone}')
        except Exception as e:
            print(f'  SMS failed: {e}', file=sys.stderr)

    elif channel == 'slack':
        chan = target or '#general'
        try:
            subprocess.run(
                ['python3', SLACK_SCRIPT, chan, msg],
                capture_output=True, text=True, timeout=30
            )
            print(f'  Slack posted to {chan}')
        except Exception as e:
            print(f'  Slack failed: {e}', file=sys.stderr)

    else:
        print(f'  \033[32m{msg}\033[0m')


def add_watch(url, name=None, notify_channel='terminal', notify_target=None):
    db = get_db()
    info = parse_shopify_url(url)
    variant_id = info['variant_id'] if info else None
    if not name:
        name = auto_detect_name(url) or url
    db.execute(
        'INSERT INTO watches (url, variant_id, name, notify_channel, notify_target) VALUES (?, ?, ?, ?, ?)',
        (url, variant_id, name, notify_channel, notify_target)
    )
    db.commit()
    watch_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
    db.close()
    return watch_id


def remove_watch(watch_id):
    db = get_db()
    db.execute('DELETE FROM check_log WHERE watch_id = ?', (watch_id,))
    db.execute('DELETE FROM watches WHERE id = ?', (watch_id,))
    db.commit()
    db.close()


def list_watches():
    db = get_db()
    rows = db.execute('SELECT * FROM watches ORDER BY id').fetchall()
    db.close()
    return [dict(r) for r in rows]


def set_paused(watch_id, paused):
    db = get_db()
    db.execute('UPDATE watches SET paused = ? WHERE id = ?', (1 if paused else 0, watch_id))
    db.commit()
    db.close()


def run_check(watch_id=None, url=None, dry_run=False):
    db = get_db()
    results = []

    if url:
        results.append(check_shopify_variant(url))
        db.close()
        return results

    if watch_id:
        watches = db.execute('SELECT * FROM watches WHERE id = ? AND paused = 0', (watch_id,)).fetchall()
    else:
        watches = db.execute('SELECT * FROM watches WHERE paused = 0').fetchall()

    for w in watches:
        w = dict(w)
        result = check_shopify_variant(w['url'])

        if result.get('available') is None:
            results.append({'watch_id': w['id'], 'name': w['name'], 'error': result.get('error')})
            continue

        status = 'in_stock' if result['available'] else 'out_of_stock'
        prev_status = w['last_status']
        changed = prev_status is not None and prev_status != status
        back_in_stock = changed and status == 'in_stock'

        db.execute(
            'UPDATE watches SET last_status = ?, last_checked_at = ? WHERE id = ?',
            (status, now_iso(), w['id'])
        )

        notified = 0
        if back_in_stock and not dry_run:
            send_notification(
                w['name'], result.get('price', '0'), w['url'],
                w['notify_channel'], w['notify_target']
            )
            notified = 1

        db.execute(
            'INSERT INTO check_log (watch_id, status, changed, notified) VALUES (?, ?, ?, ?)',
            (w['id'], status, 1 if changed else 0, notified)
        )

        results.append({
            'watch_id': w['id'],
            'name': w['name'],
            'status': status,
            'previous': prev_status,
            'changed': changed,
            'back_in_stock': back_in_stock,
            'notified': notified == 1,
            'price': result.get('price'),
            'title': result.get('title'),
        })

    db.commit()
    db.close()
    return results
