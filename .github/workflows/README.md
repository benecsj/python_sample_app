# GitHub Workflows

This folder contains CI workflows for python_sample_app.

- 00-test.yml: Basic install and smoke tests
- 01-test-and-coverage.yml: Full test run with coverage, artifacts upload
- 03-deploy-website.yml: Publishes docs and reports to GitHub Pages
- 10-release.yml: Creates a release snapshot of the project

Package name: `python_sample_app`
Main entry point: `python_sample_app.main` or `python main.py`