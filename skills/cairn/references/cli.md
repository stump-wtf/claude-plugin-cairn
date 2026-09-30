# Cairn CLI

When the **CLI beats the MCP** (large bodies, scripts, subagents that don't inherit MCP tools),
use the `cairn` CLI for creating, reading, and managing Cairn artifacts from the command line.

## Authentication

```bash
# Token login (OAuth 2.1 + PKCE is a follow-up, not yet implemented)
cairn login

# Or use a token
cairn login --token <token>

# Check authentication
cairn whoami
```

Tokens are stored securely (OS keychain on macOS, file on Linux, Credential Manager on Windows). Never log or echo tokens.

## Create artifacts

```bash
# Pipe content, get a link printed and copied to clipboard
cat incident-report.md | cairn

# Create artifact from a file
cairn screenshots.pdf

# Bundle multiple files
cairn add bug-screenshot.png error.log database.sql

# Set custom TTL, title, and tags
cairn --ttl 24h --title "incident notes" --tag handoff --tag lane:m notes.md
```

**Common flags:**

| Flag | Meaning |
|------|---------|
| `--json` | Machine-readable output |
| `--no-copy` | Don't copy link to clipboard |
| `--redact` | Store detected secrets as `[REDACTED]` |
| `--ttl` | Set artifact TTL (e.g. `"24h"`, `"7d"`) |
| `--title` | Display title for the artifact |
| `--tag` | Add routing tags (repeatable) |

## Server deployment

`cairn` is a single monolithic binary; `cairn serve` provides the web app, API, SSE, and MCP
server (formerly the `cairnd` binary). Configuration is environment-based:

```bash
CAIRN_DATABASE_URL="postgres://..." CAIRN_S3_ENDPOINT="..." CAIRN_S3_BUCKET="..." \
cairn serve
```

The container image ships a `cairnd` shim for backwards compatibility.

## Use CLI instead of MCP when:

- **Larger payloads** — the CLI doesn't hit MCP tool limits
- **Scripts and automation** — piped output is only the bare link on stdout
- **Batch operations** — `cairn add` bundles multiple files efficiently
- **Binary content** — MCP bodies must be text; images and binaries go over the CLI or REST

## Quick recipes using CLI

**Share a long report:**
```bash
cat audit-log.txt | cairn --title "audit 2026-09-29"
# outputs: cairn.stump.wtf/abc123
```

**Bundle diagnostics:**
```bash
cairn --title "incident-291-diagnostics" --ttl 7d \
  add logs/screenshot.png logs/error.log diagnostics/system.txt
```

**Machine-readable output:**
```bash
cat report.md | cairn --json
```
