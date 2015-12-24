from strategy import Strategy
import random


class StrategyMinimaxMemoize(Strategy):
    '''A strategy that picks a move which leads to a winnable game
    state. 
    
    Optimizes speed by avoiding redundant computations.
    '''
    def __init__(self):
        '''(StrategyMinimaxMemoize) -> NoneType
        
        Initialize a StrategyMinimaxMemoize instance with a states_dict 
        dictionary of computed GameStates.
        '''
        self.states_dict = {}
    
    def _get_score(self, state):
        '''(StrategyMinimaxMemoize, GameState) -> float
        
        Return the score of a state.
        
        A score for a GameState is:
        1.0 if winnable.
        0.0 if only tieable.
        -1.0 if only losable.
        
        >>> t = SubtractSquareState("p2", current_total = 16)
        >>> s = StrategyMinimaxMemoize()
        >>> s._get_score(t)
        -1.0
        >>> t.current_total = 2
        >>> s._get_score(t)
        1.0
        '''
        s = state.__repr__()
        #Check if state has already been computed.
        if(s in self.states_dict):
            return self.states_dict[s]
        
        if state.over:
            result = -1 * state.outcome()
            #Cache the computed score.
            self.states_dict[s] = result
            return result
        
        #Simulate Minimax's opponent...
        result = min([-1 * self._get_score(state.apply_move(move)) 
                      for move in state.possible_next_moves()])
        
        #Cache the computed score.
        self.states_dict[s] = result      
        return result

    def suggest_move(self, state):
        '''(StrategyMinimaxMemoize, GameState) -> Move
        
        Return a move that takes the computer to a winnable game state.
        
        >>> t = TippyGameState("p2", grid=[[None, 'x', 'x'], ['x', None, 'o'], 
        ['o', 'o', 'x']])
        >>> s = StrategyMinimaxMemoize()
        >>> s.suggest_move(t)
        TippyMove(2, 2)
        >>> n = t.apply_move(s.suggest_move(t))
        TippyGameSate("p1", [[None, 'x', 'x'], ['x', 'o', 'o'], 
        ['o', 'o', 'x']])
        >>> str(n.grid)
        '[None, 'x', 'x']
        ['x', 'o', 'o']
        ['o', 'o', 'x']
        Current player: p1'
        '''
        #Should not ask Minimax to suggest a move on a finished game. 
        if state.over:
            raise Exception("Cannot suggest a move, game is over.")

        possible_moves = state.possible_next_moves()
        
        tie_move = None
        #Score the resultant states of all possible moves...
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
    docttest.testmod()