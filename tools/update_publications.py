#!/usr/bin/env python3
"""Update website publication blocks from OpenAlex.

Google Scholar does not provide an official public API, so this script uses
OpenAlex with the author's ORCID as a stable machine-readable source.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import textwrap
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INDEX_MD = DOCS / "index.md"
PUBLICATIONS_MD = DOCS / "publications.md"

ORCID = "0000-0001-9318-8177"
OPENALEX_AUTHOR_ID = "A5008347336"
OPENALEX_MAILTO = os.environ.get("OPENALEX_MAILTO", "k.aslansefat@hull.ac.uk")
SCHOLAR_URL = "https://scholar.google.com/citations?user=YBa4Tl8AAAAJ&hl=en"
MAX_PUBLICATIONS = int(os.environ.get("MAX_PUBLICATIONS", "15"))
MAX_NEWS = int(os.environ.get("MAX_NEWS_PUBLICATIONS", "5"))

NEWS_START = "<!-- AUTO_PUBLICATIONS_NEWS_START -->"
NEWS_END = "<!-- AUTO_PUBLICATIONS_NEWS_END -->"
LIST_START = "<!-- AUTO_PUBLICATIONS_LIST_START -->"
LIST_END = "<!-- AUTO_PUBLICATIONS_LIST_END -->"


def fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": f"koo-ec.github.io publication updater (mailto:{OPENALEX_MAILTO})",
        },
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_openalex_works() -> list[dict[str, Any]]:
    params = {
        "filter": f"author.orcid:{ORCID}",
        "sort": "publication_date:desc",
        "per-page": "100",
        "mailto": OPENALEX_MAILTO,
        "select": ",".join(
            [
                "id",
                "doi",
                "display_name",
                "publication_date",
                "publication_year",
                "type",
                "authorships",
                "primary_location",
                "cited_by_count",
            ]
        ),
    }
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    data = fetch_json(url)
    return dedupe_works(data.get("results", []))


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", title.lower())


def work_score(work: dict[str, Any]) -> tuple[int, int, str]:
    source = get_source(work)
    work_type = work.get("type") or ""
    has_doi = 1 if work.get("doi") else 0
    has_source = 1 if source else 0
    not_preprint = 1 if work_type != "preprint" else 0
    return (not_preprint + has_doi + has_source, int(work.get("cited_by_count") or 0), work.get("publication_date") or "")


def dedupe_works(works: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_title: dict[str, dict[str, Any]] = {}
    for work in works:
        title = (work.get("display_name") or "").strip()
        if not title:
            continue
        key = normalize_title(title)
        existing = by_title.get(key)
        if existing is None or work_score(work) > work_score(existing):
            by_title[key] = work
    return sorted(by_title.values(), key=lambda item: item.get("publication_date") or "0000-00-00", reverse=True)


def get_source(work: dict[str, Any]) -> str:
    location = work.get("primary_location") or {}
    source = location.get("source") or {}
    return (source.get("display_name") or "").strip()


def get_url(work: dict[str, Any]) -> str:
    doi = work.get("doi")
    if doi:
        return doi
    location = work.get("primary_location") or {}
    return location.get("landing_page_url") or work.get("id") or ""


def clean_title(title: str) -> str:
    return re.sub(r"\s+", " ", title).strip()


def format_date(date_text: str) -> str:
    try:
        return dt.date.fromisoformat(date_text).strftime("%d %b %Y")
    except ValueError:
        return date_text


def format_type(work_type: str) -> str:
    labels = {
        "article": "article",
        "book-chapter": "book chapter",
        "conference-paper": "conference paper",
        "data-paper": "data paper",
        "preprint": "preprint",
        "report": "report",
    }
    return labels.get(work_type or "", work_type or "work")


def format_authors(work: dict[str, Any], limit: int = 8) -> str:
    names: list[str] = []
    for authorship in work.get("authorships") or []:
        author = authorship.get("author") or {}
        name = author.get("display_name")
        if not name:
            continue
        if "aslansefat" in name.lower():
            name = f"**{name}**"
        names.append(name)
    if len(names) > limit:
        return ", ".join(names[:limit]) + ", et al."
    return ", ".join(names)


def publication_entry(work: dict[str, Any]) -> str:
    title = clean_title(work.get("display_name") or "")
    url = get_url(work)
    source = get_source(work)
    year = work.get("publication_year") or ""
    work_type = format_type(work.get("type") or "")
    authors = format_authors(work)
    cited_by = work.get("cited_by_count")
    citation = f"{source}, {year}" if source else f"{work_type.title()}, {year}"
    doi_line = f"[DOI / source]({url})" if url else ""
    cited_line = f"Cited by {cited_by} in OpenAlex." if cited_by else ""

    lines = [
        f"**[{title}]({url})**" if url else f"**{title}**",
        authors,
        f"*{citation}.* {doi_line} {cited_line}".strip(),
    ]
    return "<br>\n".join(line for line in lines if line)


def render_publications(works: list[dict[str, Any]]) -> str:
    generated = [
        "<div class=\"publication-list\" markdown>",
        "",
    ]
    for work in works[:MAX_PUBLICATIONS]:
        generated.append(publication_entry(work))
        generated.append("")
    generated.append("</div>")
    generated.append("")
    generated.append(
        f"_Automatically updated from [OpenAlex](https://openalex.org/authors/{OPENALEX_AUTHOR_ID}) using ORCID "
        f"[{ORCID}](https://orcid.org/{ORCID}). Google Scholar remains available as the public profile: "
        f"[Koorosh Aslansefat]({SCHOLAR_URL})._"
    )
    return "\n".join(generated).strip()


def render_news(works: list[dict[str, Any]]) -> str:
    lines = []
    for work in works[:MAX_NEWS]:
        title = clean_title(work.get("display_name") or "")
        url = get_url(work)
        date_text = format_date(work.get("publication_date") or str(work.get("publication_year") or ""))
        work_type = format_type(work.get("type") or "")
        source = get_source(work)
        venue = f" in {source}" if source else ""
        link = f"[{title}]({url})" if url else title
        lines.append(f"- **{date_text}** - New {work_type}: {link}{venue}.")
    return "\n".join(lines)


def replace_between_markers(text: str, start: str, end: str, replacement: str) -> str:
    pattern = re.compile(rf"{re.escape(start)}.*?{re.escape(end)}", re.DOTALL)
    block = f"{start}\n{replacement.strip()}\n{end}"
    if not pattern.search(text):
        raise RuntimeError(f"Missing markers: {start} / {end}")
    return pattern.sub(block, text, count=1)


def ensure_publication_markers(text: str) -> str:
    if LIST_START in text and LIST_END in text:
        return text
    insert = textwrap.dedent(
        f"""

        ## Latest Papers

        {LIST_START}
        Pending first automated update.
        {LIST_END}
        """
    ).strip()
    return text.replace("## Selected Papers", insert + "\n\n## Selected Papers", 1)


def ensure_news_markers(text: str) -> str:
    if NEWS_START in text and NEWS_END in text:
        return text
    insert = textwrap.dedent(
        f"""

        ## Latest Papers

        {NEWS_START}
        Pending first automated update.
        {NEWS_END}
        """
    ).rstrip()
    return text.replace("## Latest News", insert + "\n\n## Latest News", 1)


def main() -> int:
    works = fetch_openalex_works()
    if not works:
        print("No OpenAlex works found; leaving files unchanged.", file=sys.stderr)
        return 1

    publications_text = ensure_publication_markers(PUBLICATIONS_MD.read_text(encoding="utf-8"))
    publications_text = replace_between_markers(
        publications_text,
        LIST_START,
        LIST_END,
        render_publications(works),
    )
    PUBLICATIONS_MD.write_text(publications_text.rstrip() + "\n", encoding="utf-8")

    index_text = ensure_news_markers(INDEX_MD.read_text(encoding="utf-8"))
    index_text = replace_between_markers(
        index_text,
        NEWS_START,
        NEWS_END,
        render_news(works),
    )
    INDEX_MD.write_text(index_text.rstrip() + "\n", encoding="utf-8")

    print(f"Updated {PUBLICATIONS_MD} and {INDEX_MD} with {min(len(works), MAX_PUBLICATIONS)} publications.")
    print(f"Latest publication: {clean_title(works[0].get('display_name') or '')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
