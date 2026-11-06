#!/usr/bin/env python3
"""Audit a light-keynote deck in a real browser.

Checks every slide in its final state (all step reveals shown) for:
  - elements that spill outside the 1920x1080 stage or into the footer zone
  - text boxes that overlap other text boxes
  - text smaller than the minimum font size (default 15px)
  - scroll-clipped containers (content cut off)
  - JavaScript errors while pressing through the whole deck with the arrow key

Usage:
  python audit.py deck.html                  # audit all slides
  python audit.py deck.html --slides 4,7-9   # only some slides (1-based)
  python audit.py deck.html --shots out/     # also save one PNG per slide + contact sheets

Needs Playwright with Chromium (pip install playwright && playwright install chromium).
Overlap reports can include false positives from tight display headings
(line-height < 1); look at the screenshot before changing anything.
"""
import argparse, asyncio, json, os, sys
from pathlib import Path
from playwright.async_api import async_playwright

PROBE = r'''(opts) => {
 const st=document.getElementById('stage'), sr=st.getBoundingClientRect(), sc=sr.width/1920;
 const s=document.querySelector('.slide.active');
 const res={out:[],overlap:[],tiny:[],clipped:[]};
 const leaves=[];
 const skip=opts.clipSel ? opts.clipSel : '[data-clip]';
 for(const el of s.querySelectorAll('*')){
   if(el.closest('.notes')||el.closest('[hidden]')) continue;
   if(el.closest('svg') && el.tagName.toLowerCase()!=='svg') continue;
   const cs=getComputedStyle(el); if(cs.display==='none'||cs.visibility==='hidden') continue;
   let op=1,p=el; while(p&&p!==s){op*=+getComputedStyle(p).opacity;p=p.parentElement;} if(op<0.05) continue;
   const r=el.getBoundingClientRect(); if(!r.width||!r.height) continue;
   const x1=(r.left-sr.left)/sc,y1=(r.top-sr.top)/sc,x2=(r.right-sr.left)/sc,y2=(r.bottom-sr.top)/sc;
   const inClip=el.closest(skip);
   const txt=(el.textContent||'').trim().replace(/\s+/g,' ').slice(0,40);
   if(!inClip && (x2>1925||y2>1030||x1<-5||y1<-5)) res.out.push({el:el.className||el.tagName,box:[x1,y1,x2,y2].map(Math.round),text:txt});
   if(!inClip && el.scrollWidth>el.clientWidth+2 && cs.overflowX!=='visible') res.clipped.push({el:el.className||el.tagName,text:txt});
   const own=[...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());
   if(own){
     const fs=parseFloat(cs.fontSize);
     if(fs<opts.minFont && !inClip) res.tiny.push({el:el.className||el.tagName,px:fs,text:txt});
     const rg=document.createRange(); rg.selectNodeContents(el); const rr=rg.getBoundingClientRect();
     leaves.push({el,fs,x1:(rr.left-sr.left)/sc,y1:(rr.top-sr.top)/sc,x2:(rr.right-sr.left)/sc,y2:(rr.bottom-sr.top)/sc,t:txt});
   }
 }
 for(let i=0;i<leaves.length;i++)for(let j=i+1;j<leaves.length;j++){
   const a=leaves[i],b=leaves[j]; if(a.el.contains(b.el)||b.el.contains(a.el)) continue;
   if(a.fs>=90&&b.fs>=90) continue; // stacked display lines overlap by design
   const ix=Math.min(a.x2,b.x2)-Math.max(a.x1,b.x1), iy=Math.min(a.y2,b.y2)-Math.max(a.y1,b.y1);
   if(ix>4&&iy>8) res.overlap.push({a:a.t,b:b.t,px:[Math.round(ix),Math.round(iy)]});
 }
 for(const k of Object.keys(res)) res[k]=res[k].slice(0,6);
 return res;
}'''

def parse_slides(spec, n):
    if not spec: return list(range(n))
    out=[]
    for part in spec.split(','):
        if '-' in part:
            a,b=part.split('-'); out+=range(int(a)-1,int(b))
        else: out.append(int(part)-1)
    return [i for i in out if 0<=i<n]

async def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('deck'); ap.add_argument('--slides'); ap.add_argument('--shots')
    ap.add_argument('--min-font',type=float,default=15)
    ap.add_argument('--clip',default='[data-clip]',help='CSS selector for containers that clip on purpose')
    ap.add_argument('--json',help='write the full report here')
    a=ap.parse_args()
    url=Path(a.deck).resolve().as_uri()
    errors=[]
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1920,'height':1100})
        pg.on('pageerror',lambda e:errors.append(f'pageerror: {e}'))
        pg.on('console',lambda m: errors.append(f'console: {m.text}') if m.type=='error' and 'fonts.g' not in m.text and 'ERR_' not in m.text else None)
        await pg.goto(url); await pg.wait_for_timeout(1500)
        n=await pg.evaluate("document.querySelectorAll('.slide').length")
        # 1. press through the whole deck
        presses=0
        for _ in range(n*20):
            if await pg.evaluate("window.__deck.current()")==n-1:
                left=await pg.evaluate("[...document.querySelectorAll('.slide.active .frag')].filter(f=>!f.classList.contains('shown')).length")
                if left==0: break
            await pg.keyboard.press('ArrowRight'); presses+=1; await pg.wait_for_timeout(40)
        reached=await pg.evaluate("window.__deck.current()")+1
        # 2. per-slide layout probe in final state
        report={}; idxs=parse_slides(a.slides,n)
        if a.shots: os.makedirs(a.shots,exist_ok=True)
        for i in idxs:
            await pg.evaluate(f"window.__show({i},true)"); await pg.wait_for_timeout(2600)
            r=await pg.evaluate(PROBE,{'minFont':a.min_font,'clipSel':a.clip})
            report[i+1]=r
            if a.shots: await pg.screenshot(path=os.path.join(a.shots,f'{i+1:03d}.png'))
        await b.close()
    print(f'slides: {n} · pressed → {presses} times · reached slide {reached}/{n}')
    print('js errors:', errors[:10] if errors else 'none')
    bad=0
    for k,r in report.items():
        issues={x:v for x,v in r.items() if v}
        if issues:
            bad+=1; print(f'\n-- slide {k}')
            for x,v in issues.items():
                for item in v: print(f'   {x}: {item}')
    print(f'\n{bad} slide(s) with findings out of {len(report)} checked.')
    if a.json: json.dump({'errors':errors,'slides':report},open(a.json,'w'),indent=1)
    if a.shots:
        try:
            from PIL import Image
            files=sorted(f for f in os.listdir(a.shots) if f[:3].isdigit() and f.endswith('.png'))
            for s in range(0,len(files),12):
                chunk=files[s:s+12]; sheet=Image.new('RGB',(3*640,4*360),'white')
                for j,f in enumerate(chunk):
                    im=Image.open(os.path.join(a.shots,f)).resize((640,366)).crop((0,0,640,360))
                    sheet.paste(im,((j%3)*640,(j//3)*360))
                sheet.save(os.path.join(a.shots,f'sheet-{s//12+1}.png'))
            print('contact sheets written to',a.shots)
        except ImportError:
            print('(install pillow for contact sheets)')
    sys.exit(1 if errors or reached!=n else 0)

asyncio.run(main())
