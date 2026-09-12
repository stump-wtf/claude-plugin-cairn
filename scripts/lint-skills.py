#!/usr/bin/env python3
"""
Frontmatter And Budget Lint For The Skills

Checks the things that make a skill fail to *load* rather than fail to work, plus the
two budgets a harness enforces silently.

A skill whose frontmatter is malformed, or whose name disagrees with its directory, is
dropped at discovery with a logged warning nobody reads. A description that exceeds the
hard cap once XML-escaped vanishes the same way — which is why the house cap is 900 and
not 1024, and why apostrophes and quotes are counted here: each one costs six characters
in the prompt and one on disk.

The 180-line body cap is what keeps the always-loaded cost bounded. Overflow belongs in
references/, which is read only when it is needed.

@joestump 09/12/2026 - Added with the skill's MCP-surface correction.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DESC_CAP = 900
BODY_CAP = 180
ESCAPABLE = '&<>"\''

errors = []


def fail(msg):
    errors.append(msg)


skills = sorted(ROOT.glob("skills/*/SKILL.md"))
if not skills:
    fail("no skills/*/SKILL.md found")

for skill in skills:
    rel = skill.relative_to(ROOT)
    text = skill.read_text()

    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        fail(f"{rel}: missing or unterminated YAML frontmatter — the skill cannot load")
        continue
    front, body = m.group(1), m.group(2)

    name_line = next((l for l in front.splitlines() if l.startswith("name:")), None)
    if name_line is None:
        fail(f"{rel}: frontmatter is missing 'name'")
    else:
        declared = name_line.split(":", 1)[1].strip()
        if declared != skill.parent.name:
            fail(f"{rel}: name {declared!r} does not match directory {skill.parent.name!r}")

    desc = re.search(r"^description:.*?(?=\n[a-zA-Z_-]+:|\Z)", front, re.S | re.M)
    if desc is None:
        fail(f"{rel}: frontmatter is missing 'description'")
    else:
        flat = " ".join(desc.group(0).split())[len("description: "):]
        escaped = len(flat) + sum(flat.count(c) for c in ESCAPABLE) * 5
        if len(flat) > DESC_CAP:
            fail(f"{rel}: description is {len(flat)} chars, over the {DESC_CAP} house cap")
        elif escaped > 1024:
            fail(
                f"{rel}: description is {len(flat)} chars but {escaped} once XML-escaped, "
                f"over the 1024 hard cap — the skill would be dropped silently"
            )

    # A skill carrying shell snippets must not be user-invocable: invoking it as a slash
    # command runs the whole body through the prompt's HTML escaper, mangling every
    # quote, >, and < in every snippet.
    if any(l.strip().startswith("user-invocable:") for l in front.splitlines()):
        if "```" in body:
            fail(f"{rel}: 'user-invocable' on a body containing fenced snippets mangles them")

    n = len(body.splitlines())
    if n > BODY_CAP:
        fail(f"{rel}: body is {n} lines, over the {BODY_CAP} cap — move detail to references/")

for msg in errors:
    print(f"FAIL {msg}")
print(f"{len(skills)} skill(s) checked, {len(errors)} failure(s)")
sys.exit(1 if errors else 0)
