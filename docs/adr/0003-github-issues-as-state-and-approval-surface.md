# GitHub Issues are the pipeline's state store and approval surface

Each Gig is one issue on `Roon/gig-agent`; its stage is a `gig:*` label (`drafted` → `approved` → `sent`/`packet-ready` → `submitted` → outcome, → `active`). Aaron approves by labelling, edits Drafts in the issue body, and requests rewrites by comment. We chose this over a committed JSON/SQLite file or a custom web page because cloud runs start stateless, Issues are already wired up, work from a phone, and keep an audit trail of what was sent. Listings rejected by filters are recorded as Seen without becoming issues.
