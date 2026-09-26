"""Remotive public API. Terms: link back to Remotive, credit it as the source, fetch at most 4 times a day."""

import json
import urllib.request

from gig_agent.listing import Listing

NAME = "remotive"
URL = "https://remotive.com/api/remote-jobs?category=data"
# Remotive rejects Python's default User-Agent with a 403.
USER_AGENT = "gig-agent/0.1 (personal job search; github.com/Roon/gig-agent)"


def fetch() -> dict:
    request = urllib.request.Request(URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def parse(payload: dict) -> list[Listing]:
    return [
        Listing(
            source=NAME,
            source_id=str(job["id"]),
            url=job["url"],
            title=job["title"],
            company=job["company_name"],
            description=job["description"],
            location=job["candidate_required_location"],
            employment_type=job["job_type"],
            pay_text=job["salary"],
            application_email=None,
            application_url=job["url"],
        )
        for job in payload["jobs"]
    ]
