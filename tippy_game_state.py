from game_state import GameState
from tippy_move import TippyMove
from strategy_minimax import StrategyMinimax
import copy


class TippyGameState(GameState):
    '''The state of a Tippy game. 
    
    grid (list) - A nested list representing a 2D grid
    
    'p1' (the user) always places 'x', 'p2' (the computer) places 'o'.
    '''
    
    def __init__(self, p, grid=[], interactive=False):
        '''(TippyGameState, str, list) -> NoneType
        
        Initialize a TippyGameState self with a grid.
        
        Pass in True for interactive to play the game.
        
        >>> t = TippyGameState("p1", True)
        NoneType
        '''
        GameState.__init__(self, p)
        self.instructions = ('Pick a row and column to place your x. '
                             'First player to form a Tippy wins! ')
        self.grid = grid
        if interactive:
            dimension = int(input("What dimension for the Tippy grid? "))
            for x in range(dimension):
                self.grid.append([None for i in range(dimension)])
        self.over = self.is_over()
    
    def __repr__(self):
        '''(TippyGameState) -> str
        
        Return TippyGameState self's constructor as evaluable string. 
        
        >>> t = TippyGameState('p1', grid=[[None, 'x', 'x'], ['o', 'o', None], 
                [None, None, None]])
        >>> t
        TippyGameState('p1', grid=[[None, 'x', 'x'], ['o', 'o', None], 
        [None, None, None]])
        '''
        return 'TippyGameState({}, {})'.format(self.next_player, self.grid)

    def __eq__(self, other):
        ''' (TippyGameState, TippyGameState) -> bool

        Return whether TippyGameState self is the same as other.

        >>> t1 = TippyGameState('p1', grid=[[None, 'x', 'x'], ['o', 'o', None], 
                 [None, None, None]])
        >>> t2 = TippyGameState('p1', grid=[[None, 'x', 'x'], ['o', 'o', None], 
                 [None, None, None]])
        >>> t1 == t2
        True
        '''
        return (isinstance(other, TippyGameState) and
                self.grid == other.grid and
                self.next_player == other.next_player)
        
    def __str__(self):
        '''(TippyGameState) -> str
        
        Return a user friendly string version of TippyGameState self. 
        
        >>> t = TippyGameState('p1', grid=[['x', 'x', 'o'], ['x', 'o', None], 
                [None, None, None]])
        >>> print(t)
        1: ['x', 'x', 'o']
        2: ['x', 'o', None]
        3: [None, None, None]
        Current player: p1
        '''
        grid = ''
        row_counter = 1
        for row in self.grid:
            grid = grid + '\n' + str(row_counter) + ': ' + str(row)
            row_counter += 1
        return (grid + '\n' + 'Current player: {}'.format(self.next_player) 
                + '\n')

    def get_move(self):
        '''(TippyGameState) -> TippyMove
        
        Return a move for a game of Tippy, based on user input.
        '''
        y = int(input("Pick a row: "))
        x = int(input("Pick a column: "))
        return TippyMove(x, y)
    
    def apply_move(self, move):
        ''' (TippyGameState, TippyMove) -> TippyGameState
       
        Return the new TippyGameState after TippyMove is applied.
       
        >>> t1 = TippyGameState('p1')
        >>> m1 = t1.apply_move(TippyMove(3, 1))
        >>> print(t1)
        1: [None, None, 'x']
        2: [None, None, None]
        3: [None, None, None]
        Current player: p2
        '''
        if move in self.possible_next_moves():
            #use a copy?
            new_grid = copy.deepcopy(self.grid)
            
            c = "x"
            if self.next_player == "p2":
                c = "o"
                
            new_grid[move.y - 1][move.x - 1] = c
            return TippyGameState(self.opponent(), grid=new_grid) 
        else:
            return None
            
    def possible_next_moves(self):
        '''(TippyGameState) -> list
        
        Return a list of legal Tippy moves from the current TippyGameState 
        self.
        
        >>> t = TippyGameState('p1')
        >>> t.grid=[['x', 'x', 'o'], ['x', 'o', 'o'], ['x', 'o', None]]
        >>> t.possible_next_moves()
        [TippyMove(1, 3)]
        '''
        legal_moves = []
        #check each row of the grid...
        for row_num in range(len(self.grid)):
            for column_num in range(len(self.grid[row_num])):
                y = row_num + 1
                x = column_num + 1
                #if there is no letter at position, append to legal_moves
                if (not self.grid[row_num][column_num] == 'x' 
                    and not self.grid[row_num][column_num] == 'o'):
                    legal_moves.append(TippyMove(x, y))
        return legal_moves
    
    def win(self):
        '''(TippyGameState) -> bool
        
        Return whether a game of Tippy has a winning sequence.
        
        >>> t = TippyGameState('p1')
        >>> t.grid=[['x', 'x', 'o'], ['o', 'x', 'x'], ['o', 'o', None]]
        >>> t.win()
        True
        '''
        #check to see how many letters have been placed on the grid
        letter_count = 0
        for row_num in range(len(self.grid)):
            for column_num in range(len(self.grid[row_num])):
                if (self.grid[row_num][column_num] == 'x' or 
                    self.grid[row_num][column_num] == 'o'):
                        letter_count += 1
        #if there are enough letters to win the game...
        if letter_count >= 7:
            #loop through the grid, and check for winning combinations
            for x in range(len(self.grid)):
                for y in range(len(self.grid)):
                    try:
                        if ((self.grid[x][y] == self.grid[x][y + 1] == 
                             self.grid[x + 1][y + 1] == 
                             self.grid[x + 1][y + 2])):
                            return True
                    except IndexError:
                        pass
                    try:
                        if ((self.grid[x][y + 1] == self.grid[x][y + 2] == 
                             self.grid[x + 1][y] == self.grid[x + 1][y + 1])):
                            return True
                    except IndexError:
                        pass
                    try:
                        if ((self.grid[x + 1][y] == self.grid[x + 1][y + 1] == 
                             self.grid[x + 2][y + 1] == 
                             self.grid[x + 2][y + 2])):
                            return True
                    except IndexError:
                        pass
                    try:
                        if ((self.grid[x + 1][y + 1] == 
                             self.grid[x + 1][y + 2] == 
                             self.grid[x + 2][y] == self.grid[x + 2][y + 1])):
                            return True
                    except IndexError:
                        pass
                    try:
                        if ((self.grid[x][y] == self.grid[x + 1][y] == 
                             self.grid[x + 1][y + 1] == 
                             self.grid[x + 2][y + 1])):
                            return True
                    except IndexError:
                        pass
                    try:
                        if ((self.grid[x][y + 1] == self.grid[x + 1][y + 1] == 
                             self.grid[x + 1][y + 2] == 
                             self.grid[x + 2][y + 2])):
                            return True
                    except IndexError:
                        pass
                    try:
                        if ((self.grid[x][y + 2] == self.grid[x + 1][y + 1] == 
                             self.grid[x + 1][y + 2] == 
                             self.grid[x + 2][y + 1])):
                            return True
                    except IndexError:
                        pass
                    try:
                        if ((self.grid[x][y + 1] == self.grid[x + 1][y] == 
                             self.grid[x + 1][y + 1] == 
                             self.grid[x + 2][y + 1])):
                            return True
                    except IndexError:
                        pass
        return False
                
    def winner(self, player):
        '''(TippyGameState, str) -> bool
        
        Return if player has won the game of Tippy.
        
        >>> t = TippyGameState('p2')
        >>> t.grid=[['o', 'o', 'x'], ['x', 'o', 'o'], ['x', 'x', None]]
        >>> t.winner('p2')
        True
        >>> t.winner('p1')
        False
        '''
        #check to see if there are enough x's and o's for there to be a winner.
        return self.win() and self.opponent() == player
        
        
    def is_over(self):
        '''(TippyGameState) -> bool
        
        Return whether the game of Tippy is over.
        
        >>> t = TippyGameState('p1')
        >>> t.is_over()
        False
        >>> t.grid = [[None, 'x', 'x'], ['x', 'x', 'o'], ['o', 'o', None]]
        >>> t.is_over()
        True
        '''
        return len(self.possible_next_moves()) == 0 or self.winner('p1') or self.winner('p2')
        #self.win() or not self.possible_next_moves()
        
          
    def rough_outcome(self):
        '''(TippyGameState) -> float

        Return an estimate of outcome for next_player from a TippyGameState.
        1 for win, 0 for tie, -1 for loss. 

        >>> t = TippyGameState('p1')
        >>> t.grid == [['x', 'x', None], [None, 'x', None], [None, None, None]]
        >>> t.rough_outcome()
        1.0
        >>> t = TippyGameState('p1')
        >>> t.grid == [['o', 'o', None], [None, 'o', None], [None, None, None]]
        >>> t.rough_outcome()
        -1.0
        >>> t = TippyGameState('p1')
        >>> t.rough_outcome()
        0
        '''
        for x in range(len(self.grid)):
            for y in range(len(self.grid)):
                #if there are 2 adjacent x's, and rough_outcome() is evaluating 
                    #the user:
                if (self.grid[x][y] == self.grid[x][y + 1] 
                    and self.next_player == 'p1' 
                    and self.grid[x][y] == 'x'):
                    #is the user one move away from winning?
                    if (self.grid[x - 1][y] == self.grid[x][y] or
                        self.grid[x - 1][y] == self.grid[x][y + 1] or
                        self.grid[x + 1][y] == self.grid[x][y] or
                        self.grid[x + 1][y] == self.grid[x][y + 1]):
                        return 1.0
                #when next_player is user, is the computer close to winning?
                if (self.grid[x][y] == self.grid[x][y + 1] 
                    and self.next_player == 'p1' 
                    and self.grid[x][y] == 'o'):
                    if (self.grid[x - 1][y] == self.grid[x][y] or
                        self.grid[x - 1][y] == self.grid[x][y + 1] or
                        self.grid[x + 1][y] == self.grid[x][y] or
                        self.grid[x + 1][y] == self.grid[x][y + 1]):
                        return -1.0
                #rough_outcome() is now evaluating the computer:
                elif (self.grid[x][y] == self.grid[x][y + 1] 
                    and self.next_player == 'p2' 
                    and self.grid[x][y] == 'o'):
                    if (self.grid[x - 1][y] == self.grid[x][y] or
                        self.grid[x - 1][y] == self.grid[x][y + 1] or
                        self.grid[x + 1][y] == self.grid[x][y] or
                        self.grid[x + 1][y] == self.grid[x][y + 1]):
                        return 1.0
                #next_player is computer, user is close to winning
                elif (self.grid[x][y] == self.grid[x][y + 1] 
                    and self.next_player == 'p2' 
                    and self.grid[x][y] == 'x'):
                    if (self.grid[x - 1][y] == self.grid[x][y] or
                        self.grid[x - 1][y] == self.grid[x][y + 1] or
                        self.grid[x + 1][y] == self.grid[x][y] or
                        self.grid[x + 1][y] == self.grid[x][y + 1]):
                        return -1.0
                #else it is a tie
                else:
                    return 0.0


if __name__ == '__main__':
    import doctest
    doctest.testmod()