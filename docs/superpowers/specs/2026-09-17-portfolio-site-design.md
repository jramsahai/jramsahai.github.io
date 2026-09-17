# Portfolio Site Design

Date: 2026-09-17 (revised 2026-09-17)

## Purpose

A personal portfolio site showcasing a mix of Vidyard product-management work
and personal side projects. Ships as a static site on GitHub Pages, with a
landing page linking out to a dedicated page per project. Projects are added
incrementally, one at a time, after the initial site skeleton is in place.

## Hosting & Repo

- Repo: `jramsahai/jramsahai.github.io` (public). The repo must be named
  exactly this for GitHub to serve it at the apex user URL; the local
  checkout is currently `ji-portfolio` with no remote, so the remote should
  be created under that name before the first push.
- Hosting: GitHub Pages, "Deploy from a branch", `main` branch, `/ (root)`
  folder. No GitHub Actions workflow to maintain.
- Live URL: `https://jramsahai.github.io`.
- GitHub Pages runs Jekyll on every push by default. We do not use Jekyll
  for templating, but we keep it enabled and add a minimal `_config.yml`
  whose only job is to `exclude` non-site files (`docs/`, `README.md`) from
  the published output. Files without front matter are copied through
  untouched, so this has no effect on local preview and no local tooling is
  needed. Without this, the design spec under `docs/` would be publicly
  served at `jramsahai.github.io/docs/...`.
- Custom domain: not in scope now. If wanted later, it is a `CNAME` file plus
  a DNS record and nothing else in the site changes.

## Tech Approach

Plain static HTML/CSS/JS. No framework, no static site generator, no build
tooling. Rationale: small page count, long-term low-maintenance goal, and
GitHub Pages can serve the repo root as-is.

### Shared chrome (header/footer)

The header and footer are duplicated verbatim in each page rather than
injected at runtime. The original draft proposed fetching partials with a
small vanilla-JS include; that was dropped because:

- The chrome flashes in after first paint (header/footer missing for a
  frame or more), which is most visible on exactly the slow connections a
  static site is supposed to serve well.
- `fetch()` of a local partial fails when a page is opened via `file://`, so
  every preview needs a local server, and the site silently loses its nav
  and contact links for any visitor with JS disabled or blocked.
- Crawlers and link-preview bots may not execute the include, so the nav
  and footer links are invisible to them.

The chrome is intentionally tiny to make duplication cheap: the header is a
name/logo link back to `/` and nothing else; the footer is the contact links
(email, LinkedIn, GitHub) and a copyright line. At a page count in the low
double digits, keeping these in sync is a project-wide find-and-replace,
not a maintenance burden. Each page also owns its own `<head>` (title,
description, social tags), which a partial could never have provided anyway.

If the page count ever grows past that, the upgrade path is Jekyll
`_layouts`, which GitHub Pages builds natively with no Actions workflow.
That is deliberately deferred; it would add a Ruby dependency to local
preview.

### Project page template

A reference copy of a complete project page lives at
`docs/templates/project-page.html` (excluded from publishing by
`_config.yml`). New project pages start as a copy of this file so every
project page has the same skeleton, head tags, and chrome.

## Site Structure

```
/
├── _config.yml                 Jekyll exclude list only (see Hosting)
├── README.md                   repo readme, not published
├── index.html                  landing page
├── 404.html                    custom not-found page
├── projects/
│   └── <project-slug>/
│       └── index.html          one page per project
├── assets/
│   ├── css/
│   │   └── style.css
│   ├── fonts/                  self-hosted woff2 (if not using a system stack)
│   ├── images/
│   │   ├── og-default.png      1200x630 social preview image
│   │   └── <project-slug>/     per-project screenshots/media
│   └── favicon.svg             plus favicon.ico and apple-touch-icon.png at root
└── docs/
    ├── templates/
    │   └── project-page.html   starting point for new project pages
    └── superpowers/specs/      design docs (this file)
```

- **Landing page (`index.html`)**: intro/header (who you are: PM at Vidyard
  and builder), a short about paragraph, a project grid where each card
  shows a title, one-line description, and a tag (`Vidyard` / `Personal`),
  and a footer with contact/links.
- **Project pages (`projects/<slug>/index.html`)**: one per project, built
  one at a time in collaboration. Each covers what the project is, your
  role, and outcomes, with screenshots/media as relevant. Each page ends
  with a link back to the landing page so the site never dead-ends.
- **404 page**: simple custom not-found page with the site chrome and a link
  home. GitHub Pages serves `404.html` from the root automatically.

## Content Model

Each project card on the landing page links to its own `projects/<slug>/`
page. There is no CMS or data file; each project page is hand-authored
static HTML, added one project at a time as directed by the user.

- A card is added to the landing page in the same commit as its project
  page. No "coming soon" cards and no links to pages that do not exist yet.
- Cards are ordered by hand in the landing page markup (most impressive
  first, not chronological). Reordering is a markup edit.
- Slugs are lowercase, hyphenated, and stable once published, since they
  form public URLs.

### Confidentiality (Vidyard projects)

Vidyard project pages default to generic/high-level descriptions of role,
skills, and impact: no confidential specifics, internal data, or unreleased
product details, unless the user explicitly says more detail is safe to
include for that specific project. This is decided case-by-case, per
project, not globally.

This applies to media as well as text. Screenshots of internal tools,
dashboards, customer names, metrics, or unreleased UI leak more than prose
does. Default to publicly available marketing/product imagery, public
release-note screenshots, or none. Any other screenshot needs the same
per-project explicit approval as the text.

## Page Head & Sharing

Every page carries its own head tags, since this is a portfolio that will be
shared as links on LinkedIn and in email:

- Unique `<title>` and `<meta name="description">` per page.
- Open Graph and Twitter card tags (`og:title`, `og:description`,
  `og:image`, `og:url`, `twitter:card`). Project pages use a project
  screenshot as the image when one exists; otherwise
  `assets/images/og-default.png`.
- Canonical URL on each page.
- Favicon set: `favicon.svg`, `favicon.ico`, `apple-touch-icon.png`.
- `<meta name="viewport">` and `lang="en"` on `<html>`.

## Visual Design

Reference: `startingline.digital`'s dark theme, adapted and pushed to be
"more interesting" rather than copied.

- Dark theme only. No light-mode variant; set `color-scheme: dark` so
  native form controls and scrollbars match.
- Near-black background (`#0A0A0A`), off-white text (`#F5F5F5`).
- Primary accent: bright cornflower-blue (`#3388FF`), matching the reference
  site. Check contrast where it is used as text on the dark background; it
  passes for large text but should be verified for small labels and links.
- Secondary accent: a warm amber/coral, used sparingly to visually
  distinguish project tags (`Vidyard` vs. `Personal`), the point of
  difference from the reference site's single-accent look.
- Bold/heavy display type for headlines paired with a lighter or italic
  subhead treatment; monospace-style micro-labels for small accents (tags,
  numbers).
- Subtle hover/scroll interaction on project cards instead of a static grid.
  Every motion effect is wrapped in `@media (prefers-reduced-motion:
  no-preference)` so the reduced-motion version is the static grid.

Exact font choices and card interaction details are decided during
implementation, not locked in this spec, with one constraint: fonts are
either a system stack or self-hosted `woff2` files under `assets/fonts/`
with `font-display: swap`. No runtime requests to Google Fonts or other
third-party hosts, for privacy, offline preview, and one fewer external
dependency to break.

## Accessibility Baseline

Cheap to do from the start, expensive to retrofit:

- Semantic landmarks (`header`, `nav`, `main`, `footer`) and a single `h1`
  per page.
- Visible focus styles on all links and cards; hover effects must not be
  the only affordance.
- Text and accent colours meet WCAG AA contrast on the dark background.
- Meaningful `alt` text on every screenshot describing what it shows, or
  `alt=""` for purely decorative images.
- Card links wrap the whole card so the click target is not just the title.

## Images & Media

- Screenshots exported at 2x, saved as WebP (PNG fallback only if a specific
  image needs it), and kept under roughly 300 KB each. Anything over that is
  resized before commit, not served as-is.
- Every `<img>` has explicit `width` and `height` attributes to prevent
  layout shift, and `loading="lazy"` for anything below the fold.
- Video, if any, is a short muted looping MP4/WebM with `playsinline` and a
  poster image, not an embedded third-party player, unless the project is
  itself a Vidyard video, in which case the Vidyard embed is the point.

## Out of Scope

- CMS, templating engine, or build pipeline.
- Contact form or any server-side functionality (static only).
- Analytics/tracking (can be revisited later if wanted).
- Light theme.
- Custom domain (path noted above; not part of this build).
- Automated tests. This is a static content site; verification is visual
  (local preview + browser check) rather than a test suite.

## Verification

Before pushing:

1. Serve the site locally from the repo root (for example
   `python3 -m http.server 8000`) and open `http://localhost:8000/`.
2. Visually check the landing page and at least one project page at desktop
   width and at a phone width (about 375px). Check the 404 page renders
   with chrome by visiting a bogus path.
3. Confirm every internal link resolves and every card links to an existing
   project page.
4. Run a Lighthouse pass on the landing page and one project page in
   Chrome DevTools; performance, accessibility, and SEO should all be green.
   This catches missing alt text, low contrast, missing meta description,
   and oversized images in one step.
5. Toggle "Emulate CSS prefers-reduced-motion" in DevTools and confirm the
   card grid is static.
6. After the first push, confirm the live site serves `/` and `/404.html`
   and does not serve `/docs/` (the Jekyll exclude is working).

## Changes in this revision

- Dropped the client-side partial include in favour of duplicating the
  (deliberately tiny) header/footer; recorded why.
- Added the Jekyll `_config.yml` exclude so design docs under `docs/` are
  not published, and noted the repo-name requirement for the apex URL.
- Added a project page template file so new pages start from the same
  skeleton.
- Added sections for page head/sharing tags, accessibility baseline, and
  image handling, none of which the original spec covered.
- Extended the confidentiality rule to cover screenshots and media.
- Added content-model rules: no cards without pages, hand-ordered grid,
  stable slugs.
- Pinned fonts to system or self-hosted, and required reduced-motion
  handling for card interactions.
- Made the verification list concrete and added the post-push check.
