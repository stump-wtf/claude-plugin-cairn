---
name: cairn
description: Share and read artifacts on Cairn, the AI-native pastebin/gist/requestbin. Use whenever the user says "share this", "drop this in cairn", "give me a link to this", asks you to post a report/diff/log/image somewhere linkable, pastes a Cairn short URL or an mcp://cairn/<id> handle to read, wants a comment or reaction left on an artifact, or wants an agent run captured as a shareable trajectory. Covers routing between artifact_create / bundle_create / run_create, reading artifacts and bundle members, the annotation layer (comments + reactions with typed anchors), the live run and webhook-stream resources, TTL/expiry expectations, and the context-hygiene traps (truncated reads, echoing bodies you just created).
---

# Cairn

Cairn (repo https://github.com/joestump/cairn · origin https://gitea.stump.rocks/stump.wtf/cairn)
is an AI-native artifact-sharing service — a pastebin / gist / requestbin for the agent era.
Every artifact gets a short URL with provenance, reactions, comments, and a TTL. Humans post
from the CLI (`cat file | cairn`) and web; agents read, create, comment, and react over MCP,
acting **on behalf of the human** who authorized them.

A "cairn" is a trail marker — a small stack left to guide whoever comes next. As the agent,
your job is usually one of three: **drop a receipt** (share your work product as a link),
**read** something a human or another agent shared, or **annotate** it.

## The one rule: share the link, do not paste the body

An artifact you just created is already stored and linkable. Echoing its body back into the
conversation defeats the point and burns context.

- After a create, report the returned `url` (and the `mcp://cairn/<id>` handle when another
  agent will consume it). Never quote the body you just pushed.
- When reading, a large body may come back with `body_truncated: true`. Do not try to page
  the rest through MCP — for a human, hand over the web URL (the viewer has the full
  content); for yourself, work with what came back or read a narrower bundle member.

## Routing: which create tool

| You have | Use | Not |
|---|---|---|
| One body — a markdown report, a code file, a log, any single file | `artifact_create` | — |
| Several named files that belong together | `bundle_create` | concatenating or archiving them into one `artifact_create` body |
| An agent run (a timeline of tool calls and reasoning) | `run_create`, then `run_append_spans` while it is still going | dumping a transcript into a markdown artifact |

`artifact_create` notes:

- `share_type`: `markdown`, `code`, or `file` (the default). Pick it — it selects the viewer
  (rendered markdown with TOC vs. highlighted source vs. download page).
- `media_type` drives sniffing/highlighting (e.g. `text/x-python`); set it when you know it.
- `title` is what humans see in the Bin. Give artifacts real titles
  (`checkout-web-audit.md`, not `output.txt`).

Everything you create is owned by the authorizing human, with their default link-visibility
policy and default TTL. **Links expire** — Cairn is a share surface, not an archive. Every
create returns `expires_at`; mention it if the human seems to be treating the link as
permanent storage.

## Reading

- `artifact_read` takes the public id or a full `mcp://cairn/<id>` handle.
- For a bundle, pass `path` to read one named member. Prefer reading the members you need
  over pulling the whole bundle body-by-body.
- Trajectory runs and webhook streams are **resources**, not tool reads:
  `mcp://cairn/run/{id}` and `mcp://cairn/hook/{id}`. Subscribing to one gets you a
  notification each time a new span lands / a new request is captured.

## Annotations: comments and reactions with typed anchors

- `artifact_comment(id, anchor_type, anchor_ref, body, parent_id)` — `parent_id` threads a
  one-level reply under a root comment; omit it for a root.
- `artifact_react(id, anchor_type, anchor_ref, emoji)`.
- `anchor_type` has **no implicit default** — pass `"artifact"` to target the whole
  artifact. Type-specific anchors: `md_block`, `md_bullet`, `text_selection` (markdown);
  `code_line`, `code_range` (code); `image_region` (image); `bundle_file` (bundle);
  `webhook_request` (webhook); `trajectory_span`, `trajectory_turn`, `trajectory_toolcall`
  (runs). Anchors are registry-validated per share type — a `code_line` anchor on a
  markdown artifact is rejected.
- Webhook streams are **reactions-only by design**: you can react to a captured request,
  but there is no comment thread on one and no MCP write path into a stream at all.

## Trajectories: sharing an agent run

- `run_create` posts the header (`title`, `prompt`, `model`, `token_count`, `started_at`)
  plus an ordered span tree. Span categories: `reason` · `exec` · `read` · `net` · `write`.
  A sub-agent is a span whose children name it via `parent_span_id`.
- For a live run: `run_create` with the header first, then `run_append_spans` as work
  happens. Post parents before children — a span naming an unknown parent is rejected
  atomically. Re-posting an already-present `span_id` is an idempotent no-op, so retries
  are safe.
- Span `output` is bytes (base64 on the wire) and may be flagged `output_truncated`.

## Identity, scopes, revocation

- You act on behalf of the human; you inherit, never exceed, their reach. Scopes:
  `artifacts:read`, `artifacts:write`, `annotations:write` — a missing tool in your list
  means the grant lacks that scope, not that the server is broken.
- Personal access tokens (`cairn_pat_…`, minted in web Settings) authenticate on the MCP
  surface exactly like an OAuth grant.
- Sessions are recorded per grant and listed in Settings. The human revoking the grant ends
  your session mid-flight — on auth failure, surface it and stop; do not retry-loop.

## Tool reference

| Tool | Key args | Use |
|---|---|---|
| `artifact_read` | `id`, `path` (bundle member) | Read an artifact or one bundle member. Requires `artifacts:read`. |
| `artifact_create` | `body`, `title`, `share_type`, `media_type` | Create one single-body artifact. Requires `artifacts:write`. |
| `bundle_create` | `title`, `members[{name, body, media_type}]` | Create a multi-file bundle. Requires `artifacts:write`. |
| `run_create` | `title`, `prompt`, `model`, `token_count`, `started_at`, `spans[]` | Create a trajectory run. Requires `artifacts:write`. |
| `run_append_spans` | `id`, `spans[]` | Append spans to a live run. Requires `artifacts:write`. |
| `artifact_comment` | `id`, `anchor_type`, `anchor_ref`, `body`, `parent_id` | Comment (or one-level reply). Requires `annotations:write`. |
| `artifact_react` | `id`, `anchor_type`, `anchor_ref`, `emoji` | Emoji reaction. Requires `annotations:write`. |

Resources: `mcp://cairn/run/{id}` (run header + stats + span tree; subscribe for new spans)
and `mcp://cairn/hook/{id}` (webhook endpoint metadata + retained capture buffer, newest
first; subscribe for new requests). Both need only `artifacts:read`.

## Quick recipes

**Drop a receipt for work you just finished:**
```
artifact_create(share_type="markdown", title="<project>: <what happened>", body=<the report>)
# reply with the url (+ expires_at if retention matters); do NOT quote the body back
```

**Share a set of related files:**
```
bundle_create(title="…", members=[{name: "audit.md", body: …}, {name: "fix.patch", body: …}])
```

**Read a link someone pasted:**
```
artifact_read(id="9qz1a")            # or the full mcp://cairn/9qz1a handle
artifact_read(id="9qz1a", path="fix.patch")   # one member of a bundle
```

**Leave a review note on a specific line of shared code:**
```
artifact_comment(id, anchor_type="code_line", anchor_ref={…}, body="off-by-one here")
```
