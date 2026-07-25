---
description: Drop a Cairn receipt — a markdown summary of this session's work, shared as a link.
argument-hint: "[optional focus, e.g. 'the migration' — defaults to the whole session]"
---

Drop a receipt on Cairn for this session's work (scoped to `$ARGUMENTS` if given,
otherwise the whole session).

1. Compose a concise markdown receipt: what was asked, what changed (with links to the
   actual PRs/commits/issues touched), what was verified, and any follow-ups left open.
   Write it for someone catching up later, not as a chat transcript.
2. `artifact_create(share_type="markdown", title="<project>: <one-line outcome>", body=…)`.
3. Reply with just the returned `url` and a one-line description. Do NOT paste the
   receipt body back into the conversation — the link is the deliverable.
