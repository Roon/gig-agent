# gig-agent

A personal agent that finds remote, part-time data-analysis work Aaron can do around a day job, drafts applications for it, and submits them once Aaron approves.

## Discovery

**Source**:
A job board or feed whose terms allow automated access, and which the agent reads listings from.
_Avoid_: Site, platform, board

**Listing**:
A single job posting as it appears in a Source, before any judgment is applied.
_Avoid_: Post, job, ad

**Hard filter**:
A pass/fail rule a Listing must satisfy before it is scored: remote, part-time/contract/flexible hours, not Excluded, stated rate not below the Rate floor, and not already Seen.
_Avoid_: Screen, criteria

**Seen**:
A Listing the agent has already evaluated, whatever the result; it is never evaluated again.
_Avoid_: Processed, visited

**Exclusion**:
A company or industry Aaron must not work for. Currently all of aviation, because of Aaron's employment at Jeppesen ForeFlight.
_Avoid_: Blocklist, banned, competitor

**Fit score**:
A 1–5 judgment of how well a Listing matches Aaron's Profile; only 4 and 5 become Gigs.
_Avoid_: Relevance, match score, rating

**Rate unknown**:
A flag on a Listing that states no pay; it passes the Rate floor filter rather than being dropped.

## Gigs and applications

**Gig**:
A Listing that passed the Hard filters and Fit score and is now tracked through the pipeline until an Outcome.
_Avoid_: Opportunity, lead, job

**Draft**:
The agent's proposed application text for a Gig, awaiting Aaron's Approval.
_Avoid_: Proposal, cover letter

**Email application**:
An application delivered by email to an address stated in the Listing; the agent sends it after Approval.

**Packet**:
A paste-ready bundle (link, tailored note, likely form answers) for a Gig whose application is a web form; Aaron submits it by hand.
_Avoid_: Kit, bundle

**Approval**:
Aaron's explicit go-ahead for a Draft, given by Aaron personally; nothing is sent without it.
_Avoid_: Sign-off, OK

**Rewrite request**:
Aaron's instruction on a Draft asking the agent to revise it; the revised Draft needs a fresh Approval.

**Submission**:
The moment an application actually reaches the employer, either sent by the agent (Email application) or by Aaron (Packet).
_Avoid_: Apply, send

**Outcome**:
What happened after Submission: reply, interview, won, lost, or ghosted. Recorded by Aaron.
_Avoid_: Result, status

**Active gig**:
A won Gig Aaron is currently working, with an estimated weekly hours figure.

## Aaron's constraints

**Profile**:
The material the agent writes from: résumé, preferences, project stories, and a voice sample.
_Avoid_: Bio, persona

**Rate floor**:
The minimum acceptable pay: $50/hr.

**Capacity**:
The weekly hours Aaron can give to gigs: 10. When Active gigs reach it, the agent stops drafting.
_Avoid_: Availability, bandwidth

**Weekly draft cap**:
The most Drafts the agent produces in a week: 7.

## Runs

**Discovery run**:
The early-morning run that reads Sources, applies Hard filters and Fit scores, and produces Drafts.

**Send run**:
The evening run that handles Rewrite requests and makes Submissions of approved Email applications.

**Weekly report**:
The Monday summary of Gigs by Source, Approvals, Submissions, Outcomes, and Capacity used.
