#!/usr/bin/env python3
"""
Convert SleuthKit MediaWiki XML export to Jekyll GitHub Pages site.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

XML_FILE = "SleuthKitWiki-20260329162944.xml"
OUT_DIR = Path(".")
MW_NS = "http://www.mediawiki.org/xml/export-0.8/"

# Formatting issues log
issues = []


# ---------------------------------------------------------------------------
# Slug / URL helpers
# ---------------------------------------------------------------------------

def title_to_slug(title: str) -> str:
    slug = title.strip()
    slug = re.sub(r'[:/]', '-', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'[^A-Za-z0-9_\-]', '', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug


def title_to_mw_paths(title: str) -> list[str]:
    """Return the two old MediaWiki path-based URL forms for a title.

    MediaWiki uses underscores for spaces, e.g. "The Sleuth Kit" →
      /wiki/The_Sleuth_Kit
      /index.php/The_Sleuth_Kit
    """
    mw = title.strip().replace(' ', '_')
    return [f"/wiki/{mw}", f"/index.php/{mw}"]


def title_to_url(title: str, redirect_map: dict = None,
                 canonical_titles: dict = None) -> str:
    """Return the Jekyll relative URL, resolving redirects if provided.

    canonical_titles: dict mapping lower-case title → canonical cased title
    """
    if redirect_map and title in redirect_map:
        title = redirect_map[title]
    # Resolve case: e.g. "timelines" → "Timelines"
    if canonical_titles:
        title = canonical_titles.get(title.lower(), title)
    return f"/{title_to_slug(title)}/"


# ---------------------------------------------------------------------------
# MediaWiki → Markdown converter
# ---------------------------------------------------------------------------

def mw_to_md(wikitext: str, page_title: str, all_titles: set,
             redirect_map: dict, canonical_titles: dict) -> str:
    text = wikitext

    # ---- 1. Stash <nowiki> and code blocks so later steps don't corrupt them ----
    stash: dict[str, str] = {}
    stash_idx = [0]

    def stash_block(rendered: str) -> str:
        key = f"\x00STASH{stash_idx[0]}\x00"
        stash[key] = rendered
        stash_idx[0] += 1
        return key

    def stash_nowiki(m):
        return stash_block(m.group(1))
    text = re.sub(r'<nowiki>(.*?)</nowiki>', stash_nowiki, text, flags=re.DOTALL)

    # ---- 2. Source / syntaxhighlight code blocks (stash after converting) ----
    def convert_source(m):
        lang = (m.group(1) or '').lower().strip()
        code = m.group(2).strip()
        return stash_block(f"\n```{lang}\n{code}\n```\n")
    text = re.sub(
        r'<(?:source|syntaxhighlight)[^>]*\blang=["\']?(\w+)["\']?[^>]*>(.*?)</(?:source|syntaxhighlight)>',
        convert_source, text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(
        r'<(?:source|syntaxhighlight)[^>]*>(.*?)</(?:source|syntaxhighlight)>',
        lambda m: stash_block(f"\n```\n{m.group(1).strip()}\n```\n"),
        text, flags=re.DOTALL | re.IGNORECASE)

    # ---- 3. <pre> blocks (stash after converting) ----
    text = re.sub(r'<pre>(.*?)</pre>',
                  lambda m: stash_block(f"\n```\n{m.group(1).strip()}\n```\n"),
                  text, flags=re.DOTALL | re.IGNORECASE)

    # ---- 4. <code> inline ----
    text = re.sub(r'<code>(.*?)</code>', r'`\1`', text, flags=re.DOTALL | re.IGNORECASE)

    # ---- 5. Tables (before anything else messes up | chars) ----
    text = convert_tables(text, page_title)

    # ---- 6. Strip [[Category:...]] (extracted separately) ----
    text = re.sub(r'\[\[Category:[^\]]*\]\]\n?', '', text, flags=re.IGNORECASE)

    # ---- 7. File / Image links ----
    def convert_file(m):
        full = m.group(1)
        parts = [p.strip() for p in full.split('|')]
        bare = re.sub(r'^(?:File|Image):', '', parts[0], flags=re.IGNORECASE)
        alt = parts[-1] if len(parts) > 1 else bare
        link_param = next((p for p in parts if p.lower().startswith('link=')), None)
        if link_param:
            target = link_param[5:]
            url = title_to_url(target, redirect_map, canonical_titles) if target in all_titles else target
            return f"[![{alt}](/assets/images/{bare})]({url})"
        return f"![{alt}](/assets/images/{bare})"
    text = re.sub(r'\[\[(?:File|Image):([^\]]+)\]\]', convert_file, text, flags=re.IGNORECASE)

    # ---- 8. Internal wiki links ----
    def convert_internal(m):
        inner = m.group(1)
        if '|' in inner:
            target, label = inner.split('|', 1)
        else:
            target = label = inner
        target = target.strip()
        label = label.strip()
        url = title_to_url(target, redirect_map, canonical_titles)
        return f"[{label}]({url})"
    text = re.sub(r'\[\[([^\[\]]+)\]\]', convert_internal, text)

    # ---- 9. External links: [url text] and [url] ----
    text = re.sub(r'\[(\S+https?://[^\s\]]+)\s+([^\]]+)\]', r'[\2](\1)', text)
    text = re.sub(r'\[(https?://[^\s\]]+)\s+([^\]]+)\]', r'[\2](\1)', text)
    text = re.sub(r'\[(https?://[^\s\]]+)\]', r'<\1>', text)

    # ---- 10. Lists — MUST happen before heading conversion ----
    # Ordered/unordered nested lists: ##, **, ***  etc.
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        # Nested list items (2+ markers)
        m = re.match(r'^(\*{2,}|\#{2,})(.*)', line)
        if m:
            markers = m.group(1)
            rest = m.group(2)
            depth = len(markers) - 1
            indent = '  ' * depth
            bullet = '*' if markers[0] == '*' else '1.'
            new_lines.append(f"{indent}{bullet} {rest.strip()}")
        else:
            # Top-level ordered list: single # NOT followed by another #
            # (Headings at this stage still use = = syntax, not # yet)
            om = re.match(r'^#([^#\n].*)', line)
            if om:
                new_lines.append(f"1. {om.group(1).strip()}")
            else:
                new_lines.append(line)
    text = '\n'.join(new_lines)

    # ---- 11. Headings (= → #) — after list processing ----
    for level in range(6, 0, -1):
        eq = '=' * level
        text = re.sub(
            rf'^{eq}\s*(.*?)\s*{eq}\s*$',
            lambda m, l=level: '#' * l + ' ' + m.group(1),
            text, flags=re.MULTILINE)

    # ---- 12. Bold/italic ----
    text = re.sub(r"'''''(.*?)'''''", r'***\1***', text)
    text = re.sub(r"'''(.*?)'''", r'**\1**', text)
    text = re.sub(r"''(.*?)''", r'*\1*', text)

    # ---- 13. Definition lists ----
    text = re.sub(r'^;(.+)$', r'**\1**', text, flags=re.MULTILINE)
    text = re.sub(r'^:([^:].+)$', r'> \1', text, flags=re.MULTILINE)

    # ---- 14. Horizontal rule ----
    text = re.sub(r'^-{4,}$', '\n---\n', text, flags=re.MULTILINE)

    # ---- 15. <br> ----
    text = re.sub(r'<br\s*/?>', '  \n', text, flags=re.IGNORECASE)

    # ---- 16. HTML comments ----
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    # ---- 17. Strip structural HTML we can't convert ----
    text = re.sub(r'</?(?:center|div|span|font)[^>]*>', '', text, flags=re.IGNORECASE)

    # ---- 18. <ref> tags ----
    text = re.sub(r'<ref[^>]*/>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<references\s*/?>', '', text, flags=re.IGNORECASE)

    # ---- 19. Templates ----
    remaining_templates = re.findall(r'\{\{([^{}]+)\}\}', text)
    for t in remaining_templates:
        issues.append(f"[{page_title}] Unconverted template: {{{{{t}}}}}")
    text = re.sub(r'\{\{[^{}]*\}\}', '', text)
    text = re.sub(r'\{\{[^{}]*\}\}', '', text)  # second pass for nesting

    # ---- 20. Restore all stashed blocks ----
    for key, val in stash.items():
        text = text.replace(key, val)

    # ---- 21. Clean up blank lines ----
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    return text


# ---------------------------------------------------------------------------
# Table conversion
# ---------------------------------------------------------------------------

def convert_tables(text: str, page_title: str) -> str:
    lines = text.split('\n')
    out_lines = []
    in_table = False
    table_lines = []

    for line in lines:
        if not in_table and line.strip().startswith('{|'):
            in_table = True
            table_lines = [line]
        elif in_table:
            table_lines.append(line)
            if line.strip() == '|}':
                in_table = False
                out_lines.append(parse_mw_table(table_lines, page_title))
                table_lines = []
        else:
            out_lines.append(line)

    if table_lines:
        issues.append(f"[{page_title}] Unclosed table — rendered as-is")
        out_lines.extend(table_lines)

    return '\n'.join(out_lines)


def parse_mw_table(lines: list, page_title: str) -> str:
    html = ['<table class="wiki-table table table-bordered table-sm">']
    header_rows = []
    body_rows = []
    current_row = []
    is_header_row = False
    caption = None
    row_started = False

    for line in lines:
        s = line.strip()
        if s.startswith('{|') or s == '|}':
            continue
        elif s.startswith('|+'):
            caption = s[2:].strip()
        elif s == '|-':
            if row_started:
                if is_header_row:
                    header_rows.append(current_row[:])
                else:
                    body_rows.append(current_row[:])
            current_row = []
            is_header_row = False
            row_started = True
        elif s.startswith('!'):
            is_header_row = True
            row_started = True
            cells = re.split(r'\|\||!!', s[1:])
            for cell in cells:
                # strip cell attributes: "attr | content"
                cell = re.sub(r'^[^|]*\|(?!\|)', '', cell).strip()
                current_row.append(('th', cell))
        elif s.startswith('|'):
            row_started = True
            cells = re.split(r'\|\|', s[1:])
            for cell in cells:
                cell = re.sub(r'^[^|]*\|(?!\|)', '', cell).strip()
                current_row.append(('td', cell))
        else:
            if current_row:
                tag, content = current_row[-1]
                current_row[-1] = (tag, content + ' ' + s)

    if current_row:
        if is_header_row:
            header_rows.append(current_row)
        else:
            body_rows.append(current_row)

    if caption:
        html.append(f'  <caption>{caption}</caption>')

    if header_rows:
        html.append('  <thead>')
        for row in header_rows:
            html.append('  <tr>')
            for tag, cell in row:
                html.append(f'    <th>{cell}</th>')
            html.append('  </tr>')
        html.append('  </thead>')

    if body_rows:
        html.append('  <tbody>')
        for row in body_rows:
            html.append('  <tr>')
            for tag, cell in row:
                html.append(f'    <{tag}>{cell}</{tag}>')
            html.append('  </tr>')
        html.append('  </tbody>')

    html.append('</table>')
    return '\n'.join(html)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_categories(wikitext: str) -> list:
    cats = re.findall(r'\[\[Category:([^\|\]]+)(?:\|[^\]]*)?\]\]', wikitext, re.IGNORECASE)
    return [c.strip() for c in cats]


def extract_redirect_target(wikitext: str) -> str | None:
    m = re.match(r'^\s*#REDIRECT\s*\[\[([^\]]+)\]\]', wikitext, re.IGNORECASE)
    return m.group(1).strip() if m else None


# ---------------------------------------------------------------------------
# Static file writers
# ---------------------------------------------------------------------------

def write_page(slug: str, title: str, body: str, categories: list,
               timestamp: str, redirect_from: list[str] = None):
    path = OUT_DIR / f"{slug}.md"
    safe_title = title.replace('"', '\\"')
    cats_yaml = ''
    if categories:
        cats_yaml = '\ncategories:\n' + ''.join(f'  - "{c}"\n' for c in categories)
    redir_yaml = ''
    if redirect_from:
        redir_yaml = '\nredirect_from:\n' + ''.join(f'  - "{r}"\n' for r in redirect_from)
    front = (f'---\nlayout: default\ntitle: "{safe_title}"{cats_yaml}'
             f'{redir_yaml}\nlast_modified: {timestamp[:10]}\n---\n')
    path.write_text(front + '\n' + body + '\n', encoding='utf-8')


def write_config():
    content = """\
title: "The Sleuth Kit Wiki"
description: "Knowledge base for The Sleuth Kit and Autopsy digital forensics tools"
baseurl: ""
url: "https://wiki.sleuthkit.org"

markdown: kramdown
highlighter: rouge

kramdown:
  input: GFM
  syntax_highlighter: rouge

plugins:
  - jekyll-redirect-from
  - jekyll-seo-tag

defaults:
  - scope:
      path: ""
    values:
      layout: default

exclude:
  - convert.py
  - "*.xml"
  - Gemfile
  - Gemfile.lock
  - vendor/
"""
    (OUT_DIR / '_config.yml').write_text(content, encoding='utf-8')


def write_gemfile():
    (OUT_DIR / 'Gemfile').write_text("""\
source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "jekyll-redirect-from"
gem "jekyll-seo-tag"
gem "kramdown-parser-gfm"
gem "rouge"
gem "webrick"
""", encoding='utf-8')


def write_layout():
    (OUT_DIR / '_layouts').mkdir(exist_ok=True)
    (OUT_DIR / '_layouts' / 'default.html').write_text("""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% if page.title %}{{ page.title }} — {% endif %}{{ site.title }}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="/assets/css/style.css" rel="stylesheet">
  {% seo %}
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark" style="background-color: #1c2130;">
  <div class="container">
    <a class="navbar-brand fw-semibold" href="/">
      <span style="color: #3b6fc4;">&#9650;</span> The Sleuth Kit Wiki
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarMain">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarMain">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="/The-Sleuth-Kit/">The Sleuth Kit</a></li>
        <li class="nav-item"><a class="nav-link" href="/Autopsy/">Autopsy</a></li>
        <li class="nav-item">
          <a class="nav-link" href="https://sleuthkit.org" target="_blank" rel="noopener">sleuthkit.org ↗</a>
        </li>
      </ul>
    </div>
  </div>
</nav>

<div class="container py-4">
  <div class="row">
    <div class="col-lg-9">
      {% if page.title and page.title != "Home" %}
        <h1 class="page-title mb-4">{{ page.title }}</h1>
      {% endif %}
      <div class="wiki-content">
        {{ content }}
      </div>
      {% if page.last_modified %}
        <hr class="mt-5">
        <p class="text-muted small">Last modified: {{ page.last_modified }}</p>
      {% endif %}
    </div>
    <div class="col-lg-3 d-none d-lg-block">
      <div class="card border-0 shadow-sm" style="position:sticky;top:1rem;">
        <div class="card-body">
          <h6 class="fw-semibold text-uppercase mb-3"
              style="color:#3b6fc4;font-size:0.7rem;letter-spacing:0.08em;">Quick Links</h6>
          <ul class="list-unstyled mb-0 small">
            <li><a href="/TSK-Tool-Overview/">TSK Tool Overview</a></li>
            <li><a href="/The-Sleuth-Kit/">The Sleuth Kit</a></li>
            <li><a href="/Autopsy/">Autopsy</a></li>
            <li><a href="/TSK-Developers-Guide/">Developer's Guide</a></li>
            <li><a href="/Blackboard/">Blackboard</a></li>
            <li><a href="/Body-file/">Body file</a></li>
            <li><a href="/Timelines/">Timelines</a></li>
            <li><a href="/FAT/">FAT</a></li>
            <li><a href="/NTFS/">NTFS</a></li>
            <li><a href="/ExtX/">ExtX</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>

<footer class="mt-5 py-4" style="background-color:#1c2130;color:#aab4c8;">
  <div class="container">
    <div class="row">
      <div class="col-md-6">
        <p class="mb-1 small">
          <strong style="color:#fff;">The Sleuth Kit Wiki</strong> —
          Archived documentation for The Sleuth Kit and Autopsy.
        </p>
        <p class="mb-0 small">
          For current docs visit <a href="https://sleuthkit.org" style="color:#3b6fc4;">sleuthkit.org</a>.
        </p>
      </div>
      <div class="col-md-6 text-md-end mt-3 mt-md-0">
        <p class="mb-0 small">Content originally from wiki.sleuthkit.org</p>
      </div>
    </div>
  </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""", encoding='utf-8')


def write_css():
    (OUT_DIR / 'assets' / 'css').mkdir(parents=True, exist_ok=True)
    (OUT_DIR / 'assets' / 'css' / 'style.css').write_text("""\
/* SleuthKit Wiki */
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 16px;
  color: #2d3748;
  background: #fff;
}
.page-title {
  font-weight: 700;
  color: #1c2130;
  border-bottom: 3px solid #3b6fc4;
  padding-bottom: .5rem;
}
.wiki-content h1,.wiki-content h2,.wiki-content h3,
.wiki-content h4,.wiki-content h5,.wiki-content h6 {
  font-weight: 600;
  color: #1c2130;
  margin-top: 1.75rem;
  margin-bottom: .75rem;
}
.wiki-content h1 { font-size:1.75rem; border-bottom:2px solid #e2e8f0; padding-bottom:.4rem; }
.wiki-content h2 { font-size:1.4rem;  border-bottom:1px solid #e2e8f0; padding-bottom:.3rem; }
.wiki-content h3 { font-size:1.15rem; }
.wiki-content a { color:#3b6fc4; text-decoration:none; }
.wiki-content a:hover { color:#2a52a0; text-decoration:underline; }
.wiki-content pre, .wiki-content code {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: .875em;
}
.wiki-content pre {
  background:#f7f8fa; border:1px solid #e2e8f0; border-radius:6px;
  padding:1rem; overflow-x:auto;
}
.wiki-content code {
  background:#f7f8fa; border-radius:3px; padding:.15em .35em; color:#c7254e;
}
.wiki-content pre code { background:none; padding:0; color:inherit; }
.wiki-content blockquote {
  border-left:4px solid #3b6fc4; padding-left:1rem; color:#4a5568; margin:1rem 0;
}
.wiki-content ul,.wiki-content ol { padding-left:1.5rem; }
.wiki-content li { margin-bottom:.25rem; }
.wiki-table, .wiki-content table {
  width:100%; margin:1rem 0; border-collapse:collapse; font-size:.9rem;
}
.wiki-table th, .wiki-content table th {
  background:#1c2130; color:#fff; padding:.5rem .75rem; font-weight:600;
}
.wiki-table td, .wiki-content table td {
  padding:.4rem .75rem; border:1px solid #e2e8f0; vertical-align:top;
}
.wiki-table tr:nth-child(even) td, .wiki-content table tr:nth-child(even) td {
  background:#f7f8fa;
}
.wiki-content .sidebar-card a { color:#3b6fc4; display:block; padding:.15rem 0; }
.wiki-content .sidebar-card a:hover { color:#2a52a0; }
.wiki-note {
  background:#ebf4ff; border-left:4px solid #3b6fc4;
  padding:.75rem 1rem; border-radius:0 4px 4px 0; margin:1rem 0;
}
.navbar-brand { font-size:1.1rem; letter-spacing:-.01em; }
.category-section { margin-bottom:2rem; }
.category-section h2 {
  font-size:1.1rem; font-weight:600; color:#3b6fc4;
  border-bottom:1px solid #e2e8f0; padding-bottom:.3rem; margin-bottom:.75rem;
}
.category-section ul {
  list-style:none; padding-left:0; column-count:2; column-gap:2rem;
}
.category-section li { margin-bottom:.25rem; break-inside:avoid; }
.category-section a { color:#3b6fc4; text-decoration:none; }
.category-section a:hover { text-decoration:underline; }
""", encoding='utf-8')


def write_images_dir():
    img = OUT_DIR / 'assets' / 'images'
    img.mkdir(parents=True, exist_ok=True)
    (img / 'README.md').write_text(
        "# Images\n\nPlace wiki image files here (renzik.png, hash3_v1_sm.jpg, etc.).\n")


# ---------------------------------------------------------------------------
# Index page
# ---------------------------------------------------------------------------

CATEGORY_ORDER = [
    "Tools", "File Systems", "Concepts", "Development",
    "Autopsy", "Documentation", "Uncategorized",
]

MANUAL_CATS = {
    "Adding Artifacts and Attributes": "Development",
    "Allocated files": "Concepts",
    "Artifact Examples": "Development",
    "Autopsy": "Autopsy",
    "Autopsy 3 Design": "Autopsy",
    "Autopsy 3 Logging and Error Checking": "Autopsy",
    "Autopsy 3 Module Versions": "Autopsy",
    "Autopsy 3 Troubleshooting": "Autopsy",
    "Autopsy 3 WinFE": "Autopsy",
    "Autopsy 3rd Party Modules": "Autopsy",
    "Autopsy Developer's Guide": "Autopsy",
    "Autopsy Keyword Search Module": "Autopsy",
    "Autopsy User's Guide": "Autopsy",
    "Autopsy: Setting Up a Case": "Autopsy",
    "Blackboard": "Development",
    "Blkcalc": "Tools", "Blkcat": "Tools", "Blkls": "Tools", "Blkstat": "Tools",
    "Block": "Concepts", "Block Address": "Concepts",
    "Body file": "Concepts",
    "Books and Courses": "Documentation",
    "Carving": "Concepts",
    "Case Studies": "Documentation",
    "Chunk": "Concepts", "Cluster": "Concepts",
    "Data unit": "Concepts",
    "Database v7.2 Schema": "Development",
    "Dcalc": "Tools", "Dcat": "Tools",
    "Deleted files": "Concepts",
    "Design Documents": "Development",
    "Developer Guidelines": "Development",
    "Disk sreset": "Tools", "Disk stat": "Tools",
    "Dls": "Tools",
    "Dstat": "Tools",
    "Error Messages": "Tools",
    "ExFAT": "File Systems", "ExFAT Implementation Notes": "File Systems",
    "ExtX": "File Systems",
    "FAT": "File Systems", "FAT Implementation Notes": "File Systems",
    "FS Analysis": "Concepts",
    "Ffind": "Tools", "Fls": "Tools",
    "Fragment": "Concepts",
    "Fsstat": "Tools",
    "Git": "Development", "Git workflow": "Development",
    "HFS": "File Systems",
    "HashDB Schema": "Development",
    "Help Documents": "Documentation",
    "Hfind": "Tools",
    "ISO9660": "File Systems", "ISO9660 Implementation Notes": "File Systems",
    "Icat": "Tools", "Ifind": "Tools", "Ils": "Tools",
    "Img cat": "Tools", "Img stat": "Tools",
    "Istat": "Tools",
    "Jcat": "Tools", "Jls": "Tools",
    "Mac-robber": "Tools", "Mactime": "Tools", "Mactime output": "Tools",
    "Main Page": "Uncategorized",
    "Metadata Address": "Concepts",
    "Mmcat": "Tools", "Mmls": "Tools", "Mmstat": "Tools",
    "NTFS": "File Systems",
    "NTFS File Recovery": "File Systems",
    "NTFS Implementation Notes": "File Systems",
    "Orphan Files": "Concepts",
    "PTK": "Tools",
    "Presentations": "Documentation",
    "Project Communication": "Development",
    "Reference Documents": "Documentation",
    "SQLite Database v2 Schema": "Development",
    "SQLite Database v3 Schema": "Development",
    "SQLite Database v6 Schema": "Development",
    "Sector": "Concepts",
    "Sigfind": "Tools",
    "Sleuthkit-users": "Development",
    "Sorter": "Tools",
    "TCT": "Tools",
    "TSK Bindings": "Development",
    "TSK Developer's Guide": "Development",
    "TSK Framework": "Development",
    "TSK Java Bindings": "Development",
    "TSK Library User's Guide": "Documentation",
    "TSK Schema Versioning": "Development",
    "TSK Tool Overview": "Tools",
    "TSK User's Guide": "Documentation",
    "TSK Version Numbers": "Development",
    "The Sleuth Kit": "Tools",
    "The Sleuth Kit commands": "Tools",
    "Timelines": "Concepts",
    "Tools Using TSK or Autopsy": "Tools",
    "Trackers": "Development",
    "Tsk comparedir": "Tools",
    "Tsk gettimes": "Tools",
    "Tsk loaddb": "Tools",
    "Tsk recover": "Tools",
    "UFS": "File Systems",
    "Windows Implementation Notes": "File Systems",
    "YAFFS2": "File Systems",
    "YAFFS2 Implementation Notes": "File Systems",
}


def write_index(pages_info: list):
    by_cat = defaultdict(list)
    for title, slug, cats in pages_info:
        if title == 'Main Page':
            continue
        assigned = cats[0] if cats else MANUAL_CATS.get(title, 'Uncategorized')
        if assigned not in CATEGORY_ORDER:
            assigned = 'Uncategorized'
        by_cat[assigned].append((title, slug))

    for cat in by_cat:
        by_cat[cat].sort(key=lambda x: x[0].lower())

    lines = [
        '---', 'layout: default', 'title: "Home"', '---', '',
        '# The Sleuth Kit Wiki', '',
        '<div class="wiki-note">',
        '<strong>Note:</strong> This is an archived version of wiki.sleuthkit.org.',
        'For current documentation, visit <a href="https://sleuthkit.org">sleuthkit.org</a>.',
        '</div>', '',
        'This wiki covers **The Sleuth Kit** (TSK) library and command-line tools,',
        '**Autopsy** forensic browser, and related digital forensics concepts.', '',
        '---', '',
        '<div class="row">',
        '<div class="col-md-4 mb-3"><div class="card border-0 shadow-sm h-100"><div class="card-body">',
        '<h5 class="card-title" style="color:#3b6fc4;">The Sleuth Kit</h5>',
        '<p class="card-text small">Library and command-line tools for disk image analysis.</p>',
        '<a href="/The-Sleuth-Kit/" class="btn btn-sm btn-outline-primary">Learn more</a>',
        '</div></div></div>',
        '<div class="col-md-4 mb-3"><div class="card border-0 shadow-sm h-100"><div class="card-body">',
        '<h5 class="card-title" style="color:#3b6fc4;">Autopsy</h5>',
        '<p class="card-text small">Graphical forensic platform built on TSK.</p>',
        '<a href="/Autopsy/" class="btn btn-sm btn-outline-primary">Learn more</a>',
        '</div></div></div>',
        '<div class="col-md-4 mb-3"><div class="card border-0 shadow-sm h-100"><div class="card-body">',
        '<h5 class="card-title" style="color:#3b6fc4;">TSK Tool Overview</h5>',
        '<p class="card-text small">Overview of all command-line tools organized by layer.</p>',
        '<a href="/TSK-Tool-Overview/" class="btn btn-sm btn-outline-primary">Learn more</a>',
        '</div></div></div>',
        '</div>', '', '---', '', '## All Pages by Category', '',
    ]

    for cat in CATEGORY_ORDER:
        if cat not in by_cat:
            continue
        lines += [
            '<div class="category-section">',
            f'<h2>{cat}</h2>',
            '<ul>',
        ]
        for title, slug in by_cat[cat]:
            lines.append(f'<li><a href="/{slug}/">{title}</a></li>')
        lines += ['</ul>', '</div>', '']

    (OUT_DIR / 'index.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    xml_path = Path(XML_FILE)
    if not xml_path.exists():
        print(f"ERROR: {XML_FILE} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Parsing {XML_FILE}...")
    tree = ET.parse(xml_path)
    root = tree.getroot()
    ns_map = {'mw': MW_NS}

    pages = root.findall('mw:page', ns_map)
    print(f"Found {len(pages)} pages")

    # Pass 1: collect titles and redirects
    all_titles: set[str] = set()
    redirect_map: dict[str, str] = {}  # redirect title → canonical title

    for p in pages:
        if p.findtext('mw:ns', namespaces=ns_map) != '0':
            continue
        title = p.findtext('mw:title', namespaces=ns_map)
        if not title:
            continue
        all_titles.add(title)
        text_el = p.find('.//mw:text', ns_map)
        wikitext = text_el.text if text_el is not None and text_el.text else ''
        target = extract_redirect_target(wikitext)
        if target:
            redirect_map[title] = target

    # canonical_titles: lowercase → properly-cased title for case-insensitive resolution
    canonical_titles: dict[str, str] = {t.lower(): t for t in all_titles}

    # reverse_redirect: canonical title → sorted list of source titles that redirect to it
    # Used to add redirect_from paths to the target page.
    reverse_redirect: dict[str, list[str]] = defaultdict(list)
    for src, dst in redirect_map.items():
        # Resolve dst case-insensitively to match an actual page title
        canonical_dst = canonical_titles.get(dst.lower(), dst)
        reverse_redirect[canonical_dst].append(src)

    print(f"Found {len(redirect_map)} redirects")

    # Set up output dirs
    (OUT_DIR / 'assets' / 'images').mkdir(parents=True, exist_ok=True)

    # Write infrastructure
    print("Writing site infrastructure...")
    write_config()
    write_gemfile()
    write_layout()
    write_css()
    write_images_dir()

    # Pass 2: convert pages
    pages_info = []
    converted = 0
    skipped_redirects = []
    skipped_empty = []

    print("Converting pages...")
    for p in pages:
        if p.findtext('mw:ns', namespaces=ns_map) != '0':
            continue
        title = p.findtext('mw:title', namespaces=ns_map)
        if not title:
            continue

        text_el = p.find('.//mw:text', ns_map)
        wikitext = text_el.text if text_el is not None and text_el.text else ''
        timestamp = p.findtext('.//mw:timestamp', namespaces=ns_map) or '2015-01-01T00:00:00Z'

        if extract_redirect_target(wikitext):
            skipped_redirects.append(title)
            continue

        if not wikitext.strip():
            skipped_empty.append(title)
            continue

        slug = title_to_slug(title)
        cats = extract_categories(wikitext)
        if not cats and title in MANUAL_CATS:
            cats = [MANUAL_CATS[title]]

        # Build redirect_from: own MediaWiki paths + paths of any redirect pages
        # that point here. Deduplicate and sort for deterministic output.
        redir_paths: list[str] = list(title_to_mw_paths(title))
        for src_title in reverse_redirect.get(title, []):
            redir_paths.extend(title_to_mw_paths(src_title))
        redir_paths = sorted(set(redir_paths))

        try:
            body = mw_to_md(wikitext, title, all_titles, redirect_map, canonical_titles)
        except Exception as e:
            issues.append(f"[{title}] Conversion error: {e}")
            body = f"<!-- conversion error: {e} -->\n\n" + wikitext

        write_page(slug, title, body, cats, timestamp, redir_paths)
        pages_info.append((title, slug, cats))
        converted += 1

    print("Writing index page...")
    write_index(pages_info)

    # Report
    print(f"\n{'='*60}")
    print(f"Converted:            {converted} pages")
    print(f"Skipped (redirects):  {len(skipped_redirects)}")
    print(f"Skipped (empty):      {len(skipped_empty)}")

    print(f"\nRedirects resolved (links rewritten to canonical page):")
    for src, dst in sorted(redirect_map.items()):
        print(f"  [[{src}]] → [[{dst}]]")

    if issues:
        print(f"\n⚠ Formatting issues ({len(issues)}):")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\nNo formatting issues.")

    print(f"\nDone. To preview:")
    print("  bundle install && bundle exec jekyll serve")


if __name__ == '__main__':
    main()
