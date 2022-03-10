find . -iname "*.py" -not -path "./tests/*" | xargs -n1 -I {}  pylint --output-format=colorized {}; true
PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes
