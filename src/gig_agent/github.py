"""Thin wrapper over the `gh` CLI for the repo this runs in. Not unit-tested; use --dry-run."""

import json
import re
import subprocess

GIG_LABELS = {
    "gig:drafted": "Draft awaiting Aaron's Approval",
    "gig:approved": "Approved by Aaron; the Send run may send it",
    "gig:sent": "Email application sent",
    "gig:packet-ready": "Packet ready for Aaron to submit",
    "gig:submitted": "Aaron submitted the Packet",
    "gig:reply": "Outcome: employer replied",
    "gig:interview": "Outcome: interview",
    "gig:won": "Outcome: won",
    "gig:lost": "Outcome: lost",
    "gig:ghosted": "Outcome: no response",
    "gig:active": "Won Gig Aaron is working; counts toward Capacity",
}
LEDGER_LABEL = "seen-ledger"
LEDGER_TITLE = "Seen ledger"
LEDGER_BODY = (
    "Every Listing the agent has evaluated, whatever the result. "
    "The Discovery run appends a comment per run; keys listed here are never evaluated again. "
    "Don't edit or delete these comments."
)
LEDGER_LINE = re.compile(r"^- `([^`]+)`", re.MULTILINE)


def _gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def ensure_labels() -> None:
    for name, description in {**GIG_LABELS, LEDGER_LABEL: "Record of Seen Listings"}.items():
        _gh("label", "create", name, "--description", description, "--color", "5319e7", "--force")


def ledger_number() -> int:
    found = json.loads(_gh("issue", "list", "--label", LEDGER_LABEL, "--state", "all", "--json", "number"))
    if found:
        return found[0]["number"]
    url = _gh("issue", "create", "--title", LEDGER_TITLE, "--label", LEDGER_LABEL, "--body", LEDGER_BODY)
    number = int(url.strip().rsplit("/", 1)[1])
    _gh("issue", "pin", str(number))
    return number


def seen_keys(ledger: int) -> set[str]:
    bodies = _gh("api", "--paginate", f"repos/{{owner}}/{{repo}}/issues/{ledger}/comments", "--jq", ".[].body")
    return set(LEDGER_LINE.findall(bodies))


def record_seen(ledger: int, entries: dict[str, str]) -> None:
    lines = [f"- `{key}`: {note}" for key, note in entries.items()]
    _gh("issue", "comment", str(ledger), "--body", "\n".join(lines))


def create_gig(title: str, body: str) -> int:
    url = _gh("issue", "create", "--title", title, "--label", "gig:drafted", "--body", body)
    return int(url.strip().rsplit("/", 1)[1])
