from strategy import Strategy
import random


class StrategyMinimaxPrune(Strategy):
    '''A strategy that picks a move which leads to a winnable game state. 
    
    Includes a pruning optimization to avoid unnecessary computations.
    '''
    
    def _get_score(self, state, c, bound):
        '''(StrategyMinimaxPrune, GameState, float, float) -> float
        
        Return the score of a state, limited by bound.
        
        A score for a GameState is:
        1.0 if winnable
        0.0 if only tieable
        -1.0 if only losable
        
        Use c = 1 to return a max score with upper bound.
        Use c = -1 to return a min score with lower bound.

        
        >>> t = SubtractSquareState("p2", current_total = 16)
        >>> s = StrategyMinimaxPrune()
        >>> s._get_score(t, 1.0, 1.0)
        1.0
        >>> t.current_total = 2
        >>> s._get_score(t, 1.0, 1.0)
        -1.0
        '''
        if state.over:
            return c * state.outcome()
        
        #Return value will be at most or at least this value...
        guarantee = -1 * c
        
        scores_list = []
        
        for move in state.possible_next_moves():
            new_state = state.apply_move(move)
            
            score = self._get_score(new_state, c * -1, guarantee)
            
            #Pruning, from p2's vantage...
            if c == 1:
                guarantee = max(float(guarantee), score)
                if guarantee >= bound:
                    return bound
            #Pruning, from p1's vantage...
            elif c == -1:
                guarantee = min(float(guarantee), score)
                if guarantee <= bound:
                    return bound
                
            scores_list.append(guarantee)
                   
        if c == 1:
            return max(scores_list)
        elif c == -1:
            return min(scores_list)  

    def suggest_move(self, state):
        '''(StrategyMinimaxPrune, GameState) -> Move
        
        Return a move that takes the computer to a winnable game state.
        
        >>> t = TippyGameState("p2", grid = [[None, 'x', 'x'], 
        ['x', None, 'o'], ['o', 'o', 'x']])
        >>> s = StrategyMinimaxPrune()
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
        # Consider every possible move ...
        for move in possible_moves:
            # Apply the move
            new_state = state.apply_move(move)
            # Get the score of the new state
            score = self._get_score(new_state, -1, -1.0)
            
            if score == 1.0:
                return move
            elif score == 0.0:
                tie_move = move
                
        if tie_move is not None:
            return tie_move
        else:
            return random.choice(possible_moves)
        

if __name__ == '__main__':
    import doctest
    doctest.testmod()