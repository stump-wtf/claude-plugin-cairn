# claude-plugin-cairn

A [Claude Code](https://claude.com/claude-code) and [Crush](https://github.com/charmbracelet/crush)
plugin for using [Cairn](https://cairn.stump.wtf/docs/) — the AI-native pastebin / gist /
requestbin — **well**: drop work-product receipts as short links, route correctly between
artifact / bundle / trajectory creates, annotate with typed anchors, hand work to another
agent as a tagged handoff, and keep artifact bodies out of your context window.

Mirror: https://github.com/stump-wtf/claude-plugin-cairn

## What's in it

- **`skills/cairn`** — the `cairn` skill. Auto-loads when the user wants something shared
  ("share this", "give me a link"), pastes a Cairn short URL or `mcp://cairn/<id>` handle,
  or wants an agent run captured as a trajectory. Encodes the mental model
  (*share the link, do not paste the body*), the create-tool routing
  (`artifact_create` vs `bundle_create` vs `run_create`), the typed-anchor annotation
  layer, tags and the handoff convention, what provenance can and cannot prove,
  TTL/expiry expectations, and the context-hygiene traps.
- **`commands/`** — slash commands that run in the main (tool-holding) session:
  - `/cairn:share [files…]` — share files or session content as an artifact or bundle.
  - `/cairn:receipt` — drop a markdown receipt of this session's work as a Cairn link.

## Install

The plugin is public, so it installs from the GitHub mirror on any machine.

### Claude Code

```bash
claude plugin marketplace add stump-wtf/claude-plugin-cairn
claude plugin install cairn@claude-plugin-cairn
```

Verify it loaded by asking Claude to list its skills, or by starting a request with
"share this on cairn" and checking that it reaches for `artifact_create` rather than
inventing a paste service.

### Crush

Crush reads `options.skills_paths` **plus several directories it scans with no configuration at
all** — `~/.config/crush/skills`, `~/.config/agents/skills`, `~/.agents/skills`,
`~/.claude/skills`, and the `.crush/skills` / `.agents/skills` equivalents inside a project. So
there are two working routes; a clone on its own does nothing until one of them holds.

```bash
git clone https://github.com/stump-wtf/claude-plugin-cairn.git ~/src/claude-plugin-cairn
```

**Register the clone.** Crush has two config formats and both set the same `skills_paths` list:
`crushrc` (Bash with Crush builtins) and `crush.json`. Both work, and where a directory holds
both Crush merges them with `crushrc` winning on conflict — but **`crush.json` is deprecated
upstream**: still supported, and frozen, with new options landing only in the Bash config. So
prefer `crushrc`. `option skill-path` adds to the list rather than replacing it, is upstream
Crush rather than a fork-only directive, and expands `~`, so no absolute path is needed:

```
# ~/.config/crush/crushrc
option skill-path ~/src/claude-plugin-cairn/skills
```

**Or copy it into a scanned directory**, for zero configuration:

```bash
cp -R ~/src/claude-plugin-cairn/skills/* ~/.config/crush/skills/
```

**Copy — do not symlink.** Crush resolves symlinks before deciding whether a file sits inside a
skills directory, so a symlinked skill still *loads*, while the files it wants to read resolve
back to the clone, outside that directory. Those reads then truncate and start asking for
permission, which looks like the skill misbehaving rather than a path problem. To keep the files
where you cloned them, register that path instead of copying.

## What the skill does not do

- **It grants nothing.** Scopes come from the OAuth grant or the personal access token, not
  from the skill. Installing it does not widen what an agent can reach.
- **It is not required to use Cairn.** The MCP tools work without it; the skill is the
  difference between using them and using them well.
- **It does not connect you.** Wiring the MCP server is a separate step —
  [Connect your agent over MCP](https://cairn.stump.wtf/docs/guides/connect-your-agent).

## Development

```bash
make check        # lint (manifests, frontmatter, caps, dead links)
```

The lint enforces the two budgets a harness applies silently: a description over the cap
(900 house, 1024 hard once XML-escaped) makes the skill vanish from the prompt with no
diagnostic, and a body over 180 lines belongs partly in `references/`. It also greps for two
link patterns that must stay dead — the retired GitHub source URL, which 404s, and any
private-forge URL, which no reader of this public repo can open. Both patterns are spelled
out in the `Makefile`.

## License

MIT
