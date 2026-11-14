# Renew Counseling website

The website for **Renew Counseling**, the private counseling practice of Elisa D. Yost, MS, LPC, in Milford, PA. The business is registered as Elisa D Yost LLC.

- **Live site:** <https://www.renewcounselingpa.com/>
- **Hosting:** GitHub Pages, served from the `main` branch. DNS and email are managed in Cloudflare.

It's a plain static site: HTML pages, one stylesheet and one small JavaScript file. **All the words on the site live in one file, `content.txt`.** A small script (`build.py`, Python standard library only) combines it with the page layouts in `templates/` to produce the `.html` files. There's no framework or package manager.

> **Non-technical editors:** see [EDITING.md](EDITING.md). Changing text only needs a web browser. GitHub rebuilds the pages automatically when `content.txt` is saved.

## Contents

1. [Quick start](#quick-start)
2. [Project structure](#project-structure)
3. [Content, templates and the build](#content-templates-and-the-build)
4. [Common edits](#common-edits)
5. [Photos and images](#photos-and-images)
6. [Styling](#styling)
7. [JavaScript](#javascript)
8. [Contact form (Formspree)](#contact-form-formspree)
9. [SEO and link previews](#seo-and-link-previews)
10. [Accessibility](#accessibility)
11. [Privacy and compliance](#privacy-and-compliance)
12. [Hosting, domain and email](#hosting-domain-and-email)
13. [Testing checklist](#testing-checklist)
14. [Possible future improvements](#possible-future-improvements)
15. [Sources for site content](#sources-for-site-content)

---

## Quick start

```bash
git clone https://github.com/gansel51/renewcounselingpa.git
cd renewcounselingpa
python3 build.py           # regenerates the .html pages from content.txt + templates/
open index.html            # macOS; or double-click the file
```

Most things work when a page is opened straight from disk. To preview it as it runs online (for example, to test the form), run a local server:

```bash
python3 -m http.server 8000    # then visit http://localhost:8000
```

To publish a change, commit and push to `main`. The live site updates within a minute or two. If GitHub rebuilt the pages in the meantime, run `git pull --rebase` before pushing.

---

## Project structure

```
.
├── content.txt         ALL the website's text (edit this for wording changes)
├── build.py            Builds the pages below from content.txt + templates/
├── templates/          Page layouts with {{placeholders}} (_layout.html is the header/footer)
├── .github/workflows/  Runs build.py automatically when content.txt changes
├── EDITING.md          Plain-language guide for editing content.txt on github.com
├── index.html          Home                (generated; don't edit by hand)
├── therapies.html      Focused Therapies   (generated)
├── about.html          About Me            (generated)
├── fees.html           Fees & Insurance    (generated)
├── contact.html        Contact, hours, map, contact form (generated)
├── privacy.html        Website privacy policy and Notice of Privacy Practices (generated)
├── 404.html            "Page not found" (generated)
├── docs/               Downloadable documents (Notice of Privacy Practices PDF)
├── css/styles.css      All styling
├── js/main.js          Mobile menu, mobile call bar, footer year, contact form
├── images/             Photos, logo, icons, link-preview image
├── fonts/              Site fonts (.woff2) and their licenses
├── sitemap.xml         Page list for search engines (generated)
├── robots.txt          Crawling rules (generated)
├── CNAME               Custom domain for GitHub Pages
├── .nojekyll           Tells GitHub Pages to serve files as-is
└── README.md           This file
```

---

## Content, templates and the build

**The `.html` files in the project root, `sitemap.xml` and `robots.txt` are generated.** Don't edit them directly; the next build overwrites them.

- **Words** → edit `content.txt` (its header explains the format and special marks).
- **Layout/markup** → edit the files in `templates/`. `_layout.html` holds the parts shared by every page (`<head>`, header, navigation, crisis bar, footer, mobile Call/Message bar). `_jsonld.html` is the home page's structured data. Each page has its own template containing the contents of `<main>`.
- Run `python3 build.py`, then commit both the sources and the regenerated pages.

**Automatic builds:** `.github/workflows/build.yml` runs `build.py` whenever `content.txt`, `templates/` or `build.py` change on `main`, and commits the regenerated pages. If a line in `content.txt` is malformed, the build fails with a plain-language message in the repository's **Actions** tab, and the live site stays unchanged.

**Template syntax** (details in `build.py`):

| Syntax | Meaning |
|---|---|
| `{{key}}` | The text for `key:` in `content.txt`, with bold/italic/links applied |
| `{{plain key}}` | Same, as plain text safe for attributes (titles, alt text, meta tags) |
| `{{json key}}`, `{{json_list key}}` | As JSON, for the structured data |
| `{{#each list}}…{{this}}…{{/each}}` | Repeat for each `- item` of a list. Use `{{this.1}}` / `{{this.2}}` for `Part one \| Part two` items |
| `{{#if key}}…{{/if}}`, `{{#unless key}}…{{/unless}}` | Show only when the setting is on (anything but empty/`no`/`false`/`off`) |
| `{{> file.html}}` | Include another template |
| `{{current page.html}}` | ` aria-current="page"` when building that page (navigation) |

In `content.txt` text, `{key}` inserts another setting (e.g. `{years}`), and `{phone}` / `{email}` become links. `phone_tel`, `address_line2` and `map_query` are computed by the build.

**Adding a page:** create `templates/newpage.html`, add `newpage_title:`, `newpage_description:` and its text to `content.txt`, add an entry to `PAGES` in `build.py`, and link it from the navigation in `templates/_layout.html`. `sitemap.xml` is generated from `PAGES`.

---

## Common edits

Each fact is stored once in `content.txt` and filled in wherever it appears.

| Detail | Setting |
|---|---|
| Phone, email | `phone`, `email` |
| Address (also drives the map and directions) | `address_street`, `address_city`, `address_state`, `address_zip` |
| PA / NJ license | `pa_license`, `nj_license` |
| Fees | `fee_individual`, `fee_couples` |
| Years in practice | `years`. **Update it each year**, along with Psychology Today. |
| Domain (canonical links, link previews, sitemap, robots) | `site_url` |
| Contact form ID | `formspree_id` |
| "Accepting new clients" on/off | `accepting_clients` (`yes`/`no`) |
| Accepted insurance | `insurance_accepted` (list), plus `trust_items` and `fee_strip_insurance` on the home page |
| Notice of Privacy Practices PDF | replace `docs/notice-of-privacy-practices.pdf` (same filename) |

**The main call-to-action button** (`cta_button`) is a phone link: the free 15-minute consultation is a phone call. Keep that wording consistent wherever the consultation is mentioned.

**Writing style:** the site speaks in Elisa's voice, in the first person. Bio wording, methods and payment options follow her [Psychology Today profile](https://www.psychologytoday.com/us/therapists/elisa-d-yost-milford-pa/1815786), so keep the two in sync. Don't list services, methods, insurers or credentials she hasn't confirmed.

**Placeholders:** text that still needs content is written with double square brackets, like `[[date]]`, and shows with a yellow highlight (the `.tbd` style). Search `content.txt` for `[[` to find them. None are left at the moment.

---

## Photos and images

To swap a photo, replace the file in `images/` **using the same filename**.

| File | Where it's used | Shape / size |
|---|---|---|
| `hero-forest.jpg` | Home, top banner (set in CSS) | Wide, 1920×1100 |
| `elisa-yost.jpg` | Home intro, About page, Contact form (small circle) | Portrait 4:5 |
| `headshot-3.jpg` | About, "My approach" | 4:3, 1200×900 |
| `office-plants.jpg` | Home, "Three simple steps" | 4:3, 1200×900 |
| `therapy-1.jpg` … `therapy-4.jpg` | Therapies page | Square, 800×800 |
| `banner-ferns.jpg`, `banner-canopy.jpg`, `banner-path.jpg` | Page banners | Wide, 1920×700 |
| `cta-leaves.jpg` | "Get in touch" bands (set in CSS) | Wide, 1920×900 |
| `logo.svg` | Header, footer, 404 page, browser tab | Vector |
| `favicon-32.png`, `favicon-48.png`, `apple-touch-icon.png`, `icon-512.png` | Browser tab and home-screen icons | Made from `logo.svg` |
| `og-image.jpg` | Preview image when a link is shared | 1200×630 |

- Resize photos to about 2000px wide or less and save as JPEG at 75–80% quality.
- Banners and CTA bands have text over them, so choose calm photos and check readability.
- When a photo changes, update its alt text in `content.txt` (the `…_alt` lines). CSS background images are decorative and have no `alt`.
- When the logo changes, recreate the four icon PNGs and `og-image.jpg` from it.
- Current nature and room photos are CC0 from Unsplash (via Wikimedia Commons), so no credit is required. Avoid stock photos of people, so visitors aren't misled about who they'll see.

---

## Styling

All styling is in `css/styles.css`.

**Colors** are defined once at the top of the file:

| Variable | Color | Used for |
|---|---|---|
| `--fig-leaf` | `#2f4a3a` deep green | Headings, header, footer |
| `--moss` | `#4f6b55` mid green | Accents, CTA band background |
| `--sage` / `--sage-light` | soft greens | Accents, tinted section backgrounds |
| `--cream` | `#f6f3ec` | Page background |
| `--paper` | `#fffdf8` | Cards |
| `--plum` | `#6b3e5a` | Buttons and links |
| `--ink` / `--ink-soft` | dark grey-greens | Body text |

**Fonts:** *Cormorant Garamond* (headings) and *Nunito Sans* (body), self-hosted in `fonts/` via `@font-face` (SIL Open Font License; licenses are in `fonts/`). Visitors' browsers make no requests to Google for them. To change fonts, add the `.woff2` files, update the `@font-face` rules and the `--font-serif` / `--font-sans` variables, and update the `<link rel="preload">` lines in `templates/_layout.html`.

**Layout:** `--max` (1120px) sets the content width. Card grids use `.card-grid` or `.card-grid.four` (four columns, dropping to two, then one).

Later rules in the file override earlier ones, so if a change doesn't take effect, search for the class name and check further down. The site uses a light color scheme only, by design.

---

## JavaScript

`js/main.js` is loaded on every page and does four things:

1. **Mobile menu:** opens and closes the navigation on small screens (also closes on a link tap, an outside tap, or <kbd>Esc</kbd>).
2. **Mobile Call/Message bar:** hides the sticky bar on phones while the page's own call buttons or the form are on screen, and while someone is typing.
3. **Footer year:** fills in the current year wherever there's a `data-year` attribute.
4. **Contact form:** validates fields, shows friendly errors, and sends the message to Formspree without leaving the page.

The site still works without JavaScript: the `no-js` class on `<html>` shows the navigation as a simple list, and the form falls back to the browser's own checks.

---

## Contact form (Formspree)

The form on `contact.html` sends messages through [Formspree](https://formspree.io), because a static site can't send email by itself. The form ID is the `formspree_id` setting in `content.txt`.

- **Sent:** first name, last name, email, phone (optional) and message. The subject is set by the hidden `_subject` field. A hidden `_gotcha` field catches spam bots.
- **To change where messages go,** change the recipient in the Formspree dashboard (Form → Settings). No code change is needed.
- **To replace the form,** create a new one at formspree.io, copy the part after `/f/` in its address, and paste it into `formspree_id`.
- **Limits:** the free plan allows 50 messages a month and includes spam filtering.
- **Formspree is not HIPAA-compliant.** That's why the form tells people not to include private health details. If clients should share clinical information online, use a HIPAA-compliant client portal instead.
- If `formspree_id` is ever missing or invalid, the form offers email buttons (Email app, Gmail, Outlook, Copy message) as a fallback.

The Google Map on `contact.html` is a plain embed using a search link, so it needs no API key. To use Google's official embed instead, choose **Share → Embed a map → Copy HTML** on Google Maps and paste only the `src="…"` URL into the `<iframe>`.

---

## SEO and link previews

- **Titles and descriptions:** each page has its own `<title>` and `<meta name="description">`.
- **Canonical links:** point to `https://www.renewcounselingpa.com/` (from `site_url`).
- **Link previews:** `og:` and `twitter:` tags use `images/og-image.jpg`.
- **Structured data:** the `application/ld+json` block on the home page describes the practice (name, address, phone, email, prices, areas served). Keep it in sync with the visible content.
- **`sitemap.xml` and `robots.txt`:** generated by the build. Submit the sitemap in [Google Search Console](https://search.google.com/search-console).

---

## Accessibility

When editing, please keep the site usable with a keyboard and a screen reader:

- Every content photo needs meaningful `alt` text. Decorative images use `alt=""`.
- Keep the heading order logical: one `<h1>` per page, then `<h2>`, `<h3>`.
- Form fields have visible labels, and error messages are linked to their fields.
- Keep the "Skip to content" link at the top of each page.
- Keep text over photos readable. The dark overlays on the hero, banners and CTA bands are there for contrast.
- The crisis notice (988 / 911) appears on every page. Don't remove it.

---

## Privacy and compliance

- The site uses **no analytics, tracking or advertising cookies.** Third-party services are limited to the Google Map embed and Formspree, and `privacy.html` lists them. If you add any other service (analytics, a booking widget, chat), update the privacy page.
- **Notice of Privacy Practices:** posted as a PDF at `docs/notice-of-privacy-practices.pdf` and linked from the privacy page and the footer.
- **Good Faith Estimate:** under the No Surprises Act, self-pay clients have the right to an estimate of costs. `fees.html` includes the required notice. Keep it.
- **License display:** the PA license number is in every page's footer, and both PA and NJ numbers are on the About page.
- The website privacy policy is a plain-language statement, **not legal advice.**
- Email through Gmail is not end-to-end encrypted and isn't covered by a HIPAA agreement unless the account is on a plan with a signed BAA (for example Google Workspace). Keep client communication by email brief.

---

## Hosting, domain and email

**Hosting:** **Settings → Pages** in the GitHub repository deploys from the `main` branch, `/ (root)` folder, with the custom domain `www.renewcounselingpa.com` (stored in the `CNAME` file; don't delete it). **Enforce HTTPS** is on. Check build progress in the **Actions** tab. Leave `.nojekyll` in place.

**DNS (Cloudflare):** the domain is registered and managed in Cloudflare.

| Type | Name | Content |
|---|---|---|
| CNAME | `www` | `gansel51.github.io` |
| A | `@` | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153` |

Site records are set to **DNS only** (grey cloud) so GitHub can manage the HTTPS certificate. If they are ever proxied (orange cloud), set Cloudflare SSL/TLS to **Full**, not Flexible. If the domain changes, update `site_url` (and `email`) in `content.txt`, and update the `CNAME`.

**Email:**
- **Receiving:** Cloudflare Email Routing forwards `elisa@renewcounselingpa.com` to a Gmail inbox. It handles receiving only; it has no SMTP server.
- **Sending:** Gmail's **Settings → Accounts and Import → Send mail as** uses `smtp.gmail.com`, port 587, TLS, with the Gmail address as the username and a Google **App Password** as the password. The confirmation code arrives through the forwarding.
- **DNS records:** one SPF TXT record on `@` that includes both senders (`v=spf1 include:_spf.mx.cloudflare.net include:_spf.google.com ~all`; a domain can have only one), and a DMARC TXT record at `_dmarc` (`v=DMARC1; p=none; rua=mailto:elisa@renewcounselingpa.com`).
- To test, send to a non-Gmail address and check in **Show original** that SPF and DMARC pass.

---

## Testing checklist

Run through this after significant changes:

- [ ] Every page loads, and every navigation, footer and button link goes to the right place.
- [ ] Phone links start a call on a phone; email links open an email addressed to a working address.
- [ ] Contact form: submitting it empty shows error messages; a real test message arrives in Elisa's inbox.
- [ ] Phone layout (about 375px wide): the menu opens and closes, the Call/Message bar appears and hides correctly, and nothing scrolls sideways.
- [ ] Photos load, and the text over banner photos is readable.
- [ ] No yellow placeholder highlights are left (search `content.txt` for `[[`).
- [ ] A nonexistent address (e.g. `/nope`) shows the 404 page.
- [ ] Sharing the home page link by text or social media shows the right title and preview image.
- [ ] The map shows the right location, and "Get directions" opens it.
- [ ] `renewcounselingpa.com` redirects to `https://www.renewcounselingpa.com/`.
- [ ] The Notice of Privacy Practices PDF opens from the privacy page.

---

## Possible future improvements

- A photo of Elisa in her office to replace the plants photo in `images/headshot-3.jpg` (update `about_approach_photo_alt` in `content.txt` to match).
- A larger portrait: `images/elisa-yost.jpg` is only 320×400, and a 1000×1250 original would look sharper.
- The final fig-tree logo in `images/logo.svg`, then recreate the icons and `og-image.jpg`.
- Keep outside listings consistent with the site: the Psychology Today profile (website link, payment methods, insurance, phone number) and the NPI registry record (<https://nppes.cms.hhs.gov>). Create or claim a Google Business Profile for the office.
- Submit `sitemap.xml` in Google Search Console.

---

## Sources for site content

- **Elisa's [Psychology Today profile](https://www.psychologytoday.com/us/therapists/elisa-d-yost-milford-pa/1815786):** the main source for her bio, specialties, methods, fees, insurance and payment methods.
- **[NPPES NPI Registry](https://npiregistry.cms.hhs.gov/):** her individual provider record (NPI 1891613063) lists both licenses; the practice (Elisa D Yost LLC, doing business as Renew Counseling) is NPI 1013822063.
- **[Pennsylvania PALS](https://www.pals.pa.gov/#/page/search):** license verification, linked from the About page.
- Office details (entrance, accessibility, waiting room) came from Elisa directly.
