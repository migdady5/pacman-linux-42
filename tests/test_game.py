"""Behavioral checks runnable without a graphical desktop."""
from __future__ import annotations

import json
import os
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402

from src.assets import resource_root  # noqa: E402
from src.config import load_config  # noqa: E402
from src.entities import GhostState, Player, RIGHT  # noqa: E402
from src.game import Game, State  # noqa: E402
from src.highscore import HighscoreManager  # noqa: E402
from src.level import Level  # noqa: E402
from src.maze_adapter import GenerationError, generate_maze  # noqa: E402


class GameChecks(unittest.TestCase):
    """Exercise gameplay state transitions and persistence."""

    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.config = load_config("config.json")
        self.config["highscore_filename"] = str(
            Path(self.directory.name) / "scores.json")
        self.game = Game(self.config)

    def tearDown(self) -> None:
        pygame.quit()
        self.directory.cleanup()

    def test_levels_and_collectibles(self) -> None:
        previous_area = 0
        for spec in self.config["levels"]:
            for seed in (1, 42, 99):
                maze = generate_maze(**spec, seed=seed)
                level = Level(maze, 0, random.Random(seed))
                cells = {(x, y) for y in range(maze.height)
                         for x in range(maze.width)} - maze.blocked_cells
                self.assertEqual(len(level.super_pacgums), 4)
                self.assertFalse(level.pacgums & level.super_pacgums)
                self.assertEqual(level.pacgums | level.super_pacgums,
                                 cells - {level.player_start})
                self.assertEqual(len(level.ghosts), 4)
            area = spec["width"] * spec["height"]
            self.assertGreater(area, previous_area)
            previous_area = area

    def test_seed_and_missing_generator(self) -> None:
        self.assertEqual(generate_maze(15, 15, 42).edges,
                         generate_maze(15, 15, 42).edges)
        with self.assertRaises(GenerationError):
            generate_maze(15, 15, package_name="missing_maze_package")

    def test_movement_respects_walls(self) -> None:
        maze = generate_maze(15, 15, 42)
        for y in range(maze.height):
            for x in range(maze.width):
                if (x, y) in maze.blocked_cells:
                    continue
                player = Player(x, y)
                player.set_direction(RIGHT)
                player.advance(maze, 0.5, 1.0)
                self.assertEqual((player.x, player.y), (x, y))
                player.advance(maze, 0.5, 1.0)
                expected = x + int(maze.can_move(x, y, 1, 0))
                self.assertEqual((player.x, player.y), (expected, y))

    def test_menus_pause_and_cheats(self) -> None:
        self.game._render()
        self.game._handle_menu_key(pygame.K_DOWN)
        self.game._handle_menu_key(pygame.K_RETURN)
        self.assertEqual(self.game.state, State.HIGHSCORES)
        self.game._render()
        self.game.state = State.INSTRUCTIONS
        self.game._render()
        self.game.start_new_game()
        self.game._handle_playing_key(pygame.K_p)
        self.assertEqual(self.game.state, State.PAUSED)
        self.game._render()
        self.game._handle_pause_key(pygame.K_p)
        self.game._handle_playing_key(pygame.K_c)
        for key in (pygame.K_i, pygame.K_f, pygame.K_PLUS):
            self.game._handle_playing_key(key)
        self.assertTrue(self.game.invincible)
        self.assertTrue(self.game.ghosts_frozen)
        self.game._handle_playing_key(pygame.K_c)
        self.assertFalse(self.game.invincible)
        self.assertFalse(self.game.ghosts_frozen)
        self.assertEqual(self.game.speed_multiplier, 1.0)

    def test_collision_and_edible_scoring(self) -> None:
        self.game.start_new_game()
        assert self.game.level is not None
        assert self.game.player is not None
        ghost = self.game.level.ghosts[0]
        ghost.x, ghost.y = self.game.player.x, self.game.player.y
        ghost.make_edible(7)
        self.game._handle_ghost_collisions()
        self.assertEqual(self.game.score, 200)
        self.assertEqual(ghost.state, GhostState.EATEN)
        self.game._handle_ghost_collisions()
        self.assertEqual(self.game.score, 200)
        ghost.state = GhostState.CHASE
        self.game._handle_ghost_collisions()
        self.assertEqual(self.game.lives, 2)

    def test_pellets_and_power(self) -> None:
        self.game.start_new_game()
        assert self.game.level is not None
        assert self.game.player is not None
        self.game.player.x, self.game.player.y = next(
            iter(self.game.level.pacgums))
        self.game._handle_collectibles()
        self.game._handle_collectibles()
        self.assertEqual(self.game.score, 10)
        self.game.player.x, self.game.player.y = next(
            iter(self.game.level.super_pacgums))
        self.game._handle_collectibles()
        self.assertEqual(self.game.score, 60)
        self.assertTrue(all(g.state == GhostState.EDIBLE
                            for g in self.game.level.ghosts))

    def test_timeout_and_completion(self) -> None:
        self.game.start_new_game()
        self.game.time_left = 0.001
        self.game._update_playing(0.02)
        self.assertEqual(self.game.lives, 2)
        self.game.invincible = True
        self.game.ghosts_frozen = True
        for _ in self.config["levels"]:
            assert self.game.level is not None
            self.game._render()
            self.game.level.pacgums.clear()
            self.game.level.super_pacgums.clear()
            self.game._update_playing(0.02)
        self.assertEqual(self.game.state, State.ENTER_NAME)
        self.assertTrue(self.game.victory)
        self.game._render()
        self.game._handle_name_key(pygame.event.Event(
            pygame.KEYDOWN, key=pygame.K_RETURN, unicode="\r"))
        self.assertEqual(self.game.state, State.VICTORY)
        self.assertTrue(Path(self.config["highscore_filename"]).exists())

    def test_highscore_validation_and_errors(self) -> None:
        path = Path(self.directory.name) / "board.json"
        path.write_text('{broken', encoding="utf-8")
        board = HighscoreManager(str(path))
        self.assertEqual(board.top(), [])
        for number in range(15):
            board.add_score("Ali", number)
        self.assertEqual(len(HighscoreManager(str(path)).top()), 10)
        self.assertEqual(board.top()[0]["score"], 14)
        path.write_text(json.dumps([{"name": "Ali", "score": True}]))
        self.assertEqual(HighscoreManager(str(path)).top(), [])
        board.filename = self.directory.name
        board.save()

    def test_config_comments_defaults_and_types(self) -> None:
        path = Path(self.directory.name) / "config.json"
        path.write_text('{"lives": true, /* comment */ "seed": 9, '
                        '"highscore_filename": "https://x/#y"}')
        config = load_config(str(path))
        self.assertEqual(config["lives"], 3)
        self.assertEqual(config["seed"], 9)
        self.assertEqual(config["highscore_filename"], "https://x/#y")
        path.write_text("[]")
        self.assertEqual(load_config(str(path))["lives"], 3)

    def test_packaged_resource_location(self) -> None:
        with patch("sys.frozen", True, create=True):
            with patch("sys.executable", str(
                    Path(self.directory.name) / "pacman.exe")):
                self.assertEqual(resource_root(), Path(self.directory.name))

    def test_eaten_ghost_has_eyes_not_live_body(self) -> None:
        image = self.game.assets.ghost_image('green', RIGHT, False,
                                             eaten=True)
        self.assertEqual(image.get_at((0, 0)).a, 0)
        self.assertEqual(image.get_at((image.get_width() // 3,
                                      image.get_height() // 2)).a, 255)

    def test_eaten_ghost_returns_once_without_duplication(self) -> None:
        self.game.start_new_game()
        assert self.game.level is not None
        level = self.game.level
        ghost = level.ghosts[0]
        ghost.x, ghost.y = level.player_start
        ghost.get_eaten(6)
        identities = [id(g) for g in level.ghosts]
        for _ in range(2000):
            ghost.update_timers(0.02)
            ghost.advance(level.maze, level.player_start,
                          random.Random(42), 0.02, 0.18)
            self.assertEqual([id(g) for g in level.ghosts], identities)
            if ghost.state == GhostState.CHASE:
                break
        self.assertEqual(ghost.state, GhostState.CHASE)
        self.assertEqual((ghost.x, ghost.y), (ghost.home_x, ghost.home_y))


if __name__ == "__main__":
    unittest.main()
