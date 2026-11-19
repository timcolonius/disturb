# ── DISTURB website ─────────────────────────────────────────────────────────
#   make site     → rebuild docs/ from content.py + the Google Sheet
#   make serve    → build and preview at http://localhost:8001
#   make deploy   → commit everything and push (GitHub Actions publishes)
MSG ?= Update site content
.PHONY: site serve deploy
site:
	python3 build.py
serve: site
	@echo "Serving docs/ at http://localhost:8001  (Ctrl+C to stop)"
	@cd docs && python3 -m http.server 8001
deploy: site
	git add -A
	@git diff --cached --quiet || git commit -m "$(MSG)"
	git pull --rebase origin main
	git push
