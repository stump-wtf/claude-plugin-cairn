# claude-plugin-cairn

A [Claude Code](https://claude.com/claude-code) plugin for using
[Cairn](https://github.com/joestump/cairn) — the AI-native pastebin / gist / requestbin —
**well**: drop work-product receipts as short links, route correctly between
artifact / bundle / trajectory creates, annotate with typed anchors, and keep artifact
bodies out of your context window.

Home: https://gitea.stump.rocks/stump.wtf/claude-plugin-cairn ·
Mirror: https://github.com/stump-wtf/claude-plugin-cairn

## What's in it

- **`skills/cairn`** — the `cairn` skill. Auto-loads when the user wants something shared
  ("share this", "give me a link"), pastes a Cairn short URL or `mcp://cairn/<id>` handle,
  or wants an agent run captured as a trajectory. Encodes the mental model
  (*share the link, do not paste the body*), the create-tool routing
  (`artifact_create` vs `bundle_create` vs `run_create`), the typed-anchor annotation
  layer, TTL/expiry expectations, and the context-hygiene traps (truncated reads,
  echoing bodies you just pushed).
- **`commands/`** — slash commands that run in the main (tool-holding) session:
  - `/cairn:share [files…]` — share files or session content as an artifact or bundle
    and hand back the link.
  - `/cairn:receipt` — drop a markdown receipt of this session's work as a Cairn link.

## Why a skill and commands (and no agents)

Cairn is reached through its MCP tools, and — as with the sibling
[claude-plugin-switchboard](https://gitea.stump.rocks/stump.wtf/claude-plugin-switchboard) —
subagents do not inherit MCP tools in practice, so the share flows must run in the main
session. This plugin ships no MCP-dependent agents for that reason.

## Install

This plugin lives in a plugin marketplace / is added directly to a Claude Code project or
your user config. See the Claude Code plugin docs for the current install flow. The plugin
root is this repository (it contains `.claude-plugin/plugin.json`).
