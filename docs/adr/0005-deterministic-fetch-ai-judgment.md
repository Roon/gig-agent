# Python does fetching and filtering; the AI does judgment and writing

Fetching Sources, de-duplicating Seen listings, and applying Hard filters (including the aviation keyword/company blocklist) are plain Python: deterministic, testable, and cheap. The AI is used only where judgment is needed: Fit scoring (including a second Exclusion check with stated reasoning), Drafts, Packets, rewrites, and the Weekly report. We rejected an all-prompt agent because silent misses in fetching or filtering would be invisible and untestable.
