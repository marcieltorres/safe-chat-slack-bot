# Contributing [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

Welcome, please read with careful and patience our manifest and coding style.

# Be pythonic!

```
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```
[The zen of python - PEP20](https://www.python.org/dev/peps/pep-0020/)

# Manifest

- First of all: **Be pythonic** :)
- [DRY](http://deviq.com/don-t-repeat-yourself/) - Don't repeat yourself.
- [KISS](https://deviq.com/keep-it-simple/) - Keep it simple stupid.

# Coding Style

We are using [Ruff](https://github.com/astral-sh/ruff) to manage the coding style [rules](https://beta.ruff.rs/docs/rules/).

Rule | Description
--- | ---
E,W | [pycode style](https://pypi.org/project/pycodestyle/)
F | [pyflakes](https://pypi.org/project/pyflakes/)
I | [isort](https://pypi.org/project/isort/)
N | [pep8-naming](https://pypi.org/project/pep8-naming/)
S | [flake8-bandit](https://pypi.org/project/flake8-bandit/)

# Releasing

Releases are cut from `main`. The decision is manual, the mechanics are automated: you bump the version and write the changelog entry inside your pull request, and [`release.yml`](.github/workflows/release.yml) creates the tag and publishes the GitHub Release on merge.

1. In the same pull request as your change, bump `version` in [pyproject.toml](pyproject.toml) following semver.
2. Move the `## [Unreleased]` content in [CHANGELOG.md](CHANGELOG.md) into a new `## [X.Y.Z] - YYYY-MM-DD` section.
3. Update the comparison links at the bottom of the changelog.
4. Merge. The tag and the release show up on their own in about a minute.
5. If something goes wrong, fix `CHANGELOG.md` and re-run `release` from **Actions → release → Run workflow**. Running it with `dry_run: true` prints the notes without creating anything.

Tags are plain `X.Y.Z`, without a `v` prefix. Never create a tag or a release by hand — the workflow owns both, and it derives the tag from `pyproject.toml` so the two cannot drift apart.

When to bump:

Change | Bump
--- | ---
New detection rule, new listener, new locale | minor
Regex fix, bug fix, translation tweak | patch
Change to `manifest.json` scopes, breaking configuration change | major
Dependency bump (Dependabot), docs, CI | none

The release notes are the changelog section verbatim, so write the entry for whoever reads the release page, not for the diff.

# AI Coding Agents

If you use an AI coding agent (Claude Code, Cursor, Copilot, Codex and friends) to contribute, point it at [AGENTS.md](AGENTS.md). It follows the [agents.md](https://agents.md/) convention and covers setup, commands, code style, testing conventions, commit format and the security rules that apply to this bot — it handles Slack tokens and PII, so those rules are not optional.

You are still responsible for everything you submit: read the diff, run `make local/lint` and `make local/tests`, and make sure the pull request describes the change in your own words.
