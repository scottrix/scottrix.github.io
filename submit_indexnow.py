#!/usr/bin/env python3
"""
submit_indexnow.py - Bulk-submit URLs to IndexNow (Bing, Yandex, Seznam, Naver).

All five scottrix.github.io subsites (root, /devtools/, /fintools/, /gcserevise/, /EasyPlayTV-docs/)
live on the same host, so a single key file at the root covers every URL.

Usage:
    python3 submit_indexnow.py          # submit ALL known URLs
    python3 submit_indexnow.py --dry    # show plan, don't POST
    python3 submit_indexnow.py --delta [path1 path2 ...]
                                        # submit only the URLs in the given
                                        # local file paths (relative to one
                                        # of the repo roots), mapping each
                                        # path to its public URL.

The IndexNow key file is at https://scottrix.github.io/a07cbf5c3cc787b087a172571cf323c7.txt
and contains the value `a07cbf5c3cc787b087a172571cf323c7`.

IndexNow API limits: 10,000 URLs per request, max 1 request per ~10 minutes.
This script batches URLs in groups of 10,000 with a 60s pause between batches.
"""
import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

KEY = 'a07cbf5c3cc787b087a172571cf323c7'
KEY_LOCATION = f'https://scottrix.github.io/{KEY}.txt'
API_ENDPOINT = 'https://api.indexnow.org/IndexNow'
BASE = 'https://scottrix.github.io'
BATCH_SIZE = 10000

# Local repo roots and how their files map to public URLs.
REPO_ROOTS = [
    (Path('/home/scott/src/scottrix.github.io'), ''),
    (Path('/home/scott/src/devtools'),           '/devtools'),
    (Path('/home/scott/src/fintools'),           '/fintools'),
    (Path('/home/scott/src/gcserevise'),         '/gcserevise'),
    (Path('/home/scott/src/EasyPlayTV-docs'),     '/EasyPlayTV-docs'),
]


def enumerate_all_urls():
    """Walk every *.html file in every repo root, map to its public URL.

    Returns a sorted list of unique URLs.
    For directory roots, the file index.html maps to the directory URL ending /.
    For other files, .html is preserved (matching the canonical URL form).
    """
    urls = set()
    for repo, subpath in REPO_ROOTS:
        for p in sorted(repo.rglob('*.html')):
            rel = p.relative_to(repo).as_posix()
            # Skip files not served at top-level of GitHub Pages (e.g. backups).
            if rel.startswith('.') or '/__pycache__/' in rel:
                continue
            # Skip Google/Bing site-verification files (not user-facing content).
            name = p.name
            if name.startswith('google') and name.endswith('.html'):
                continue
            if name == 'BingSiteAuth.xml':
                continue
            # index.html -> directory URL
            if rel == 'index.html':
                public = f'{BASE}{subpath}/'
            elif rel.endswith('/index.html'):
                public = f'{BASE}{subpath}/{rel[:-len("/index.html")]}/'
            else:
                public = f'{BASE}{subpath}/{rel}'
            urls.add(public)
    return sorted(urls)


def paths_to_urls(paths):
    """Map local file paths (relative to a repo root) to public URLs.

    Each given path is checked against every repo root; the first match wins.
    """
    urls = set()
    for arg in paths:
        p = Path(arg).resolve()
        matched = False
        for repo, subpath in REPO_ROOTS:
            try:
                rel = p.relative_to(repo).as_posix()
            except ValueError:
                continue
            matched = True
            # Skip Google/Bing verification files.
            name = p.name
            if name.startswith('google') and name.endswith('.html'):
                print(f'  SKIP verification file: {arg}')
                break
            if rel == 'index.html':
                public = f'{BASE}{subpath}/'
            elif rel.endswith('/index.html'):
                public = f'{BASE}{subpath}/{rel[:-len("/index.html")]}/'
            else:
                public = f'{BASE}{subpath}/{rel}'
            urls.add(public)
            break
        if not matched:
            print(f'  WARN: {arg} does not live under any known repo root - skipped')
    return sorted(urls)


def submit_batch(url_list, dry):
    """POST a batch of URLs (<=10000) to IndexNow. Returns the HTTP status code."""
    body = {
        'host': 'scottrix.github.io',
        'key': KEY,
        'keyLocation': KEY_LOCATION,
        'urlList': url_list,
    }
    if dry:
        print(f'  DRY-RUN: would POST {len(url_list)} URLs to {API_ENDPOINT}')
        print(f'    sample: {url_list[0]}')
        if len(url_list) > 1:
            print(f'    sample: {url_list[-1]}')
        return 200  # pretend success

    data = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(
        API_ENDPOINT,
        data=data,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            status = resp.status
            print(f'  HTTP {status} - OK ({len(url_list)} URLs accepted)')
    except urllib.error.HTTPError as e:
        status = e.code
        body_text = e.read().decode('utf-8', errors='replace')
        print(f'  HTTP {status} - {e.reason}')
        print(f'    body: {body_text[:300]}')
    except Exception as e:
        status = 0
        print(f'  NETWORK ERROR: {e}')
    return status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true', help='Plan-only, do not POST')
    ap.add_argument('--delta', nargs='*', default=None,
                    help='Submit only URLs mapped from the given local file paths')
    args = ap.parse_args()

    if args.delta is not None:
        if not args.delta:
            print('--delta requires at least one path')
            sys.exit(2)
        urls = paths_to_urls(args.delta)
        print(f'Delta mode: {len(urls)} URL(s) mapped from given paths')
    else:
        urls = enumerate_all_urls()
        print(f'Full mode: {len(urls)} URL(s) enumerated across 5 repo roots')

    if not urls:
        print('No URLs to submit. Exiting.')
        return

    print(f'\nKey location: {KEY_LOCATION}')
    print(f'API endpoint: {API_ENDPOINT}')
    print(f'Batch size:   {BATCH_SIZE}')

    total_batches = (len(urls) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f'Batches:      {total_batches}\n')

    overall_ok = True
    for i in range(0, len(urls), BATCH_SIZE):
        batch = urls[i:i + BATCH_SIZE]
        bn = i // BATCH_SIZE + 1
        print(f'Batch {bn}/{total_batches} ({len(batch)} URLs):')
        status = submit_batch(batch, args.dry)
        if status != 200:
            overall_ok = False
        if i + BATCH_SIZE < len(urls):
            print('  Pausing 60s before next batch (rate-limit courtesy)...')
            time.sleep(60)

    print(f'\nDone. {"All batches OK." if overall_ok else "Some batches failed - see above."}')
    if not args.dry and overall_ok:
        print('Verify in Bing Webmaster Tools -> URL Submission -> IndexNow.')


if __name__ == '__main__':
    main()
