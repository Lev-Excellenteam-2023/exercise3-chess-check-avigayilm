#
# The GUI engine for Python Chess
#
# Author: Boo Sung Kim, Eddie Sharick
# Note: The pygame tutorial by Eddie Sharick was used for the GUI engine. The GUI code was altered by Boo Sung Kim to
# fit in with the rest of the project.
#
import chess_engine
import pygame as py
import logging
import colorlog

import ai_engine
from enums import Player

"""Variables"""
WIDTH = HEIGHT = 512  # width and height of the chess board
DIMENSION = 8  # the dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board
MAX_FPS = 15  # FPS for animations
IMAGES = {}  # images for the chess pieces
colors = [py.Color("white"), py.Color("gray")]

# TODO: AI black has been worked on. Mirror progress for other two modes
def load_images():
    '''
    Load images for the chess pieces
    '''
    for p in Player.PIECES:
        IMAGES[p] = py.transform.scale(py.image.load("images/" + p + ".png"), (SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, game_state, valid_moves, square_selected):
    ''' Draw the complete chess board with pieces

    Keyword arguments:
        :param screen       -- the pygame screen
        :param game_state   -- the state of the current chess game
    '''
    draw_squares(screen)
    highlight_square(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state)


def draw_squares(screen):
    ''' Draw the chess board with the alternating two colors

    :param screen:          -- the pygame screen
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            py.draw.rect(screen, color, py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, game_state):
    ''' Draw the chess pieces onto the board

    :param screen:          -- the pygame screen
    :param game_state:      -- the current state of the chess game
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = game_state.get_piece(r, c)
            if piece is not None and piece != Player.EMPTY:
                screen.blit(IMAGES[piece.get_player() + "_" + piece.get_name()],
                            py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_square(screen, game_state, valid_moves, square_selected):
    if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]):
        row = square_selected[0]
        col = square_selected[1]

        if (game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_1)) or \
                (not game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_2)):
            # hightlight selected square
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(py.Color("blue"))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

            # highlight move squares
            s.fill(py.Color("green"))

            for move in valid_moves:
                screen.blit(s, (move[1] * SQ_SIZE, move[0] * SQ_SIZE))


def main():


    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        log_colors={
            'DEBUG': 'green',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red'
        }))

    # Create a logger object
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG
    logger.addHandler(handler)

    # Log some messages
    # logger.debug('This is a debug message')
    # logger.info('This is an info message')
    # logger.warning('This is a warning message')
    # logger.error('This is an error message')
    # logger.critical('This is a critical message')

    # Check for the number of players and the color of the AI

    human_player = ""
    while True:
        try:
            number_of_players = input("How many players (1 or 2)?\n")
            if int(number_of_players) == 1:
                number_of_players = 1
                while True:
                    human_player = input("What color do you want to play (w or b)?\n")
                    if human_player is "w" or human_player is "b":
                        break
                    else:
                        print("Enter w or b.\n")
                break
            elif int(number_of_players) == 2:
                number_of_players = 2
                #logger.info('Two players are using the game')
                break
            else:
                print("Enter 1 or 2.\n")
        except ValueError:
            print("Enter 1 or 2.")

    py.init()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    game_state = chess_engine.game_state()
    load_images()
    running = True
    square_selected = ()  # keeps track of the last selected square
    player_clicks = []  # keeps track of player clicks (two tuples)
    valid_moves = []
    game_over = False

    ai = ai_engine.chess_ai()
    game_state = chess_engine.game_state()
    if human_player is 'b':
        #def minimax_white(self, game_state, depth, alpha, beta, maximizing_player, player_color):
        # returns the best move ((row, col), so on place[0]= row, and [1]=column
        ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)
        game_state.move_piece(ai_move[0], ai_move[1], True)


#now it is human turn
    while running:
        for e in py.event.get():
            # if the player clicks the window's close button
            if e.type == py.QUIT:
                # set the running variable to False to exit the loop and end the game
                running = False
            # if the player clicks the mouse button
            elif e.type == py.MOUSEBUTTONDOWN:
                # if the game is not over
                if not game_over:
                    # get the coordinates of the mouse click
                    location = py.mouse.get_pos()
                    # calculate the row and column of the clicked square on the chessboard
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    # if the player clicks on the same square twice
                    #becuase it checks if he newly clicked qured is he same as tthe square
                    #that the player had previously selected.
                    if square_selected == (row, col):
                        # if pressed twice the squre selecttted is deseleced.
                        square_selected = ()
                        player_clicks = []
                    # if the player clicks on a different square
                    else:
                        # set the square_selected variable to the new square
                        square_selected = (row, col)
                        # add the new square to the player_clicks list
                        player_clicks.append(square_selected)
                    # if the player has clicked on two squares
                    if len(player_clicks) == 2:
                        # if the second square is not a valid move for the selected piece
                        if (player_clicks[1][0], player_clicks[1][1]) not in valid_moves:
                            # reset the square_selected, player_clicks, and valid_moves variables
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []
                        # if the second square is a valid move for the selected piece
                        else:
                            # move the piece on the game_state object
                            game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
                                                  (player_clicks[1][0], player_clicks[1][1]), False)
                            # reset the square_selected, player_clicks, and valid_moves variables
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []

                            print("hi")

                            # if it is the human player's turn
                            if human_player is 'w':
                                # call the minimax_white function of the ai object to get the AI player's move
                                #player 2 is black
                                ai_move = ai.minimax_white(game_state, 3, -100000, 100000, True, Player.PLAYER_2)
                                # execute the AI player's move on the game_state object
                                game_state.move_piece(ai_move[0], ai_move[1], True)
                            elif human_player is 'b':
                                # call the minimax_black function of the ai object to get the AI player's move
                                ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)
                                # execute the AI player's move on the game_state object
                                game_state.move_piece(ai_move[0], ai_move[1], True)
                    # if no piece is currently selected
                    else:
                        # get a list of valid moves for the clicked square from the game_state object
                        valid_moves = game_state.get_valid_moves((row, col))
                        # if there are no valid moves for the clicked square
                        if valid_moves is None:
                            # set the valid_moves variable to an empty list
                            valid_moves = []

                    endgame = game_state.checkmate_stalemate_checker()
                    print(endgame)
                    if endgame == 0:
                        game_over = True
                        draw_text(screen, "Black wins.")
                    elif endgame == 1:
                        game_over = True
                        draw_text(screen, "White wins.")
                    elif endgame == 2:
                        game_over = True
                        draw_text(screen, "Stalemate.")

                # if the game is over you should break fromm tthe loop
                else:
                    break
            elif e.type == py.KEYDOWN:
                # checks if the key pressed is the "r" key. If it is, the game is reset by setting various game-related variables to their initial state.
                if e.key == py.K_r:
                    game_over = False
                    game_state = chess_engine.game_state()
                    valid_moves = []
                    square_selected = ()
                    player_clicks = []
                    valid_moves = []
                #If it is, the last move made in the game is undone by calling the undo_move()
                elif e.key == py.K_u:
                    game_state.undo_move()
                    print(len(game_state.move_log))



        #end of for loop

        draw_game_state(screen, game_state, valid_moves, square_selected)
        # checks if the game ended by checking if there is no possible moves but not by checking if the king is capttured....




        clock.tick(MAX_FPS)
        py.display.flip()

    # elif human_player is 'w':
    #     ai = ai_engine.chess_ai()
    #     game_state = chess_engine.game_state()
    #     valid_moves = []
    #     while running:
    #         for e in py.event.get():
    #             if e.type == py.QUIT:
    #                 running = False
    #             elif e.type == py.MOUSEBUTTONDOWN:
    #                 if not game_over:
    #                     location = py.mouse.get_pos()
    #                     col = location[0] // SQ_SIZE
    #                     row = location[1] // SQ_SIZE
    #                     if square_selected == (row, col):
    #                         square_selected = ()
    #                         player_clicks = []
    #                     else:
    #                         square_selected = (row, col)
    #                         player_clicks.append(square_selected)
    #                     if len(player_clicks) == 2:
    #                         if (player_clicks[1][0], player_clicks[1][1]) not in valid_moves:
    #                             square_selected = ()
    #                             player_clicks = []
    #                             valid_moves = []
    #                         else:
    #                             game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
    #                                                   (player_clicks[1][0], player_clicks[1][1]), False)
    #                             square_selected = ()
    #                             player_clicks = []
    #                             valid_moves = []
    #
    #                             ai_move = ai.minimax(game_state, 3, -100000, 100000, True, Player.PLAYER_2)
    #                             game_state.move_piece(ai_move[0], ai_move[1], True)
    #                     else:
    #                         valid_moves = game_state.get_valid_moves((row, col))
    #                         if valid_moves is None:
    #                             valid_moves = []
    #             elif e.type == py.KEYDOWN:
    #                 if e.key == py.K_r:
    #                     game_over = False
    #                     game_state = chess_engine.game_state()
    #                     valid_moves = []
    #                     square_selected = ()
    #                     player_clicks = []
    #                     valid_moves = []
    #                 elif e.key == py.K_u:
    #                     game_state.undo_move()
    #                     print(len(game_state.move_log))
    #         draw_game_state(screen, game_state, valid_moves, square_selected)
    #
    #         endgame = game_state.checkmate_stalemate_checker()
    #         if endgame == 0:
    #             game_over = True
    #             draw_text(screen, "Black wins.")
    #         elif endgame == 1:
    #             game_over = True
    #             draw_text(screen, "White wins.")
    #         elif endgame == 2:
    #             game_over = True
    #             draw_text(screen, "Stalemate.")
    #
    #         clock.tick(MAX_FPS)
    #         py.display.flip()
    #
    # elif human_player is 'b':
    #     pass


def draw_text(screen, text):
    font = py.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, False, py.Color("Black"))
    text_location = py.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                      HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)


if __name__ == "__main__":
    main()
