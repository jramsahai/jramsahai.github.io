# Site Review Fixes

Date: 2026-09-20

Outcome of a structure / performance / quality review of the whole site. The
architecture in the design spec (plain static HTML, no build step, header and
footer duplicated per page) is kept as-is. Everything below works within it.

## Findings

| # | Severity | Finding |
|---|----------|---------|
| F1 | High | `404.html` has drifted from the shared chrome: footer still carries placeholder links (`mailto:you@example.com`, `linkedin.com/in/your-handle`), header text differs from every other page, and the font preload is missing. |
| F2 | Medium | `index.html` has no `<h1>`. The only one is inside the commented-out hero. The spec requires one per page. |
| F3 | Medium | Nothing guards against chrome/head drift, broken internal links, wrong image dimensions, or leftover placeholders. F1 is exactly the bug class that duplication without a check produces. |
| F4 | Low | Carousel autoplay can stall silently on touch devices: a tap on a slide fires a compatibility `mouseenter` with no matching `mouseleave`, so `hovering` stays true while the toggle still shows "pause". |
| F5 | Low | Project page `<title>`s are the bare project name ("Blasterscribe"), so tabs, history and search results carry no site identity. |
| F6 | Low | No `theme-color` meta, so Chrome on Android paints a light toolbar over a dark site. |
| F7 | Low | The video figure plus its reduced-motion inline script is copy-pasted on three pages but is not in the project template, so the next video page will be copied from a sibling page rather than the canonical source. Same for the carousel markup. |
| F8 | Trivial | `.empty` in `style.css` is unused. `.playwright-mcp/` is untracked and not ignored, so it is one `git add .` away from being committed. |

Reviewed and deliberately left alone: media encoding (MP4s are faststart,
no audio track, sane bitrates; all WebP under the 300 KB budget), the inline
reduced-motion script staying inline (it must run before autoplay starts, a
deferred external file would not), CSS size (12 KB, gzipped by Pages),
`sitemap.xml` (11 fully interlinked pages, not worth another file to keep in
sync).

## Rules for both work packages

- Do not commit. Leave changes in the working tree.
- Do not touch files owned by the other package.
- Match the surrounding code style (2-space indent, ES5 `var` in
  `carousel.js`, comment density of `style.css`).
- Do not change any page copy other than what is listed here.

## Work package A: page, CSS and JS fixes

Owns: `index.html`, `404.html`, `projects/*/index.html`,
`docs/templates/project-page.html`, `assets/css/style.css`,
`assets/js/carousel.js`.

### A1. Repair 404.html (F1)

- Header link text becomes `Jivan Ramsahai - Product Builder Portfolio`.
- Replace the whole `<footer class="site-footer">…</footer>` block with a
  byte-for-byte copy of the one in `index.html` (LinkedIn + GitHub, no
  email item).
- Add the font preload line immediately before the stylesheet link, copied
  byte-for-byte from `index.html`.
- Verify: `awk '/<footer/,/<\/footer>/' 404.html | md5` equals the same
  command on `index.html`; same for
  `awk '/<header class="site-header">/,/<\/header>/'`.

### A2. Give the landing page an h1 (F2)

- In `style.css`, at the end of the Base section, add the standard utility:

  ```css
  .visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    margin: -1px;
    padding: 0;
    overflow: hidden;
    clip-path: inset(50%);
    white-space: nowrap;
    border: 0;
  }
  ```

- In `index.html`, as the first child of `<main class="container">`, above
  the commented-out hero, add:

  ```html
  <!-- Stands in for the hero below. Delete this h1 if the hero comes back. -->
  <h1 class="visually-hidden">Jivan Ramsahai - Product Builder Portfolio</h1>
  ```

- The h1 is now the first child of `main`, which breaks
  `main > .section:first-child { padding-top: 0; }`. Change that selector to
  `main > .section:first-of-type`. (The About block is the first `<section>`
  in `main`; the h1 is not a `section`, so this keeps the current spacing.)
- Leave the commented-out hero itself untouched.

### A3. theme-color (F6)

Add `<meta name="theme-color" content="#0A0A0A">` on the line directly after
the viewport meta in all 12 pages (`index.html`, `404.html`, 10 project
pages) and in the template.

### A4. Title suffix (F5)

- Each of the 10 project pages: `<title>NAME</title>` becomes
  `<title>NAME - Jivan Ramsahai</title>`. `og:title` stays the bare name.
- `404.html`: `<title>Page not found - Jivan Ramsahai</title>`.
- Template: `<title>PROJECT TITLE - Jivan Ramsahai</title>`, and extend
  how-to step 6 to say the title keeps the ` - Jivan Ramsahai` suffix while
  `og:title` is the bare project name.
- `index.html` title is unchanged.

### A5. Carousel touch-hover fix (F4)

In `assets/js/carousel.js`, replace the `mouseenter` / `mouseleave`
listeners with `pointerenter` / `pointerleave` that ignore non-mouse
pointers:

```js
root.addEventListener('pointerenter', function (e) {
  if (e.pointerType !== 'mouse') return;
  hovering = true;
  sync();
});
root.addEventListener('pointerleave', function (e) {
  if (e.pointerType !== 'mouse') return;
  hovering = false;
  sync();
});
```

Add a one-line comment saying why (a tap fires a synthetic mouseenter with
no mouseleave, which would stall autoplay). Change nothing else in the file.
Verify with `node --check assets/js/carousel.js` if node is available.

### A6. Template carries the video and carousel snippets (F7)

In the how-to comment at the top of `docs/templates/project-page.html`, add
steps (renumber as needed) covering:

- **Video**: MP4 (H.264, no audio track, `-movflags +faststart`) plus a WebP
  poster in `/assets/images/<slug>/`. Include the canonical markup, copied
  from `projects/wayfinder/index.html`: the `<figure>` with
  `<video autoplay muted loop playsinline controls preload="metadata"
  poster=… width=… height=… aria-label=…>`, its `<source>`, the
  `<figcaption>`, and the inline reduced-motion `<script>` that must directly
  follow the figure and must stay inline (it has to run before autoplay
  begins). Replace the wayfinder-specific paths and text with placeholders.
  Mention `class="portrait"` on the figure for phone video.
- **Carousel**: copy the `<section class="carousel" …>` block from
  `projects/video-impact-reports/index.html` (landscape) or
  `projects/blasterscribe/index.html` (portrait, adds `carousel-portrait`),
  and add `<script src="/assets/js/carousel.js" defer></script>` to the head.
  Keep each slide's `aria-label="N of TOTAL"` in step with the slide count.
- **Final step before deleting the comment**: run `python3 scripts/check.py`
  from the repo root and fix anything it reports.

An HTML comment must not contain `--`; check the pasted snippet does not.

### A7. Remove dead CSS (F8)

Delete the `.empty` rule from `style.css`.

### A verification

- Serve with `python3 -m http.server 8000` from the repo root and load `/`,
  `/404.html`, `/projects/blasterscribe/`, `/projects/wayfinder/`. If browser
  tooling is unavailable, at minimum `curl` each and confirm 200.
- `grep -c '<meta name="theme-color"' index.html 404.html projects/*/index.html docs/templates/project-page.html`
  is 1 for every file.
- `grep -rn 'example.com\|your-handle' index.html 404.html projects` returns
  nothing.
- Header and footer md5s (commands in A1) are identical across all 12 pages
  and the template.

## Work package B: drift check and repo hygiene

Owns: `scripts/check.py` (new), `_config.yml`, `.gitignore`, `README.md`.

### B1. scripts/check.py (F3)

Python 3, standard library only, run from the repo root as
`python3 scripts/check.py`. Prints one line per problem as
`path: message`, a final summary line, and exits 1 if there were any errors
(0 otherwise). Warnings do not affect the exit code. Keep it a single
readable file, no classes needed, under ~250 lines.

Published pages = `index.html`, `404.html`, `projects/*/index.html`.
Template = `docs/templates/project-page.html`.

Strip HTML comments (`<!-- … -->`, DOTALL) from page text before running any
check below, so the commented-out hero and the template how-to are ignored.
Regex-based parsing is fine for this hand-written markup; do not add an HTML
parser dependency.

Errors:

1. **Chrome drift.** The `<header class="site-header">…</header>` block and
   the `<footer class="site-footer">…</footer>` block of every published
   page and the template are byte-identical to those in `index.html`.
2. **Shared head lines.** Every published page and the template contains
   each of these exact lines as they appear in `index.html`: charset meta,
   viewport meta, theme-color meta, the three icon links, the font preload
   link, the stylesheet link. (Read them out of `index.html` by matching
   those tags rather than hardcoding the strings.)
3. **One h1.** Exactly one `<h1` per published page.
4. **Head metadata.** Every published page has a non-empty `<title>`,
   `meta description`, `canonical`, `og:title`, `og:description`, `og:url`,
   `og:image`. `canonical` and `og:url` are equal and match the file's path
   (`https://jramsahai.github.io/` for `index.html`,
   `…/404.html` for `404.html`, `…/projects/<slug>/` for project pages).
   `og:image` starts with `https://jramsahai.github.io/` and the path after
   the host exists on disk.
5. **Internal references resolve.** Every root-absolute `href`, `src` and
   `poster` value (starts with `/`, not `//`) in published pages, with any
   `#fragment` removed, exists on disk; a path ending in `/` resolves to
   its `index.html`. Also check `url("/…")` references in
   `assets/css/style.css`. If an href has a fragment pointing at another
   published page, the target page contains `id="<fragment>"`.
6. **Cards and pages agree.** The set of `/projects/<slug>/` hrefs inside
   `index.html` equals the set of directories under `projects/` that contain
   an `index.html`.
7. **No placeholders in published pages.** None of: `example.com`,
   `your-handle`, `PROJECT TITLE`, `ONE-LINE DESCRIPTION`, `<slug>`, `YEAR<`.
8. **Images.** Every `<img` in published pages has non-empty-or-present
   `alt`, plus `width` and `height`. For `.webp` and `.png` sources, the
   attributes equal the file's real pixel size. Read sizes with `struct`:
   PNG from IHDR; WebP for all three chunk types (`VP8 ` lossy: 14-bit
   width/height at bytes 26-29 after the `9d 01 2a` start code; `VP8L`:
   14-bit fields packed after the `0x2f` signature byte, each +1; `VP8X`:
   24-bit little-endian canvas width-1 and height-1 at bytes 24-29). Same
   check for `<video>` `poster` against its `width`/`height` **aspect
   ratio** only (posters may be a different resolution than the video;
   tolerate 1% difference).
9. **Carousel slide labels.** Within each `<section class="carousel…">`,
   the slides' `aria-label="N of M"` values run 1..M and M equals the number
   of slides. Any page containing `class="carousel` includes the
   `/assets/js/carousel.js` script tag, and pages without a carousel do not.

Warnings:

10. Any file under `assets/images/` that is `.webp`, `.png` or `.jpg` and
    larger than 300 KB (the spec's budget). Any `.mp4` larger than 4 MB.
11. Any image file under `assets/images/` not referenced by any published
    page (og images count as referenced).

Note for whoever runs it: until work package A lands, checks 1, 2 and 7 are
expected to fail on `404.html` and check 2 on every page (theme-color) and
check 3 on `index.html`. That is the script working, not a bug in it. Do not
"fix" those pages; they belong to package A. Do confirm that every *other*
check passes against the current tree, and sanity-test the failure paths by
running the functions against a temporary broken copy under a temp directory
(not inside the repo).

### B2. Keep scripts/ out of the published site

Add `- scripts/` to the `exclude` list in `_config.yml`.

### B3. .gitignore (F8)

Add `.playwright-mcp/`.

### B4. README

Add a short "Checks" section after "Local preview": run
`python3 scripts/check.py` before pushing; one sentence on what it covers
(shared header/footer/head drift, broken internal links, image dimensions,
leftover template placeholders). Update the Publishing note to say
`_config.yml` also keeps `scripts/` out of the published site.

## After both packages

Run `python3 scripts/check.py` from the repo root. It must exit 0. Then do
the spec's visual verification on `/`, `/404.html`, one carousel page and
one video page.
