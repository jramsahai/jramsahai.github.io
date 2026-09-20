#!/usr/bin/env python3
"""Drift and hygiene checks for the published pages of this static site.

Run from the repo root: python3 scripts/check.py

Regex-based on purpose -- the markup is small and hand-written, so an HTML
parser dependency isn't worth it. Prints one `path: message` line per
problem, then a summary line. Exits 1 if there were any errors; warnings
(asset size budget, unreferenced images) don't affect the exit code.

See docs/superpowers/plans/2026-09-20-site-review-fixes.md (work package B1)
for the full spec this implements.
"""
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://jramsahai.github.io/'
COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)

def strip_comments(text):
    return COMMENT_RE.sub('', text)

def read(path):
    return path.read_text(encoding='utf-8')

def rel(root, path):
    return str(path.relative_to(root))

def published_pages(root):
    pages = [root / 'index.html', root / '404.html']
    pages += sorted((root / 'projects').glob('*/index.html'))
    return pages

def template_page(root):
    return root / 'docs' / 'templates' / 'project-page.html'

HEADER_RE = re.compile(r'<header class="site-header">.*?</header>', re.DOTALL)
FOOTER_RE = re.compile(r'<footer class="site-footer">.*?</footer>', re.DOTALL)

def check_chrome_drift(root, errors, warnings):
    """1. Header/footer blocks byte-identical to index.html, on every page + template."""
    index_text = strip_comments(read(root / 'index.html'))
    idx_header, idx_footer = HEADER_RE.search(index_text), FOOTER_RE.search(index_text)
    if not idx_header or not idx_footer:
        errors.append('index.html: missing header or footer block; cannot use as the reference')
        return
    idx_header, idx_footer = idx_header.group(0), idx_footer.group(0)

    for page in published_pages(root) + [template_page(root)]:
        if page == root / 'index.html':
            continue
        label, text = rel(root, page), strip_comments(read(page))
        m = HEADER_RE.search(text)
        if not m:
            errors.append(f'{label}: missing <header class="site-header"> block')
        elif m.group(0) != idx_header:
            errors.append(f'{label}: header block differs from index.html')
        m = FOOTER_RE.search(text)
        if not m:
            errors.append(f'{label}: missing <footer class="site-footer"> block')
        elif m.group(0) != idx_footer:
            errors.append(f'{label}: footer block differs from index.html')

HEAD_LINE_PATTERNS = [
    ('charset meta', re.compile(r'<meta charset="[^"]*">')),
    ('viewport meta', re.compile(r'<meta name="viewport"[^>]*>')),
    ('theme-color meta', re.compile(r'<meta name="theme-color"[^>]*>')),
    ('svg icon link', re.compile(r'<link rel="icon"[^>]*type="image/svg\+xml"[^>]*>')),
    ('png icon link', re.compile(r'<link rel="icon"[^>]*type="image/png"[^>]*>')),
    ('apple-touch-icon link', re.compile(r'<link rel="apple-touch-icon"[^>]*>')),
    ('font preload link', re.compile(r'<link rel="preload"[^>]*>')),
    ('stylesheet link', re.compile(r'<link rel="stylesheet"[^>]*>')),
]

def check_head_lines(root, errors, warnings):
    """2. Shared head lines (read from index.html) present verbatim everywhere."""
    index_text = strip_comments(read(root / 'index.html'))
    pages = published_pages(root) + [template_page(root)]
    for name, pattern in HEAD_LINE_PATTERNS:
        matches = pattern.findall(index_text)
        expected = matches[0] if matches else None
        for page in pages:
            text = strip_comments(read(page))
            if expected is not None and expected not in text:
                errors.append(f'{rel(root, page)}: missing or differing {name} (expected the line from index.html)')
            elif expected is None and not pattern.search(text):
                errors.append(f'{rel(root, page)}: missing {name}')

H1_RE = re.compile(r'<h1\b')

def check_single_h1(root, errors, warnings):
    """3. Exactly one <h1> per published page."""
    for page in published_pages(root):
        count = len(H1_RE.findall(strip_comments(read(page))))
        if count != 1:
            errors.append(f'{rel(root, page)}: {count} <h1> elements found, expected exactly 1')

TITLE_RE = re.compile(r'<title>(.*?)</title>', re.DOTALL)
META_DESC_RE = re.compile(r'<meta name="description" content="([^"]*)"')
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]*)"')
OG_TITLE_RE = re.compile(r'<meta property="og:title" content="([^"]*)"')
OG_DESC_RE = re.compile(r'<meta property="og:description" content="([^"]*)"')
OG_URL_RE = re.compile(r'<meta property="og:url" content="([^"]*)"')
OG_IMAGE_RE = re.compile(r'<meta property="og:image" content="([^"]*)"')

def expected_canonical(root, page):
    if page == root / 'index.html':
        return SITE
    if page == root / '404.html':
        return SITE + '404.html'
    return f'{SITE}projects/{page.parent.name}/'

def _val(match):
    return match.group(1).strip() if match and match.group(1).strip() else None

def check_head_metadata(root, errors, warnings):
    """4. title/description/canonical/og:* present; canonical == og:url == expected path; og:image resolves."""
    for page in published_pages(root):
        text, label = strip_comments(read(page)), rel(root, page)
        fields = {
            'title': TITLE_RE.search(text), 'meta description': META_DESC_RE.search(text),
            'canonical': CANONICAL_RE.search(text), 'og:title': OG_TITLE_RE.search(text),
            'og:description': OG_DESC_RE.search(text), 'og:url': OG_URL_RE.search(text),
            'og:image': OG_IMAGE_RE.search(text),
        }
        for name, m in fields.items():
            if not _val(m):
                errors.append(f'{label}: empty or missing {name}')

        expected = expected_canonical(root, page)
        canonical, og_url = _val(fields['canonical']), _val(fields['og:url'])
        if canonical is not None and canonical != expected:
            errors.append(f'{label}: canonical {canonical!r} does not match expected {expected!r}')
        if og_url is not None and og_url != expected:
            errors.append(f'{label}: og:url {og_url!r} does not match expected {expected!r}')

        og_image = _val(fields['og:image'])
        if og_image:
            if not og_image.startswith(SITE):
                errors.append(f'{label}: og:image {og_image!r} does not start with {SITE}')
            elif not (root / og_image[len(SITE):]).is_file():
                errors.append(f'{label}: og:image {og_image!r} does not exist on disk')

ATTR_RE = re.compile(r'\b(?:href|src|poster)="(/(?!/)[^"]*)"')
CSS_URL_RE = re.compile(r'url\("(/(?!/)[^"]*)"\)')

def resolve_path(root, path_value):
    if path_value.endswith('/'):
        path_value += 'index.html'
    return root / path_value.lstrip('/')

def check_internal_links(root, errors, warnings):
    """5. Root-absolute href/src/poster (and CSS url()) targets exist; same-page fragments have a matching id."""
    pages = published_pages(root)
    page_paths = {p.resolve() for p in pages}

    for page in pages:
        text, label = strip_comments(read(page)), rel(root, page)
        for m in ATTR_RE.finditer(text):
            value = m.group(1)
            base, _, frag = value.partition('#')
            base = base or '/'
            fs_path = resolve_path(root, base)
            if not fs_path.is_file():
                errors.append(f'{label}: broken internal reference {value!r} ({rel(root, fs_path)} does not exist)')
                continue
            if frag and fs_path.resolve() in page_paths and f'id="{frag}"' not in read(fs_path):
                errors.append(f'{label}: fragment #{frag} in {value!r} not found in {rel(root, fs_path)}')

    css_path = root / 'assets' / 'css' / 'style.css'
    if css_path.is_file():
        for m in CSS_URL_RE.finditer(read(css_path)):
            fs_path = resolve_path(root, m.group(1))
            if not fs_path.is_file():
                errors.append(f'{rel(root, css_path)}: broken url() reference {m.group(1)!r} ({rel(root, fs_path)} does not exist)')

CARD_HREF_RE = re.compile(r'href="/projects/([a-z0-9-]+)/"')

def check_cards_match_pages(root, errors, warnings):
    """6. /projects/<slug>/ cards on index.html match the directories under projects/."""
    card_slugs = set(CARD_HREF_RE.findall(strip_comments(read(root / 'index.html'))))
    projects_dir = root / 'projects'
    dir_slugs = {p.name for p in projects_dir.iterdir() if p.is_dir() and (p / 'index.html').is_file()} if projects_dir.is_dir() else set()
    for slug in sorted(dir_slugs - card_slugs):
        errors.append(f'index.html: no project card links to /projects/{slug}/')
    for slug in sorted(card_slugs - dir_slugs):
        errors.append(f'index.html: project card links to /projects/{slug}/ but that page does not exist')

PLACEHOLDERS = ['example.com', 'your-handle', 'PROJECT TITLE', 'ONE-LINE DESCRIPTION', '<slug>', 'YEAR<']

def check_no_placeholders(root, errors, warnings):
    """7. No leftover template placeholders in published pages."""
    for page in published_pages(root):
        text, label = strip_comments(read(page)), rel(root, page)
        for placeholder in PLACEHOLDERS:
            if placeholder in text:
                errors.append(f'{label}: leftover placeholder {placeholder!r}')

ATTR_PAIR_RE = re.compile(r'([a-zA-Z-]+)="([^"]*)"')
IMG_TAG_RE = re.compile(r'<img\b([^>]*)>')
VIDEO_TAG_RE = re.compile(r'<video\b([^>]*)>')

def parse_attrs(tag_inner):
    return dict(ATTR_PAIR_RE.findall(tag_inner))

def png_size(data):
    if data[:8] != b'\x89PNG\r\n\x1a\n' or data[12:16] != b'IHDR':
        return None
    return struct.unpack('>II', data[16:24])

def webp_size(data):
    if data[:4] != b'RIFF' or data[8:12] != b'WEBP':
        return None
    fourcc = data[12:16]
    if fourcc == b'VP8 ':
        if data[23:26] != b'\x9d\x01\x2a':
            return None
        w = struct.unpack('<H', data[26:28])[0] & 0x3FFF
        h = struct.unpack('<H', data[28:30])[0] & 0x3FFF
        return w, h
    if fourcc == b'VP8L':
        if data[20:21] != b'\x2f':
            return None
        bits = struct.unpack('<I', data[21:25])[0]
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if fourcc == b'VP8X':
        return int.from_bytes(data[24:27], 'little') + 1, int.from_bytes(data[27:30], 'little') + 1
    return None

def real_image_size(path):
    try:
        data = path.read_bytes()
    except OSError:
        return None
    suffix = path.suffix.lower()
    if suffix == '.png':
        return png_size(data)
    if suffix == '.webp':
        return webp_size(data)
    return None

def check_images(root, errors, warnings):
    """8. <img> has alt/width/height; webp/png dims match the real file; video poster aspect ratio matches (1% tolerance)."""
    for page in published_pages(root):
        text, label = strip_comments(read(page)), rel(root, page)

        for m in IMG_TAG_RE.finditer(text):
            attrs = parse_attrs(m.group(1))
            src = attrs.get('src')
            ref = src or m.group(0)[:60]
            if 'alt' not in attrs:  # alt="" is allowed: the spec uses it for decorative images
                errors.append(f'{label}: <img> missing alt ({ref})')
            if not attrs.get('width') or not attrs.get('height'):
                errors.append(f'{label}: <img> missing width/height ({ref})')
                continue
            if not src or not src.startswith('/'):
                continue
            src_path = root / src.lstrip('/')
            if src_path.suffix.lower() not in ('.webp', '.png') or not src_path.is_file():
                continue  # not a checkable format, or already reported by the link check
            real = real_image_size(src_path)
            if real is None:
                errors.append(f'{label}: could not read dimensions of {src}')
                continue
            try:
                declared = (int(attrs['width']), int(attrs['height']))
            except ValueError:
                errors.append(f'{label}: non-numeric width/height on <img src="{src}">')
                continue
            if declared != real:
                errors.append(f'{label}: <img src="{src}"> width/height {declared[0]}x{declared[1]} does not match real size {real[0]}x{real[1]}')

        for m in VIDEO_TAG_RE.finditer(text):
            attrs = parse_attrs(m.group(1))
            poster = attrs.get('poster')
            if not poster or not poster.startswith('/'):
                continue
            poster_path = root / poster.lstrip('/')
            if not poster_path.is_file():
                continue
            real = real_image_size(poster_path)
            if real is None:
                continue
            try:
                vw, vh = int(attrs['width']), int(attrs['height'])
            except (KeyError, ValueError):
                errors.append(f'{label}: <video poster="{poster}"> missing or non-numeric width/height')
                continue
            if abs(real[0] / real[1] - vw / vh) / (vw / vh) > 0.01:
                errors.append(f'{label}: <video poster="{poster}"> aspect ratio {real[0]}x{real[1]} does not match video {vw}x{vh} (>1% off)')

CAROUSEL_SECTION_RE = re.compile(r'<section class="carousel[^"]*"[^>]*>.*?</section>', re.DOTALL)
SLIDE_LABEL_RE = re.compile(r'aria-roledescription="slide" aria-label="(\d+) of (\d+)"')
CAROUSEL_SCRIPT_RE = re.compile(r'<script src="/assets/js/carousel\.js" defer></script>')

def check_carousels(root, errors, warnings):
    """9. Carousel slide aria-labels run 1..M; carousel.js present iff a carousel is present."""
    for page in published_pages(root):
        text, label = strip_comments(read(page)), rel(root, page)
        has_carousel = 'class="carousel' in text
        has_script = bool(CAROUSEL_SCRIPT_RE.search(text))
        if has_carousel and not has_script:
            errors.append(f'{label}: has a carousel but is missing the /assets/js/carousel.js script tag')
        if has_script and not has_carousel:
            errors.append(f'{label}: includes carousel.js but has no carousel')

        for section in CAROUSEL_SECTION_RE.findall(text):
            labels = SLIDE_LABEL_RE.findall(section)
            total = len(labels)
            if total == 0:
                continue
            numbers = [int(n) for n, _ in labels]
            totals = {int(t) for _, t in labels}
            if totals != {total}:
                errors.append(f'{label}: carousel has {total} slides but aria-label totals are {sorted(totals)}')
            if numbers != list(range(1, total + 1)):
                errors.append(f'{label}: carousel aria-label numbers are {numbers}, expected 1..{total} in order')

IMAGE_EXTS = {'.webp', '.png', '.jpg', '.jpeg'}
SIZE_LIMIT_IMAGE = 300 * 1024
SIZE_LIMIT_MP4 = 4 * 1024 * 1024

def check_asset_budgets(root, errors, warnings):
    """10. Warn on images over 300 KB and MP4s over 4 MB."""
    images_dir = root / 'assets' / 'images'
    if not images_dir.is_dir():
        return
    for path in sorted(images_dir.rglob('*')):
        if not path.is_file():
            continue
        suffix, size = path.suffix.lower(), path.stat().st_size
        if suffix in IMAGE_EXTS and size > SIZE_LIMIT_IMAGE:
            warnings.append(f'{rel(root, path)}: {size / 1024:.0f} KB exceeds the 300 KB image budget (warning)')
        elif suffix == '.mp4' and size > SIZE_LIMIT_MP4:
            warnings.append(f'{rel(root, path)}: {size / (1024 * 1024):.1f} MB exceeds the 4 MB video budget (warning)')

def check_unreferenced_images(root, errors, warnings):
    """11. Warn on image files under assets/images/ that no published page references (og:image counts)."""
    images_dir = root / 'assets' / 'images'
    if not images_dir.is_dir():
        return
    referenced = set()
    for page in published_pages(root):
        text = strip_comments(read(page))
        for m in ATTR_RE.finditer(text):
            value = m.group(1).split('#', 1)[0]
            if value.startswith('/assets/images/'):
                referenced.add((root / value.lstrip('/')).resolve())
        og_match = OG_IMAGE_RE.search(text)
        if og_match and og_match.group(1).strip().startswith(SITE):
            referenced.add((root / og_match.group(1).strip()[len(SITE):]).resolve())
    for path in sorted(images_dir.rglob('*')):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS and path.resolve() not in referenced:
            warnings.append(f'{rel(root, path)}: not referenced by any published page (warning)')

ERROR_CHECKS = [
    check_chrome_drift, check_head_lines, check_single_h1, check_head_metadata,
    check_internal_links, check_cards_match_pages, check_no_placeholders,
    check_images, check_carousels,
]
WARNING_CHECKS = [check_asset_budgets, check_unreferenced_images]

def main(root=None):
    root = root or ROOT
    errors, warnings = [], []
    for check in ERROR_CHECKS + WARNING_CHECKS:
        check(root, errors, warnings)
    for line in errors + warnings:
        print(line)
    print(f'{len(errors)} error(s), {len(warnings)} warning(s)')
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
