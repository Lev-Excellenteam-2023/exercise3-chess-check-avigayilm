import unittest
from ai_engine import chess_ai
from unittest import TestCase
from unittest.mock import Mock
import chess_engine

class Sys_test (TestCase):

    def test_system_tst(self):
        game = chess_engine.game_state()
        game.move_piece((0, 0), (2, 0), True)
        game.move_piece((6, 3), (4, 3), True)
        game.move_piece((1, 1), (3, 1), True)
        game.move_piece((7, 4), (5, 2), True)
        assert game.checkmate_stalemate_checker() == 3
