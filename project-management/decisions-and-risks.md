# Decisions and risks

## Design choices

- Keep the assigned A-Maze-ing wheel unchanged and translate its edge-bit format through `src/maze_adapter.py`.
- Use ten increasing odd-sized mazes, starting at 15×15 so the assigned generator can render its `42` pattern. Alternate width and height growth to keep the maximum window within 800×742 pixels.
- Place regular pacgums in every available corridor by default; keep `pacgum` configurable for review.
- Use a local JSON file for the top-ten leaderboard so scores persist without an account or server.
- Package a Linux executable on Linux with PyInstaller; keep configuration, assets, and brief instructions beside it.

## Open risks

| Risk | Mitigation or next action |
| --- | --- |
| Target distribution lacks a required SDL or font system library | Run the ZIP on the intended graphical Linux computer and install missing system packages if reported. |
| Gameplay takes too long or is too difficult in late levels | Manually play and adjust the level time or ghost speed if needed. Reviewer cheat controls allow rapid progression checks. |
| Leaderboard directory is read-only | Extract the ZIP into a writable user directory before running. |
| Assigned maze package is reinstalled during review | Keep the original wheel in `vendor/` and install it through `make install`. |
| Gaming-platform upload is missing | Publish the Linux ZIP as a free private/unlisted build and verify installation from that platform. |
| MLX equivalence is unverified | Audit each Pygame call against the permitted MLX feature set before peer review. |

The authors are responsible for the final graphical playtest and gaming-platform publication. AI assistance supported specification review, compatibility fixes, validation, packaging, and documentation.
