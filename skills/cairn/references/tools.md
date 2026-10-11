# Tool reference

| Tool | Key args | Scope |
|---|---|---|
| `artifact_read` | `id`, `path` (bundle member) | `artifacts:read` |
| `artifact_create` | `body`, `title`, `share_type`, `media_type`, `model`, `tags` | `artifacts:write` |
| `bundle_create` | `title`, `members[{name, body, media_type}]`, `model`, `tags` | `artifacts:write` |
| `run_create` | `mode`, `title`, `prompt`, `model`, `token_count`, `started_at`, `spans[]` | `artifacts:write` |
| `run_append_spans` | `id`, `spans[]` | `artifacts:write` |
| `artifact_comment` | `id`, `anchor_type`, `anchor_ref`, `body`, `parent_id` | `annotations:write` |
| `artifact_react` | `id`, `anchor_type`, `anchor_ref`, `emoji` | `annotations:write` |
| `a2ui_action` | `name` (`open_member`), `context` | `artifacts:read` |
| `a2ui_error` | `code`, `message`, `surfaceId` | none |

Resources: `mcp://cairn/run/{id}` and `mcp://cairn/hook/{id}` (subscribable). Rendered views
for A2UI-capable hosts — `cairn://artifact/{id}/a2ui`, `cairn://bundle/{id}/a2ui`,
`cairn://bundle/{id}/{name}/a2ui`, `cairn://run/{id}/a2ui` (add `?w=N`), each also under
`mcp://cairn/…`. **When a human asks to *see* an artifact, read the matching A2UI view**;
`artifact_read` is for your own use. Subscribing to an `/a2ui` URI is an error — subscribe to
the JSON resource instead.

## Trajectory capture details

`run_create` posts the header (`title`, `prompt`, `model`, `token_count`, `started_at`) plus
an ordered span tree; `mode` is `batch` (default, complete on creation) or `open` (get a
link now, append as work happens with `run_append_spans`). Close an open run over REST.

Each span needs `span_id`, `category`, `start_offset_ms`, `duration_ms`; `parent_span_id`
nests it under a sub-agent. Post parents before children — a span naming an unknown parent
rejects the whole batch. Re-posting an existing `span_id` is an idempotent no-op, so
retries are safe.

**Always send `output`, as plain text.** Send it verbatim: do **not** base64-encode it and
do **not** pre-truncate it. Oversized outputs are stored as blobs and fetched lazily by the
viewer. Set `output_truncated` only if *you* truncated it. A span with no `output` renders
as an empty row.

Pick one category vocabulary for the whole run — operation kinds (`reason`, `exec`, `read`,
`write`, `net`) or workflow phases (`research`, `implementation`, `review`).

Every MCP call passes through your own context, so page a big capture in modest batches, or
POST the whole run to `/v1/runs` over REST. The server's `run_capture` prompt has the detail.
