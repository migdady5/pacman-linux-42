*This activity has been created as part of the 42 curriculum by amigdadi, oaldalgm.*

# Pac-Man

## Description

A Python arcade game with ten growing maze levels, four autonomous ghosts, power pellets, a persistent top-ten leaderboard, pause controls, and reviewer cheats. The first 15×15 maze is seeded; every level grows, and later mazes are generated anew. Ghosts start slower and reach normal speed by level ten. The game uses the assigned A-Maze-ing package unchanged.

## Instructions

Use Python 3.10 or newer. The repository includes the original assigned wheel in `vendor/`. From the repository root:

```bash
make install
make run
```

Alternatively, run `python3 pac-man.py config.json`. The program takes exactly one JSON configuration path. Use arrow keys or WASD to move, `P` to pause, `Enter` to confirm, and `Esc` to return from secondary screens. In play, `C` toggles review cheat mode; when enabled, `I` toggles invincibility, `F` freezes ghosts, `L` adds a life, `K` skips a level, `+`/`-` changes player speed, and `R` resets effects.

For a prebuilt Linux x86-64 release, extract `pacman-linux-x86_64.zip` and run `./pacman/run-pacman.sh`. It contains the executable, images, editable configuration, and this README. No Python install is needed. Linux systems need a graphical desktop and the usual SDL system libraries. The game saves `highscores.json` beside its executable; the directory must be writable.

To build on Linux, run `make install` and `python3 package.py`. The output is `dist/linux/pacman/`. From Windows with Docker Desktop and a Linux-container backend, build an x86-64 release with:

```bash
docker run --rm --mount type=bind,source="$(pwd)",target=/work -w /work python:3.12-slim sh build_linux_container.sh
```

This creates `dist/pacman-linux-x86_64.zip`. To create a source release containing the unmodified wheel, run `python3 package_linux_source.py`; it creates `dist/pacman-linux-source.zip`. Packaging must run on the target OS: a Windows PyInstaller build is not a Linux executable. Run `make lint` for the prescribed checks.

## Configuration

`config.json` is JSON with optional `#`, `//`, or `/* ... */` comments outside strings. Missing, malformed, and invalid values warn and fall back to defaults; unknown keys are ignored.

| Key | Default | Meaning |
| --- | --- | --- |
| `highscore_filename` | `highscores.json` | Writable highscore JSON path |
| `levels` | Ten growing mazes, 15×15 to 25×23 | List of objects with odd `width` and `height` (minimum 11) |
| `lives` | `3` | Initial lives, minimum 1 |
| `pacgum` | `0` | `0` places a dot in every available corridor; positive values limit the count |
| `points_per_pacgum` | `10` | Points per regular dot |
| `points_per_super_pacgum` | `50` | Points per power pellet |
| `points_per_ghost` | `200` | Points per edible ghost |
| `seed` | `42` | Fixed first-level seed |
| `level_max_time` | `240` | Seconds per level, minimum 1 |
| `maze_package` | `mazegenerator` | Assigned external generator module |

Numeric values must be JSON integers. Invalid dimensions and even dimensions are adjusted to safe odd values. Super-pacgums occupy the nearest reachable cells to the four corners; regular pacgums fill every other available corridor except the player's starting cell when `pacgum` is `0`.

## Highscore

The leaderboard loads from JSON at startup, validates names (1–10 ASCII letters, digits, or spaces) and non-negative integer scores, sorts descending, and retains ten entries. A player enters a name after victory or defeat. JSON keeps the board human-readable without a service or account. Missing or invalid files start an empty board; failed writes warn instead of crashing.

## Maze Generation

`src/maze_adapter.py` calls the unmodified assigned `mazegenerator.MazeGenerator(size=(width, height), perfect=False, seed=...)` and reads its `maze` edge-bit grid. The adapter validates dimensions, reciprocal wall edges, outer borders, and connectivity before passing a normalized `GameMaze` to the game. Generation errors are reported cleanly. The first level uses the configured seed; later levels use random seeds.

## Implementation

The loop updates player and ghosts in small time steps to avoid missed collisions. Normal ghosts pursue the player; edible ghosts flee, then respawn after being eaten. Dots and edible ghosts add configurable points. Lives and score persist between levels. A level ends when all collectibles are eaten or the reviewer skips it. Time expiry restarts the level, costing one life unless invincibility is enabled. The final level leads to victory and name entry.

## General Software Architecture

`pac-man.py` loads configuration and starts `src/game.py`'s state machine. `src/config.py` validates input. `src/maze_adapter.py` isolates the external package; `src/level.py` places the player, ghosts, and collectibles. `src/entities.py` owns movement and ghost state. `src/assets.py` and `src/ui.py` render sprites, HUD, menus, and end screens. `src/highscore.py` handles leaderboard persistence. `package.py` creates a PyInstaller folder with editable assets and configuration.

## Project Management

The [project-management directory](project-management/) records the plan, technical choices, risks, and acceptance checks.

## Resources

- [Python documentation](https://docs.python.org/3/)
- [Pygame CE documentation](https://pyga.me/docs/)
- [PyInstaller documentation](https://pyinstaller.org/en/stable/)
- The assigned `mazegenerator` wheel, supplied by the activity, is used without modification.

AI assistance was used to review the specification, diagnose Python 3.10 and configuration defects, integrate the assigned wheel, prepare Linux packaging and documentation, and suggest validation checks. Game behavior and releases must still be verified by the authors during review.
