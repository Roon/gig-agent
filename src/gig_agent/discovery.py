"""The Discovery pipeline: raw Source payloads in, Listings to consider out. No I/O."""

import re
from dataclasses import dataclass, field

from gig_agent.listing import Listing
from gig_agent.sources import remotive

PARSERS = {remotive.NAME: remotive.parse}

# Location phrases that admit a remote worker based in the US (Aaron is in Denver).
US_OPEN = re.compile(
    r"\b(usa|us|u\.s\.|united states|worldwide|anywhere|americas|north(ern)? america)\b",
    re.IGNORECASE,
)


@dataclass
class DiscoveryResult:
    to_consider: list[Listing] = field(default_factory=list)
    # Seen keys of Listings dropped by a Hard filter, with the reason.
    dropped: dict[str, str] = field(default_factory=dict)


def discover(payloads: dict[str, dict], seen: set[str]) -> DiscoveryResult:
    result = DiscoveryResult()
    for source, payload in payloads.items():
        for listing in PARSERS[source](payload):
            if listing.key in seen:
                continue
            reason = _hard_filter(listing)
            if reason:
                result.dropped[listing.key] = reason
            else:
                result.to_consider.append(listing)
    return result


def _hard_filter(listing: Listing) -> str | None:
    if listing.location and not US_OPEN.search(listing.location):
        return "not remote for a US-based worker"
    return None
