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
