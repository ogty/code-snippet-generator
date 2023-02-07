max_frame_width := 92

setup:
	@chmod +x ./snippet

test:
	@python3 -m unittest discover -s ./tests -p "*_test.py"

clean-pychache:
	@find . -name "__pycache__" -exec rm -rf {} \; 2>/dev/null

docs-usage:
	@./snippet simple -p docs/usage.md -l Markdown -w ${max_frame_width} | pbcopy

docs-examples:
	@./snippet shell -p ./docs/examples.txt -l zsh -x '$$ ' -w ${max_frame_width} | pbcopy

docs-setup:
	@./snippet shell -p docs/setup.txt -l Zsh -x '$$ ' -w ${max_frame_width} | pbcopy
