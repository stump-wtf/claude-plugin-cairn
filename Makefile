# Plugin Checks
#
# This repository ships markdown guidance rather than code, so `make test` and `make lint`
# run the same gate: the plugin manifests must be valid JSON, every skill must carry usable
# frontmatter within the caps a harness actually enforces, and no shipped document may link
# a dead or private URL.
#
# The link check earns its place. The skill and plugin.json both shipped pointing at
# github.com/joestump/cairn, which 404s, and a private gitea.stump.rocks URL is unopenable
# for every reader of this public repo. A grep is the cheapest way to keep both dead.
#
# The caps are not style. A description over ~1024 characters after XML escaping makes the
# skill vanish from the prompt with no diagnostic, and the 180-line body cap is what keeps
# the loaded cost bounded; references/ is where the overflow belongs.
#
# @joestump 09/12/2026 - Added alongside the skill's MCP-surface correction.

.PHONY: check test lint

check: test lint

test: lint

lint:
	@echo "==> manifests parse"
	@for f in .claude-plugin/plugin.json .claude-plugin/marketplace.json; do \
		python3 -m json.tool "$$f" >/dev/null || exit 1; \
	done
	@echo "==> skill frontmatter and caps"
	@python3 scripts/lint-skills.py
	@echo "==> no dead or private links"
	@if grep -rn --exclude-dir=.git --exclude-dir=.claude \
		--include='*.md' --include='*.json' \
		-e 'github\.com/joestump/cairn' \
		-e 'gitea\.stump\.rocks' . ; then \
		echo "dead (joestump/cairn 404s) or private (gitea) link above; use https://cairn.stump.wtf/docs/"; \
		exit 1; \
	fi
	@echo "OK"
