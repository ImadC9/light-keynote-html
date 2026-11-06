# Component catalogue

Every component below is styled in `assets/template.html` unless it says **(scoped recipe)**: those come with CSS to paste at the bottom of the `<style>` block, already prefixed with a slide id. Rename the id to your slide's.

Contents: Title · Statement · Divider · Cards · Banner · Facts · Pipeline · Conversation · Stepper · Practice list · Finale · Quote wall (recipe) · Before/after (recipe) · Highlighted source note (recipe) · Status rows (recipe) · Tabs that swap an example (recipe)

---

## Title
```html
<h1 class="t-title"><span class="w" style="--i:0">Working</span> <span class="w" style="--i:1">with</span> <span class="w" style="--i:2">AI<span class="dot">.</span></span><span class="caret"></span></h1>
```
Words rise one by one (`--i` = order). Follow with a `.lede`, a `.spacer`, then a `.byrow` holding `.pills` (the agenda) and `.who` (presenter).

## Statement
An `h2` plus a `.lede`, optionally a `.banner.mt-auto` at the bottom. Use `<span class="hl">` for the highlighter and `<span class="sky">` for the accent half of the headline.

## Divider
`<section class="slide divider" data-blue="1">` with `.div-num`, `.div-title`, `.div-sub`, `.div-toc` (pills listing the sections ahead).

## Cards
```html
<div class="grid g3 a" style="--d:2;margin-top:60px;flex:1">
  <div class="card"><span class="k">01 · Label</span><h3>Claim</h3><p>Explanation.</p><div class="eg"><b>Example</b>Concrete case.</div></div>
</div>
```
Variants: `.card.sky` (the one to remember), `.card.sun` (human / takeaway), `.card.coral` (risk). `.g2 .g3 .g4` set the columns. `.eg` sticks to the bottom so examples line up across cards.

## Banner
`<div class="banner">…</div>`, `.banner.sky`, `.banner.coral`. One or two lines; the bold part is the takeaway.

## Facts (count-up numbers)
```html
<div class="facts a" style="--d:2">
  <div class="fact sky"><b data-to="47" data-suf="%">0</b><p>of lines followed the ideal path.</p></div>
</div>
```
`data-pre` / `data-suf` add text around the number. Always add a `.snap` source line.

## Pipeline
```html
<div class="pipe a" style="--d:2">
  <div class="pn"><small>Input</small>What goes in</div><span class="ar"></span>
  <div class="pn ai"><small>Step</small>What happens</div><span class="ar"></span>
  <div class="pn you"><small>You</small>Human checkpoint</div>
</div>
```
`.ar` is a marching dashed arrow. Keep 3–5 boxes; beyond that use a stepper.

## Conversation (rail + chat, played with →)
```html
<div class="convo">
  <div class="rail4 a" style="--d:1">
    <div class="lit"><i></i><p><b>Ask at your level</b><span>Plain words.</span></p></div>
    <div data-at="2"><i></i><p><b>Ask why</b><span>Push until it clicks.</span></p></div>
  </div>
  <div class="chat">
    <div class="bub l frag">Assistant message</div>
    <div class="bub frag">User message</div>
    <div class="plan frag"><b>Exactly.</b> Conclusion.</div>
  </div>
</div>
```
Each `.frag` is one → press. A rail item with `data-at="n"` lights at step n, so the left column narrates the moves while the chat plays. Keep bubbles short (one or two lines): ~7 bubbles fit.

## Stepper (journey of N steps)
See slide 8 of the template. `--n` on `.stp` sets the number of nodes; include **N−1** hidden `<span class="frag" hidden></span>` so → walks through the steps. Nodes are clickable. Each panel: left = what I did / said (`.did` or a `.q` quote), right = `.hap` (what happened) + `.les` (lesson). Up to 10–11 steps fit.

## Practice list
`.prac` with `.pr` items (`<i>n</i><div><b>Imperative</b><span>Why</span></div>`). Two columns, up to 12 items. For fewer items raise `row-gap` so the slide doesn't look empty.

## Finale
`data-blue="1"`, `.finale` > `.jrn` (the journey words light up in order) + `.qa-big`.

---

## Quote wall (scoped recipe)
Several real quotes, highlighted one by one with →.
```html
<section class="slide" id="s-quotes" data-k="…" data-sec="…">
  <h2 class="a">What people actually typed.</h2>
  <div class="qw">
    <p class="a" style="--d:1" data-at="0">“First quote.”</p>
    <p class="frag" data-at="1">“Second quote.”</p>
    <p class="frag" data-at="2">“Third quote.”</p>
  </div>
</section>
```
```css
#s-quotes .qw{flex:1;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px;margin-top:60px;align-content:center}
#s-quotes .qw p{border-radius:28px;background:var(--mist);padding:40px;font-family:var(--f-disp);font-weight:700;font-size:40px;line-height:1.15;letter-spacing:-.015em}
#s-quotes .qw p{transition:background .5s} #s-quotes .qw p.lit{background:var(--sky-soft)}
```

## Before / after (scoped recipe)
```html
<div class="ba a" style="--d:2">
  <div class="was"><span class="label">Before</span><p>…</p></div>
  <div class="now frag"><span class="label">After</span><p>…</p></div>
</div>
```
```css
#s-ba .ba{flex:1;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px;margin-top:50px;min-height:0}
#s-ba .ba>div{border-radius:30px;padding:40px;display:flex;flex-direction:column;gap:18px}
#s-ba .was{background:var(--mist)} #s-ba .was p{color:var(--sub);font-size:30px;line-height:1.45}
#s-ba .now{background:var(--sky-soft)} #s-ba .now .label{color:var(--sky-ink)} #s-ba .now p{font-size:30px;line-height:1.45}
```

## Highlighted source note (scoped recipe)
A dictated brief, email or document excerpt whose key phrases highlight in sequence, numbered to match a list beside it.
```html
<div class="note a">
  <p>“… <mark style="--i:0">key phrase<sup>1</sup></mark> …”</p>
</div>
```
```css
#s-note .note{border-radius:30px;background:var(--sun-soft);padding:34px 40px}
#s-note .note p{font-size:27px;line-height:1.5}
#s-note mark{background:linear-gradient(var(--sun),var(--sun)) no-repeat 0 85%/0% 45%;color:inherit;padding:0 2px;transition:background-size .9s var(--ease);transition-delay:calc(var(--i)*.45s + 1.2s)}
#s-note.active mark{background-size:100% 45%}
#s-note mark sup{font-family:var(--f-mono);font-size:15px;color:var(--sun-ink);margin-left:3px}
```

## Status rows (scoped recipe)
Small "result" readouts inside a card: `Analysis ✓ delivered`, `Files changed 0`.
```html
<div class="rows"><div class="row">Analysis first <em class="ok">✓ delivered</em></div><div class="row">Files changed <em class="no">0</em></div></div>
```
```css
#s-x .rows{display:flex;flex-direction:column;gap:10px}
#s-x .row{display:flex;justify-content:space-between;align-items:center;border-radius:14px;background:var(--paper);padding:14px 18px;font-size:22px}
#s-x .row em{font-style:normal;font-family:var(--f-mono);font-size:18px;padding:4px 12px;border-radius:8px}
#s-x .ok{background:var(--sky-soft);color:var(--sky-ink)} #s-x .no{background:var(--coral-soft);color:var(--coral)}
```

## Tabs that swap an example (scoped recipe)
Lets the presenter switch the same structure between several real cases (e.g. one prompt template filled for five projects).
```html
<div class="tabs"><button class="tab on" data-t="a">Case A</button><button class="tab" data-t="b">Case B</button></div>
<p id="tabBody">Text for case A</p>
```
```js
(function(){
  const S=document.getElementById('s-tabs'), T={a:'Text for case A', b:'Text for case B'};
  S.querySelectorAll('.tab').forEach(b=>b.addEventListener('click',e=>{
    e.stopPropagation();
    S.querySelectorAll('.tab').forEach(x=>x.classList.toggle('on',x===b));
    S.querySelector('#tabBody').textContent=T[b.dataset.t];
  }));
})();
```
```css
#s-tabs .tabs{display:flex;gap:10px}
#s-tabs .tab{border:2px solid var(--line);background:var(--paper);border-radius:30px;padding:10px 22px;font-size:22px;color:var(--sub)}
#s-tabs .tab.on{background:var(--sky-soft);border-color:var(--sky);color:var(--sky-ink)}
```
