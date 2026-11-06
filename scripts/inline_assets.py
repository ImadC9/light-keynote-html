#!/usr/bin/env python3
"""Make a deck a single, self-contained file you can email or open offline.

Inlines, as data URIs or inline code:
  - local files in src="..." / poster="..." / href="....css" (images, video, audio, scripts, stylesheets)
  - with --cdn: <script src="https://..."> files (downloaded once) so the deck works with no network

Google Fonts stay as a <link>: offline, the deck falls back to system fonts, which the
font stacks in the template are chosen for.

Usage: python inline_assets.py deck.html -o deck-standalone.html [--cdn]
"""
import argparse, base64, mimetypes, re, sys, urllib.request
from pathlib import Path

def data_uri(path):
    mt=mimetypes.guess_type(str(path))[0] or 'application/octet-stream'
    return f'data:{mt};base64,'+base64.b64encode(path.read_bytes()).decode()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('deck'); ap.add_argument('-o','--out',required=True)
    ap.add_argument('--cdn',action='store_true',help='also inline remote <script src> files')
    a=ap.parse_args()
    src=Path(a.deck); base=src.parent; html=src.read_text(encoding='utf-8'); n=0

    def local(m):
        nonlocal n
        attr,val=m.group(1),m.group(2)
        if re.match(r'^(https?:|data:|#|mailto:|javascript:)',val): return m.group(0)
        p=(base/val).resolve()
        if not p.is_file(): print('missing:',val,file=sys.stderr); return m.group(0)
        n+=1; return f'{attr}="{data_uri(p)}"'
    # local stylesheets -> <style>
    def css(m):
        nonlocal n
        val=m.group(1)
        if val.startswith('http'): return m.group(0)
        p=(base/val).resolve()
        if not p.is_file(): return m.group(0)
        n+=1; return '<style>'+p.read_text(encoding='utf-8')+'</style>'
    html=re.sub(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"[^>]*>',css,html)
    # local scripts -> inline
    def js(m):
        nonlocal n
        val=m.group(1)
        if val.startswith('http'):
            if not a.cdn: return m.group(0)
            code=urllib.request.urlopen(val).read().decode('utf-8')
        else:
            p=(base/val).resolve()
            if not p.is_file(): return m.group(0)
            code=p.read_text(encoding='utf-8')
        n+=1; return '<script>'+code.replace('</script','<\\/script')+'</script>'
    html=re.sub(r'<script[^>]*\ssrc="([^"]+)"[^>]*>\s*</script>',js,html)
    html=re.sub(r'\b(src|poster)="([^"]+)"',local,html)
    Path(a.out).write_text(html,encoding='utf-8')
    print(f'inlined {n} asset(s) -> {a.out} ({len(html)/1e6:.2f} MB)')

main()
