import json
from pathlib import Path

from gig_agent.discovery import discover

FIXTURES = Path(__file__).parent / "fixtures"


def remotive_payload():
    return json.loads((FIXTURES / "remotive.json").read_text())


def test_new_remote_listing_is_returned_for_consideration():
    result = discover({"remotive": remotive_payload()}, seen=set())

    listing = next(l for l in result.to_consider if l.key == "remotive:1001")
    assert listing.source == "remotive"
    assert listing.title == "Part-time Data Analyst"
    assert listing.company == "Acme Analytics"
    assert listing.url == "https://remotive.com/remote-jobs/data/part-time-data-analyst-1001"
    assert listing.employment_type == "part_time"
    assert listing.pay_text == "$60/hr"


def test_already_seen_listing_is_not_considered_again():
    result = discover({"remotive": remotive_payload()}, seen={"remotive:1001"})

    assert "remotive:1001" not in {l.key for l in result.to_consider}


def test_listing_not_open_to_remote_workers_in_the_us_is_dropped_and_marked_seen():
    result = discover({"remotive": remotive_payload()}, seen=set())

    assert "remotive:1002" not in {l.key for l in result.to_consider}
    assert result.dropped["remotive:1002"] == "not remote for a US-based worker"


def test_worldwide_listing_is_considered():
    result = discover({"remotive": remotive_payload()}, seen=set())

    assert "remotive:1003" in {l.key for l in result.to_consider}
