import unittest
from ai_engine import chess_ai
from unittest import TestCase
from unittest.mock import Mock
import chess_engine
from enums import Player
from Piece import Knight

import ai_engine

class Integration_test (TestCase):
    knight = Knight('n', 3, 4, Player.PLAYER_1)

    def test_get_valid_piece_moves(self):
        game_state = Mock()
        game_state.get_piece = Mock(return_value=Player.EMPTY)
        game_state.is_valid_piece = Mock(return_value=False)
        assert self.knight.get_valid_piece_moves(game_state) == [(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 5),(5,3)]

