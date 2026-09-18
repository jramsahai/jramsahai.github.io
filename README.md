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
