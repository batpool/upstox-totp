SPHINXOPTS    ?=
SPHINXBUILD  ?= uv run sphinx-build
SOURCEDIR    = .
BUILDDIR     = _build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile


html: clean
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)



%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


.PHONY: clean-all install-deps serve watch livehtml


clean-all: clean
	rm -rf _build/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete


install-deps:
	cd .. && uv sync --group docs


serve: html
	@echo "Serving documentation at http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	cd _build/html && python -m http.server 8000


watch:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


livehtml:
	sphinx-autobuild -b html --host 0.0.0.0 --port 8000 "$(SOURCEDIR)" "$(BUILDDIR)/html"


all: html epub pdf


strict:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" -W --keep-going $(SPHINXOPTS) $(O)


linkcheck:
	@$(SPHINXBUILD) -M linkcheck "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


verbose:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" -v $(SPHINXOPTS) $(O)


quick:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" -E -a $(SPHINXOPTS) $(O)


dev: clean-all install-deps html serve


check: clean strict linkcheck


custom-help:
	@echo "Custom documentation targets:"
	@echo "  clean-all    Clean all build artifacts and cache files"
	@echo "  install-deps Install documentation dependencies with uv"
	@echo "  serve        Build HTML docs and serve at http://localhost:8000"
	@echo "  watch        Auto-rebuild on file changes (requires sphinx-autobuild)"
	@echo "  livehtml     Live rebuild with web server (requires sphinx-autobuild)"
	@echo "  all          Build HTML, EPUB, and PDF versions"
	@echo "  strict       Build with warnings treated as errors"
	@echo "  linkcheck    Check for broken external links"
	@echo "  verbose      Build with detailed output"
	@echo "  quick        Quick build skipping some checks"
	@echo "  dev          Full development workflow (clean, install, build, serve)"
	@echo "  check        Complete build validation (strict + linkcheck)"
	@echo ""
	@echo "Standard Sphinx targets:"
