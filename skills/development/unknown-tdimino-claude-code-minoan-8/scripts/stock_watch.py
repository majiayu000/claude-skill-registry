#!/usr/bin/env python3
"""Manage the stock monitor watchlist: add, remove, list, pause, resume."""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _stock_utils import add_watch, remove_watch, list_watches, set_paused


def cmd_add(args):
    watch_id = add_watch(
        url=args.url,
        name=args.name,
        notify_channel=args.notify,
        notify_target=args.target,
    )
    print(f'Added watch #{watch_id}: {args.url}')
    if args.name:
        print(f'  Name: {args.name}')
    print(f'  Notify: {args.notify}' + (f' → {args.target}' if args.target else ''))


def cmd_list(args):
    watches = list_watches()
    if not watches:
        print('No items being watched.')
        return
    for w in watches:
        status_icon = {'in_stock': '[IN STOCK]', 'out_of_stock': '[OUT]', None: '[?]'}.get(w['last_status'], '[?]')
        paused = ' (PAUSED)' if w['paused'] else ''
        notify = w['notify_channel']
        if w['notify_target']:
            notify += f' → {w["notify_target"]}'
        print(f'  #{w["id"]} {status_icon}{paused} {w["name"]}')
        print(f'     URL: {w["url"]}')
        print(f'     Notify: {notify}  |  Last checked: {w["last_checked_at"] or "never"}')
        print()


def cmd_remove(args):
    remove_watch(args.id)
    print(f'Removed watch #{args.id}')


def cmd_pause(args):
    set_paused(args.id, True)
    print(f'Paused watch #{args.id}')


def cmd_resume(args):
    set_paused(args.id, False)
    print(f'Resumed watch #{args.id}')


def main():
    parser = argparse.ArgumentParser(description='Manage stock monitor watchlist')
    sub = parser.add_subparsers(dest='command', required=True)

    p_add = sub.add_parser('add', help='Add a product to watch')
    p_add.add_argument('url', help='Product URL (Shopify supported)')
    p_add.add_argument('--name', help='Human-readable name (auto-detected if omitted)')
    p_add.add_argument('--notify', choices=['terminal', 'sms', 'slack'], default='terminal')
    p_add.add_argument('--target', help='Phone number (sms) or channel (slack)')

    p_list = sub.add_parser('list', help='List all watched items')

    p_rm = sub.add_parser('remove', help='Remove a watched item')
    p_rm.add_argument('id', type=int, help='Watch ID')

    p_pause = sub.add_parser('pause', help='Pause a watch')
    p_pause.add_argument('id', type=int, help='Watch ID')

    p_resume = sub.add_parser('resume', help='Resume a paused watch')
    p_resume.add_argument('id', type=int, help='Watch ID')

    args = parser.parse_args()
    {'add': cmd_add, 'list': cmd_list, 'remove': cmd_remove, 'pause': cmd_pause, 'resume': cmd_resume}[args.command](args)


if __name__ == '__main__':
    main()
