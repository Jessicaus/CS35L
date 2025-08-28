from test_main import TestChorusLapilli

from selenium.webdriver.common.by import By

class TestCustom(TestChorusLapilli):
    def test_new_board_empty(self):
        '''Check if a new game always starts with an empty board.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        self.assertBoardEmpty(tiles)

    def test_button_click(self):
        '''Check if clicking the top-left button adds an X.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        self.assertTileIs(tiles[0], self.SYMBOL_BLANK)
        tiles[0].click()
        self.assertTileIs(tiles[0], self.SYMBOL_X)
    
    def test_alternate_button_click(self):
        '''Check if clicking the top-left button adds an X.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        self.assertTileIs(tiles[0], self.SYMBOL_BLANK)
        tiles[0].click()
        self.assertTileIs(tiles[0], self.SYMBOL_X)
        tiles[1].click()
        self.assertTileIs(tiles[1], self.SYMBOL_O)
    
    def test_player_win(self):
        '''Check if player can still move after one Player has won the game.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        tiles[0].click() # X
        tiles[1].click() # O
        tiles[4].click() # X
        tiles[3].click() # O
        tiles[8].click() # X won
        tiles[2].click()
        expected = [
            'X', 'O', '',
            'O', 'X', '',
            '', '', 'X'
        ]
        self.assertBoardState(tiles, expected)
    
    def test_valid_adjacent_move(self):
        '''After 3 pieces placed, player can move one piece to an adjacent empty tile.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)

        # X and O take turns placing 3 each
        tiles[0].click()  # X
        tiles[1].click()  # O
        tiles[3].click()  # X
        tiles[2].click()  # O
        tiles[8].click()  # X (X now has 3)
        tiles[5].click()  # O (O now has 3)

        # X moves piece from 8 → 7
        tiles[8].click()  # select piece
        tiles[7].click()  # move to adjacent empty square

        expected = [
            'X', 'O', 'O',
            'X', '', 'O',
            '', 'X', ''
        ]
        self.assertBoardState(tiles, expected)
    
    def test_center_cannot_move(self):
        '''Player cannot move any other tile because their center tile is still occupied and next move is not a winning move.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        tiles[3].click()  # X
        tiles[1].click() # O
        tiles[4].click() # x
        tiles[5].click() # O
        tiles[8].click() # x
        tiles[0].click() # O

        tiles[8].click()  # select piece
        tiles[7].click()  # failed to move to adjacent empty square

        expected = [
            'O', 'O', '',
            'X', 'X', 'O',
            '', '', 'X'
        ]
        self.assertBoardState(tiles, expected)

        tiles[4].click()  # select center piece
        tiles[3].click() # select another piece
        tiles[6].click() # failed to move to adjacent empty square
        expected = [
            'O', 'O', '',
            'X', 'X', 'O',
            '', '', 'X'
        ]
        self.assertBoardState(tiles, expected)

        tiles[4].click()
        tiles[2].click() # moved successfully
        expected = [
            'O', 'O', 'X',
            'X', '', 'O',
            '', '', 'X'
        ]
        self.assertBoardState(tiles, expected)

        tiles[4].click() # nothing happens
        tiles[0].click()
        tiles[4].click() # move to center
        expected = [
            '', 'O', 'X',
            'X', 'O', 'O',
            '', '', 'X'
        ]
        self.assertBoardState(tiles, expected)

        tiles[8].click()
        tiles[7].click()
        expected = [
            '', 'O', 'X',
            'X', 'O', 'O',
            '', 'X', ''
        ]
        self.assertBoardState(tiles, expected)

        tiles[5].click()
        tiles[6].click() #nothing happens
        tiles[5].click()
        tiles[8].click() #nothing happens
        expected = [
            '', 'O', 'X',
            'X', 'O', 'O',
            '', 'X', ''
        ]
        self.assertBoardState(tiles, expected)
        
        tiles[4].click()
        tiles[0].click()
        expected = [
            'O', 'O', 'X',
            'X', '', 'O',
            '', 'X', ''
        ]
        self.assertBoardState(tiles, expected)

    def test_can_win_from_center(self):
        '''Player may keep center if their move completes a win.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)

        # X at 0, 4 (center), and moves 8 → 7 to win via 0-4-7 (diagonal down-left)
        tiles[1].click()  # X
        tiles[3].click()  # O
        tiles[5].click()  # X (center)
        tiles[4].click()  # O
        tiles[2].click()  # X
        tiles[7].click()  # O

        # X moves 1 → 0 and wins
        tiles[1].click()
        tiles[0].click()

        expected = [
            'X', '', 'X',
            'O', 'O', 'X',
            '', 'O', ''
        ]
        self.assertBoardState(tiles, expected)

        tiles[3].click() # not selecting center
        tiles[1].click() # completes win
        expected = [
            'X', 'O', 'X',
            '', 'O', 'X',
            '', 'O', ''
        ]
        self.assertBoardState(tiles, expected)
