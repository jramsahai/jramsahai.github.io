# Site Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the portfolio site skeleton: landing page, 404 page, stylesheet, self-hosted fonts, icons, social image, and a project page template, so that individual project pages can be added one at a time afterwards.

**Architecture:** Plain static HTML and CSS served by GitHub Pages from the repo root. No JavaScript is needed for the skeleton, so there is no `assets/js/` directory. Every page carries its own full `<head>` and a duplicated header/footer. All asset URLs are root-absolute (`/assets/...`) so pages at any depth resolve them identically on GitHub Pages and on a local server started from the repo root.

**Tech Stack:** HTML5, CSS (custom properties, grid, `clamp()`), two self-hosted variable/static woff2 fonts from Fontsource (OFL licensed), headless Chrome for screenshots and PNG generation, `python3 -m http.server` for local preview, Lighthouse via `npx` for the final check.

**Spec:** `docs/superpowers/specs/2026-09-17-portfolio-site-design.md`

## Global Constraints

Copied from the spec. Every task's requirements include these.

- Dark theme only. `color-scheme: dark` is set on `:root`.
- Colours: background `#0A0A0A`, text `#F5F5F5`, primary accent `#3388FF`, secondary accent warm amber for the `Personal` tag.
- Tag values are exactly `Vidyard` and `Personal`, marked up with `data-tag="vidyard"` / `data-tag="personal"`.
- Fonts are self-hosted `woff2` under `assets/fonts/` with `font-display: swap`. No runtime requests to any third-party host, anywhere, for anything.
- Every motion effect sits inside `@media (prefers-reduced-motion: no-preference)`.
- Semantic landmarks (`header`, `nav` where there is navigation, `main`, `footer`), exactly one `h1` per page, visible focus styles, WCAG AA contrast.
- No all-caps text, no `→` glyphs in link text, no eyebrow labels above headings, no numbered markers.
- Every `<img>` has explicit `width` and `height`; images below the fold have `loading="lazy"`.
- Every page has: unique `<title>`, `<meta name="description">`, canonical link, Open Graph tags (`og:type`, `og:title`, `og:description`, `og:url`, `og:image`), `twitter:card`, viewport meta, `lang="en"`, favicon links.
- Header is a single link (site owner's name) back to `/`. Footer is contact links plus a copyright line.
- No project card may link to a page that does not exist. The skeleton ships with zero cards and an empty-state line.
- The `docs/` directory is served locally but excluded from GitHub Pages by `_config.yml`, which already exists. Do not create `.nojekyll`.
- Commit after every task with a message in imperative mood. Do not push until the final task says to.

## Design decisions locked by this plan

The spec left fonts and card interaction to implementation. This plan locks them:

- **Display and body face:** Bricolage Grotesque (variable, weights 200 to 800). Headlines at 800 with tight tracking; body at 400.
- **Subhead face:** Instrument Serif, italic only. Used for the one-line lede under each `h1` and for the empty-state line. It is the "lighter or italic subhead" from the spec, and a serif italic against a heavy grotesk is a clearer contrast than a light weight of the same family.
- **Micro-label face:** system monospace stack (`ui-monospace`, SF Mono, Menlo, Consolas). No font file needed.
- **Secondary accent:** `#F5A524` (amber). Contrast against `#0A0A0A` is about 9.7:1. The primary `#3388FF` is about 5.8:1, which passes AA for normal text.
- **Card interaction:** cards are cells in a hairline grid (1px `gap` over a line-coloured background), not floating rounded cards. On hover, the cell background lifts to `#141414` and the title takes the card's tag colour (blue for Vidyard, amber for Personal). That is the only motion on the site.
- **Hero:** the memorable element is the headline type itself, set very large at weight 800, with the italic serif lede beneath. Nothing else on the page competes with it.
- **Copy:** first-draft copy is written into the pages below. It is real content, not lorem ipsum, and the site owner is expected to edit it.
- **Contact links:** the GitHub link is real. The email and LinkedIn hrefs are set to obviously-fake placeholders (`you@example.com`, `linkedin.com/in/your-handle`) because those values were not provided and must not be guessed. The final report must call this out.

## Working setup (read before Task 1)

- Repo root: `/Users/jramsahai/github/jramsahai.github.io`. Run everything from there.
- Scratch directory for screenshots and downloads: `/private/tmp/claude-501/-Users-jramsahai-github-ji-portfolio/d55533d3-632f-44df-a229-08fd6284e577/scratchpad`. Call it `$SCRATCH` below; export it at the start of each shell command that uses it.
- Local server (start once, in the background, leave it running):

```bash
cd /Users/jramsahai/github/jramsahai.github.io && python3 -m http.server 8765 --bind 127.0.0.1
```

- Screenshot helper. `CHROME` is the full binary path. Screenshots land in `$SCRATCH` and are then viewed with the Read tool (it renders PNGs). This is how you check your own work; do it every time the plan says "screenshot".

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,1000 --screenshot="$SCRATCH/index-desktop.png" "http://127.0.0.1:8765/" 2>/dev/null
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=375,1200 --screenshot="$SCRATCH/index-mobile.png" "http://127.0.0.1:8765/" 2>/dev/null
```

---

### Task 1: Self-hosted fonts

**Files:**
- Create: `assets/fonts/bricolage-grotesque-latin-wght-normal.woff2`
- Create: `assets/fonts/instrument-serif-latin-400-italic.woff2`
- Create: `assets/fonts/LICENSE-bricolage-grotesque.txt`
- Create: `assets/fonts/LICENSE-instrument-serif.txt`

**Interfaces:**
- Produces: the two woff2 paths above, referenced verbatim by `@font-face` in Task 2.

- [ ] **Step 1: Download the font files and licenses**

```bash
cd /Users/jramsahai/github/jramsahai.github.io
mkdir -p assets/fonts
curl -fsSL -o assets/fonts/bricolage-grotesque-latin-wght-normal.woff2 \
  "https://cdn.jsdelivr.net/npm/@fontsource-variable/bricolage-grotesque/files/bricolage-grotesque-latin-wght-normal.woff2"
curl -fsSL -o assets/fonts/instrument-serif-latin-400-italic.woff2 \
  "https://cdn.jsdelivr.net/npm/@fontsource/instrument-serif/files/instrument-serif-latin-400-italic.woff2"
curl -fsSL -o assets/fonts/LICENSE-bricolage-grotesque.txt \
  "https://cdn.jsdelivr.net/npm/@fontsource-variable/bricolage-grotesque/LICENSE"
curl -fsSL -o assets/fonts/LICENSE-instrument-serif.txt \
  "https://cdn.jsdelivr.net/npm/@fontsource/instrument-serif/LICENSE"
ls -la assets/fonts
```

Expected: four files. Each woff2 is between 10 KB and 200 KB. Each license file starts with text mentioning the SIL Open Font License.

If either woff2 URL returns 404, list the package's files with `curl -s https://data.jsdelivr.com/v1/package/npm/@fontsource-variable/bricolage-grotesque/flat | python3 -m json.tool | grep woff2` (or the `@fontsource/instrument-serif` equivalent), pick the `latin` file for the same weight/style, download it, and rename it to the filename above so Task 2 does not change.

- [ ] **Step 2: Verify the files are real fonts**

```bash
cd /Users/jramsahai/github/jramsahai.github.io
for f in assets/fonts/*.woff2; do printf '%s: ' "$f"; head -c 4 "$f" | xxd | head -1; done
```

Expected: each line shows the bytes `774f 4632` (the ASCII `wOF2` magic number). If a file shows HTML or anything else, the download failed; re-run Step 1.

- [ ] **Step 3: Commit**

```bash
cd /Users/jramsahai/github/jramsahai.github.io
git add assets/fonts
git commit -m "Add self-hosted Bricolage Grotesque and Instrument Serif fonts"
```

---

### Task 2: Stylesheet and landing page

**Files:**
- Create: `assets/css/style.css`
- Create: `index.html`

**Interfaces:**
- Consumes: the two woff2 paths from Task 1.
- Produces: CSS class names used by every later task: `container`, `site-header`, `site-footer`, `hero`, `hero-compact`, `lede`, `section`, `prose`, `project-grid`, `project-card`, `tag`, `empty`, `project-meta`, `back`. The `data-tag` attribute with values `vidyard` | `personal` drives tag colour.

- [ ] **Step 1: Write the stylesheet**

Create `assets/css/style.css` with exactly this content:

```css
/* ==========================================================================
   Tokens
   ========================================================================== */

:root {
  color-scheme: dark;

  --bg: #0A0A0A;
  --bg-raised: #141414;
  --fg: #F5F5F5;
  --fg-soft: #C9C9C9;
  --fg-muted: #9A9A9A;
  --line: #262626;
  --blue: #3388FF;
  --amber: #F5A524;

  --font-sans: "Bricolage Grotesque", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-serif: "Instrument Serif", Georgia, "Times New Roman", serif;
  --font-mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;

  --measure: 64ch;
  --container: 1080px;
  --gutter: 1.5rem;

  --space-1: 0.5rem;
  --space-2: 1rem;
  --space-3: 1.5rem;
  --space-4: 2.5rem;
  --space-5: 4rem;
  --space-6: 6rem;
}

@font-face {
  font-family: "Bricolage Grotesque";
  src: url("/assets/fonts/bricolage-grotesque-latin-wght-normal.woff2") format("woff2");
  font-weight: 200 800;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: "Instrument Serif";
  src: url("/assets/fonts/instrument-serif-latin-400-italic.woff2") format("woff2");
  font-weight: 400;
  font-style: italic;
  font-display: swap;
}

/* ==========================================================================
   Base
   ========================================================================== */

*,
*::before,
*::after {
  box-sizing: border-box;
}

html {
  -webkit-text-size-adjust: 100%;
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: var(--font-sans);
  font-size: 1.0625rem;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}

img,
video {
  display: block;
  max-width: 100%;
  height: auto;
}

a {
  color: var(--blue);
  text-decoration-thickness: 1px;
  text-underline-offset: 0.15em;
}

a:hover {
  color: var(--fg);
}

:focus-visible {
  outline: 2px solid var(--amber);
  outline-offset: 3px;
  border-radius: 2px;
}

::selection {
  background: var(--blue);
  color: var(--bg);
}

h1,
h2,
h3 {
  margin: 0;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.02;
  text-wrap: balance;
}

p {
  margin: 0;
  max-width: var(--measure);
}

/* ==========================================================================
   Layout
   ========================================================================== */

.container {
  width: 100%;
  max-width: var(--container);
  margin-inline: auto;
  padding-inline: var(--gutter);
}

.site-header {
  padding-block: var(--space-3);
}

.site-header a {
  color: var(--fg);
  font-weight: 600;
  letter-spacing: -0.01em;
  text-decoration: none;
}

.site-header a:hover {
  color: var(--blue);
}

main {
  padding-block: var(--space-4) var(--space-6);
}

.site-footer {
  border-top: 1px solid var(--line);
  padding-block: var(--space-3) var(--space-4);
  color: var(--fg-muted);
  font-size: 0.9375rem;
}

.site-footer .container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: var(--space-2) var(--space-3);
}

.site-footer ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
}

.site-footer a {
  color: var(--fg-muted);
}

.site-footer a:hover {
  color: var(--fg);
}

/* ==========================================================================
   Hero and text
   ========================================================================== */

.hero {
  padding-block: var(--space-4) var(--space-5);
}

.hero h1 {
  font-size: clamp(2.75rem, 7.5vw, 6rem);
  max-width: 18ch;
}

.hero-compact {
  padding-block: var(--space-2) var(--space-4);
}

.hero-compact h1 {
  font-size: clamp(2.25rem, 6vw, 4.5rem);
  max-width: 20ch;
}

.lede {
  margin-top: var(--space-3);
  max-width: 36ch;
  font-family: var(--font-serif);
  font-style: italic;
  font-size: clamp(1.375rem, 2.4vw, 1.875rem);
  line-height: 1.3;
  color: var(--fg-soft);
}

.section {
  padding-block: var(--space-5) 0;
}

.section h2 {
  margin-bottom: var(--space-3);
  font-size: clamp(1.5rem, 3vw, 2rem);
}

.prose > * + * {
  margin-top: var(--space-2);
}

.prose h2 {
  font-size: clamp(1.5rem, 3vw, 2rem);
}

.prose > * + h2 {
  margin-top: var(--space-5);
}

.empty {
  font-family: var(--font-serif);
  font-style: italic;
  font-size: 1.25rem;
  color: var(--fg-muted);
}

/* ==========================================================================
   Project grid (landing page)
   ========================================================================== */

.project-grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1px;
  background: var(--line);
  border: 1px solid var(--line);
}

.project-card {
  background: var(--bg);
}

.project-card a {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  height: 100%;
  padding: var(--space-3);
  color: inherit;
  text-decoration: none;
}

.project-card h3 {
  font-size: 1.375rem;
  letter-spacing: -0.02em;
}

.project-card p {
  font-size: 0.9375rem;
  color: var(--fg-muted);
}

.tag {
  margin-top: auto;
  font-family: var(--font-mono);
  font-size: 0.8125rem;
}

[data-tag="vidyard"] .tag,
[data-tag="vidyard"].tag,
li[data-tag="vidyard"] {
  color: var(--blue);
}

[data-tag="personal"] .tag,
[data-tag="personal"].tag,
li[data-tag="personal"] {
  color: var(--amber);
}

.project-card a:hover {
  background: var(--bg-raised);
}

.project-card[data-tag="vidyard"] a:hover h3 {
  color: var(--blue);
}

.project-card[data-tag="personal"] a:hover h3 {
  color: var(--amber);
}

@media (prefers-reduced-motion: no-preference) {
  .project-card a {
    transition: background-color 150ms ease;
  }

  .project-card h3 {
    transition: color 150ms ease;
  }
}

/* ==========================================================================
   Project page
   ========================================================================== */

.project-meta {
  list-style: none;
  margin: var(--space-3) 0 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1) var(--space-3);
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--fg-muted);
}

figure {
  margin: var(--space-4) 0;
}

figure img {
  border: 1px solid var(--line);
}

figcaption {
  margin-top: var(--space-1);
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--fg-muted);
}

.back {
  display: inline-block;
  margin-top: var(--space-5);
}
```

- [ ] **Step 2: Write the landing page**

Create `index.html` with exactly this content:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Jivan Ramsahai</title>
  <meta name="description" content="Product manager at Vidyard and builder of side projects. A page for each project covering what it is, my role, and how it turned out.">
  <link rel="canonical" href="https://jramsahai.github.io/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Jivan Ramsahai">
  <meta property="og:description" content="Product manager at Vidyard and builder of side projects.">
  <meta property="og:url" content="https://jramsahai.github.io/">
  <meta property="og:image" content="https://jramsahai.github.io/assets/images/og-default.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/bricolage-grotesque-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a href="/">Jivan Ramsahai</a>
    </div>
  </header>

  <main class="container">
    <section class="hero">
      <h1>Product manager at Vidyard. Builder of side projects.</h1>
      <p class="lede">A record of what I have shipped, at work and on my own time, and what I learned doing it.</p>
    </section>

    <section class="section prose" aria-labelledby="about-heading">
      <h2 id="about-heading">About</h2>
      <p>I am Jivan Ramsahai. At Vidyard I work on video tools for go-to-market teams: figuring out what to build, why, and how to tell whether it worked. Outside work I build small software projects to learn things a roadmap cannot teach me.</p>
      <p>Each project below has its own page covering what it is, what I did, and how it turned out. Work projects stay high level; the interesting parts are usually the decisions, not the details.</p>
    </section>

    <section class="section" aria-labelledby="projects-heading">
      <h2 id="projects-heading">Projects</h2>
      <p class="empty">Project pages are being added one at a time. The first one is on its way.</p>
      <!--
        When the first project is added, replace the paragraph above with a
        <ul class="project-grid"> and copy the card snippet from
        docs/templates/project-page.html into it.
      -->
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <ul>
        <li><a href="mailto:you@example.com">Email</a></li>
        <li><a href="https://www.linkedin.com/in/your-handle">LinkedIn</a></li>
        <li><a href="https://github.com/jramsahai">GitHub</a></li>
      </ul>
      <p>&copy; 2026 Jivan Ramsahai</p>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 3: Start the local server and screenshot**

```bash
cd /Users/jramsahai/github/jramsahai.github.io && python3 -m http.server 8765 --bind 127.0.0.1
```

Run that in the background. Then:

```bash
SCRATCH=/private/tmp/claude-501/-Users-jramsahai-github-ji-portfolio/d55533d3-632f-44df-a229-08fd6284e577/scratchpad
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
curl -s -o /dev/null -w "index: %{http_code}\ncss: " http://127.0.0.1:8765/
curl -s -o /dev/null -w "%{http_code}\nfont: " http://127.0.0.1:8765/assets/css/style.css
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8765/assets/fonts/bricolage-grotesque-latin-wght-normal.woff2
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,1000 --screenshot="$SCRATCH/index-desktop.png" "http://127.0.0.1:8765/" 2>/dev/null
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=375,1200 --screenshot="$SCRATCH/index-mobile.png" "http://127.0.0.1:8765/" 2>/dev/null
ls -la "$SCRATCH"/index-*.png
```

Expected: three `200` lines, then two PNG files.

- [ ] **Step 4: Review the screenshots**

Use the Read tool on `$SCRATCH/index-desktop.png` and `$SCRATCH/index-mobile.png`. Check all of the following and fix the CSS or HTML if any fail, then re-screenshot:

- Headline renders in a heavy grotesk (Bricolage), not a fallback sans. If it looks like Helvetica/Arial, the font did not load; check the `@font-face` URL against the filename in `assets/fonts`.
- The lede renders in an italic serif (Instrument Serif).
- At 1440 the headline is at most 4 lines. If it is 5 or more, raise `.hero h1 { max-width }` to `22ch`.
- At 375 nothing overflows horizontally and the headline is readable (about 2.75rem).
- The footer links sit on one row on desktop and wrap cleanly on mobile.
- Background is near-black, text off-white, footer text grey.

- [ ] **Step 5: Commit**

```bash
cd /Users/jramsahai/github/jramsahai.github.io
git add assets/css/style.css index.html
git commit -m "Add stylesheet and landing page"
```

---

### Task 3: 404 page

**Files:**
- Create: `404.html`

**Interfaces:**
- Consumes: `hero`, `lede`, `site-header`, `site-footer`, `container` from Task 2.

- [ ] **Step 1: Write the page**

Create `404.html` with exactly this content:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page not found</title>
  <meta name="description" content="Nothing lives at this address on jramsahai.github.io.">
  <meta name="robots" content="noindex">
  <link rel="canonical" href="https://jramsahai.github.io/404.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Page not found">
  <meta property="og:description" content="Nothing lives at this address.">
  <meta property="og:url" content="https://jramsahai.github.io/404.html">
  <meta property="og:image" content="https://jramsahai.github.io/assets/images/og-default.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a href="/">Jivan Ramsahai</a>
    </div>
  </header>

  <main class="container">
    <section class="hero">
      <h1>Page not found</h1>
      <p class="lede">Nothing lives at this address. It may have moved, or the link had a typo.</p>
      <p class="back"><a href="/">Go to the home page</a></p>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <ul>
        <li><a href="mailto:you@example.com">Email</a></li>
        <li><a href="https://www.linkedin.com/in/your-handle">LinkedIn</a></li>
        <li><a href="https://github.com/jramsahai">GitHub</a></li>
      </ul>
      <p>&copy; 2026 Jivan Ramsahai</p>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 2: Screenshot and review**

```bash
SCRATCH=/private/tmp/claude-501/-Users-jramsahai-github-ji-portfolio/d55533d3-632f-44df-a229-08fd6284e577/scratchpad
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,900 --screenshot="$SCRATCH/404-desktop.png" "http://127.0.0.1:8765/404.html" 2>/dev/null
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=375,900 --screenshot="$SCRATCH/404-mobile.png" "http://127.0.0.1:8765/404.html" 2>/dev/null
```

Read both PNGs. Expected: same header and footer as the landing page, heavy "Page not found" headline, italic lede, one blue link below it. Python's server does not route unknown paths to `404.html`, so testing a bogus path locally shows Python's own 404; the GitHub Pages behaviour is checked after push in Task 6.

- [ ] **Step 3: Commit**

```bash
cd /Users/jramsahai/github/jramsahai.github.io
git add 404.html
git commit -m "Add custom 404 page"
```

---

### Task 4: Icons and social image

**Files:**
- Create: `favicon.svg`
- Create: `favicon-32.png`
- Create: `apple-touch-icon.png`
- Create: `assets/images/og-default.png`
- Create: `docs/templates/icon.html` (source page rendered to the PNG icons)
- Create: `docs/templates/og-default.html` (source page rendered to the OG image)
- Modify: `docs/superpowers/specs/2026-09-17-portfolio-site-design.md` (favicon filenames)

**Interfaces:**
- Produces: the four image files referenced by the `<head>` of every page written in Tasks 2, 3, and 5.

- [ ] **Step 1: Write the SVG favicon**

Create `favicon.svg`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="12" fill="#0A0A0A"/>
  <rect x="10" y="34" width="20" height="20" fill="#3388FF"/>
  <rect x="34" y="10" width="20" height="20" fill="#F5A524"/>
</svg>
```

Two offset squares in the two tag colours. It needs no font, so it renders identically everywhere.

- [ ] **Step 2: Write the icon source page**

Create `docs/templates/icon.html`:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Icon source</title>
  <style>
    html, body { margin: 0; width: 720px; height: 720px; background: #0A0A0A; overflow: hidden; }
    svg { display: block; width: 720px; height: 720px; }
  </style>
</head>
<body>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
    <rect width="64" height="64" fill="#0A0A0A"/>
    <rect x="10" y="34" width="20" height="20" fill="#3388FF"/>
    <rect x="34" y="10" width="20" height="20" fill="#F5A524"/>
  </svg>
</body>
</html>
```

No rounded corners here: iOS applies its own mask to touch icons.

- [ ] **Step 3: Write the OG image source page**

Create `docs/templates/og-default.html`:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>OG image source</title>
  <link rel="stylesheet" href="/assets/css/style.css">
  <style>
    html, body { width: 1200px; height: 630px; overflow: hidden; }
    body { position: relative; padding: 72px 80px; }
    .og-name { font-size: 120px; font-weight: 800; letter-spacing: -0.04em; line-height: 0.95; max-width: 12ch; }
    .og-lede { margin-top: 32px; max-width: 24ch; font-family: var(--font-serif); font-style: italic; font-size: 44px; line-height: 1.2; color: var(--fg-soft); }
    .og-mark { position: absolute; left: 80px; bottom: 72px; width: 64px; height: 64px; }
    .og-url { position: absolute; right: 80px; bottom: 80px; font-family: var(--font-mono); font-size: 26px; color: var(--fg-muted); }
  </style>
</head>
<body>
  <div class="og-name">Jivan Ramsahai</div>
  <div class="og-lede">Product manager at Vidyard. Builder of side projects.</div>
  <svg class="og-mark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true">
    <rect x="10" y="34" width="20" height="20" fill="#3388FF"/>
    <rect x="34" y="10" width="20" height="20" fill="#F5A524"/>
  </svg>
  <div class="og-url">jramsahai.github.io</div>
</body>
</html>
```

- [ ] **Step 4: Render the PNGs**

The local server from Task 2 must still be running (fonts only load over http, not `file://`).

```bash
cd /Users/jramsahai/github/jramsahai.github.io
SCRATCH=/private/tmp/claude-501/-Users-jramsahai-github-ji-portfolio/d55533d3-632f-44df-a229-08fd6284e577/scratchpad
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p assets/images
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=720,720 --screenshot="$SCRATCH/icon-720.png" "http://127.0.0.1:8765/docs/templates/icon.html" 2>/dev/null
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1200,630 --screenshot="assets/images/og-default.png" "http://127.0.0.1:8765/docs/templates/og-default.html" 2>/dev/null
sips -z 180 180 "$SCRATCH/icon-720.png" --out apple-touch-icon.png >/dev/null
sips -z 32 32 "$SCRATCH/icon-720.png" --out favicon-32.png >/dev/null
for f in apple-touch-icon.png favicon-32.png assets/images/og-default.png; do printf '%s: ' "$f"; sips -g pixelWidth -g pixelHeight "$f" | awk '/pixel/{printf "%s ", $2} END{print ""}'; done
```

Expected output:

```
apple-touch-icon.png: 180 180
favicon-32.png: 32 32
assets/images/og-default.png: 1200 630
```

If the OG image is not 1200x630, Chrome clamped the window. Re-run with `--window-size=1200,630 --force-device-scale-factor=1` and, if still wrong, crop with `sips -c 630 1200 assets/images/og-default.png`.

- [ ] **Step 5: Review the OG image**

Read `assets/images/og-default.png`. Expected: the name in heavy Bricolage on two lines, the italic serif line beneath in soft grey, the two-square mark bottom-left, the URL in mono bottom-right, nothing clipped. If the name renders in a fallback sans, the server is not running or the font path is wrong. Also check `ls -la assets/images/og-default.png` is under 300 KB.

- [ ] **Step 6: Update the spec's favicon filenames**

In `docs/superpowers/specs/2026-09-17-portfolio-site-design.md`, make these two edits.

In the Site Structure block, replace these four lines:

```
│   ├── images/
│   │   ├── og-default.png      1200x630 social preview image
│   │   └── <project-slug>/     per-project screenshots/media
│   └── favicon.svg             plus favicon.ico and apple-touch-icon.png at root
```

with these six:

```
│   └── images/
│       ├── og-default.png      1200x630 social preview image
│       └── <project-slug>/     per-project screenshots/media
├── favicon.svg
├── favicon-32.png
├── apple-touch-icon.png
```

and replace:

```
    ├── templates/
    │   └── project-page.html   starting point for new project pages
```

with:

```
    ├── templates/
    │   ├── project-page.html   starting point for new project pages
    │   ├── icon.html           source rendered to the PNG icons
    │   └── og-default.html     source rendered to og-default.png
```

In the Page Head & Sharing section, replace:

```
- Favicon set: `favicon.svg`, `favicon.ico`, `apple-touch-icon.png`.
```

with:

```
- Favicon set: `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`.
  PNG rather than ICO: every current browser accepts a PNG icon, and PNG
  can be generated from the SVG with no extra tooling.
```

- [ ] **Step 7: Commit**

```bash
cd /Users/jramsahai/github/jramsahai.github.io
git add favicon.svg favicon-32.png apple-touch-icon.png assets/images/og-default.png docs/templates/icon.html docs/templates/og-default.html docs/superpowers/specs/2026-09-17-portfolio-site-design.md
git commit -m "Add favicons and default social image"
```

---

### Task 5: Project page template and README

**Files:**
- Create: `docs/templates/project-page.html`
- Modify: `README.md`

**Interfaces:**
- Consumes: `hero-compact`, `lede`, `project-meta`, `prose`, `back`, `project-grid`, `project-card`, `tag` from Task 2.
- Produces: the file every future project page is copied from.

- [ ] **Step 1: Write the template**

Create `docs/templates/project-page.html` with exactly this content. The words in capitals are template fields for the person adding a project, and are the only capitalised text anywhere in the site.

```html
<!--
  HOW TO ADD A PROJECT

  1. Copy this file to /projects/<slug>/index.html. The slug is lowercase,
     hyphenated, and never changes once published (it is the public URL).
  2. Replace every PROJECT TITLE, ONE-LINE DESCRIPTION, <slug>, YEAR, and the
     body paragraphs. Keep the three h2 headings.
  3. In the project-meta list, set data-tag to "vidyard" or "personal" and
     the visible text to "Vidyard" or "Personal".
  4. Update <title>, description, canonical, og:url, og:title,
     og:description. Point og:image at a project screenshot if there is one,
     otherwise leave og-default.png.
  5. Put images in /assets/images/<slug>/ as WebP exported at 2x, under
     300 KB each, with width and height attributes set to the file's pixel
     size. Images below the first screen get loading="lazy".
  6. Add a card to the <ul class="project-grid"> in /index.html. If this is
     the first project, create the list and delete the <p class="empty">.
     Card markup:

     <li class="project-card" data-tag="vidyard">
       <a href="/projects/<slug>/">
         <h3>PROJECT TITLE</h3>
         <p>ONE-LINE DESCRIPTION</p>
         <span class="tag">Vidyard</span>
       </a>
     </li>

  7. Vidyard projects: keep text and screenshots generic unless the site
     owner has approved more detail for this specific project. Screenshots of
     internal tools, customer names, metrics, or unreleased UI need the same
     approval as text.
  8. Delete this comment block from the copy.
-->
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PROJECT TITLE</title>
  <meta name="description" content="ONE-LINE DESCRIPTION">
  <link rel="canonical" href="https://jramsahai.github.io/projects/<slug>/">
  <meta property="og:type" content="article">
  <meta property="og:title" content="PROJECT TITLE">
  <meta property="og:description" content="ONE-LINE DESCRIPTION">
  <meta property="og:url" content="https://jramsahai.github.io/projects/<slug>/">
  <meta property="og:image" content="https://jramsahai.github.io/assets/images/og-default.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/bricolage-grotesque-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a href="/">Jivan Ramsahai</a>
    </div>
  </header>

  <main class="container">
    <article>
      <header class="hero hero-compact">
        <h1>PROJECT TITLE</h1>
        <p class="lede">ONE-LINE DESCRIPTION</p>
        <ul class="project-meta">
          <li data-tag="vidyard">Vidyard</li>
          <li>Product manager</li>
          <li>YEAR</li>
        </ul>
      </header>

      <div class="prose">
        <h2>What it is</h2>
        <p>Two or three sentences on the problem and the thing that was built to address it. Written for someone who has never heard of it.</p>

        <figure>
          <img src="/assets/images/<slug>/cover.webp" width="1600" height="1000" alt="Describe what the screenshot shows, in one sentence.">
          <figcaption>One line of context for the image.</figcaption>
        </figure>

        <h2>My role</h2>
        <p>What you personally did: the decisions you owned, who you worked with, and what you were responsible for.</p>

        <h2>Outcomes</h2>
        <p>How it turned out. Shipped or not, what changed, what you would do differently. Public numbers only unless approved.</p>
      </div>

      <a class="back" href="/#projects-heading">Back to all projects</a>
    </article>
  </main>

  <footer class="site-footer">
    <div class="container">
      <ul>
        <li><a href="mailto:you@example.com">Email</a></li>
        <li><a href="https://www.linkedin.com/in/your-handle">LinkedIn</a></li>
        <li><a href="https://github.com/jramsahai">GitHub</a></li>
      </ul>
      <p>&copy; 2026 Jivan Ramsahai</p>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 2: Render a throwaway sample to verify the template and the card grid**

This creates a temporary project page and a temporary card, screenshots them, and then removes both. Nothing from this step is committed.

```bash
cd /Users/jramsahai/github/jramsahai.github.io
SCRATCH=/private/tmp/claude-501/-Users-jramsahai-github-ji-portfolio/d55533d3-632f-44df-a229-08fd6284e577/scratchpad
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p projects/sample-project assets/images/sample-project
sed -e 's/PROJECT TITLE/Sample project/g' -e 's/ONE-LINE DESCRIPTION/A one-line description of the sample project./g' -e 's/<slug>/sample-project/g' -e 's/YEAR/2026/g' docs/templates/project-page.html > projects/sample-project/index.html
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1600,1000 --screenshot="assets/images/sample-project/cover.webp" "http://127.0.0.1:8765/" 2>/dev/null
python3 - <<'EOF'
import re, pathlib
p = pathlib.Path("index.html")
html = p.read_text()
cards = '''<ul class="project-grid">
        <li class="project-card" data-tag="vidyard">
          <a href="/projects/sample-project/">
            <h3>Sample project</h3>
            <p>A one-line description of the sample project.</p>
            <span class="tag">Vidyard</span>
          </a>
        </li>
        <li class="project-card" data-tag="personal">
          <a href="/projects/sample-project/">
            <h3>Second sample with a longer title that wraps</h3>
            <p>Another one-liner, a bit longer, so the card heights differ and the tag still sits at the bottom.</p>
            <span class="tag">Personal</span>
          </a>
        </li>
        <li class="project-card" data-tag="vidyard">
          <a href="/projects/sample-project/">
            <h3>Third sample</h3>
            <p>Short.</p>
            <span class="tag">Vidyard</span>
          </a>
        </li>
      </ul>'''
html = re.sub(r'<p class="empty">.*?</p>', cards, html, count=1, flags=re.S)
p.write_text(html)
EOF
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,1400 --screenshot="$SCRATCH/index-with-cards.png" "http://127.0.0.1:8765/" 2>/dev/null
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=375,1600 --screenshot="$SCRATCH/index-with-cards-mobile.png" "http://127.0.0.1:8765/" 2>/dev/null
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,1800 --screenshot="$SCRATCH/project-desktop.png" "http://127.0.0.1:8765/projects/sample-project/" 2>/dev/null
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=375,2200 --screenshot="$SCRATCH/project-mobile.png" "http://127.0.0.1:8765/projects/sample-project/" 2>/dev/null
```

Note: the "cover.webp" is actually a PNG screenshot saved with a `.webp` name. That is fine for a throwaway render; browsers sniff the bytes.

- [ ] **Step 3: Review the four screenshots**

Read all four PNGs. Check:

- Landing page: three cells in a hairline grid, equal heights per row, tags at the bottom of each cell, blue tag text for Vidyard and amber for Personal. On mobile the grid is a single column.
- Project page: compact heavy title, italic lede, mono meta row with the first item in blue, three headed sections, bordered image with a mono caption, "Back to all projects" link at the end. On mobile nothing overflows.
- If card cells have uneven heights within a row, confirm `.project-card a { height: 100% }` is present.

Fix CSS if needed, re-screenshot, and only then continue.

- [ ] **Step 4: Remove the throwaway sample**

```bash
cd /Users/jramsahai/github/jramsahai.github.io
git checkout -- index.html
rm -rf projects assets/images/sample-project
git status --short
```

Expected: only `docs/templates/project-page.html` (untracked) shows. If `index.html` still shows as modified, the checkout did not run from the repo root.

- [ ] **Step 5: Update the README**

Replace the entire contents of `README.md` with:

```markdown
# jramsahai.github.io

Personal portfolio site. Plain static HTML/CSS served by GitHub Pages from
the `main` branch root. No build step.

- Design spec: `docs/superpowers/specs/2026-09-17-portfolio-site-design.md`
- Project page template: `docs/templates/project-page.html` (the comment at
  the top of that file is the full procedure for adding a project)

## Local preview

```
python3 -m http.server 8000
```

Then open <http://localhost:8000/>. Asset paths are root-absolute, so the
server must be started from the repo root.

## Publishing

Push to `main`. GitHub Pages rebuilds within about a minute. `_config.yml`
keeps `docs/` and this README out of the published site.
```

- [ ] **Step 6: Commit**

```bash
cd /Users/jramsahai/github/jramsahai.github.io
git add docs/templates/project-page.html README.md
git commit -m "Add project page template and README instructions"
```

---

### Task 6: Final verification and publish

**Files:**
- None created. This task checks and pushes.

- [ ] **Step 1: Link and asset check**

Every `href` and `src` that starts with `/` in the three HTML pages must resolve locally.

```bash
cd /Users/jramsahai/github/jramsahai.github.io
for f in index.html 404.html; do
  grep -oE '(href|src)="/[^"]*"' "$f" | sed -E 's/^[a-z]+="([^"]*)"$/\1/' | sort -u | while read -r p; do
    printf '%s %s -> ' "$f" "$p"; curl -s -o /dev/null -w '%{http_code}\n' "http://127.0.0.1:8765$p"
  done
done
```

Expected: every line ends in `200`. Anything else is a broken path; fix it and re-run.

- [ ] **Step 2: Lighthouse**

```bash
cd /Users/jramsahai/github/jramsahai.github.io
export SCRATCH=/private/tmp/claude-501/-Users-jramsahai-github-ji-portfolio/d55533d3-632f-44df-a229-08fd6284e577/scratchpad
npx --yes lighthouse "http://127.0.0.1:8765/" --quiet --chrome-flags="--headless=new" --only-categories=performance,accessibility,best-practices,seo --output=json --output-path="$SCRATCH/lh-index.json"
python3 - <<'EOF'
import json, os
d = json.load(open(os.environ.get("SCRATCH", "/private/tmp/claude-501/-Users-jramsahai-github-ji-portfolio/d55533d3-632f-44df-a229-08fd6284e577/scratchpad") + "/lh-index.json"))
for k, v in d["categories"].items():
    print(f"{k}: {round(v['score'] * 100)}")
fails = [a for a in d["audits"].values() if a.get("score") is not None and a["score"] < 1 and a.get("scoreDisplayMode") in ("binary", "numeric")]
for a in fails:
    print("-", a["id"], ":", a["title"])
EOF
```

Expected: accessibility 100, seo 100, best-practices at least 90, performance at least 90. The audit list below the scores names anything that failed. Fix real issues in the HTML/CSS and re-run. Ignore `is-on-https` and `uses-http2`, which are artifacts of the local server. If `npx lighthouse` cannot install (no network or npm error), skip this step and say so explicitly in the final report.

- [ ] **Step 3: Reduced motion check**

```bash
cd /Users/jramsahai/github/jramsahai.github.io
grep -n "transition" assets/css/style.css
```

Expected: every `transition` line appears after the line containing `prefers-reduced-motion: no-preference` and before that block's closing brace. There must be no `transition` or `animation` outside that block.

- [ ] **Step 4: Confirm a clean tree and push**

```bash
cd /Users/jramsahai/github/jramsahai.github.io
git status --short
git log --oneline origin/main..HEAD
git push
```

Expected: empty status, five commits listed (fonts, stylesheet and landing page, 404, icons, template), push succeeds.

- [ ] **Step 5: Post-push checks on the live site**

Wait for the Pages build, then verify the published site.

```bash
for i in $(seq 1 18); do s=$(gh api repos/jramsahai/jramsahai.github.io/pages --jq .status); [ "$s" = "built" ] && break; sleep 10; done; echo "status=$s"
for p in / /404.html /assets/css/style.css /assets/fonts/bricolage-grotesque-latin-wght-normal.woff2 /favicon.svg /favicon-32.png /apple-touch-icon.png /assets/images/og-default.png; do
  printf '%s -> ' "$p"; curl -s -o /dev/null -w '%{http_code}\n' "https://jramsahai.github.io$p"
done
printf '/no-such-page -> '; curl -s -o /dev/null -w '%{http_code}\n' https://jramsahai.github.io/no-such-page
printf '/docs/templates/project-page.html -> '; curl -s -o /dev/null -w '%{http_code}\n' https://jramsahai.github.io/docs/templates/project-page.html
curl -s https://jramsahai.github.io/no-such-page | grep -c "Page not found"
```

Expected: every asset path `200`; `/no-such-page` `404`; the docs path `404`; the final grep prints `1`, proving GitHub serves the custom 404 page. If the Pages status is still `building` after three minutes, wait and re-run; do not report success until this step passes.

- [ ] **Step 6: Screenshot the live site**

```bash
SCRATCH=/private/tmp/claude-501/-Users-jramsahai-github-ji-portfolio/d55533d3-632f-44df-a229-08fd6284e577/scratchpad
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,1000 --screenshot="$SCRATCH/live-index.png" "https://jramsahai.github.io/" 2>/dev/null
```

Read the PNG. It should match the local desktop screenshot from Task 2, with the fonts loaded. Stop the background server when done.

## Final report

The executor's final report must include:

1. Lighthouse scores for the landing page, or the reason Lighthouse was skipped.
2. The post-push check output from Task 6 Step 5.
3. A reminder that `mailto:you@example.com` and `linkedin.com/in/your-handle` are placeholders in `index.html`, `404.html`, and `docs/templates/project-page.html`, and that the hero, about, and lede copy are first drafts.
4. Anything that deviated from this plan and why.
