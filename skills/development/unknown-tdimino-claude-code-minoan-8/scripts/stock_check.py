#!/usr/bin/env python3
"""Check stock status for all watched products or a one-off URL."""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _stock_utils import run_check, check_shopify_variant


def main():
    parser = argparse.ArgumentParser(description='Check stock for watched products')
    parser.add_argument('--id', type=int, help='Check a specific watch by ID')
    parser.add_argument('--url', help='One-off check for a URL (no watchlist entry)')
    parser.add_argument('--dry-run', action='store_true', help='Check without sending notifications')
    parser.add_argument('--json', action='store_true', dest='json_out', help='JSON output')
    args = parser.parse_args()

    if args.url:
        result = check_shopify_variant(args.url)
        if args.json_out:
            print(json.dumps(result, indent=2))
        elif 'error' in result:
            print(f'Error: {result["error"]}')
            sys.exit(1)
        elif 'variants' in result:
            for v in result['variants']:
                icon = 'IN STOCK' if v['available'] else 'OUT'
                print(f'  [{icon}] {v["title"]} — ${float(v["price"])/100:.2f}')
        else:
            icon = 'IN STOCK' if result['available'] else 'OUT'
            print(f'  [{icon}] {result.get("product_title", "")} — {result["title"]} — ${float(result["price"])/100:.2f}')
        return

    results = run_check(watch_id=args.id, dry_run=args.dry_run)

    if args.json_out:
        print(json.dumps(results, indent=2, default=str))
        return

    if not results:
        print('No active watches. Use stock_watch.py add <url> to start watching.')
        return

    for r in results:
        if 'error' in r:
            print(f'  #{r.get("watch_id", "?")} ERROR: {r["error"]} — {r.get("name", "")}')
            continue

        icon = 'IN STOCK' if r['status'] == 'in_stock' else 'OUT'
        change = ''
        if r['changed']:
            if r['back_in_stock']:
                change = ' << RESTOCKED!'
                if r['notified']:
                    change += ' (notified)'
            else:
                change = ' (went out of stock)'

        print(f'  #{r["watch_id"]} [{icon}] {r["name"]}{change}')


if __name__ == '__main__':
    main()
