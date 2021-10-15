#!/bin/bash

git add .
git commit -m "Release $1"
git push
git tag "$1"
git push --tags
hub release create "$1"
rm -rf dist
portray on_github_pages
python setup.py sdist bdist_wheel
twine upload --skip-existing dist/*