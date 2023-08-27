import ai_engine
import chess_engine
from enums import Player
from Piece import Knight
from enums import Player
from unittest.mock import Mock
from Piece import Knight, Rook, Bishop, Queen, Pawn, King
from chess_engine import game_state

import unittest



class TestKnightMethods(unittest.TestCase):

    def test_get_valid_peaceful_moves_empty_board(self):
        game_state_1 = Mock()

        knight = Mock()
        knight.get_valid_peaceful_moves.return_value = []

        game_state_1.board = [[(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()]]

        moves = knight.get_valid_peaceful_moves(game_state_1)

        assert moves == []

    def test_get_valid_peaceful_moves_blocking_positions(self):
        game_state_1 = Mock()

        knight = Mock()
        knight.get_valid_peaceful_moves.return_value = []

        game_state_1.board = [[knight, (), (), (), (), (), (), ()],
                              [(), (), Rook, (), (), (), (), ()],
                              [(), Rook, (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()]]

        moves = knight.get_valid_peaceful_moves(game_state_1)

        assert moves == []

    def test_get_valid_peaceful_moves_normal_test(self):
        game_state_1 = Mock()

        knight = Mock()
        knight.get_valid_peaceful_moves.return_value = [(6,8),(8,6)]

        game_state_1.board = [[(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), knight]]

        moves = knight.get_valid_peaceful_moves(game_state_1)

        assert moves == [(6,8),(8,6)]

    def test_get_valid_piece_takes_catching_pawn(self):
        game_state_1 = Mock()

        knight = Mock()
        knight.get_valid_piece_takes.return_value = [(3,2),(2,3)]

        game_state_1.board = [[knight, (), (), (), (), (), (), ()],
                              [(), (), Pawn, (), (), (), (), ()],
                              [(), Pawn, (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()]]

        assert knight.get_valid_piece_takes(game_state_1) == [(3,2),(2,3)]

    def test_get_valid_piece_takes_catching(self):
        game_state_1 = Mock()

        knight = Mock()
        knight.get_valid_piece_takes.return_value = [(2, 5), (6, 3)]

        game_state_1.board = [[(), (), (), (), (), (), (), ()],
                              [(), (), (), (), Rook, (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), knight, (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), Bishop, (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()]]
        assert knight.get_valid_piece_takes(game_state_1) == [(2, 5), (6, 3)]

    def test_get_valid_piece_takes_no_one_to_catch(self):
        game_state_1 = Mock()

        knight = Mock()
        knight.get_valid_piece_takes.return_value = []

        game_state_1.board = [[knight, (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()],
                              [(), (), (), (), (), (), (), ()]]

        assert knight.get_valid_piece_takes(game_state_1) == []





if __name__ == '__main__':
    unittest.main()