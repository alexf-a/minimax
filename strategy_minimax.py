from strategy import Strategy
import random


class StrategyMinimax(Strategy):
    '''A strategy that picks a move which leads to a winnable game
    state. 
    '''
    def _get_score(self, state):
        '''(StrategyMinimax, GameState) --> float
        
        Return the score of a state.
        
        A score for a GameState is:
        1 if winnable
        0 if only tieable
        -1 if only losable
        
        Use c = 1 and c = -1 to represent competitors. 
        
        >>> t = SubtractSquareState("p2", 16)
        >>> s = StrategyMinimax()
        >>> s._get_score(t, 1)
        1
        >>> t.current_total = 2
        >>> s._get_score(t, 1)
        -1
        '''
        if state.over:
            return -1 * state.outcome()
        else:
            return min([-1 * self._get_score(state.apply_move(move)) 
                        for move in state.possible_next_moves()])  

    def suggest_move(self, state):
        '''(StrategyMinimax, GameState) --> Move
        
        Return a move that takes the computer to a winnable game state.
        
        >>> t = TippyGameState("p1", grid=[[None, 'x', 'x'], ['x', None, 'o'], 
                ['o', 'o', 'x']])
        >>> s = StrategyMinimax()
        >>> s.suggest_move(t)
        TippyMove(2, 2)
        >>> n = t.apply_move(s.suggest_move(t))
        >>> str(n.grid)
        [None, 'x', 'x']
        ['x', 'o', 'o']
        ['o', 'o', 'x']
        Current player: p2
        '''
        #Should not ask Minimax to suggest a move on a finished game. 
        if state.over:
            raise Exception("Cannot suggest a move, game is over.")

        possible_moves = state.possible_next_moves()
        
        suggested_move = None
        # Consider every possible move ...
        for move in possible_moves:
            new_state = state.apply_move(move)
    
            score = self._get_score(new_state)
    
            if score == 1:
                return move
            elif score == 0:
                suggested_move = move
                
        if suggested_move is not None:
            return suggested_move
        else:
            return random.choice(possible_moves)
  
  
if __name__ == '__main__':
    import doctest
    doctest.testmod()