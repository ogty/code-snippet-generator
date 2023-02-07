include .env

max_frame_width := 92
shell_name      := zsh

setup:
	@chmod +x ./snippet

test:
	@python3 -m unittest discover -s ./tests -p "*_test.py"

clean-pychache:
	@find . -name "__pycache__" -exec rm -rf {} \; 2>/dev/null

docs-usage:
	@./snippet simple -p docs/usage.md -l Markdown -w ${max_frame_width} -f docs/usage.md | pbcopy

docs-examples:
	@./snippet shell -p ./docs/examples.txt -l ${shell_name} -x '$$ ' -w ${max_frame_width} | pbcopy

docs-setup:
	@./snippet shell -p docs/setup.txt -l ${shell_name} -x '$$ ' -w ${max_frame_width} | pbcopy

.PHONY: coverage
coverage:
	@coverage run -m unittest discover -s ./tests -p "*_test.py"

coverage-report: coverage
	@coverage report --omit=${IGNORE_PATH}
