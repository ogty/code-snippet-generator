test:
	@python3 -m unittest discover -s ./tests -p "*_test.py"

clean-pychache:
	@find . -name "__pycache__" -exec rm -rf {} \; 2>/dev/null
