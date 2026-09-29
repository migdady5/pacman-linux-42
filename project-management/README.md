# Project management

- [Acceptance tests](acceptance-tests.md) records verified checks and open manual checks.
- [Decisions and risks](decisions-and-risks.md) records technical choices and remaining delivery risks.

## Plan and progress

| Phase | Deliverable | Status |
| --- | --- | --- |
| Requirements | Map the 42 PDF to game features | Reviewed |
| Core game | Menu, maze, entities, score, ten levels | Implemented |
| Compatibility | Python 3.10 syntax, configuration, assigned wheel | Corrected |
| Release | Linux PyInstaller folder and ZIP | Built and smoke-tested |
| Distribution | New source repository and private/unlisted gaming-platform build | GitHub uploaded; gaming platform pending |

## Choices

- Keep the assigned maze wheel unchanged and isolate its edge-bit format in an adapter.
- Use JSON for editable configuration and persistent highscores.
- Package with PyInstaller on Linux, rather than copying a Windows executable.
- Keep assets and configuration outside the executable so reviewers can inspect and edit them.

## Risks and mitigation

- Linux host library differences: test the packaged executable in a Linux container and on a graphical Linux desktop.
- Maze generator replacement during review: install the original assigned wheel via `make install`, keep the adapter isolated, and check maze validation.
- Invalid configuration or leaderboard files: warn and continue with safe defaults.
- Gaming-platform account access: keep the ZIP ready and publish as private/unlisted after account login is available.

## Acceptance checks

- Python 3.10 compilation succeeds.
- `make lint` succeeds with flake8 and required mypy flags.
- `make install` installs the assigned wheel as well as other dependencies.
- All ten levels can be generated; cheat skipping reaches the victory/name-entry screen.
- Invalid JSON and malformed highscore entries do not crash the game.
- Linux ZIP contains a runnable executable, launcher, assets, configuration, and README.

The project was handled by the repository authors with AI-assisted auditing, fixes, packaging, and documentation. Final graphical playtesting and publication are tracked separately.
