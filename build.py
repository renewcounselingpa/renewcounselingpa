#!/usr/bin/env python3
"""Builds the website's pages from content.txt and the files in templates/.

    python3 build.py

Reads:   content.txt      all the words on the site (the file people edit)
         templates/       the page layouts, with {{placeholders}} for the words
Writes:  index.html, about.html, ... sitemap.xml, robots.txt   (don't edit these by hand)

GitHub runs this automatically whenever content.txt changes (see
.github/workflows/build.yml), so people editing content.txt never need to run it.
Uses only the Python standard library.
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import quote_plus

ROOT = Path(__file__).parent
TEMPLATES = ROOT / "templates"

# output file -> template, the prefix of its title/description keys in content.txt, and
# the photo to preload at the top of the page ("" for none).
PAGES = {
    "index.html": ("index.html", "home", "images/hero-forest.jpg"),
    "therapies.html": ("therapies.html", "therapies", "images/banner-ferns.jpg"),
    "about.html": ("about.html", "about", "images/banner-canopy.jpg"),
    "fees.html": ("fees.html", "fees", "images/banner-canopy.jpg"),
    "contact.html": ("contact.html", "contact", "images/banner-path.jpg"),
    "privacy.html": ("privacy.html", "privacy", "images/banner-path.jpg"),
    "404.html": ("404.html", "notfound", ""),
}
# Pages listed in sitemap.xml (everything except the 404 page)
SITEMAP_PAGES = [p for p in PAGES if p != "404.html"]

GENERATED_NOTE = "<!-- This file is generated from content.txt and templates/. Don't edit it directly; edit content.txt, then run build.py. -->"


class BuildError(Exception):
    pass


# ---------------------------------------------------------------- content.txt

KEY_LINE = re.compile(r"^([a-z0-9_]+):(.*)$")


def parse_content(path):
    """Returns {key: "text"} or {key: ["item", ...]} from content.txt."""
    data = {}
    current_list = None  # name of the list we're adding "- " items to
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            if current_list is None:
                raise BuildError(f"content.txt line {number}: this list item has no list name above it:\n    {line}")
            data[current_list].append(stripped[2:].strip())
            continue
        match = KEY_LINE.match(stripped)
        if not match:
            raise BuildError(
                f"content.txt line {number} isn't in the form  name: text\n    {line}\n"
                "(Each line needs a name, a colon, then the text. Lines starting with # are notes.)"
            )
        key, value = match.group(1), match.group(2).strip()
        if key in data:
            raise BuildError(f"content.txt line {number}: '{key}' appears twice. Each name can only be used once.")
        if value:
            data[key] = value
            current_list = None
        else:
            data[key] = []  # a list follows (or an empty text if nothing does)
            current_list = key
    # A name with nothing after it and no list items is just empty text.
    for key, value in list(data.items()):
        if value == []:
            data[key] = ""
    return data


# ------------------------------------------------------------ text rendering

LINK_TOKENS = ("phone", "email")  # {phone} and {email} become clickable links


def esc(text, quotes=False):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text.replace('"', "&quot;") if quotes else text


def expand(text, ctx, trail=()):
    """Fills {name} with that setting's text. {phone}/{email} are kept as markers for render_inline."""

    def swap(match):
        name = match.group(1)
        if name in LINK_TOKENS:
            return match.group(0)
        if name in trail:
            raise BuildError(f"content.txt: {{{name}}} refers to itself.")
        value = ctx.get(name)
        if not isinstance(value, str):
            raise BuildError(f"content.txt: {{{name}}} is used in some text, but there's no text setting called '{name}'.")
        return expand(value, ctx, trail + (name,))

    return re.sub(r"\{([a-z0-9_]+)\}", swap, text)


def render_inline(text, ctx):
    """Turns a piece of content.txt text into HTML (bold, italic, links, {phone}, [[to-do]])."""
    html = esc(expand(text, ctx))
    html = re.sub(r"\[\[(.+?)\]\]", r'<span class="tbd">[\1]</span>', html)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"(?<![\*\w])\*(?!\*)(.+?)(?<!\*)\*(?![\*\w])", r"<em>\1</em>", html)

    def link(match):
        label, url = match.group(1), match.group(2)
        extra = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
        return f'<a href="{url}"{extra}>{label}</a>'

    html = re.sub(r"\[([^\[\]]+)\]\(([^()\s]+)\)", link, html)
    html = html.replace("{phone}", f'<a href="tel:{ctx["phone_tel"]}">{esc(ctx["phone"])}</a>')
    html = html.replace("{email}", f'<a href="mailto:{esc(ctx["email"], True)}">{esc(ctx["email"])}</a>')
    return html


def render_plain(text, ctx):
    """Text with no formatting at all, for page titles and meta tags."""
    text = expand(text, ctx).replace("{phone}", ctx["phone"]).replace("{email}", ctx["email"])
    text = re.sub(r"\[\[(.+?)\]\]", r"[\1]", text)
    text = re.sub(r"\[([^\[\]]+)\]\([^()\s]+\)", r"\1", text)
    text = text.replace("**", "")
    text = re.sub(r"(?<![\*\w])\*(?!\*)(.+?)(?<!\*)\*(?![\*\w])", r"\1", text)
    return text


# -------------------------------------------------------------- templates

def read_template(name):
    path = TEMPLATES / name
    if not path.exists():
        raise BuildError(f"templates/{name} is missing.")
    return path.read_text(encoding="utf-8")


def truthy(value):
    return isinstance(value, str) and value.strip().lower() not in ("", "no", "false", "off")


def need(ctx, key, where):
    if key not in ctx:
        raise BuildError(f"templates/{where} uses '{key}', but content.txt has no line called '{key}:'.")
    return ctx[key]


def render(template_name, ctx):
    text = read_template(template_name)

    # {{> other.html}}  includes another template
    text = re.sub(r"\{\{>\s*(@page|[\w.\-]+)\s*\}\}",
        lambda m: render(ctx["page_template"] if m.group(1) == "@page" else m.group(1), ctx), text)

    # {{#if key}}...{{/if}} and {{#unless key}}...{{/unless}}
    def conditional(kind):
        def run(match):
            value = truthy(need(ctx, match.group(1), template_name))
            return match.group(2) if value == (kind == "if") else ""

        return run

    text = re.sub(r"\{\{#if\s+(\w+)\s*\}\}(.*?)\{\{/if\}\}", conditional("if"), text, flags=re.S)
    text = re.sub(r"\{\{#unless\s+(\w+)\s*\}\}(.*?)\{\{/unless\}\}", conditional("unless"), text, flags=re.S)

    # {{#each list}}...{{this}} / {{this.1}} {{this.2}}...{{/each}}
    def loop(match):
        items = need(ctx, match.group(1), template_name)
        if not isinstance(items, list):
            raise BuildError(f"templates/{template_name}: '{match.group(1)}' should be a list ('- item' lines) in content.txt.")
        body, out = match.group(2), []
        for item in items:
            parts = [p.strip() for p in item.split("|")]

            def field(m):
                index = m.group(1)
                if index is None:
                    return render_inline(item, ctx)
                i = int(index)
                if i > len(parts):
                    raise BuildError(f"content.txt: the item '{item}' in '{match.group(1)}' needs a | separating its parts.")
                return render_inline(parts[i - 1], ctx)

            out.append(re.sub(r"\{\{this(?:\.(\d))?\}\}", field, body))
        return "".join(out)

    text = re.sub(r"\{\{#each\s+(\w+)\s*\}\}(.*?)\{\{/each\}\}", loop, text, flags=re.S)

    # {{plain key}}, {{json key}}, {{json_list key}}, {{current page.html}}, {{key}}
    def variable(match):
        expr = match.group(1).strip()
        if expr.startswith("current "):
            return ' aria-current="page"' if expr.split(None, 1)[1] == ctx["page_file"] else ""
        if " " in expr:
            mode, key = expr.split(None, 1)
        else:
            mode, key = "inline", expr
        value = need(ctx, key, template_name)
        if mode == "json_list":
            return json.dumps([render_plain(v, ctx) for v in value], ensure_ascii=False)
        if isinstance(value, list):
            raise BuildError(f"templates/{template_name}: '{key}' is a list, so it needs {{{{#each {key}}}}}.")
        if mode == "inline":
            return render_inline(value, ctx)
        if mode == "plain":
            return esc(render_plain(value, ctx), True)
        if mode == "json":
            return json.dumps(render_plain(value, ctx), ensure_ascii=False)
        raise BuildError(f"templates/{template_name}: unknown {{{{{expr}}}}}.")

    return re.sub(r"\{\{([^{}]+)\}\}", variable, text)


# ------------------------------------------------------------------- build

def main():
    try:
        content = parse_content(ROOT / "content.txt")
        text_ctx = dict(content)
        digits = re.sub(r"\D", "", text_ctx.get("phone", ""))
        if len(digits) != 10:
            raise BuildError("content.txt: 'phone' should be a 10-digit phone number, like (570) 734-7798.")
        text_ctx["phone_tel"] = "+1" + digits
        text_ctx["address_line2"] = f'{text_ctx["address_city"]}, {text_ctx["address_state"]} {text_ctx["address_zip"]}'
        text_ctx["map_query"] = quote_plus(f'{text_ctx["address_street"]}, {text_ctx["address_line2"]}')
        text_ctx["site_url"] = text_ctx["site_url"].rstrip("/")

        for out_name, (template, prefix, preload) in PAGES.items():
            ctx = dict(text_ctx)
            ctx.update(
                page_file=out_name,
                page_path="" if out_name == "index.html" else out_name,
                page_title=need(ctx, prefix + "_title", "(page title)"),
                page_description=need(ctx, prefix + "_description", "(page description)"),
                preload_image=preload,
                is_home="yes" if out_name == "index.html" else "",
                is_404="yes" if out_name == "404.html" else "",
            )
            ctx["page_template"] = template
            html = render("_layout.html", ctx)
            html = html.replace("<!doctype html>", "<!doctype html>\n" + GENERATED_NOTE, 1)
            (ROOT / out_name).write_text(html, encoding="utf-8")

        urls = "".join(
            f'  <url><loc>{esc(text_ctx["site_url"])}/{"" if p == "index.html" else p}</loc></url>\n' for p in SITEMAP_PAGES
        )
        (ROOT / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n",
            encoding="utf-8",
        )
        (ROOT / "robots.txt").write_text(
            f'User-agent: *\nAllow: /\n\nSitemap: {text_ctx["site_url"]}/sitemap.xml\n', encoding="utf-8"
        )
    except (BuildError, KeyError) as error:
        print(f"\nCouldn't build the site:\n\n  {error}\n", file=sys.stderr)
        sys.exit(1)
    print(f"Built {len(PAGES)} pages from content.txt.")


if __name__ == "__main__":
    main()
