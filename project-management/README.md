# Project management

## Plan and progress

| Phase | Deliverable | Status |
| --- | --- | --- |
| Requirements | Map the 42 PDF to game features | Reviewed |
| Core game | Menu, maze, entities, score, ten levels | Implemented |
| Compatibility | Python 3.10 syntax, configuration, assigned wheel | Corrected |
| Release | Linux PyInstaller folder and ZIP | Built and smoke-tested |
| Distribution | Source repository and private/unlisted gaming-platform build | GitHub uploaded; gaming platform pending |

## Design choices

- Keep the assigned A-Maze-ing wheel unchanged and translate its edge-bit format through `src/maze_adapter.py`.
- Use ten increasing odd-sized mazes, starting at 15×15 so the assigned generator can render its `42` pattern. Alternate width and height growth to keep the maximum window within 800×742 pixels.
- Place regular pacgums in every available corridor by default; keep `pacgum` configurable for review.
- Use a local JSON file for the top-ten leaderboard so scores persist without an account or server.
- Package a Linux executable on Linux with PyInstaller; keep configuration, assets, and instructions beside it.

## Acceptance tests

| Requirement | Check | Result |
| --- | --- | --- |
| Python 3.10 compatibility | Compile all `src` modules and `pac-man.py` in Python 3.10 Linux | Passed |
| Clean installation | Run `make install` in a fresh Python 3.10 Linux container and import the assigned package | Passed |
| Coding rules | Run `flake8 .` and mypy with the prescribed flags | Passed |
| Maze progression | Generate all ten configured mazes; verify every level has a larger area | Passed |
| Collectibles | Check every playable cell except the start and four super-pacgum cells contains a regular pacgum | Passed |
| Game completion | Start a game and advance through ten levels; verify victory/name-entry state | Passed |
| Fault handling | Load malformed and incomplete configuration and leaderboard JSON | Passed |
| Linux package | Check ZIP contents, executable permissions, and headless startup in Linux | Passed |
| Full manual playthrough | Play using a graphical Linux desktop and check controls, collisions, pause, and highscores | Not yet verified |
| Gaming-platform delivery | Upload free, private/unlisted build to a public gaming platform | Not yet done |
| MLX-equivalent graphics calls | Check every Pygame call against the subject's MLX-equivalence rule | Not yet verified |

## Risks and next actions

| Risk | Mitigation or next action |
| --- | --- |
| Target distribution lacks a required SDL or font system library | Run the ZIP on the intended graphical Linux computer and install missing system packages if reported. |
| Late levels take too long or are too difficult | Manually play and adjust the level time or ghost speed if needed. Reviewer cheat controls allow rapid progression checks. |
| Leaderboard directory is read-only | Extract the ZIP into a writable user directory before running. |
| Assigned maze package is reinstalled during review | Keep the original wheel in `vendor/` and install it through `make install`. |
| Gaming-platform upload is missing | Publish the Linux ZIP as a free private/unlisted build and verify installation from that platform. |
| MLX equivalence is unverified | Audit each Pygame call against the permitted MLX feature set before peer review. |

Automated checks do not replace a full graphical playthrough. The GitHub ZIP is a downloadable build, but GitHub alone does not fulfill the gaming-platform requirement. The authors are responsible for final playtesting and publication. AI assistance supported specification review, compatibility fixes, validation, packaging, and documentation.
