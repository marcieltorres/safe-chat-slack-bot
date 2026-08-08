# AGENTS.md

Guidance for AI coding agents working on this repository. Human contributors should read
[CONTRIBUTING.md](CONTRIBUTING.md) and [README.md](README.md) first — this file is the condensed,
machine-facing version.

## Project overview

SafeChat Slack Bot is a Slack bot (Slack Bolt, Socket Mode) that detects PII — Brazilian CPF, email
addresses and Brazilian phone numbers — in channel messages and replies in-thread asking the author
not to share sensitive data. Python 3.11, Poetry, Docker-first, i18n via gettext.

## Repo layout

```
src/bot.py                              entrypoint: builds AsyncApp, starts AsyncSocketModeHandler
src/listeners/register.py               registers every listener
src/listeners/messages/regex_message.py new messages matching the compiled pattern
src/listeners/messages/message_changed.py  edited messages (subtype message_changed)
src/rules/constants.py                  the regex patterns
src/rules/pattern.py                    Pattern singleton: compiles the rules, find_all(text) -> int
src/config/settings.py                  settings.conf + ENV via ConfigParser
src/config/language.py                  gettext wrapper: language.translate(msgid)
src/locales/{en,pt_BR}/LC_MESSAGES/base.po  translations
tests/                                  mirrors src/
```

## Setup

Prerequisites: Python 3.11, Docker + Docker Compose, `gettext` (provides `msgfmt`), Poetry.

- `make docker/install` — recommended, and what CI runs.
- `make local/install` — local Poetry install.

Both targets create `.env` from [env.template](env.template) if absent and compile the `.mo` files.
`.env` and `*.mo` are gitignored and must stay that way — never commit either.

## Commands

| Task | Docker (canonical) | Local |
| --- | --- | --- |
| install | `make docker/install` | `make local/install` |
| tests | `make docker/test` | `make local/tests` |
| lint | `make docker/lint` | `make local/lint` |
| lint + autofix | `make docker/lint/fix` | `make local/lint/fix` |
| run | `make docker/run` | `make local/run` |
| compile translations | `make generate-mo-files` | `make generate-mo-files` |

CI ([`.github/workflows/pull_request.yml`](.github/workflows/pull_request.yml)) runs
`make docker/install` → `make docker/lint` → `make docker/test`. See the [Makefile](Makefile) for
every target.

## Code style

Ruff, configured in [pyproject.toml](pyproject.toml): `line-length = 120`, `target-version = py311`,
4-space indent, double quotes. Lint rules: `E`, `F`, `W` (pycodestyle/pyflakes), `I` (isort),
`N` (pep8-naming), `S` (flake8-bandit). Run `make local/lint/fix` before committing.

Project ethos from [CONTRIBUTING.md](CONTRIBUTING.md): be pythonic, DRY, KISS.

## Testing

`pytest` with `testpaths = ["tests"]` and `pythonpath = ["src"]`.

- Tests in this repo are `unittest.TestCase` / `IsolatedAsyncioTestCase` classes with
  `unittest.mock` (`AsyncMock`, `MagicMock`, `patch`) — **not** bare pytest functions. Follow the
  existing style.
- Name tests for the behaviour they assert, e.g. `test_if_text_can_be_a_cpf_with_success`.
- Coverage runs in branch mode with **`fail_under = 100`** (`src/bot.py` omitted). New code without
  tests breaks the build.
- `pytest-asyncio` is installed but no `asyncio_mode` is configured — write async tests with
  `IsolatedAsyncioTestCase`.

## Adding a detection rule

1. Add the regex to `src/rules/constants.py`.
2. Append it to `self.rules` in `Pattern.__init__` (`src/rules/pattern.py`).
3. Add positive **and** negative cases to `tests/rules/test_pattern.py`.

Watch for over-matching: the rules are joined with `|` into one pattern, and the current CPF regex
matches any run of 11 digits — a phone number counts as a CPF. Assert exact `find_all` counts.

## Internationalization

User-facing strings must go through `language.translate("...")`. Add the msgid to **both**
`src/locales/en/LC_MESSAGES/base.po` and `src/locales/pt_BR/LC_MESSAGES/base.po`, then run
`make generate-mo-files`. Adding a new locale also requires a `msgfmt` line in the
[Dockerfile](Dockerfile).

## Commits and pull requests

- Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`,
  `chore:`, `refactor:`, `test:`. (History predates this convention and is inconsistent — follow the
  convention going forward.)
- **Never add `Co-Authored-By` lines or any AI / "Generated with" attribution** to commits or PR
  bodies.
- Never commit directly to `main` — always work on a branch.
- An issue must exist before a PR (see the [pull request template](.github/PULL_REQUEST_TEMPLATE)).
  Reference it with `closes #NN`.
- Make sure lint and tests pass locally before opening the PR.

## Releases

The tag and the GitHub Release are created automatically by
[`.github/workflows/release.yml`](.github/workflows/release.yml) when a version without a tag lands
on `main`. [CONTRIBUTING.md](CONTRIBUTING.md) has the full process.

- **Never create a tag or a GitHub Release by hand** — the workflow owns both.
- Tags are plain `X.Y.Z`, without a `v` prefix, always derived from `tool.poetry.version` in
  [pyproject.toml](pyproject.toml).
- A PR that changes the bot's behaviour must bump `version` in `pyproject.toml` **and** add the
  matching `## [X.Y.Z] - YYYY-MM-DD` section to [CHANGELOG.md](CHANGELOG.md). Without both, the
  release never fires.
- A PR that only touches dependencies, docs or CI does not bump the version.
- The release notes are the changelog section verbatim, so the section must not be empty — the
  workflow fails loudly if it is missing or blank.

## Security

This bot handles credentials and PII by definition. Treat these as hard rules:

- `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN` come from environment variables only. Never hardcode a
  token, never log one, and never paste a real value into docs, tests or fixtures — reference
  [env.template](env.template) and the variable names instead.
- **Never log raw message text or matched PII.** Listeners log exceptions only; keep it that way.
- Do not suppress Ruff `S` (bandit) findings with `# noqa` without a written justification.
- Changes to scopes in [manifest.json](manifest.json) are security-relevant — call them out
  explicitly in the pull request.
- Report vulnerabilities through [SECURITY.md](SECURITY.md), not a public issue.
