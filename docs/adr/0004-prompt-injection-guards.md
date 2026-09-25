# Contain untrusted listing text away from the ability to send email

Listings are untrusted text read by the same AI that has access to Aaron's Gmail. We contain this structurally rather than trusting the model:

- The Discovery run (which reads Listings) has no Gmail access; only the Send run does.
- An Email application goes only to the address captured by deterministic fetch code, never one written by the AI.
- The Send run acts only on issues whose `gig:approved` label was added by Aaron's GitHub account, verified via the API, and sends the issue body verbatim.
- The cloud environment's network allowlist contains only the Source API domains.

A malicious Listing can therefore at worst produce a bad Draft that Aaron rejects.
