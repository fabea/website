import re
import html
import datetime
from pybtex.database.input import bibtex

from site_config import SITE


# --------------------------------------------------------------------------
# 个人信息与页面文案（数据来自 site_config.py）
# --------------------------------------------------------------------------


def get_name():
    return SITE["name"]


def get_bio_text():
    return SITE["bio_text"]


def get_social_media_html():
    email = SITE["email"]
    scholar = SITE["scholar"]
    cv_en = SITE["cv_en"]
    cv_cn = SITE["cv_cn"]
    return f"""
                <div class="hero-links">
                <details class="about-details">
                <summary class="link-pill"><i class="fa-solid fa-graduation-cap"></i>About</summary>
                <div class="about-body">{SITE["bio"]}</div>
                </details>
                <div class="cv-menu">
                <button type="button" class="link-pill cv-trigger" aria-haspopup="true" aria-expanded="false" aria-controls="cv-panel"><i class="fa-solid fa-address-card"></i>CV <span class="cv-chev">▾</span></button>
                <div class="cv-menu-panel" id="cv-panel">
                <a class="cv-menu-item" href="{cv_en}" target="_blank">English CV</a>
                <a class="cv-menu-item" href="{cv_cn}" target="_blank">中文简历</a>
                </div>
                </div>
                <a class="link-pill" href="mailto:{email}"><i class="fa-solid fa-envelope-open"></i>Mail</a>
                <a class="link-pill" href="https://scholar.google.com/citations?user={scholar}&hl=en" target="_blank"><i class="fa-brands fa-google-scholar"></i>Scholar</a>
                </div>
    """


def get_interests_html():
    s = '<div class="interests">'
    for item in SITE["interests"]:
        s += f'<span class="interest-chip">{html.escape(item)}</span>'
    s += "</div>"
    return s


def get_contact_html():
    email = SITE["email"]
    items = [
        ("fa-solid fa-envelope", "Email", f"mailto:{email}", False),
        ("fa-brands fa-orcid", "ORCID", f"https://orcid.org/{SITE['orcid']}", True),
        (
            "fa-brands fa-google-scholar",
            "Scholar",
            f"https://scholar.google.com/citations?user={SITE['scholar']}&hl=en",
            True,
        ),
        ("fa-brands fa-github", "GitHub", f"https://github.com/{SITE['github']}", True),
    ]
    s = '<div class="contact-grid">'
    for icon, label, href, external in items:
        target = ' target="_blank" rel="me noopener"' if external else ""
        s += (
            f'<a class="contact-item" href="{html.escape(href, quote=True)}"{target}>'
            f'<i class="{icon}"></i><span>{label}</span></a>'
        )
    s += "</div>"
    return s


def get_footer_html():
    today = datetime.date.today()
    year = today.year
    updated = today.strftime("%Y-%m-%d")
    return f"""
                <p>© {year} {SITE['short_name']} · Last updated {updated}</p>
                <p>
                This website follows the design of <a href="https://m-niemeyer.github.io/" target="_blank">Michael Niemeyer</a> and <a href="https://jonbarron.info/" target="_blank">Jon Barron</a>.
                </p>
    """


# --------------------------------------------------------------------------
# 作者与期刊格式化
# --------------------------------------------------------------------------


def get_author_dict():
    return {
        "Shuxian Zhang": "https://www.xyafu.edu.cn/wgyxy/info/1127/7073.htm",
        "Mansour Amini": "https://ppblt.usm.my/index.php/lecturer-profile/393-mansour-amini-dr",
        "Hualing Gong": "https://s.wanfangdata.com.cn/paper?q=%E4%BD%9C%E8%80%85%3A%22%E9%BE%9A%E5%8D%8E%E7%8E%B2%22%20%E4%BD%9C%E8%80%85%E5%8D%95%E4%BD%8D%3A%20%22%E4%BF%A1%E9%98%B3%E5%86%9C%E6%9E%97%E5%AD%A6%E9%99%A2%22",
        "Qiongqiong Fan": "https://www.xyafu.edu.cn/wgyxy/info/1127/7062.htm",
        "Junyue Wang": "https://www.xyafu.edu.cn/wgyxy/info/1127/7079.htm",
        "Shaidatul Kasuma": "https://ppblt.usm.my/index.php/lecturer-profile/188-shaidatul-akma-adi-kasuma",
        "Chenjin Jia": "https://scholar.google.com/citations?hl=en&user=Nk-Ar0IAAAAJ",
        "Feng Tian": "https://orcid.org/0009-0006-1905-3921",
        "Yu Gao": "https://www.xyafu.edu.cn/wgyxy/info/1126/7057.htm",
    }


def generate_person_html(
    persons,
    connection=", ",
    make_bold=True,
    make_bold_name=None,
    add_links=True,
    equal_contribution=None,
):
    if make_bold_name is None:
        make_bold_name = SITE["short_name"]
    links = get_author_dict() if add_links else {}
    s = ""
    last = len(persons) - 1
    for idx, p in enumerate(persons):
        plain = " ".join(p.get_part("first") + p.get_part("last"))
        piece = html.escape(plain)
        if plain in links:
            piece = f'<a href="{html.escape(links[plain], quote=True)}" target="_blank">{piece}</a>'
        if make_bold and plain == make_bold_name:
            piece = f'<span class="self-name">{html.escape(make_bold_name)}</span>'
        if equal_contribution is not None and idx < equal_contribution:
            piece += "*"
        s += piece
        if idx != last:
            s += connection
    return s


_ACCEPTED_LIKE = {"accepted", "in press", "online first", "ahead-of-print"}


def format_venue(entry):
    fields = entry.fields
    venue = fields.get("booktitle", "")
    year = fields.get("year", "").strip()
    vol = fields.get("volume", "").strip()
    num = fields.get("number", "").strip()
    pages = fields.get("pages", "").strip()

    parts = [venue]
    if vol:
        if vol.lower() in _ACCEPTED_LIKE:
            parts.append(vol)
        elif vol != year:
            detail = vol
            if num and num.lower() not in _ACCEPTED_LIKE and num.lower() != "n/a":
                detail += f"({num})"
            if re.fullmatch(r"\d+(?:\s*[-–—]\s*\d+)?|e\d+", pages):
                detail += f": {pages.replace('--', '–')}"
            parts.append(detail)
    if year and not re.search(rf"{re.escape(year)}[\)]?$", venue):
        parts.append(year)
    return ", ".join(parts)


def build_cite(entry, entry_key):
    authors = generate_person_html(
        entry.persons["author"], make_bold=False, add_links=False, connection=" and "
    )
    cite = f"@{entry.type}{{{entry_key}, \n"
    cite += f"\tauthor = {{{authors}}}, \n"
    for entr in ["title", "booktitle", "year"]:
        cite += f"\t{entr} = {{{entry.fields[entr]}}}, \n"
    cite += "}"
    return html.escape(cite)


# --------------------------------------------------------------------------
# 论文 / 会议卡片
# --------------------------------------------------------------------------

_PAPER_ARTEFACTS = {
    "html": "Web view",
    "pdf": "Postprint archive",
    "supp": "Supplementary",
    "video": "Video",
    "poster": "Poster",
    "code": "Code",
}

_TALK_ARTEFACTS = {
    "slides": "Slides",
    "video": "Recording",
}


def _artefact_links(fields, artefacts):
    """渲染条目附带资源链接；缺失的可选字段静默跳过。"""
    s = ""
    first = True
    for key, label in artefacts.items():
        if key in fields:
            if not first:
                s += '<span class="sep">·</span>'
            s += (
                f'<a class="pub-link" href="{html.escape(fields[key], quote=True)}" '
                f'target="_blank">{label}</a>'
            )
            first = False
    return s


def get_paper_entry(entry_key, entry):
    fields = entry.fields
    featured = " featured" if "highlight" in fields else ""
    badge = '<span class="featured-badge">Featured</span>' if "highlight" in fields else ""
    title = html.escape(fields["title"])
    href = html.escape(fields["html"], quote=True)
    img = html.escape(fields["img"], quote=True)

    s = f'<article class="pub-card{featured}">{badge}'
    s += (
        f'<div class="pub-thumb"><img src="{img}" alt="{title}" loading="lazy"></div>'
    )
    s += '<div class="pub-body">'

    award = ""
    if "award" in fields:
        award = f'<span class="pub-award">({html.escape(fields["award"])})</span>'
    s += f'<h3 class="pub-title"><a href="{href}" target="_blank">{title}</a>{award}</h3>'

    if "equal_contribution" in fields:
        authors = generate_person_html(
            entry.persons["author"], equal_contribution=int(fields["equal_contribution"])
        )
    else:
        authors = generate_person_html(entry.persons["author"])
    s += f'<p class="pub-authors">{authors}</p>'

    s += f'<p class="pub-meta">{html.escape(format_venue(entry))}</p>'
    s += '<div class="pub-links">'
    s += _artefact_links(fields, _PAPER_ARTEFACTS)
    s += (
        '<details class="bib"><summary>Bibtex</summary>'
        "<pre><code>" + build_cite(entry, entry_key) + "</code></pre></details>"
    )
    s += "</div></div></article>"
    return s


def get_talk_entry(entry_key, entry):
    fields = entry.fields
    title = html.escape(fields["title"])
    img = html.escape(fields["img"], quote=True)
    s = '<article class="pub-card">'
    s += (
        f'<div class="pub-thumb"><img src="{img}" alt="{title}" loading="lazy"></div>'
    )
    s += '<div class="pub-body">'
    s += f'<h3 class="pub-title">{title}</h3>'
    s += f'<p class="pub-meta">{html.escape(format_venue(entry))}</p>'
    s += '<div class="pub-links">'
    s += _artefact_links(fields, _TALK_ARTEFACTS)
    s += "</div></div></article>"
    return s


def _group_by_year(entries):
    groups = {}
    for key, entry in entries.items():
        year = entry.fields.get("year", "").strip() or "n.d."
        groups.setdefault(year, []).append(key)
    return groups


def get_publications_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file("publication_list.bib")
    entries = bib_data.entries
    groups = _group_by_year(entries)
    s = ""
    for year in sorted(groups, key=lambda y: y if y.isdigit() else "0", reverse=True):
        count = len(groups[year])
        s += f'<h3 class="year-label">{year}<span class="year-count">&nbsp;·&nbsp;{count}</span></h3>'
        for key in groups[year]:
            s += get_paper_entry(key, entries[key])
    return s


def get_talks_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file("talk_list.bib")
    entries = bib_data.entries
    groups = _group_by_year(entries)
    s = ""
    for year in sorted(groups, key=lambda y: y if y.isdigit() else "0", reverse=True):
        s += f'<h3 class="year-label">{year}</h3>'
        for key in groups[year]:
            s += get_talk_entry(key, entries[key])
    return s


# --------------------------------------------------------------------------
# 页面模板
# --------------------------------------------------------------------------


def get_index_html():
    pub = get_publications_html()
    talks = get_talks_html()
    name = get_name()
    bio_text = get_bio_text()
    social_media = get_social_media_html()
    interests = get_interests_html()
    contact = get_contact_html()
    footer = get_footer_html()
    short_name = SITE["short_name"]
    tagline = SITE["tagline"]
    title_suffix = SITE["title"]

    s = f"""<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{name[0]}{name[1]} | {title_suffix}</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico">
  <script>
    (function(){{try{{var t = localStorage.getItem("theme");if (t !== "light" && t !== "dark"){{t = (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";}}document.documentElement.setAttribute("data-theme", t);}}catch(e){{document.documentElement.setAttribute("data-theme", "light");}}}})();
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,500;0,600;1,400&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Merriweather:wght@400;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
    integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer">
  <link rel="stylesheet" type="text/css" href="assets/stylesheet.css">
</head>

<body>
  <nav class="site-nav">
    <div class="container nav-inner">
      <a class="nav-brand" href="#top">{short_name}</a>
      <div class="nav-links">
        <a href="#interests">Interests</a>
        <a href="#publications">Publications</a>
        <a href="#talks">Conferences</a>
        <a href="#contact">Contact</a>
        <button id="theme-toggle" class="theme-toggle" type="button" aria-label="Toggle color theme">
          <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
          <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
      </div>
    </div>
  </nav>

  <main id="top">
    <div class="container">
      <header class="hero">
        <div class="hero-grid">
          <div class="hero-text">
            <h1 class="hero-name">{name[0]}<span class="hero-suffix">{name[1]}</span></h1>
            <p class="hero-tagline">{tagline}</p>
            <div class="hero-bio">{bio_text}</div>
            {social_media}
          </div>
          <div class="hero-photo">
            <img src="assets/img/profile.jpg" alt="Da Yan's profile photo">
          </div>
        </div>
      </header>

      <section id="interests" class="section">
        <h2 class="section-heading">Research Interests</h2>
        {interests}
      </section>

      <section id="publications" class="section">
        <h2 class="section-heading">Publications</h2>
        {pub}
      </section>

      <section id="talks" class="section">
        <h2 class="section-heading">Conferences</h2>
        {talks}
      </section>

      <section id="contact" class="section">
        <h2 class="section-heading">Contact</h2>
        {contact}
      </section>

      <footer class="site-footer">
        {footer}
      </footer>
    </div>
  </main>

  <script src="assets/theme.js"></script>
  <script src="assets/thumbs.js"></script>
  <script src="assets/cvmenu.js"></script>
  <script src="assets/nav.js"></script>
</body>

</html>
    """
    return s


def write_index_html(filename="index.html"):
    s = get_index_html()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(s)
    print(f"Written index content to {filename}.")


if __name__ == "__main__":
    write_index_html("index.html")
