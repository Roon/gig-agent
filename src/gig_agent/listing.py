from dataclasses import dataclass


@dataclass(frozen=True)
class Listing:
    """A single job posting as it appears in a Source, in a common shape."""

    source: str
    source_id: str
    url: str
    title: str
    company: str
    description: str
    location: str
    employment_type: str
    pay_text: str
    application_email: str | None
    application_url: str

    @property
    def key(self) -> str:
        return f"{self.source}:{self.source_id}"
