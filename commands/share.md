---
description: Share content on Cairn — one artifact or a bundle — and hand back the link.
argument-hint: "[file ...] or a description of what to share"
---

Share `$ARGUMENTS` on Cairn. If `$ARGUMENTS` names files, read them locally; if it
describes content from this session (a report, a diff, a log), assemble that content.

1. Route per the `cairn` skill:
   - one body → `artifact_create`, with `share_type` picked from the content
     (`markdown` for prose/reports, `code` for source, `file` otherwise) and a
     `media_type` when you know it;
   - several files that belong together → `bundle_create` with one named member per
     file — never concatenate them into one body.
2. Give the artifact a real, human-legible `title`.
3. Reply with the returned `url` (and the `mcp://cairn/<id>` handle if another agent
   will consume it), plus `expires_at` if retention seems to matter. Do NOT quote the
   body back into the conversation — the link is the deliverable.
