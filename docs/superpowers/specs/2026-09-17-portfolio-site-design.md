# Portfolio Site Design

Date: 2026-09-17

## Purpose

A personal portfolio site showcasing a mix of Vidyard product-management work
and personal side projects. Ships as a static site on GitHub Pages, with a
landing page linking out to a dedicated page per project. Projects are added
incrementally, one at a time, after the initial site skeleton is in place.

## Hosting & Repo

- Repo: `jramsahai/jramsahai.github.io` (public).
- Hosting: GitHub Pages, served directly from the `main` branch root — no
  build step, no GitHub Actions required.
- Live URL: `https://jramsahai.github.io`.

## Tech Approach

Plain static HTML/CSS/JS. No framework, no static site generator, no build
tooling. Rationale: small page count, long-term low-maintenance goal, and
GitHub Pages can serve the repo root as-is.

To avoid hand-duplicating the header/nav/footer across every project page
without introducing a build step, shared chrome lives in small partial HTML
files that are injected client-side via a minimal vanilla-JS include (fetch +
inject). This keeps every page a plain static file while avoiding copy-paste
drift as project pages are added.

## Site Structure

```
/
├── index.html                  landing page
├── 404.html                    custom not-found page
├── projects/
│   └── <project-slug>/
│       └── index.html          one page per project
├── partials/
│   ├── header.html
│   └── footer.html
└── assets/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── include.js          fetches & injects partials
    └── images/
        └── <project-slug>/     per-project screenshots/media
```

- **Landing page (`index.html`)**: intro/header (who you are — PM at Vidyard
  and builder), a project grid where each card shows a title, one-line
  description, and a tag (e.g. "Vidyard" / "Personal"), and a footer with
  contact/links.
- **Project pages (`projects/<slug>/index.html`)**: one per project, built
  one at a time in collaboration — each covers what the project is, your
  role, and outcomes, with screenshots/media as relevant.
- **404 page**: simple custom not-found page, supported natively by GitHub
  Pages.

## Content Model

Each project card on the landing page links to its own `projects/<slug>/`
page. There is no CMS or data file — each project page is hand-authored
static HTML, added one project at a time as directed by the user.

### Confidentiality (Vidyard projects)

Vidyard project pages default to generic/high-level descriptions of role,
skills, and impact — no confidential specifics, internal data, or unreleased
product details — unless the user explicitly says more detail is safe to
include for that specific project. This is decided case-by-case, per
project, not globally.

## Visual Design

Reference: `startingline.digital`'s dark theme, adapted and pushed to be
"more interesting" rather than copied:

- Near-black background (`#0A0A0A`), off-white text (`#F5F5F5`).
- Primary accent: bright cornflower-blue (`#3388FF`), matching the
  reference site.
- Secondary accent: a warm amber/coral, used sparingly to visually
  distinguish project tags (e.g. Vidyard vs. Personal) — the point of
  difference from the reference site's single-accent look.
- Bold/heavy display type for headlines paired with a lighter or italic
  subhead treatment; monospace-style micro-labels for small accents (tags,
  numbers).
- Subtle hover/scroll interaction on project cards instead of a static grid.

Exact font choices and card interaction details are decided during
implementation, not locked in this spec.

## Out of Scope

- CMS, templating engine, or build pipeline.
- Contact form or any server-side functionality (static only).
- Analytics/tracking (can be revisited later if wanted).
- Automated tests — this is a static content site; verification is visual
  (local preview + browser check) rather than a test suite.

## Verification

Before pushing: serve the site locally, visually check the landing page and
at least one project page in a browser, confirm the partial include works
(header/footer render), confirm internal links resolve, and check basic
mobile-width responsiveness.
