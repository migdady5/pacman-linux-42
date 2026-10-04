# Acceptance tests

## Review on 2026-10-04

Verified on Windows with Python 3.12.14 and pygame-ce 2.5.8:

- `python -m flake8 .` and `python -m mypy . --strict` passed.
- Ten headless behavioral tests passed, including 30 generated mazes,
  movement against walls, edible-ghost scoring, life loss, timeout,
  all ten level transitions, menus, cheats, and persistent scores.
- `python package.py` built a Windows executable. A three-second
  dummy-display startup check completed without an early process exit.
- Menu and gameplay renders were inspected. Resource paths now work
  relative to the source root or packaged executable; the HUD fully
  hides decorative scores in the background image.
- The missing `build_linux_container.sh` was restored, but its Linux
  build was not run in this review because Docker was unavailable.

The older Linux results below are historical records, not newly verified
results for this revision. Manual Linux playtesting, MLX equivalence,
and itch.io publication remain outstanding.

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

Automated checks do not replace a full manual playthrough on the target Linux desktop. The GitHub ZIP is a downloadable build, but GitHub alone does not fulfill the gaming-platform requirement.
