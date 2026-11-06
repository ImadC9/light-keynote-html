---
name: light-keynote-html
description: Build visually stunning, animated HTML presentations in a light "keynote" style — white paper, one sky-blue signature colour, a yellow highlighter, big display type, one idea per slide, step-by-step reveals, presenter notes and an animations on/off toggle, all in one self-contained HTML file. Use this skill whenever someone asks for a presentation, slide deck, keynote, workshop, training session, talk, pitch or "slides" and wants it in HTML, animated, interactive, impressive or "like a keynote" — and also when they hand over notes, a markdown outline or a document and say "turn this into a presentation", even if they never say HTML. Prefer it over PowerPoint output unless a .pptx file is explicitly required.
---

# Light keynote HTML decks

This skill produces decks that look like a well-designed keynote: calm white slides, huge confident headlines, a single accent colour, and motion that tells the story instead of decorating it. It was distilled from a ~100-slide workshop deck that went through many rounds of real feedback, so the rules below are the ones that survived contact with an actual audience and a picky presenter.

Everything lives in **one HTML file**: a 1920×1080 stage that scales to any screen, keyboard navigation, step reveals, presenter notes, and an animations toggle. `assets/template.html` contains the engine, the design system and ten example slides — always start from it rather than writing a deck engine from scratch.

## Workflow

1. **Get the content right before any design.** Read the source material fully. Decide the narrative: parts → sections → slides. Write a one-line outline per slide (headline + the one thing it proves). Share the outline for a long deck before building; for a short one, build and show.
2. **Copy `assets/template.html`** to the output location. Keep the `<style>` base, the controls and the `<script>` engine. Delete the example slides you don't use; copy the ones you need.
3. **Build in batches** (one part or ~10 slides at a time), auditing after each batch. A long deck written in one pass is where spacing errors pile up.
4. **Audit** with `python scripts/audit.py deck.html --shots shots/` (Playwright + Chromium). Look at the contact sheets yourself, fix what's wrong, re-run. See "Checking your work".
5. **Deliver.** If the deck references local images/video, run `python scripts/inline_assets.py deck.html -o deck-final.html` so it's a single file that works when emailed or opened offline.

Read `references/components.md` when you need a component beyond the basics, and `references/slide-patterns.md` when choosing how to visualise an idea.

## Design system

### Palette and roles
| Token | Hex | Use for |
|---|---|---|
| `--paper` | #FFFFFF | slide background |
| `--mist` / `--mist-2` | #F2F5F7 / #E8EEF2 | neutral cards, tracks, rails |
| `--ink` | #0F1B26 | headlines, body text, small user chat bubbles |
| `--sub` / `--faint` | #5A6B7B / #93A2AF | secondary text, labels |
| `--sky` / `--sky-ink` / `--sky-soft` | #42B0D5 / #0E78A6 / #E3F3F9 | the signature: accent words, active states, highlighted card, divider backgrounds |
| `--sun` / `--sun-soft` | #FFD84D / #FFF3BF | highlighter, the "you / human" element, banners, lessons |
| `--coral` / `--coral-soft` | #F2553A / #FDE9E4 | warnings, wrong answers, risks — nothing else |

Why this works: with one accent colour, every use of sky means "look here". Yellow is the human (you, your judgment, the takeaway). Coral is reserved so a warning actually reads as one.

**Keep it light.** No dark slide backgrounds, no large black or dark-navy panels, no dark themes: presenters using this style find them hard on the eye and projectors wash them out. The only full-bleed colour is the sky-blue section divider (`data-blue="1"`). Navy (`--navy`) is for text on sky only.

**No 3D** (three.js, WebGL scenes) unless the user explicitly asks. It's slow on work laptops, rarely explains anything better than a 2D diagram, and was the most-rejected element in the source deck. Prefer SVG, CSS and HTML.

### Typography
- Display: **Bricolage Grotesque** 800, tight tracking (`letter-spacing:-.025em` to `-.05em`). Body: **Onest**. Labels, data, code: **IBM Plex Mono**, uppercase with wide tracking for labels.
- Scale on the 1920×1080 stage: title 236px · divider 250px · slide headline (`h2`) 84–104px · card heading 40–44px · lede 30–38px · body 22–28px · labels 18–20px. **Nothing below 15px** — the audit flags it, and people at the back of the room can't read it.
- Headlines are short sentences ending with a full stop. They make a claim ("Three phrases that kept me in control."), not a topic ("Control"). Put the key words in `<span class="sky">` or `<span class="hl">`.
- A headline should fit on one line, two at most. If it wraps to two, check nothing below is pushed off the slide; lower the size via inline `style="font-size:84px"` rather than letting it crowd the content.

### Layout and spacing
- The content box is fixed: 150px side margins, 150px top, 120px bottom → **1620×810px** usable. The kicker (section badge + title), page number and progress rail sit in the margins automatically.
- Each slide is a flex column: headline, optional lede, then one main visual that takes the remaining space (`flex:1;min-height:0`), then optionally a banner or takeaway at the bottom (`.mt-auto`).
- Generous gaps: 40–70px between headline and visual, 20–30px between cards. Rounded corners 18–30px. No borders on cards — tinted backgrounds separate them.
- Grids use `repeat(n,minmax(0,1fr))` so long words can't blow out a column.
- **Fill the box.** The main visual should use the height it's given. If the content ends in the top half of the slide, scale it up (larger type and cards, taller rows) or centre it vertically with `align-content:center`; a projected slide with a small block at the top and an empty bottom half looks unfinished. This was the most common flaw when testing the skill.

### Motion
Motion should reveal the order of an idea. The template gives you three mechanisms:
- **Entrance**: add class `a` and a stagger `style="--d:2"` (each unit ≈110ms). Elements rise in with a soft blur when the slide opens. Use `drop` for a bouncy drop-in.
- **Steps**: any element with class `frag` stays hidden until the presenter presses →. The slide gets `data-step="n"`, so CSS like `#s-x[data-step="2"] .thing{…}` can react, and elements with `data-at="2"` get class `lit` from step 2. Use steps for conversations, reveals, "before/after" and quizzes — whenever the presenter wants to talk before the next thing appears.
- **Ambient**: small loops (marching dashed arrows, a blinking caret, a pulsing node) under `.slide.active` only, so nothing runs on hidden slides.

Rules that came out of real feedback:
- Animations are **on by default for everyone**. The template deliberately ignores the OS "reduce motion" setting and gives an explicit **Animations: On/Off** button (and the A key) instead, remembered per browser. Every animated element must still look right when motion is off: final state at rest, animation only on entry.
- Don't put `a` and `frag` on the same element: the entrance animation's fill mode overrides the hidden state, so the step shows immediately. Wrap one inside the other.
- Never animate something into a state that differs from its resting layout (e.g. a keyframe ending in `transform:none` will cancel a positioning `translate()`); put the animation on an inner element instead.
- Count-ups: `<b data-to="208" data-suf="k">0</b>` animates the number when the slide opens.

### Content rules
- **One idea per slide.** A second idea gets a second slide.
- Prefer showing over telling: a conversation playing out, a pipeline, a before/after, real quotes, a small interactive control — rather than a bullet list. Lists are fine for a closing "what to copy" slide.
- **Use the audience's world.** Examples, numbers and names should come from their domain (their tools, their processes, their data), not generic placeholders.
- Real quotes beat paraphrases. If the source has the actual words someone used, put them on the slide in quotation marks.
- **Never invent data.** Illustrative numbers must be labelled (`<span class="snap">Illustrative · arithmetic checked</span>`), arithmetic in examples must be correct, and dated facts (prices, rankings, versions) carry a "snapshot as of <date>" label.
- Avoid redundancy across the deck: the same example or lesson told on several slides in different outfits is the most common flaw in long decks. Each slide must earn its place; when reviewing, look for repeated stories across sections and parts, not just neighbouring slides.
- Every slide gets presenter notes in `<aside class="notes">` (press N). Write what to say and what to click, not a copy of the slide.

## Building slides

Slide skeleton:
```html
<section class="slide" id="s-short-name" data-k="Section · Slide title" data-sec="2">
  <h2 class="a">Headline that makes a claim.</h2>
  <p class="lede a" style="--d:1;margin-top:30px">One supporting sentence, <b>with the key part bold</b>.</p>
  <div class="… a" style="--d:2;flex:1;min-height:0"> main visual </div>
  <aside class="notes"><p>What to say.</p></aside>
</section>
```
- `data-k` fills the kicker at the top-left; `data-sec` fills its round badge (section number or letter).
- `data-blue="1"` turns the page sky blue (dividers, finale).
- Give every slide a unique `id` starting with `s-`.

### Scope your CSS — the most important engineering rule
Put slide-specific CSS at the bottom of the `<style>` block and **prefix every selector with the slide's id** (`#s-ladder .rung{…}`). In the source deck, two unscoped rules caused the worst bugs: a new slide's `.gate` rule silently pulled a box out of a pipeline on another slide, and a new `.ctl` class collided with the viewer's control buttons. Before inventing a class name, search the file for it. Reuse template components as-is; anything new is scoped.

### Interactivity
Small interactive pieces make a deck feel alive: tabs that swap an example, a stepper you can click, a slider, a toggle. Wire them inside the engine's IIFE pattern or a separate `<script>` after it, listen to the slide's `stepchange` / `slideenter` events, and call `e.stopPropagation()` on clicks so they don't advance the deck. Media: `<video muted loop playsinline>` inside a slide auto-plays when the slide opens and pauses when it leaves.

## Checking your work

Run after every batch and before delivering:
```bash
python scripts/audit.py deck.html --shots shots/
```
It presses → through the whole deck (catching JS errors and stuck steps), then shows every slide in its final state and reports: elements spilling off the stage or into the footer, overlapping text, text under 15px, and clipped containers. Mark containers that clip on purpose with `data-clip`.

Then **look at the contact sheets** (`shots/sheet-*.png`) — the script can't judge balance. Check that:
- each slide uses its height (no block stuck in the top half with empty space below)
- the headline doesn't crowd the visual and nothing sits under the bottom banner
- cards in a row line up (equal heights, bottoms aligned)
- the slide isn't half-empty; if it is, enlarge the visual or add breathing room deliberately
- step reveals end in a sensible final state

Fix, re-run, and only then deliver. When you change one slide, re-check slides that share its components.

## Delivering

- One `.html` file. Fonts load from Google Fonts; offline it falls back to system fonts gracefully.
- Local images/video: `python scripts/inline_assets.py deck.html -o final.html` (add `--cdn` to also inline remote scripts).
- Email filters often strip `.html` attachments: suggest zipping it or sharing via a drive link.
- If the environment can publish HTML pages (e.g. an artifact tool), publish it so the user gets a link, and also hand over the file.
- For a different audience (e.g. management instead of the team), make a **copy** with audience-specific changes rather than editing the original, and renumber sections if slides are removed.
