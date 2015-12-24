from strategy import Strategy
import random


class StrategyMinimaxMyopic(Strategy):
    '''A strategy that picks a move which leads to a winnable game
    state.
    
    Will return a rough estimate of GameState's score after limit number of
    moves-ahead are examined.
    '''
    def __init__(self, interactive=False, limit=3):
        '''(StrategyMinimaxMyopic, bool, int) -> NoneType
        
        Initialize a StrategyMinimaxMyopic instance with a bool for user 
        interactive, and a limit number of moves before a move is suggested
        based on a rough outcome.
        
        >>> s = StrategyMinimaxMyopic()
        NoneType
        '''
        self.limit = limit
    
    def _get_score(self, state, moves_count=0):
        '''(StrategyMinimaxMyopic, GameState, int) -> float
        
        Return the score of a state.
        
        Use state's rough outcome if moves_count (number of moves ahead 
        examined) exceeds self.limit.
        
        A score for a GameState is:
        1.0 if winnable
        0.0 if only tieable
        -1.0 if only losable 
        
        >>> t = SubtractSquareState("p2", current_total = 16)
        >>> s = StrategyMinimaxMyopic()
        >>> s._get_score(t)
        -1.0
        >>> t.current_total = 2
        >>> s._get_score(t)
        1.0
        >>> t.current_total = 150
        >>> s._get_score(t)
        -1.0
        '''
        if state.over:
            return -1 * state.outcome()
        elif moves_count >= self.limit:
            return -1 * state.rough_outcome()
        
        return min([-1 * self._get_score(state.apply_move(move), 
                                         moves_count + 1) 
                    for move in state.possible_next_moves()])

    def suggest_move(self, state):
        '''(StrategyMinimaxMyopic, GameState) -> Move
        
        Return a move that takes the computer to a winnable game state.
        
        >>> t = TippyGameState("p2", grid = [[None, 'x', 'x'], 
        ['x', None, 'o'], ['o', 'o', 'x']])
        >>> s = StrategyMinimaxMyopic()
        >>> n = t.apply_move(s.suggest_move(t))
        TippyGameSate("p1", [[None, 'x', 'x'], 
        ['x', 'o', 'o'], ['o', 'o', 'x']])
        >>> str(n.grid)
        '[None, 'x', 'x']
        ['x', 'o', 'o']
        ['o', 'o', 'x']
        Current player: p1'
        '''
        if state.over:
            raise Exception("Cannot suggest a move, game is over.")

        possible_moves = state.possible_next_moves()
        
        tie_move = None
        #Score the resultant GameState for all possible moves...
        for move in possible_moves:
            new_state = state.apply_move(move)
            score = self._get_score(new_state)
            #Return the first winning move.
            if score == 1:
                return move
            #Remember the first tying move.
            elif score == 0:
                tie_move = move        
        if tie_move is not None:
            return tie_move
        else:
            return random.choice(possible_moves)
        

if __name__ == '__main__':
    import doctest
    doctest.testmod()