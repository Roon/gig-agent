"""Command line: `python -m gig_agent discover [--dry-run] [--max-gigs N] [--payload SOURCE=PATH]`."""

import argparse
import json
from pathlib import Path

from gig_agent import gig_issue, github
from gig_agent.discovery import discover
from gig_agent.sources import remotive

FETCHERS = {remotive.NAME: remotive.fetch}
PLACEHOLDER_DRAFT = "_Placeholder: AI drafting arrives with Fit scoring (#10)._"


def main() -> None:
    parser = argparse.ArgumentParser(prog="gig_agent")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("discover", help="the Discovery run")
    run.add_argument("--dry-run", action="store_true", help="print intended actions; no GitHub writes")
    run.add_argument("--max-gigs", type=int, default=1, help="most Gigs to create this run")
    run.add_argument("--payload", action="append", default=[], metavar="SOURCE=PATH",
                     help="read a Source's payload from a file instead of fetching it")
    args = parser.parse_args()

    payloads = _payloads(args.payload)
    if args.dry_run:
        ledger, seen = None, set()
    else:
        github.ensure_labels()
        ledger = github.ledger_number()
        seen = github.seen_keys(ledger)

    result = discover(payloads, seen)
    gigs = result.to_consider[: args.max_gigs]
    newly_seen = dict(result.dropped)

    for listing in gigs:
        title = gig_issue.title(listing)
        if args.dry_run:
            print(f"would create Gig: {title} [{listing.key}]")
            continue
        number = github.create_gig(title, gig_issue.render(listing, PLACEHOLDER_DRAFT))
        newly_seen[listing.key] = f"became Gig #{number}"
        print(f"created Gig #{number}: {title}")

    for key, reason in result.dropped.items():
        print(f"dropped {key}: {reason}")
    left = len(result.to_consider) - len(gigs)
    if left:
        print(f"{left} more Listing(s) passed but were left for a later run (--max-gigs {args.max_gigs})")
    if args.dry_run:
        print(f"would mark {len(newly_seen)} Listing(s) Seen")
    elif newly_seen:
        github.record_seen(ledger, newly_seen)


def _payloads(overrides: list[str]) -> dict[str, dict]:
    files = dict(o.split("=", 1) for o in overrides)
    return {
        source: json.loads(Path(files[source]).read_text()) if source in files else fetch()
        for source, fetch in FETCHERS.items()
    }


if __name__ == "__main__":
    main()
