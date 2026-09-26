"""Rendering a Gig as a GitHub issue body, and reading its metadata back."""

import html
import json
import re

from gig_agent.listing import Listing

SOURCE_NAMES = {"remotive": "Remotive"}
DESCRIPTION_LIMIT = 20_000
META_RE = re.compile(r"<!-- gig-meta\n(.*?)\n-->", re.DOTALL)


def title(listing: Listing) -> str:
    return f"{listing.company} — {listing.title}"


def render(listing: Listing, draft: str) -> str:
    meta = {
        "key": listing.key,
        "source": listing.source,
        "url": listing.url,
        "application_email": listing.application_email,
        "application_url": listing.application_url,
    }
    source_name = SOURCE_NAMES.get(listing.source, listing.source)
    return "\n".join([
        f"**{listing.company}**: {listing.title}",
        "",
        f"- Source: [{source_name}]({listing.url}) (listing via {source_name})",
        f"- Location: {listing.location or 'not stated'}",
        f"- Type: {listing.employment_type or 'not stated'}",
        f"- Pay: {listing.pay_text or 'not stated'}",
        "",
        f"<!-- gig-meta\n{json.dumps(meta)}\n-->",
        "",
        "## Draft",
        "",
        "<!-- draft:start -->",
        draft,
        "<!-- draft:end -->",
        "",
        "## Listing",
        "",
        "<details><summary>Full text</summary>",
        "",
        _plain_text(listing.description),
        "",
        "</details>",
    ])


def parse_meta(body: str) -> dict:
    """The fetch-captured metadata. Reads the first block, which precedes any listing text."""
    match = META_RE.search(body)
    if not match:
        raise ValueError("issue body has no gig-meta block")
    return json.loads(match.group(1))


def _plain_text(description: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", " ", description))
    # Listing text is untrusted: stop it forging our HTML-comment markers.
    text = text.replace("<!--", "").replace("-->", "")
    text = re.sub(r"[ \t]+", " ", text).strip()
    return text[:DESCRIPTION_LIMIT]
